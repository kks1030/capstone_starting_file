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
            
            splitcondition_tp: null,
            splitcondition_tps: {
                sent: '문장',
                para: '문단',
            },
            src_col:           null,
            ht_col:            null,
            paraid_col:        null,
            is_gather_blank:   false,
        }
    },
    watch: {
        //src_col(v) {
        //},
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null

            this.axios.get('/main/request/' + this.$route.params.timestamp + '/splitcondition/prepare')
            .then((res) => {
                this.$data.showLoading = false
                this.$data.message = null

                if(res.data.columns) {
                    this.$data.showControl = true
                    this.$data.columns     = res.data.columns
                } else if(res.data.message) {
                    this.$data.showControl = false
                    this.$data.message     = res.data.message
                }

                this.$data.columns.forEach((x) => {
                    // 자동선택
                    this.is_src(x)    ? this.$data.src_col    = x : null
                    this.is_ht(x)     ? this.$data.ht_col     = x : null
                    this.is_paraid(x) ? this.$data.paraid_col = x : null
                })
            })
            .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false

            this.axios.post('/main/request/' + this.$route.params.timestamp + '/splitcondition', {
                splitcondition_tp: this.$data.splitcondition_tp,
                src_col:           this.$data.src_col,
                ht_col:            this.$data.ht_col,
                paraid_col:        this.$data.paraid_col,
                is_gather_blank:   this.$data.is_gather_blank,
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
                <h3>최종본 구분</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxList2Vue v-model="splitcondition_tp" :columns="splitcondition_tps" type="radio"></RadioCheckboxList2Vue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>원문 컬럼을 선택하세요</h3><small>어절수가 없는 파일에 어절수를 계산합니다.</small>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="src_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>번역 컬럼을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="ht_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>문단ID 컬럼을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="paraid_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>빈칸인 문장을 따로 수집합니까?</h3>
            </div>
            <div class="col-6">
                <CheckboxVue v-model="is_gather_blank" label="빈칸만 따로 수집합니다."></CheckboxVue>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute($event)">🔥최종본 작성 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>