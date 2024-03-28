<script setup>
import handleErrorMixin from '../mixins/HandleErrorMixin'
import { useTimeoutFn } from '@vueuse/core'
</script>
<script>
export default {
    mixins: [handleErrorMixin],
    props: ['userid'],
    data() {
        return {
            showLoading: false,
            message: null,
            showLoadingBtnUser: false,
            user: {
                id: null,
                email: null,
                username: null,
                password: null,
                is_verified: null,
                created_at: null,
                created_by_username: null,
                updated_at: null,
                updated_by_username: null,
                deleted_at: null,
                deleted_by_username: null
            },
        }
    },
    watch: {
        userid: {
            //immediate: true,
            handler(newVal, oldVal) {
                this.read_user()
            }
        }
    },
    methods: {
        read_user() {
            if( ! this.$props.userid) return

            this.$data.showLoading = true
            this.$data.message = null
            this.axios.get('/users/' + this.$props.userid)
                .then((res) => {
                    this.$data.message = null
                    if (res.data.message) {
                        this.$data.message = res.data.message
                    } else {
                        this.$data.user = res.data
                    }
                })
                .catch(this.handleError)
                .finally(() => {
                    this.$data.showLoading = false
                })
        },
        add_user() {},
        edit_user() {
            if( ! this.$props.userid) return

            let params = {
                username: this.$data.user.username,
                password: this.$data.user.password,
                is_verified: this.$data.user.is_verified,
            }

            this.$data.showLoadingBtnUser = true
            this.$data.message = null
            this.axios.patch('/users/' + this.$props.userid, params)
                .then((res) => {
                    this.$data.message = null
                })
                .catch(this.handleError)
                .finally(() => {
                    this.$data.showLoadingBtnUser = false
                })
        },
        delete_user() {
            if( ! this.$props.userid) return

            if( ! confirm('유저를 탈퇴 처리하시겠습니까?')) return

            this.$data.message = null
            this.axios.delete('/users/' + this.$props.userid)
                .then((res) => {
                    this.$data.message = '탈퇴되었습니다.'

                    if(this.$props.userid == 'me') {
                        const { isPending, start, stop } = useTimeoutFn(() => {
                            this.$router.push('/request')
                        }, 3000)
                        start()
                    }
                })
                .catch(this.handleError)
        }
    },
    mounted() {
        this.read_user()
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

        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>ID</h3>
            </div>
            <div class="col-6">
                <input v-model="user.id" type="text" disabled>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>email</h3>
            </div>
            <div class="col-6">
                <input v-model="user.email" type="email" disabled>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>username</h3>
            </div>
            <div class="col-6">
                <input v-model="user.username" type="text">
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6">
                <h3>password</h3>
            </div>
            <div class="col-6">
                <input v-model="user.password" type="password" placeholder="변경할 패스워드를 입력하세요.">
            </div>
        </div>

        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>is_verified</h3>
            </div>
            <div class="col-6">
                <input v-model="user.is_verified" type="checkbox">
            </div>
        </div>

        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>등록일시</h3>
            </div>
            <div class="col-6">
                <input v-model="user.created_at" type="text" disabled>
            </div>
        </div>

        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>등록자</h3>
            </div>
            <div class="col-6">
                <input v-model="user.created_by_username" type="text" disabled>
            </div>
        </div>
        
        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>최근 갱신일시</h3>
            </div>
            <div class="col-6">
                <input v-model="user.updated_at" type="text" disabled>
            </div>
        </div>

        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>최근 갱신자</h3>
            </div>
            <div class="col-6">
                <input v-model="user.updated_by_username" type="text" disabled>
            </div>
        </div>

        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>탈퇴일시</h3>
            </div>
            <div class="col-6">
                <input v-model="user.deleted_at" type="text" disabled>
            </div>
        </div>

        <div class="row mt-3" v-if="'me' != $props.userid">
            <div class="col-6">
                <h3>탈퇴처리자</h3>
            </div>
            <div class="col-6">
                <input v-model="user.deleted_by_username" type="text" disabled>
            </div>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-green flex justify-center" @click="edit_user" v-bind:disabled="showLoadingBtnUser">
                <svg v-if="showLoadingBtnUser" aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                </svg>
                <div>유저 저장</div>
            </button>
        </div>

        <div class="row mt-3">
            <button type="button" class="btn btn-red flex justify-center" @click="delete_user" v-bind:disabled="user.deleted_at != null">
                <div>{{ user.deleted_at != null ? '탈퇴됨' : '유저 탈퇴' }}</div>
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