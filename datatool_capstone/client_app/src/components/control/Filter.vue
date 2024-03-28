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
            trg_tp:       null,
            trg_tps:      {
                excel: '엑셀 Row',
                file:  '파일',
            },
            src_dir_name: null,
            check_col:    null,
        }
    },
    watch: {
        src_dir_name(v) {
            this.prepareColumn(v, (res) => {
                if(res.data.columns) {
                    this.$data.columns = res.data.columns
                } else if(res.data.message) {
                    this.$data.message     = res.data.message
                } else {
                    console.log(res)
                }
            })
        }
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/main/request/' + this.$route.params.timestamp + '/filter/prepare')
                .then((res) => {
                    this.$data.showLoading = false
                    this.$data.message = null
                    if (res.data.dirs) {
                        this.$data.showControl = true
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
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/filter', {
                trg_dir_name: this.$data.trg_dir_name,
                trg_tp:       this.$data.trg_tp,
                src_dir_name: this.$data.src_dir_name,
                check_col:    this.$data.check_col,
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
                <h3>추출 대상 폴더를 선택해 주세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="trg_dir_name" :columns="dirs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>추출 할 것을 선택해 주세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxList2Vue v-model="trg_tp" :columns="trg_tps" type="radio"></RadioCheckboxList2Vue>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-6">
                <h3>추출할 ID가 있는 파일의 폴더를 선택해 주세요.</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="src_dir_name" :columns="dirs" type="radio"></RadioCheckboxListVue>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-6">
                <h3>추출할 ID 컬럼(대상 컬럼)을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="check_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute($event)">🔥추출 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>