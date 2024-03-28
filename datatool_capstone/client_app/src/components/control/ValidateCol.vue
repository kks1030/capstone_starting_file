<script>
import ControlMixin from '../mixins/ControlMixin'
import { useWebNotification } from '@vueuse/core'

export default {
    mixins: [ControlMixin],
    data() {
        return {
            showLoading: false,
            showControl: false,
            columns: null,
        }
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/main/request/' + this.$route.params.timestamp + '/validatecol/prepare')
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
            })
            .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/validatecol', {
                col_list: this.$data.columns
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
                        tag: 'test',
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
        <div class="mt-3">
            <div class="">
                <h3>헤더에 오타가 없는지, 순서는 맞는지 확인하세요.</h3>
            </div>
            <div class="flex flex-col items-center">
                <div>
                    <input v-for="col in columns" :value="col" name="col_group" type="text" id="default-input" class="input-text">
                </div>
            </div>
        </div>
        
        <div class="mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥컬럼 검사 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>