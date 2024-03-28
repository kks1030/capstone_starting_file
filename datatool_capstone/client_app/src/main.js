import { createApp } from 'vue/dist/vue.esm-bundler.js'
import './style.css'
//import AppVue from './App.vue'
//import UploaderVue from './components/Uploader.vue'
//import ControlVue from './components/Control.vue'

import axios from 'axios'
import { DateTime } from 'luxon';
import { createWebHistory, createRouter } from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    //strict: true,
    routes: [
        {
            path: '/',
            component: () => import('./App.vue'), //AppVue,
            children: [
                { path: 'request', component: () => import('./components/Uploader.vue') },
                { path: 'request/:timestamp/control', component: () => import('./components/Control.vue') },
                { path: 'users/me', component: () => import('./components/Me.vue') },
                { path: 'users/:userid?', component: () => import('./components/Users.vue'), props: true },
            ],
        },
    ]
});

let app = createApp({})

app.use(router)

import HeaderVue from './components/common/Header.vue'
import SpinnerVue from './components/common/Spinner.vue'
import LoginModalVue from './components/common/LoginModal.vue'
import CheckboxVue from './components/common/Checkbox.vue'
import RadioCheckboxListVue from './components/common/RadioCheckboxList.vue'
import RadioCheckboxList2Vue from './components/common/RadioCheckboxList2.vue'

app.component('HeaderVue', HeaderVue)
app.component('SpinnerVue', SpinnerVue)
app.component('LoginModalVue', LoginModalVue)
app.component('CheckboxVue', CheckboxVue)
app.component('RadioCheckboxListVue', RadioCheckboxListVue)
app.component('RadioCheckboxList2Vue', RadioCheckboxList2Vue)


if(import.meta.env.MODE == 'dev') {
    console.info('mode=dev')
}
axios.defaults.baseURL = import.meta.env.VITE_API_URL

axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.headers.post['Accept'] = 'application/json'

app.config.globalProperties.axios = axios
app.config.globalProperties.DateTime = DateTime

app.mount('#app')

