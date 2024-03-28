<script setup>
import { markRaw } from 'vue'
import CardListVue from './common/CardList.vue'
import CompareDirVue from './control/CompareDir.vue'
import ControlHistoryVue from './control/ControlHistory.vue'
import DupCleanVue from './control/DupClean.vue'
import FilterVue from './control/Filter.vue'
import ListingVue from './control/Listing.vue'
import LogMonitorVue from './control/LogMonitor.vue'
import ParseVue from './control/Parse.vue'
import QtVue from './control/Qt.vue'
import ReplaceVue from './control/Replace.vue'
import SplitVue from './control/Split.vue'
import SplitConditionVue from './control/SplitCondition.vue'
import SimilarityVue from './control/Similarity.vue'
import ValidateColVue from './control/ValidateCol.vue'

Notification.requestPermission()
</script>

<script>


export default {
    data() {
      return {
        meta: null,
        currentSelection: null,
        cardList: [
          {
            id: markRaw(ValidateColVue),
            imgUrl : '',
            name : "헤더 검사",
            description : '여러개의 파일의 헤더가 통일되어 있는지 확인해줍니다. 문제가 있는 파일은 파일명을 변경하여 알려줍니다.'
          },
          {
            id: markRaw(SimilarityVue),
            imgUrl : '',
            name : "유사도 검사",
            description : '두 문장의 BLEU 점수를 산출하여 유사도 column을 추가해 줍니다.'
          },
          {
            id: markRaw(SplitVue),
            imgUrl : '',
            name : "분할/합치기/필터링",
            description : '파일을 분할기준에 따라서 분할하거나 합칩니다. 무효문장을 제외하거나 재정렬할 수도 있습니다.'
          },
          {
            id: markRaw(QtVue),
            imgUrl : '',
            name : '기계검수',
            description : '기계검수를 합니다.'
          },
          {
            id: markRaw(ListingVue),
            imgUrl : '',
            name : '파일 리스트 만들기',
            description : '엑셀로 파일 리스트를 만듭니다. 각 파일의 총 어절수를 추가할 수도 있습니다.'
          },
          {
            id: markRaw(CompareDirVue),
            imgUrl : '',
            name : '폴더 비교',
            description : '두개의 폴더에 들어가 있는 파일명을 서로 비교하여 어느 한쪽에만 없는 파일을 찾을 수 있습니다.'
          },
          {
            id: markRaw(SplitConditionVue),
            imgUrl : '',
            name : '최종본 작성',
            description : 'N사 최종본 만들기'
          },
          {
            id: markRaw(DupCleanVue),
            imgUrl : '',
            name : '중복 제거',
            description : '문장을 정렬하고 중복인 문장을 표시합니다.'
          },
          {
            id: markRaw(FilterVue),
            imgUrl : '',
            name : '추출',
            description : '엑셀 파일에서 값을 읽어서 파일을 추출하거나 엑셀의 row를 추출합니다.'
          },
          {
            id: markRaw(ReplaceVue),
            imgUrl : '',
            name : '단어 교체',
            description : '엑셀 파일에서 값을 읽어서 단어를 일부/전체 교체합니다.'
          },
          {
            id: markRaw(ParseVue),
            imgUrl : '',
            name : '파싱',
            description : '파일을 엑셀로 파싱합니다. "서버에서는 불가" 표시가 있는 기능은 관리자에게 직접 요청 바랍니다.'
          },
        ]
      }
    },
    methods: {
      toggleShowTimeline(isShow) {
        if(typeof(isShow) == 'undefined') {
          this.$refs.controlHistory.$data.showTimeline = !this.$refs.controlHistory.$data.showTimeline
        } else {
          this.$refs.controlHistory.$data.showTimeline = isShow
        }
        
        if(this.$refs.controlHistory.$data.showTimeline) this.fetchMeta()
      },
      fetchMeta() {
        this.axios.get('/main/request/' + this.$route.params.timestamp + '/control')
        .then((res) => {
          res.data.meta.history = res.data.meta.history.reverse() // 최신순
          this.$data.meta = res.data.meta
        })
        .catch(this.handleError)
      }
    },
    mounted() {
      this.fetchMeta()
    }
}
</script>

<template>
<div>
  <h1 v-if="meta">{{ meta.filename + '로 무엇을 하시겠습니까?' }}</h1>
  
  <CardListVue v-model="currentSelection" :cardList="cardList"/>
  <component :is="currentSelection" v-on:toggleShowTimeline="toggleShowTimeline"></component>
  <div>
    <div class="container">
        <div class="mt-3">
          <button type="button" @click="toggleShowTimeline()" class="btn btn-blue">🔍 히스토리</button>
        </div>
    </div>
  </div>
  <ControlHistoryVue ref="controlHistory" :meta="meta"></ControlHistoryVue>
  <LogMonitorVue></LogMonitorVue>
</div>
</template>


<style scoped>
.btn {
  width: 100%;
}
</style>