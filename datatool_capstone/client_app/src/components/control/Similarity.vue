<script>
import ControlMixin from '../mixins/ControlMixin'
import { useWebNotification } from '@vueuse/core'

export default {
    mixins: [ControlMixin],
    data() {
        return {
            showLoading: false,
            showControl: false,
            columns:     [],
            src_col:     null,
            mt_col:      [],
            trg_col:      null,
            ignore_sent_by_word_cnt: false,
        }
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null

            this.axios.get('/main/request/' + this.$route.params.timestamp + '/similarity/prepare')
            .then((res) => {
                this.$data.showLoading = false
                this.$data.message = null

                if(res.data.columns) {
                    this.$data.showControl = true
                    this.$data.columns = res.data.columns
                } else if(res.data.message) {
                    this.$data.showControl = false
                    this.$data.message = res.data.message
                }

                this.$data.mt_col = []
                this.$data.columns.forEach((x) => {
                    // 자동선택
                    this.is_src(x) ? this.$data.src_col = x    : null
                    this.is_mt(x)  ? this.$data.mt_col.push(x) : null
                    this.is_ht(x)  ? this.$data.trg_col  = x   : null
                })
            })
            .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/similarity', {
                src_col: this.$data.src_col,
                mt_cols: this.$data.mt_col,
                trg_col: this.$data.trg_col,
                ignore_sent_by_word_cnt: this.ignore_sent_by_word_cnt,
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
            <div class="col-12">
                <h3>원문 컬럼을 선택하세요</h3>
            </div>
            <div class="col-12">
                <RadioCheckboxListVue v-model="src_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-12">
                <h3>MT 컬럼을 선택하세요(복수)</h3>
            </div>
            <div class="col-12">
                <RadioCheckboxListVue v-model="mt_col" :columns="columns" type="checkbox"></RadioCheckboxListVue>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-12">
                <h3>번역 컬럼을 선택하세요</h3>
            </div>
            <div class="col-12">
                <RadioCheckboxListVue v-model="trg_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>MT커럼과 번역컬럼의 어절수가 많이 차이나는 경우(9), <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">번역제외</span>로 표시합니까?</h3>
            </div>
            <div class="col-6">
                <CheckboxVue v-model="ignore_sent_by_word_cnt" label="MT커럼과 번역컬럼의 어절수가 많이 차이나는 경우, <span class='bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300'>번역제외</span>합니다."></CheckboxVue>
            </div>
        </div>
        
        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥유사도 검사 시작🔥</button>
        </div>

    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>