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
            exclude: [],
            temp_exclude: null,
            ignorable_suffix: null,
            compare_tp: null,
            compare_tps: {
                '' : '비교 결과로 전체 리스트를 주세요. ',
                'x': '비교 결과로 어느 한쪽이 존재하지 않는 파일 리스트를 주세요.',
                'o': '비교 결과로 모든 폴더에 존재하는 파일 리스트를 주세요.',
            },
        }
    },
    computed: {
        desc_ignorable_suffix: function() {
            if(this.$data.ignorable_suffix) {
                return `<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">abc</span> 와 <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">abc${encodeURI(this.$data.ignorable_suffix)}</span>는 같은 파일명으로 처리됩니다.`
            } else {
                return null
            }
        },
        desc_exclude: function() {
            if(this.$data.temp_exclude) {
                this.$data.exclude = this.$data.temp_exclude.split('|')
                return '<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">' + this.$data.exclude.join('</span><span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">') + '</span>는 비교파일에서 제외됩니다.'
            } else {
                this.$data.exclude = []
                return null
            }
        },
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/main/request/' + this.$route.params.timestamp + '/comparedir/prepare')
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
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/comparedir', {
                exclude: this.$data.exclude,
                ignorable_suffix: this.$data.ignorable_suffix,
                compare_tp: this.$data.compare_tp,
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
                <h3>어떤 비교 결과를 받으시겠습니까?</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxList2Vue v-model="compare_tp" :columns="compare_tps" type="radio"></RadioCheckboxList2Vue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>무시할 Suffix를 입력해주세요.</h3>
            </div>
            <div class="col-6">
                <input v-model="ignorable_suffix" type="text" placeholder="_tr">
                <p v-html="desc_ignorable_suffix"></p>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>비교에서 제외할 파일 타입을 입력해주세요. 두개 이상을 입력할때는 <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">|</span>로 구분지어 주세요.</h3>
            </div>
            <div class="col-6">
                <input v-model="temp_exclude" type="text" placeholder="*.txt|*.zip|*.tar.gz">
                <p v-html="desc_exclude"></p>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥폴더 비교 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>