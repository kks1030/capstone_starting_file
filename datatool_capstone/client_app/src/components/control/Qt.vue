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
            row0:         [],

            src_col:      null,
            trg_col:      null,
            src_lang:     null,
            trg_lang:     null,
            langs:        ['ko', 'en', 'ja', 'zh-cn', 'zh-tw']
        }
    },
    watch: {
        src_col(v) {
            this.detect_lang(this.$data.row0[this.$data.columns.indexOf(v)], (res) => {
                this.$data.src_lang = res.data
            })
        },
        trg_col(v) {
            this.detect_lang(this.$data.row0[this.$data.columns.indexOf(v)], (res) => {
                this.$data.trg_lang = res.data
            })
        }
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null

            this.axios.get('/main/request/' + this.$route.params.timestamp + '/qt/prepare')
            .then((res) => {
                this.$data.showLoading = false
                this.$data.message = null

                if(res.data.columns) {
                    this.$data.showControl = true
                    this.$data.columns     = res.data.columns
                    this.$data.row0        = res.data.row0
                } else if(res.data.message) {
                    this.$data.showControl = false
                    this.$data.message     = res.data.message
                }

                this.$data.columns.forEach((x) => {
                    // 자동선택
                    this.is_src(x) ? this.$data.src_col = x : null
                    this.is_ht(x)  ? this.$data.trg_col = x : null
                })
            })
            .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/qt', {
                src_col:  this.$data.src_col,
                trg_col:  this.$data.trg_col,
                src_lang: this.$data.src_lang,
                trg_lang: this.$data.trg_lang,
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
                <table class="border-collapse border border-slate-500">
                    <thead>
                        <tr>
                            <th v-for="item in columns" class="border border-slate-600">{{item}}</th>
                        </tr>
                    </thead>
                    <tbody id="df_table">
                        <tr>
                            <td v-for="item in row0" class="border border-slate-700">{{item}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>원문 컬럼을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="src_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>원문 컬럼의 언어를 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="src_lang" :columns="langs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>번역 컬럼을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="trg_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>번역 컬럼의 언어를 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="trg_lang" :columns="langs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>
        
        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥기계검수(번호/기호) 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>