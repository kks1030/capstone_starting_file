<script>
import { useWebNotification } from '@vueuse/core'
import ControlMixin from '../mixins/ControlMixin'

export default {
    mixins: [ControlMixin],
    props: ['meta'],
    data() {
        return {
          showTimeline: false,
        }
    },
    methods: {
        close() {
          this.$data.showTimeline = false
        },
        bgColor(historyItem) {
          if(historyItem.status == 'Success') {
            return 'bg-green-500'
          } else if(historyItem.status == 'Running') {
            return 'bg-gray-300'
          } else if(historyItem.status == 'Error') {
            return 'bg-red-500'
          }
        },
        toTimeTaken(historyItem) {
          const date2 = this.DateTime.fromSeconds(historyItem.start_at)

          let text = date2.toLocaleString(this.DateTime.DATETIME_MED)

          if(historyItem.end_at) {
            const date1 = this.DateTime.fromSeconds(historyItem.end_at)
            const diff = date1.diff(date2, ['minutes', 'seconds'])
            text += ' (' + diff.toFormat('m분 s.S초')  + ')'
          }
          return text
        },
        copyHistoryItemParamsToClipboard(params) {
          window.navigator.clipboard.writeText(JSON.stringify(params,null,2))
        },
    },
    mounted() {
      
    },
}


</script>

<template>
<div v-if="showTimeline" ref="controlHistory" class='fixed inset-y-0 right-0 border' style="background-color:hsla(50, 33%, 25%, .85);">
    <div class="fixed">
      <a href="#" @click="close()" class="text-white">닫기</a>
    </div>
    <div class="p-4">
        <h1 class="text-4xl text-center font-semibold mb-6">
          히스토리
          <a href="#" class="transititext-primary text-primary transition duration-150 ease-in-out hover:text-primary-600 focus:text-primary-600 active:text-primary-700 dark:text-primary-400 dark:hover:text-primary-500 dark:focus:text-primary-500 dark:active:text-primary-600"
          title="경로를 복사합니다." @click="copyDirToClipboard($event, $route.params.timestamp)">📁</a>
        </h1>
        <div class="container">
          <div class="flex flex-col md:grid grid-cols-12 text-gray-50">
            <div v-for="item in meta.history" class="flex md:contents">
              <div class="col-start-2 col-end-4 mr-10 md:mx-auto relative">
                <div class="h-full w-6 flex items-center justify-center">
                  <div :class="bgColor(item)" class="h-full w-1 pointer-events-none"></div>
                </div>
                <div :class="bgColor(item)" class="w-6 h-6 absolute top-1/2 -mt-3 rounded-full shadow text-center">
                  <div v-if="item.status == 'Success'">
                    ⭕
                  </div>
                  <div v-if="item.status == 'Running'">
                    ⏳
                  </div>
                  <div v-if="item.status == 'Error'">
                    ☠️
                  </div>
                </div>
              </div>
              <div :class="bgColor(item)" class="col-start-4 col-end-12 p-4 rounded-xl my-4 mr-auto shadow-md w-full">
                <h3 class="font-semibold text-lg mb-1">
                  {{ titles[item.task] }}
                  <a href="#" class="transititext-primary text-primary transition duration-150 ease-in-out hover:text-primary-600 focus:text-primary-600 active:text-primary-700 dark:text-primary-400 dark:hover:text-primary-500 dark:focus:text-primary-500 dark:active:text-primary-600"
                  :title="JSON.stringify(item.params)" @click="copyHistoryItemParamsToClipboard(item.params)">🔑</a>
                </h3>
                <a href="#" class="">
                  <span class="absolute hidden group-hover:flex -left-5 -top-2 -translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:top-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-b-transparent after:border-t-gray-700">
                      모든 파일과 로그는 삭제되며 복구할 수 없습니다.
                  </span>
                </a>
                <p class="leading-tight text-justify w-full">
                  {{  toTimeTaken(item) }}
                </p>
                <div v-if="item.result_file" class="mt-3 flex items-stretch">
                  <button class="btn btn-green flex" @click="download(item.result_file)" type="button">
                    <svg class="color-white" width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 15C3 17.8284 3 19.2426 3.87868 20.1213C4.75736 21 6.17157 21 9 21H15C17.8284 21 19.2426 21 20.1213 20.1213C21 19.2426 21 17.8284 21 15" stroke="#FFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M12 3V16M12 16L16 11.625M12 16L8 11.625" stroke="#FFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>

                  <button class="btn btn-red" type="button">
                    ?
                  </button>
                </div>
                <div v-if="item.msg" class="mt-3">
                  <p>{{ item.msg }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
</div>
</template>

<style scoped>

</style>