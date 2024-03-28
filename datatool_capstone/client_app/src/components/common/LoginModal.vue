<script>
import { useLocalStorage } from '@vueuse/core'
import handleErrorMixin from '../mixins/HandleErrorMixin';

export default {
    props: ['show'],
    mixins: [handleErrorMixin],
    data() {
        return {
            showLoading: false,
            email: null,
            pw: null,
            isLogin: null,  // null: loading spinner 보여줌, false: 로그인 form보여줌, true: 로그인정보 표시
            isLogging: false,   // 로그인 시도중인지. 버튼 스피너
            me: {
                id: null,
                email: null,
                username: null,
                is_verified: null,
                scopes: null,
            },
            authorizationInStorage: useLocalStorage('Authorization', null)
        }
    },
    watch: {
        authorizationInStorage: {
            immediate: true,    // mounted() 보다 빠르게 동작. axios 쓸일 있으면 이것보다 늦게 동작해야함. 즉.. watch()에서 axios 쓰는 짓은 벌이지 마쇼
            handler(newVal, oldVal) {
                this.axios.defaults.headers.common['Authorization'] = this.$data.authorizationInStorage
            }
        }
    },
    methods: {
        login() {
            this.$data.isLogging = true
            this.axios.post('/token', {
                username: this.$data.email,
                password: this.$data.pw,
                grant_type: 'password',
            }, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then((res) => {
                // 성공했을 경우
                this.$data.authorizationInStorage = res.data.token_type + ' ' + res.data.access_token
                this.$data.errors = null
                this.$data.isLogin = true
                this.$emit('close')
            })
            .catch(this.loginErrorHandler)
            .finally(() => {
                this.$data.isLogging = false
            })
        },
        logout() {
            this.axios.post('/token/revoke', {}, {})
            .then((res) => {
                // 성공했을 경우
                this.$data.authorizationInStorage = null
                this.axios.defaults.headers.common['Authorization'] = null
                this.$data.errors = null
                this.$data.isLogin = false
            })
            .catch(this.loginErrorHandler)
        },
        chkLogin() {
            this.axios.get('/users/me')
            .then((res) => {
                // 성공했을 경우
                this.$data.errors = null
                this.$data.isLogin = true
                this.$data.me = res.data
            })
            .catch(this.loginErrorHandler)
        },
        loginErrorHandler(ex) {
            if( ! ex.response) {
                // unexpected error
                this.$data.errors = ex.message
            } else if(typeof ex.response.data.detail == 'object') {
                this.$data.errors = ex.response.data.detail.map((x) => { return x.msg + ' ' + x.loc.join(' ') }).join(', ')
            } else if(typeof ex.response.data.detail == 'string') {
                this.$data.errors = ex.response.data.detail
            }

            this.$data.isLogin = false
            this.resetMe()
        },
        resetMe() {
            this.$data.me = {
                id: null,
                email: null,
                username: null,
                is_verified: null,
                scopes: null,
            }
        },
    },
    updated() {
        if(this.show) {
            this.chkLogin()
        }
    }
}
</script>
<template>
    <Transition name="modal">
        <div v-if="show" class="modal-mask">
            <div class="modal-container z-50">
                <slot name="header"></slot>
                <div v-if="isLogin == null" class="m-4">
                    <SpinnerVue v-if="showLoading"></SpinnerVue>
                </div>
                <div v-if="isLogin" class="m-4">
                    <p class="text-gray-500 text-center"><label class="text-red-500">{{ me.username ? me.username : null }}</label>로 로그인되었습니다.</p>
                    <p class="text-center m-4">
                        <button
                            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                            type="button"
                            @click="this.$router.push('/users'); $emit('close')">
                            Manage Users
                        </button>
                    </p>
                    <p class="text-center m-4">
                        <button
                            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                            type="button"
                            @click="this.$router.push('/users/me'); $emit('close')">
                            Manage Me
                        </button>
                    </p>
                    <p class="text-center m-4">
                        <button
                            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                            type="button"
                            @click="logout">
                            Sign Out
                        </button>
                    </p>
                </div>
                <form v-if="isLogin == false" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                    <div class="mb-4">
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
                            Email
                        </label>
                        <input
                            class="text-white shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            v-model="email"
                            @keyup.enter="login"
                            type="email"
                            placeholder="email"
                            autocomplete="email">
                    </div>
                    <div class="mb-6">
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
                            Password
                        </label>
                        <input
                            class="text-white shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                            v-model="pw"
                            @keyup.enter="login"
                            type="password"
                            placeholder="Password"
                            autocomplete="password">
                        <p class="text-red-500 text-xs italic">{{errors}}</p>
                    </div>
                    <div class="flex items-center justify-between">
                        <button
                            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                            type="button"
                            @click="login">
                            <svg v-if="isLogging" aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                            </svg>
                            Sign In
                        </button>
                        <a class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800" href="#">
                            Forgot Password?
                        </a>
                    </div>
                </form>
                <p class="text-center text-gray-500 text-xs">
                    &copy;2024 글나무 Corp. All rights reserved.
                </p>
            </div>
        </div>
    </Transition>
</template>

<style>
.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    transition: opacity 0.3s ease;
}

.modal-container {
    width: 500px;
    margin: auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
}


.modal-body {
    margin: 20px 0;
}

.modal-default-button {
    float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
    opacity: 0;
}

.modal-leave-to {
    opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
}
</style>