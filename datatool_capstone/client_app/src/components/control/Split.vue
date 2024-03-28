<script>
import ControlMixin from '../mixins/ControlMixin'
import { useWebNotification } from '@vueuse/core'

export default {
    mixins: [ControlMixin],
    data() {
        return {
            showLoading:  false,
            showControl:  false,
            columns:      [],
            split_tp:     null,
            split_tps: {
                sent_cnt:   '문장수',
                id_col:     '컬럼',
                random_cnt: '추출',
            },
            split_tp_desc: {
                sent_cnt:   '문장 갯수씩 파일을 나눕니다.',
                id_col:     '컬럼에서 값이 파일을 분할하여 모읍니다.',
                random_cnt: '파일당 첫 n개씩 문장을 추출합니다. 추출되는 문장은 재정렬에 의해 바뀔 수 있습니다.',
            },
            prefix:       null,
            split_by:     1000,
            split_filter: false,
            trg_col:      null,
            order_col:    null,
            id_col:       null,
            max_sent_cnt: 3,
            split_order:  false,
            order_tp:     null,
            order_tps: {
                random: '랜덤',
                asc:    '오름차순',
                desc:   '내림차순',
            },
        }
    },
    watch: {
        split_order(v) {
            if(v) {
                // do nothing
            } else {
                this.$data.order_tp  = null
                this.$data.order_col = null
            }
        },
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null

            this.axios.get('/main/request/' + this.$route.params.timestamp + '/split/prepare')
            .then((res) => {
                this.$data.showLoading = false
                this.$data.message = null

                if(res.data.columns) {
                    this.$data.showControl = true
                    this.$data.columns     = res.data.columns
                    this.$data.prefix      = res.data.prefix
                } else if(res.data.message) {
                    this.$data.showControl = false
                    this.$data.message     = res.data.message
                    this.$data.prefix      = res.data.prefix
                }

                this.$data.mt_col = []
                this.$data.columns.forEach((x) => {
                    // 자동선택
                    this.is_src(x) ? this.$data.trg_col = x    : null
                    this.is_no(x)  ? this.$data.order_col = x  : null
                    this.is_no(x)  ? this.$data.id_col = x     : null
                })
            })
            .catch(this.handleError)
        },
        execute() {
            
            if(this.$data.split_tp == 'sent_cnt' && ! this.$data.split_by) {
                alert('분할할 갯수를 입력해 주세요')
                return
            } else if(this.$data.split_tp == 'id_col' && ! this.$data.id_col) {
                alert('나눌 컬럼명을 입력해 주세요')
                return
            } else if(this.$data.split_tp == 'random_cnt' && ! this.$data.max_sent_cnt) {
                alert('랜덤으로 뽑아낼 갯수를 입력해 주세요')
                return
            }

            if(this.$data.order_tp == 'asc' || this.$data.order_tp == 'desc') {
                if( ! this.$data.order_col) {
                    alert('재정렬할 기준 컬럼을 선택해주세요.')
                    return
                }
            }

            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/split', {
                prefix:       this.$data.prefix,
                split_by:     this.$data.split_tp == 'sent_cnt'   ? this.$data.split_by     : null,
                id_col:       this.$data.split_tp == 'id_col'     ? this.$data.id_col       : null,
                max_sent_cnt: this.$data.split_tp == 'random_cnt' ? this.$data.max_sent_cnt : null,
                trg_col:      this.$data.split_filter ? this.$data.trg_col : null,
                order_tp:     this.$data.split_order  ? this.$data.split_sort_tp : null,
                order_col:    this.$data.split_order  ? this.$data.order_col : null,
            })
            .then((res) => {
                this.$data.showLoading = false
                this.$data.message = res.data.message
                if(res.data.message) {
                    const {
                        isSupported,
                        notification,
                        show,
                        close,
                        onClick,
                        onShow,
                        onError,
                        onClose,
                    } = useWebNotification({
                        title: res.data.message,
                        dir: 'auto',
                        lang: 'ko',
                        renotify: true,
                        tag: 'Completed',
                    })
                    onClick((evt) => {
                        parent.focus()
                        window.focus() //just in case, older browsers
                        close()
                    })
                    show()
                    this.startFlashFavicon()
                }
            })
            .catch(this.handleError)
            .finally(() => {
                this.$emit('toggleShowTimeline', true)
            })

        },
    },
    mounted() {
        this.prepare()
    }
}


