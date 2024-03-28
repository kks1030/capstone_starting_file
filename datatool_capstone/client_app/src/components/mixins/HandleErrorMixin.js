const handleError = {
    data() {
        return {
            errors: null
        }
    },
    methods: {
        handleError(error) {
            if (error.response && error.response.data) {
                if(typeof(error.response.data) == 'string') {
                    if(error.response.data.includes("Time-out")) {
                        this.$data.errors = '처리가 너무 오래 걸리네요. 좀 있다가 F5를 눌러봅시다.'
                    } else {
                        this.$data.errors = error.response.data
                    }
                } else if(typeof(error.response.data) == 'object') {
                    if(error.response.data.detail) {
                        if(typeof(error.response.data.detail) == 'string') {
                            if(error.response.data.detail == 'Not authenticated') {
                                this.$data.errors = '로그인 해주세요'
                            } else {
                                this.$data.errors = error.response.data.detail
                            }
                        } else if(typeof(error.response.data.detail) == 'object') {
                            this.$data.errors = error.response.data.detail[0].msg + ': ' + error.response.data.detail[0].loc.join(',')
                        } else {
                            console.log(error.response.data.detail)
                            this.$data.errors = error.response.data.detail
                        }
                    } else if(error.response.data.errors) {
                        this.$data.errors = error.response.data.errors.toString()
                    } else {
                        console.log(error.response.data)
                        alert(error.response.data)
                    }
                } else {
                    this.$data.errors = error.response.data.toString()
                }
            } else if(error.message) {
                this.$data.errors = error.message
            }
            //alert(_.flatMap(_.values(error.response.data.errors)).join('\n'))
        }
    }
}

export default handleError;

