<script setup>
import ControlMixin from '../mixins/ControlMixin'
import { useWebNotification } from '@vueuse/core'
</script>
<script>
export default {
    mixins: [ControlMixin],
    data() {
        return {
            showLoading: false,
            showControl: false,
            dirs: [],
            dic_columns: [],
            trg_columns: [],
            dic_dir: null,
            trg_dir: null,
            compare_src_col: null,
            compare_trg_col: null,
            replace_src_col: null,
            replace_trg_col: null,
        }
    },
    watch: {
        dic_dir(v) {
            this.prepareColumn(v, (res) => {
                if(res.data.columns) {
                    this.$data.dic_columns = res.data.columns
                } else if(res.data.message) {
                    this.$data.message     = res.data.message
                } else {
                    console.log(res)
                }
            })
        },
        trg_dir(v) {
            this.prepareColumn(v, (res) => {
                if(res.data.columns) {
                    this.$data.trg_columns = res.data.columns
                } else if(res.data.message) {
                    this.$data.message     = res.data.message
                } else {
                    console.log(res)
                }
            })
        },
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/main/request/' + this.$route.params.timestamp + '/replace/prepare')
                .then((res) => {
                    this.$data.showLoading = false
                    this.$data.message = null
                    if (res.data.dirs) {
                        this.$data.showControl = true
                        this.$data.dirs = res.data.dirs
                    }
                    else if (res.data.message) {
                        this.$data.showControl = false
                        this.$data.message = res.data.message
                    }
                })
                .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/replace', {
                dic_dir: this.$data.dic_dir,
                trg_dir: this.$data.trg_dir,
                compare_src_col: this.$data.compare_src_col,
                compare_trg_col: this.$data.compare_trg_col,
                replace_src_col: this.$data.replace_src_col,
                replace_trg_col: this.$data.replace_trg_col,
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
    },
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
                <h3>DB가 될 파일이 들어가 있는 폴더를 선택해주세요.</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="dic_dir" :columns="dirs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>DB파일에서 원문 컬럼을 선택해주세요.</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="compare_src_col" :columns="dic_columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>DB파일에서 번역 컬럼을 선택해주세요.</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="replace_src_col" :columns="dic_columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>단어를 교체할 파일(번역할 파일)이 들어가 있는 폴더를 선택해주세요.</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="trg_dir" :columns="dirs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-6">
                <h3>번역할 파일에서 원문 컬럼을 선택해주세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="compare_trg_col" :columns="trg_columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>번역할 파일에서 번역 컬럼을 선택해주세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="replace_trg_col" :columns="trg_columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥단어 교체 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>