</script>

<template>
<div class="mt-3">
    <div>
        <h1>{{ message }}</h1>
        <h1 class="text-red-500">{{ errors }}</h1>
    </div>

    <SpinnerVue v-if="showLoading"></SpinnerVue>

    <div class="container" v-if="showControl">

        <div class="row mt-3">
            <div class="col-6">
                <h3>Prefix를 입력하세요</h3>
                <small>빈칸으로 입력하고 컬럼 기준으로 문장을 나누면 해당 컬럼값이 파일명이 됩니다.</small>
            </div>
            <div class="col-6">
                <input v-model="prefix" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">

            </div>
        </div>


        <div class="row mt-3">
            <div class="col-6">
                <h3>무엇을 기준으로 문장을 나누시겠습니까?</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxList2Vue v-model="split_tp" :columns="split_tps" type="radio"></RadioCheckboxList2Vue>
                <small>{{split_tp_desc[split_tp]}}</small>
            </div>
        </div>

        <div v-if="split_tp == 'sent_cnt'" class="row mt-3" id="split_tp_sent_cnt_input_div">
            <div class="col-6">
                <h3>몇 문장식 나누시겠습니까?</h3>
            </div>
            <div class="col-6">
                <input v-model="split_by" type="number" class="form-control" placeholder="1000"/>
            </div>
        </div>

        <div v-if="split_tp == 'id_col'" class="row mt-3" id="split_tp_id_col_input_div">
            <div class="col-6">
                <h3>분할할 컬럼은 무엇입니까?</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="id_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div v-if="split_tp == 'random_cnt'" class="row mt-3" id="split_tp_random_cnt_input_div">
            <div class="col-6">
                <h3>파일당 뽑아낼 문장은 몇개입니까?</h3>
            </div>
            <div class="col-6">
                <input v-model="max_sent_cnt" type="number" class="form-control" placeholder="3"/>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>문장의 순서를 재정렬하나요?</h3>
            </div>
            <div class="col-6">
                <div class="form-check form-switch">
                    <input v-model="split_order" class="form-check-input" type="checkbox" role="switch" id="split_order" />
                    <label class="form-check-label" for="split_order">선택한 컬럼을 재정렬 합니다.</label>
                </div>
            </div>
        </div>

        <div v-if="split_order" class="row mt-3">
            <div class="col-12">
                <h3>랜덤인가요? 오름차순인가요? 내림차순인가요?</h3>
            </div>
            <div class="col-12">
                <RadioCheckboxList2Vue v-model="order_tp" :columns="order_tps" type="radio"></RadioCheckboxList2Vue>
            </div>
        </div>

        <div v-if="order_tp == 'asc' || order_tp == 'desc'" class="row mt-3">
            <div class="col-12">
                <h3>재정렬 할 순서가 있는 컬럼을 선택하세요.</h3>
            </div>
            <div class="col-12">
                <RadioCheckboxListVue v-model="order_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-6">
                <div class="group relative cursor-pointer py-2">
                    <div class="absolute invisible bottom-7 group-hover:visible bg-white text-black px-4 mb-3 py-2 text-sm rounded-md">  
                      <p class=" leading-2 text-gray-600 pt-2 pb-2"> 무효 문장이란:</p>
                      <label><span class="badge text-bg-danger mx-1">빈칸</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">-</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">번역 제외</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">번역제외</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">번역 불가</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">번역불가</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">불완전한문장</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">불완전한 문장</span>, 
                        <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">SKIP</span>
                      </label>
                     </div>
                    <h3 class="underline hover:cursor-pointer">무효 문장을 제외하나요? </h3>
                </div>
            </div>


            <div class="col-6">
                <div class="form-check form-switch">
                    <input v-model="split_filter" class="form-check-input" type="checkbox" role="switch" id="split_filter" />
                    <label class="form-check-label" for="split_filter">무효 문장을 제외합니다.</label>
                </div>
            </div>
        </div>

        <div v-if="split_filter" class="row mt-3">
            <div class="col-12">
                <h3>무효 문장이 있는 컬럼을 선택하세요</h3>
            </div>
            <div class="col-12">
                <RadioCheckboxListVue v-model="trg_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥분할/합치기/필터링 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>