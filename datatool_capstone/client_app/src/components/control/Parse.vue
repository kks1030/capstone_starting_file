<script>
import ControlMixin from '../mixins/ControlMixin'
import { useWebNotification } from '@vueuse/core'

export default {
    mixins: [ControlMixin],
    data() {
        return {
            showLoading:  false,
            showControl:  false,
            preset: null,
            presets: {
                'nia-금융-보고서': '보고서',
                'nia-금융-공시': '공시',
                'treatise': '논문',
                '': '없음',
            },
            is_overwrite: false,
        }
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/main/request/' + this.$route.params.timestamp + '/parse/prepare')
                .then((res) => {
                    this.$data.showLoading = false
                    this.$data.message = null
                    
                    if (res.data.message) {
                        this.$data.showControl = false
                        this.$data.message     = res.data.message
                    } else {
                        this.$data.showControl = true
                    }
                })
                .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/parse', {
                preset: this.$data.preset,
                is_overwrite: this.$data.is_overwrite,
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
                <h3>Preset을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="preset" :columns="presets" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>(재시도하는 경우) 덮어쓰시겠습니까?</h3>
            </div>
            <div class="col-6">
                <div class="form-check form-switch">
                    <input v-model="is_overwrite" class="form-check-input" type="checkbox" role="switch" id="parse_is_overwrite"/>
                    <label class="form-check-label" for="parse_is_overwrite">예, 덮어씁니다.</label>
                </div>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥파싱 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>