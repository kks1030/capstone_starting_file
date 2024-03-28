<script>
import handleErrorMixin from './mixins/HandleErrorMixin';
import { useWebNotification } from '@vueuse/core'

export default {
    mixins: [handleErrorMixin],
    data() {
        return {
            // 파일 리스트 번호
            fileIndex: 0,
            // 등록할 전체 파일 사이즈
            totalFileSize: 0,
            // 파일 리스트
            fileList: [],
            // 파일 사이즈 리스트
            fileSizeList: [],
            // 등록 가능한 하나의 파일 사이즈 MB
            uploadSize: 500,
            // 등록 가능한 모든 파일 사이즈의 합 MB
            maxUploadSize: 500,
            showFileDragDesc: true,
            showFileListTable: false,
            showLoading: false,
            message: '업로드 가능파일 .zip',
            dropZoneBackgroundColor: null,
            requestList: [],
            isRequestListLoading: false,
        };
    },
    methods: {
        selectFile(obj) {
            // obj 는 event 혹은 files
            let files = null
            if(obj.currentTarget) {
                files = obj.currentTarget.files
            } else {
                files = obj
            }
            
            // 다중파일 등록
            if (files != null && files.length > 0) {
                this.$data.showFileDragDesc = false;
                this.$data.showFileListTable = true;
            }
            else {
                this.$data.showFileDragDesc = true;
                this.$data.showFileListTable = false;
            }
            for (var i = 0; i < files.length; i++) {
                // 파일 이름
                var fileName = files[i].name;
                var fileNameArr = fileName.split("\.");
                // 확장자
                var ext = fileNameArr[fileNameArr.length - 1];
                var fileSize = files[i].size; // 파일 사이즈(단위 :byte)
                console.log("fileSize=" + fileSize);
                if (fileSize <= 0) {
                    console.log("0kb file return");
                    return;
                }
                var fileSizeKb = fileSize / 1024; // 파일 사이즈(단위 :kb)
                var fileSizeMb = fileSizeKb / 1024; // 파일 사이즈(단위 :Mb)
                var fileSizeStr = "";
                if ((1024 * 1024) <= fileSize) { // 파일 용량이 1메가 이상인 경우 
                    console.log("fileSizeMb=" + fileSizeMb.toFixed(2));
                    fileSizeStr = fileSizeMb.toFixed(2) + " Mb";
                } else if ((1024) <= fileSize) {
                    console.log("fileSizeKb=" + parseInt(fileSizeKb));
                    fileSizeStr = parseInt(fileSizeKb) + " kb";
                } else {
                    console.log("fileSize=" + parseInt(fileSize));
                    fileSizeStr = parseInt(fileSize) + " byte";
                }

                if ( ! ['html', 'xml', 'hwp', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'png', 'pdf', 'jpg', 'jpeg', 'gif', 'zip'].some(data => data == ext)) {
                    // 확장자 체크
                    alert("등록이 불가능한 파일 입니다.(" + fileName + ")");
                } else if (fileSizeMb > this.$data.uploadSize) {
                    // 파일 사이즈 체크
                    alert("용량 초과\n업로드 가능 용량 : " + this.$data.uploadSize + " MB");
                    break;
                } else {
                    // 전체 파일 사이즈
                    this.$data.totalFileSize += fileSizeMb;
                    // 파일 배열에 넣기
                    this.$data.fileList[this.$data.fileIndex] = files[i];
                    // 파일 사이즈 배열에 넣기
                    this.$data.fileSizeList[this.$data.fileIndex] = fileSizeMb;
                    // 파일 번호 증가
                    this.$data.fileIndex++;
                }
            }

            this.uploadFile();
        },
        dragenter(e) {
            e.stopPropagation();
            e.preventDefault();
            // 드롭다운 영역 css
            this.$data.dropZoneBackgroundColor = '#E3F2FC';
        },
        dragleave(e) {
            e.stopPropagation();
            e.preventDefault();
            // 드롭다운 영역 css
            this.$data.dropZoneBackgroundColor = '';
        },
        dragover(e) {
            e.stopPropagation();
            e.preventDefault();
            // 드롭다운 영역 css
            this.$data.dropZoneBackgroundColor = '#E3F2FC';
        },
        drop(e) {
            e.preventDefault();
            // 드롭다운 영역 css
            this.$data.dropZoneBackgroundColor = '';
            var files = e.dataTransfer.files;
            if (files != null) {
                if (files.length < 1) {
                    /* alert("폴더 업로드 불가"); */
                    console.log("폴더 업로드 불가");
                    return;
                }
                else {
                    this.selectFile(files);
                }
            }
            else {
                alert("ERROR");
            }
        },
        uploadFile() {
            this.$data.showLoading = true
            this.$data.message = null
            // 등록할 파일 리스트
            let uploadFileList = Object.keys(this.$data.fileList);
            // 파일이 있는지 체크
            if (uploadFileList.length == 0) {
                // 파일등록 경고창
                alert("파일이 없습니다.");
                return;
            }
            // 용량을 500MB를 넘을 경우 업로드 불가
            if (this.$data.totalFileSize > this.$data.maxUploadSize) {
                // 파일 사이즈 초과 경고창
                alert("총 용량 초과\n총 업로드 가능 용량 : " + this.$data.maxUploadSize + " MB");
                return;
            }
            
            // 등록할 파일 리스트를 formData로 데이터 입력
            let formData = new FormData(document.querySelector('#uploadForm'))
            for (let i = 0; i < uploadFileList.length; i++) {
                formData.append('files', this.$data.fileList[uploadFileList[i]])
            }
            this.axios.post('/upload/file', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    Accept: 'application/json',
                }
            })
            .then((res) => {
                // 성공했을 경우
                this.$data.showLoading = false;
                this.$router.push('/request/' + res.data.timestamp + '/control')
            })
            .catch(this.handleError)
            .finally(() => {
                this.$data.showLoading = false
                this.$data.showFileListTable = false
                this.$data.message = '업로드 가능파일 .zip'
            })
            
        },
        parseRequestList() {
            this.$data.isRequestListLoading = true
            this.axios.get('/parse/request/list', {})
            .then((res) => {
                this.$data.isRequestListLoading = false

                // 성공했을 경우
                let sortable = [];
                for (var id in res.data) {
                    sortable.push([res.data[id][0], res.data[id][1]]);
                }

                sortable.sort(function(a, b) {
                    return b[0] - a[0];
                });

                this.$data.requestList = sortable.map((x) => {
                    let time = this.DateTime.fromSeconds(parseFloat(x[0]))
                    return {
                        timestamp: x[0],
                        filename: x[1],
                        abtime: time.toLocaleString(this.DateTime.DATETIME_MED),
                        retime: time.toRelativeCalendar()
                    }
                })
            })
            .catch((e) => {
                this.$data.isRequestListLoading = true
                this.handleError(e)
            })
        },
        deleteRequest(item) {
            if(confirm('정말 삭제하시겠습니까?') == false) return

            item.isDeleting = true
            this.axios.delete('/request/' + item.timestamp)
                .then((res) => {
                    // 성공했을 경우
                    this.parseRequestList()
                })
                .catch(this.handleError)

        }
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
            <h1>글나무</h1>
        </div>
        <div class="container text-center">
            <div class="row">
                <div class="col">
                    <h1>{{ message }}</h1>
                </div>
            </div>
        </div>
        <div id="upload_section" class="container text-center">
            <div class="hidden">
                <div class="col">
                    <input type="file" ref="input_file" multiple="multiple" @change="selectFile" />
                    <button class="upload-btn" style="display:none;">파일선택</button>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <form name="uploadForm" id="uploadForm" enctype="multipart/form-data" method="post">
                        <div id="dropZone" class="relative flex flex-col text-gray-400 border border-gray-200 border-dashed rounded cursor-pointer" :style="{'background-color': dropZoneBackgroundColor}" @dragenter.prevent @dragover.prevent @drop.prevent @dragenter="dragenter" @dragleave="dragleave" @dragover="dragover" @drop="drop">
                            <ul v-if="showFileListTable">
                                <li v-for="ff in fileList">{{ ff.name }}</li>
                            </ul>
                            <div v-if="!showLoading" class="flex flex-col items-center justify-center py-10 text-center">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                </svg>
                                <p class="m-0">파일을 여기로 드래그 드롭 해주세요.</p>
                                <span class="text-blue-600 underline" @click="$refs.input_file.click()">또는 파일을 선택하세요.</span>
                            </div>
                            <SpinnerVue v-if="showLoading"></SpinnerVue>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div class="container text-center">
            <div class="row">
                <table class="table-auto w-full" v-if="requestList.length">
                    <thead>
                        <tr>
                            <th width="25%"></th>
                            <th width="50%"></th>
                            <th width="25%"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="x in requestList">
                            <td>
                                <span class="bg-green-700 hover:bg-green-800 inline-block whitespace-nowrap rounded-full px-[0.65em] pb-[0.25em] pt-[0.35em] text-center align-baseline text-[0.75em] font-bold leading-none">
                                    {{ x.retime }}
                                </span>
                                {{ x.abtime }}
                            </td>
                            <td>
                                <router-link :to="'/request/' + x.timestamp + '/control'" >
                                    {{ x.filename }}
                                </router-link>
                            </td>
                            <td>
                                <button type="button" class="btn btn-red group relative duration-300" @click="deleteRequest(x)">
                                    <svg v-if="x.isDeleting" aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                                        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                                    </svg>
                                    삭제
                                    <span class="absolute hidden group-hover:flex -left-5 -top-2 -translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:top-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-b-transparent after:border-t-gray-700">
                                        모든 파일과 로그는 삭제되며 복구할 수 없습니다.
                                    </span>
                                </button>
                                <button type="button" class="btn btn-blue" @click="copyDirToClipboard($event, x.timestamp)" title="sshfs에서 열기">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="inline h-4">
                                        <path fill="#E5E7EB" d="M0 96C0 60.7 28.7 32 64 32H196.1c19.1 0 37.4 7.6 50.9 21.1L289.9 96H448c35.3 0 64 28.7 64 64V416c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V96zM64 80c-8.8 0-16 7.2-16 16V416c0 8.8 7.2 16 16 16H448c8.8 0 16-7.2 16-16V160c0-8.8-7.2-16-16-16H286.6c-10.6 0-20.8-4.2-28.3-11.7L213.1 87c-4.5-4.5-10.6-7-17-7H64z"/>
                                    </svg>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="row">
                <button type="button" class="btn btn-blue" @click="parseRequestList">
                    <svg v-if="isRequestListLoading" aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                    </svg>
                    업로드한 건을 시간순으로 보여드립니다.
                </button>
            </div>
        </div>

    </div>
</template>