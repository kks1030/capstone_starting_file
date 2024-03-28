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
            dirs:         [],
            trg_dir_name: null,
            src_dir_name: null,
            clean_tp:     null,
            clean_tps:    {
                regular: '완전 일치제거',
                nospace: '공백제거 후 일치제거',
            },
            check_col:       null,
            dupclean_filter: null,
            dupclean_filters: {
                '0': '한 파일로 다운로드',
                '1': '중복과 중복아닌 문장을 나누어서 다운로드',
                '2': '중복만 모아서 다운로드',
            },
        }
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/main/request/' + this.$route.params.timestamp + '/dupclean/prepare')
                .then((res) => {
                    this.$data.showLoading = false
                    this.$data.message = null
                    if (res.data.columns) {
                        this.$data.showControl = true
                        this.$data.columns     = res.data.columns
                        this.$data.dirs        = res.data.dirs
                    }
                    else if (res.data.message) {
                        this.$data.showControl = false
                        this.$data.message     = res.data.message
                    }
                })
                .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/dupclean', {
                trg_dir_name:    this.$data.trg_dir_name,
                src_dir_name:    this.$data.src_dir_name,
                clean_tp:        this.$data.clean_tp,
                check_col:       this.$data.check_col,
                dupclean_filter: this.$data.dupclean_filter,
            })
                .then((res) => {
                    this.$data.showLoading = false
                    this.$data.message = res.data.message
                    if (res.data.message) {
                        const { isSupported, notification, show, close, onClick, onShow, onError, onClose, } = useWebNotification({
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
        this.prepare();
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
                <h3>대상 폴더를 선택해 주세요</h3>
            </div>
            <div class="col-6">
                <div v-if="dirs.length < 2">폴더를 두개이상 업로드하셔야 대상폴더 선택이 가능합니다.</div>
                <RadioCheckboxListVue v-model="trg_dir_name" :columns="dirs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>중복제거에 사용할 추가원문이 담긴 폴더를 선택해 주세요</h3>
            </div>
            <div class="col-6">
                <div v-if="dirs.length < 2">폴더를 두개이상 업로드하셔야 대상폴더 선택이 가능합니다.</div>
                <RadioCheckboxListVue v-model="src_dir_name" :columns="dirs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>중복 제거 방식</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxList2Vue v-model="clean_tp" :columns="clean_tps" type="radio"></RadioCheckboxList2Vue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>중복 제거할 대상 컬럼을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="check_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <div class="group relative cursor-pointer py-2">
                    <div class="absolute invisible bottom-7 group-hover:visible bg-white text-black px-4 mb-3 py-2 text-sm rounded-md">
                      <p class=" leading-2 text-gray-600 pt-2 pb-2"> 무효 문장이란:</p>
                      <label>
                        <span class="badge text-bg-danger mx-1">빈칸</span>,
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
                    <h3 class="underline hover:cursor-pointer">중복 검사후 무효 문장을 제외하나요?</h3>
                </div>
            </div>
            <div class="col-6">
                <RadioCheckboxList2Vue v-model="dupclean_filter" :columns="dupclean_filters" type="radio"></RadioCheckboxList2Vue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-12">
                <label>무효 문장이란: <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">-</span>
                </label>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥중복 제거 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>