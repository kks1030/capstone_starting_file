<script>
import ControlMixin from '../mixins/ControlMixin'
import { useWebNotification } from '@vueuse/core'

export default {
    mixins: [ControlMixin],
    data() {
        return {
            showLoading: false,
            showControl: false,
            columns: [],
            is_wordcnt: false,
            wordcnt_col: null,
            is_charcnt: false,
            charcnt_col: null,
            include_space_charcnt: false,
            src_col: null,
            is_full_path: false,
            exclude: [],
            temp_exclude: null,
        }
    },
    watch: {
    //src_col(v) {
    //    this.detect_lang(this.$data.row0[this.$data.columns.indexOf(v)], (res) => {
    //        this.$data.src_lang = res.data
    //    })
    //},
    },
    computed: {
        desc_exclude: function() {
            if(this.$data.temp_exclude) {
                this.$data.exclude = this.$data.temp_exclude.split('|')
                return '<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">' + this.$data.exclude.join('</span><span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">') + '</span>는 비교파일에서 제외됩니다.'
            } else {
                this.$data.exclude = []
                return null
            }
        },
        desc_wordcnt_col: function() {
            if( ! this.$data.is_wordcnt || ! this.$data.src_col) return ''

            let desc = `<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">${this.$data.src_col}</span>의 어절수를 계산하고, `
            if(this.$data.wordcnt_col) {
                desc += `<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">${this.$data.wordcnt_col}</span> 컬럼에 넣습니다.`
            } else {
                desc += `<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">어절수</span> 컬럼에 넣습니다.`
            }
            return desc
        },
        desc_charcnt_col: function() {
            if( ! this.$data.is_charcnt || ! this.$data.src_col) return ''

            let desc = `<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">${this.$data.src_col}</span>의 글자수를 계산하고, `
            if(this.$data.charcnt_col) {
                desc += `<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">${this.$data.charcnt_col}</span> 컬럼에 넣습니다. `
            } else {
                desc += `<span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">글자수</span> 컬럼에 넣습니다. `
            }
            if(this.$data.include_space_charcnt) {
                desc += '글자수에 공백을 포함합니다.'
            } else {
                desc += '글자수에 공백을 포함하지 않습니다.'
            }
            return desc
        }
    },
    methods: {
        prepare() {
            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/main/request/' + this.$route.params.timestamp + '/listing/prepare')
                .then((res) => {
                this.$data.showLoading = false
                this.$data.message = null
                if (res.data.message) {
                    this.$data.showControl = false
                    this.$data.message = res.data.message
                } else {
                    if(res.data.columns) {
                        this.$data.columns = res.data.columns
                    }
                    this.$data.showControl = true
                }
            })
                .catch(this.handleError)
        },
        execute() {
            this.$data.showLoading = true
            this.$data.message = null
            this.$data.showControl = false
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/listing', {
                is_wordcnt:            this.$data.is_wordcnt,
                wordcnt_col:           this.$data.wordcnt_col,
                is_charcnt:            this.$data.is_charcnt,
                charcnt_col:           this.$data.charcnt_col,
                include_space_charcnt: this.$data.include_space_charcnt,
                src_col:               this.$data.src_col,
                is_full_path:          this.$data.is_full_path,
                exclude:               this.$data.exclude,
                
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

        <div v-if="0 < columns.length" class="row mt-3">
            <div class="col-6">
                <h3>어절수를 계산할까요?</h3>
            </div>
            <div class="col-6">
                <CheckboxVue v-model="is_wordcnt" label="어절수를 계산합니다."></CheckboxVue>
            </div>
        </div>

        <div v-if="is_wordcnt" class="row mt-3">
            <div class="col-6">
                <h3>혹시 어절수 컬럼이 이미 있나요? 어절수 컬럼이 이미 있는 경우 어절수 계산을 다시하여 값을 덮어씌웁니다.</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="wordcnt_col" :columns="columns" :nullable="true" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div v-if="0 < columns.length" class="row mt-3">
            <div class="col-6">
                <h3>글자수를 계산할까요?</h3>
            </div>
            <div class="col-6">
                <CheckboxVue v-model="is_charcnt" label="글자수를 계산합니다."></CheckboxVue>
            </div>
        </div>

        <div v-if="is_charcnt" class="row mt-3">
            <div class="col-6">
                <h3>혹시 글자수 컬럼이 이미 있나요? 글자수 컬럼이 이미 있는 경우 글자수 계산을 다시하여 값을 덮어씌웁니다.</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="charcnt_col" :columns="columns" :nullable="true" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div v-if="is_charcnt" class="row mt-3">
            <div class="col-6">
                <h3>공백을 글자수에 포함시킬까요?</h3>
            </div>
            <div class="col-6">
                <CheckboxVue v-model="include_space_charcnt" label="공백을 글자수에 포함시킵니다."></CheckboxVue>
            </div>
        </div>

        <div v-if="is_wordcnt || is_charcnt" class="row mt-3">
            <div class="col-6">
                <h3>원문 컬럼을 선택하세요</h3>
            </div>
            <div class="col-6">
                <RadioCheckboxListVue v-model="src_col" :columns="columns" type="radio"></RadioCheckboxListVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>파일을 절대경로로 표시할까요?</h3>
            </div>
            <div class="col-6">
                <CheckboxVue v-model="is_full_path" label="절대경로로 표시합니다."></CheckboxVue>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>리스팅에서 제외할 파일 타입을 입력해주세요. 두개 이상을 입력할때는 <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">|</span>로 구분지어 주세요.</h3>
            </div>
            <div class="col-6">
                <input v-model="temp_exclude" type="text" placeholder="*.txt|*.zip|*.tar.gz">
                <p v-html="desc_exclude"></p>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>요약</h3>
            </div>
            <div class="col-6">
                <p>파일 리스트를 엑셀로 작성합니다.</p>
                <p v-html="desc_wordcnt_col"></p>
                <p v-html="desc_charcnt_col"></p>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green" @click="execute(event)">🔥리스팅 시작🔥</button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>