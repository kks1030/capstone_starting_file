import { useWebNotification, useWindowFocus, useFavicon, useIntervalFn } from '@vueuse/core'

const favicon = '/favicon.ico'
const faviconActive = '/faviconActive.ico'

const handleError = {
    data() {
        return {
            message: null,
            errors: null,
            titles: {
                'split': '분할/합치기/필터링',
                'validatecol': '헤더 검사',
                'similarity': '유사도 검사',
                'qt': '기계 검수',
                'listing': '파일 리스트 만들기',
                'comparedir': '폴더 비교',
                'replace': '단어 교체',
                'splitcondition': '최종본 작성',
                'dupclean': '중복 제거',
                'filter': '추출',
                'parse': '파싱',
            },
            isFocused: useWindowFocus(),
            currentFavicon: useFavicon(),
            faviconIntervalFn: null,
        }
    },
    watch: {
        isFocused: {
            handler(newVal, oldVal) {
                if(newVal == true) this.stopFlashFavicon()
            }
        }
    },
    methods: {
        handleError(error) {
            this.$data.message = null
            this.$data.errors = null
            if (error.response && error.response.data) {
                if(typeof(error.response.data) == 'string') {
                    if(error.response.data.includes("Time-out")) {
                        this.$data.errors = '처리가 너무 오래 걸리네요. 좀 있다가 F5를 눌러봅시다.'
                    } else {
                        this.$data.errors = error.response.data
                    }
                } else if(typeof(error.response.data) == 'object') {
                    if(error.response.data.detail) {
                        if(error.response.data.detail == 'Not authenticated') {
                            this.$data.errors = '로그인 해주세요'
                        } else {
                            this.$data.errors = error.response.data.detail
                        }
                    } else {
                        this.$data.errors = error.response.data
                    }
                } else {
                    //if(error.response.status == 401) {
                    //    this.$data.errors = '로그인 해주세요.'
                    //    this.$data.errors = null
                    //    return
                    //} else {
                        this.$data.errors = error.response.data.toString()
                    //}
                }
            } else if(error.message) {
                this.$data.errors = error.message
            }

            if(this.$data.isFocused == false) {
                const { isSupported, notification, show, close, onClick, onShow, onError, onClose, } = useWebNotification({
                    title: this.$data.errors ? this.$data.errors : '에러가 발생했습니다.',
                    dir: 'auto',
                    lang: 'ko',
                    renotify: true,
                    tag: 'Completed',
                });
                onClick((evt) => {
                    parent.focus()
                    window.focus() //just in case, older browsers
                    close()
                })
                show()
                this.startFlashFavicon()
            }
        },
        startFlashFavicon() {
            if( ! this.$data.faviconIntervalFn) {
                this.$data.faviconIntervalFn = useIntervalFn(() => {
                    if(this.$data.currentFavicon == favicon) {
                        this.$data.currentFavicon = faviconActive
                    } else {
                        this.$data.currentFavicon = favicon
                    }
                }, 1000, {immediateCallback: true})
            }
        },
        stopFlashFavicon() {
            if(this.$data.faviconIntervalFn) this.$data.faviconIntervalFn.pause()
            this.$data.faviconIntervalFn = null
            this.$data.currentFavicon = favicon
        },
        download(filename) {
            this.axios.post('/main/request/' + this.$route.params.timestamp + '/download', {
                filename 
            }, {
                responseType: 'blob',
                headers: {
                    Accept: "application/octet-stream",
                }
            }).then((res) => {
                if(res.data.message) {
                    // 실패
                    this.$data.message = res.data.message
                } else {
                    const href = URL.createObjectURL(new Blob([res.data]));
                    const link = document.createElement('a');
                    link.href = href;
                    // content-disposition 은 아래 둘 중 하나로 반환된다.
                    //attachment; filename*=utf-8''20231207-%EB%B9%84%EA%B5%90.xlsx
                    //attachment; filename="20231207-listing.xlsx"
                    let filename = decodeURIComponent(res.headers['content-disposition'].split("attachment; filename*=utf-8''")[1])
                    if(filename == 'undefined') {
                        filename = decodeURIComponent(res.headers['content-disposition'].split("attachment; filename=\"")[1])
                        // 마지막 "을 삭제해준다.
                        filename = filename.slice(0, -1)
                    }

                    link.setAttribute('download', filename)
                    document.body.appendChild(link);
                    link.click();
                
                    // clean up "a" element & remove ObjectURL
                    document.body.removeChild(link);
                    URL.revokeObjectURL(href);
                }
            });
        },
        is_no(name) {
            if(name == 'no' || name == 'NO' || name == 'No' || name == 'sn') return true
            return false
        },
        is_src(name) {
            if(name == 'sent') return true
            if(name == 'source') return true
            if(name == 'source_original') return true
            return false
        },
        is_mt(name) {
            if(name.includes('mt') && name.includes('유사도') == false) return true
            return false
        },
        is_ht(name) {
            if(name == 'ht') return true
            if(name == 'source_cleaned') return true
            return false
        },
        is_paraid(name) {
            if(name == 'para_id') return true
            return false
        },
        detect_lang(sent, callback) {
            this.axios.get('/detect_lang?text=' + sent)
            .then((res) => {
                callback(res)
            })
            .catch(this.handleError)
        },
        prepareColumn(dirname, callback) {
            this.axios.get("/main/request/" + this.$route.params.timestamp + "/columns/" + dirname)
            .then((res) => {
                callback(res)
            })
            .catch(this.handleError)
        },
    }
}

export default handleError;

