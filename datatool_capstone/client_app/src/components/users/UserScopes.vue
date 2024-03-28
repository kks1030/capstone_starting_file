<script setup>
import handleErrorMixin from '../mixins/HandleErrorMixin'
</script>
<script>
export default {
    mixins: [handleErrorMixin],
    props: ['userid', 'readonly'],
    data() {
        return {
            showLoading: false,
            message: null,
            showLoadingBtnUserScopes: false,
            user_scopes: {
                'datatool': false,
                'deletedocu': false,
                'assignuserscope': false,
                'b-user'    : false,
                'r-user'    : false,
                'e-user'    : false,
                'a-user'    : false,
                'd-user'    : false,
            },
            scopes_desc: {
                'datatool': 'Can `upload` files, `download` files and `execute` jobs.',
                'deletedocu': 'Can delete file in own IP address range.',
                'assignuserscope': 'Can assign scopes to users',
                'b-user'    : 'Can browse users.',
                'r-user'    : 'Can read user information.',
                'e-user'    : 'Can edit user information.',
                'a-user'    : 'Can add user accounts',
                'd-user'    : 'Can delete user accounts',
            },
        }
    },
    watch: {
        userid: {
            //immediate: true,
            handler(newVal, oldVal) {
                this.read_user_scope()
            }
        }
    },
    methods: {
        reset_user_scope() {
            for(let k in this.$data.user_scopes){
                this.$data.user_scopes[k] = false
            }
        },
        read_user_scope() {
            if( ! this.$props.userid) return
            
            this.$data.showLoadingBtnUserScopes = true
            this.reset_user_scope()  
            this.axios.get('/users/' + this.$props.userid + '/scope')
                .then((res) => {
                    this.$data.message = null
                    if (res.data.message) {
                        this.$data.message = res.data.message
                    } else {
                        res.data.forEach((x) => {
                            this.$data.user_scopes[x.scope] = true
                        })
                    }
                })
                .catch(this.handleError)
                .finally(() => {
                    this.$data.showLoadingBtnUserScopes = false
                })
        },
        edit_user_scope() {
            if( ! this.$props.userid) return

            this.$data.showLoading = true
            //this.reset_user_scope()

            this.axios.put('/users/' + this.$props.userid + '/scope', this.$data.user_scopes)
                .then((res) => {
                    this.$data.message = null
                    if (res.data.message) {
                        this.$data.message = res.data.message
                    }
                })
                .catch(this.handleError)
                .finally(() => {
                    this.$data.showLoading = false
                })
        },
    },
    mounted() {
        this.read_user_scope()
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

    <div class="container">
        <div class="row mt-3">
            <div class="col-6">
                <h3>User Scopes</h3>
            </div>
            <div class="col-6">
                <ul>
                    <li v-for="v, k in user_scopes">
                        <CheckboxVue v-model="user_scopes[k]" :label="scopes_desc[k]" :readonly="$props.readonly"></CheckboxVue>
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="row mt-3" v-if=" ! $props.readonly">
            <button type="button" id="logsim" class="btn btn-green flex justify-center" @click="edit_user_scope" v-bind:disabled="showLoadingBtnUserScopes">
                <svg v-if="showLoadingBtnUserScopes" aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                </svg>
                <div>User Scope 저장</div>
            </button>
        </div>
    </div>
</div>
</template>

<style scoped>
.btn {
    width: 100%;
}
</style>