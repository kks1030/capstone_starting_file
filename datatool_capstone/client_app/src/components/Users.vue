<script setup>
import handleErrorMixin from './mixins/HandleErrorMixin'
import UserVue from './users/User.vue';
import UserScopesVue from './users/UserScopes.vue';

DataTable.use(DataTablesCore);
</script>

<script>

export default {
    mixins: [handleErrorMixin],
    props: ['userid'],
    data() {
        return {
            showLoading: false,
            message: null,
            page: 0,
            search_keyword: null,
            search_is_verified: null,
            users: [],
        };
    },
    watch: {
        //userid: {
        //    immediate: true, // axios Authorization 넣는 것보다 늦게 동작해야 하기때문에, mounted()로 이동
        //    handler(newVal, oldVal) {
        //        this.current_userid = this.$props.userid
        //    }
        //}
        search_is_verified: {
            handler(newVal, oldVal) {
                this.fetchUsers()
            }
        }
    },
    methods: {
        fetchUsers() {
            this.$data.showLoading = true;
            let params = {
                page:   this.$data.page,
                search_keyword: this.$data.search_keyword,
                is_verified: this.$data.search_is_verified
            }
            this.axios.get('/users', {params})
            .then((res) => {
                // 성공했을 경우
                this.$data.users = res.data
            })
            .catch(this.handleError)
            .finally(() => {
                this.$data.showLoading = false
            })
        },
        keyup($ev) {
            console.log($ev)
        },
        detailUser(item) {
            this.$router.push('/users/' + item.id )
        },
    },
    mounted() {
        this.fetchUsers()
    }
}
</script>


<style scoped>
#uploadForm:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}
</style>

<template>
<div class="container">
    <div class="container text-center">
        <div class="row">
            <div class="col">
                <h1>{{ message }}</h1>
            </div>
        </div>
    </div>

    <div class="container text-center">
        <div class="row">
            <input
                v-model="search_keyword"
                placeholder="검색"
                @keyup.enter="fetchUsers"
                type="text"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <RadioCheckboxList2Vue v-model="search_is_verified" :columns="{null:'모두', true:'인증됨', false:'인증안됨'}" type="radio"></RadioCheckboxList2Vue>
        </div>    
    </div>

    <div class="container text-center">
        <div class="row" v-if="0 < users.length">
            <table class="table-auto w-full">
                <thead>
                    <tr>
                        <th width="25%">이메일</th>
                        <th width="50%">이름</th>
                        <th width="25%">인증</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in users">
                        <td><a href="#" @click="detailUser(item)">{{ item.email }}</a></td>
                        <td>{{ item.username }}</td>
                        <td>{{ item.is_verified ? 'Verified' : null }}</td>
                    </tr>
                </tbody>

            </table>
        </div>
        <div class="row flex">
            <table class="table-auto w-full">
                <tfoot>
                    <tr>
                        <td><a href="#" @click="page=0;fetchUsers()">{{ '<<' }}</a></td>
                        <td><a href="#" @click="page-=1;fetchUsers()">{{ '<' }}</a></td>
                        <td><a href="#" @click="page+=1;fetchUsers()">{{ '>' }}</a></td>
                    </tr>
                </tfoot>
            </table>
        </div>
        <div class="row" v-if="0 == users.length">
            <p>유저를 찾을 수 없습니다.</p>
        </div>
    </div>

    <div class="container text-center" v-if="$props.userid">
        <div class="row">
            <UserVue :userid="$props.userid"></UserVue>
        </div>
    </div>

    <div class="container text-center" v-if="$props.userid">
        <div class="row">
            <UserScopesVue :userid="$props.userid" :readonly="false"></UserScopesVue>
        </div>
    </div>
    
</div>
</template>