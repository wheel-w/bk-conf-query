<template>
    <div style="height:100%">
        <bk-exception class="exception-wrap-item" type="403" v-if="!isBizAuth">
            <span>{{$t('无业务权限')}}</span>
            <div class="text-subtitle">{{$t('你没有相应业务的访问权限，请前往申请相关业务权限')}}</div>
            <div class="text-wrap">
                <span class="text-btn" @click="applyBizAuth">{{$t('去申请')}}</span>
            </div>
        </bk-exception>
        <div class="host-sea-content" v-if="isBizAuth">
            <div class="my-dialog">
                <bk-dialog v-model="treeVisible"
                    :fullscreen="true"
                    :show-footer="true"
                    render-directive="if"
                >
                    <div>
                        <bk-tab :active.sync="active" :type="currentType" style="margin-top: 20px;;">
                            <bk-tab-panel
                                v-for="(panel, index) in panels"
                                v-bind="panel"
                                :key="index">
                            </bk-tab-panel>
                            <div v-if="active === 'ipSelect'" style="height:calc(100vh - 350px);display:flex;width: calc(80vw - 200px);">
                                <div class="my-tree">
                                    <div style="text-align:center">
                                        <bk-button :theme="'default'" type="submit" @click="handleReset" class="mr10" style="width: 80%;">
                                            {{$t('重置')}}
                                        </bk-button>
                                    </div>
                                
                                    <section style="margin-top:15px">
                                        <bk-big-tree ref="tree"
                                            @select-change="treeDataChange"
                                            :selectable="true"
                                            :data="treeData"
                                            node-icon="bk-icon icon-rtx"
                                            :padding="30">
                                        </bk-big-tree>
                                    </section>
                                </div>
                                <div class="my-host-table" v-bkloading="{ isLoading: isDataLoading , zIndex: 10 }">
                                    <div class="my-host-table-content">
                                        <bk-table
                                            ref="hostTable"
                                            :data="data"
                                            @selection-change="selectHost"
                                            :max-height="'calc(100vh - 450px)'"
                                            :height="'calc(100vh - 450px)'"
                                            :pagination="pagination"
                                            :row-key="getRowKeys"
                                            @page-change="handlePageChange"
                                            @page-limit-change="handleLimitChange">
                                            <bk-table-column type="selection" :reserve-selection="true" width="60" :selectable="selectable"></bk-table-column>
                                            <bk-table-column type="index" :label="$t('序列')" width="70" align="center"></bk-table-column>
                                            <bk-table-column :label="$t('主机ID')" prop="bk_host_id" align="center"></bk-table-column>
                                            <bk-table-column :label="$t('主机名称')" prop="bk_host_name" align="center"></bk-table-column>
                                            <bk-table-column :label="$t('内网IP')" prop="bk_host_innerip" align="center"></bk-table-column>
                                            <bk-table-column :label="$t('外网IP')" prop="bk_host_outerip" align="center"></bk-table-column>
                                            <bk-table-column :label="$t('云区域')" prop="bk_cloud_name" align="center"></bk-table-column>
                                            <bk-table-column :label="$t('主机类型')" prop="host_system" align="center">
                                            </bk-table-column>
                                            <bk-table-column :label="$t('操作')" align="center">
                                                <template slot-scope="props">
                                                    <bk-button class="mr10" theme="primary" text @click="applyAuth(props.row)" v-if="!props.row.is_auth">{{$t('权限申请')}}</bk-button>
                                                </template>
                                            </bk-table-column>
                                        </bk-table>

                                    </div>
            
                                </div>

                            </div>
                            <div v-if="active === 'ipInput'" style="height:calc(100vh - 350px);display:flex;width: calc(80vw - 200px);">
                                <bk-input
                                    :placeholder="ipInputPlaceholder"
                                    :type="'textarea'"
                                    v-model="value"
                                >
                                </bk-input>
                            </div>
                        </bk-tab>
                    </div>
                    <div slot="footer">
                        <span class="select-items">{{$t('已选择')}}:  <span class="strong number choose-host">{{multipleSelection.length}}</span>{{$t('台主机')}}</span>

                        <bk-button :theme="'primary'" :title="'主要按钮'" class="mr50" @click="doSeclectHosts">
                            {{$t('确认添加')}}
                        </bk-button>
                    </div>
                </bk-dialog>
            </div>
            <div class="my-form">
                <bk-form :label-width="120" :model="formData">
                    <bk-form-item :label="$t('业务')" :required="true">
                        <bk-select v-model="bkBizId" searchable @change="businessChange" :placeholder="$t('请选择业务')" :search-with-pinyin="true">
                            <bk-option v-for="option in businessList"
                                :key="option.bk_biz_id"
                                :id="option.bk_biz_id"
                                :name="option.bk_biz_name">
                                {{option.bk_biz_name}}
                                <i class="bk-icon icon-lock" v-if="!option.is_auth"></i>
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item :label="$t('目标主机')" :required="true" :property="'name'">
                        <bk-button :theme="'primarydefault'" type="submit" @click="addHosts" class="mr10">
                            {{$t('添加服务器')}}
                        </bk-button>
                        <bk-button :theme="'default'" :title="'主要按钮'" class="mr10" @click="clearHosts">
                            {{$t('清空')}}
                        </bk-button>
                        <bk-table style="margin-top: 15px;"
                            :data="selectData"
                            :max-height="'calc(100vh - 600px)'"
                            :height="'calc(100vh - 600px)'"
                        >
                            <bk-table-column type="index" :label="$t('序列')" width="70" align="center"></bk-table-column>
                            <bk-table-column :label="$t('主机IP')" prop="bk_host_innerip" align="center"></bk-table-column>
                            <bk-table-column :label="$t('云区域')" prop="bk_cloud_name" align="center"></bk-table-column>
                            <bk-table-column :label="$t('主机名称')" prop="bk_host_name" align="center"></bk-table-column>
                            <bk-table-column :label="$t('主机类型')" prop="host_system" align="center">
                            </bk-table-column>
                            <bk-table-column :label="$t('操作')" align="center" width="80">
                                <template slot-scope="props">
                                    <bk-button theme="primary" text @click="remove(props.row)">{{$t('移除')}}</bk-button>
                                </template>
                            </bk-table-column>
                        </bk-table>
                    </bk-form-item>
                    <bk-form-item :label="$t('主机类型')" :required="true">
                        <bk-radio-group v-model="osType">
                            <bk-radio :value="0">linux</bk-radio>
                            <bk-radio :value="1">windows</bk-radio>
                        </bk-radio-group>
                    </bk-form-item>
                    <bk-form-item :label="$t('目录')" :required="true">
                        <bk-input v-model="formData.file_path"></bk-input>
                    </bk-form-item>
                    <bk-form-item :label="$t('文件后缀')" :required="true">
                        <bk-input v-model="formData.file_suffix1"></bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-button style="margin-right: 3px;" theme="primary" title="提交" @click.stop.prevent="searchHostFiles" :loading="isSearch">{{$t('查询')}}</bk-button>
                        <bk-button v-if="isError" style="margin-left: 30px;" theme="warning" @click="isShowErrInfo = true" title="提交">{{$t('查看异常信息')}}</bk-button>
                    </bk-form-item>
                </bk-form>
                <div class="my-step">
                    <bk-process
                        :list="loadingList"
                        :cur-process.sync="loadingProcess"
                        :display-key="'content'"
                        :show-steps="false"
                        style="pointer-events:none"
                        :controllable="false"
                    >
                    </bk-process>
                </div>
            </div>
    
            <div class="my-search-result">
                <div style="margin-top:30px;margin-left:20px">
                    <bk-table
                        :data="resultData"
                        :max-height="'calc(100vh - 450px)'"
                        :height="'calc(100vh - 450px)'">
                        <bk-table-column type="expand" width="30">
                            <template slot-scope="props">
                                <bk-table :data="props.row.file_list.split(',')" :outer-border="false" :show-header="false" :header-cell-style="{ background: '#fff', borderRight: 'none' }">
                                    <bk-table-column align="center" :show-overflow-tooltip="true">
                                        <template slot-scope="props1">
                                            <div style="text-align:center">{{props1.row}}</div>
                                        </template>
                                    </bk-table-column>
                                </bk-table>
                            </template>
                        </bk-table-column>
                        <bk-table-column type="index" :label="$t('序列')" width="70" align="center"></bk-table-column>
                        <bk-table-column :label="$t('主机IP')" prop="ip.ip" align="center"></bk-table-column>
                        <bk-table-column :label="$t('文件目录')" prop="file_directory" align="center"></bk-table-column>
                        <bk-table-column :label="$t('文件列表')" prop="file_list" align="center"></bk-table-column>
                        <bk-table-column :label="$t('文件大小')" prop="file_size" align="center">
                            <template slot-scope="props">
                                {{byteConvert(props.row.file_size)}}
                            </template>
                        </bk-table-column>
                        <bk-table-column :label="$t('文件数量')" prop="file_count" align="center"></bk-table-column>
                        <bk-table-column :label="$t('操作')" align="center">
                            <template slot-scope="props">
                                <bk-button class="mr10" theme="primary" text @click="backupFile(props.row)" :disabled="props.row.isBackup || props.row.file_count === 0">{{$t('立即备份')}}</bk-button>
                            </template>
                        </bk-table-column>
                    </bk-table>
                </div>
           
            </div>
            <bk-sideslider :is-show.sync="isShowErrInfo" :quick-close="true" :show-mask="false" :width="500" :transfer="true">
                <div slot="header">{{ $t("错误详情") }}</div>
                <div class="p20" slot="content">
                    <div v-for="(item,index) in errInfo" :key="index">
                        <bk-alert type="error" style="margin: 10px;">
                            <div slot="title">{{$t(item.ip)}} : {{item.err_msg}}</div>
                        </bk-alert>
                    </div>
                </div>
            </bk-sideslider>
        </div>
    </div>
  
</template>
<script>
    export default {
        components: {
         
        },
        data () {
            return {
                ipInputPlaceholder: '请输入IP地址,多个IP请使用 , 或者换行分隔。\n带云区域请使用:分隔,如(0:192.168.0.1)',
                bkBizId: '',
                bkSetId: '',
                bkModuleId: '',
                businessList: '',
                multipleSelection: [],
                osType: 0,
                isBizAuth: true,
                isDataLoading: false,
                curBusiness: {},
                loadingProcess: 1,
                isSearch: false,
                interval: null,
                isError: false,
                isShowErrInfo: false,
                errInfo: [],
                loadingList: [
                    {
                        content: this.$t('表单填写'),
                        isLoading: true
                    },
                    {
                        content: this.$t('查询'),
                        isLoading: true
                    },
                    {
                        content: this.$t('结束')
                    }
                ],
                filterCondition: {},
                treeVisible: false,
                treeData: [],
                data: [],
                selectData: [],
                resultData: [],
                pagination: {
                    current: 1,
                    count: 100,
                    limit: 20
                },
                formData: { },
                panels: [
                    { name: 'ipSelect', label: this.$t('静态-IP选择'), count: 10 }
                    // { name: 'ipInput', label: '手动输入', count: 20 }
                ],
                active: 'ipSelect',
                type: ['card', 'border-card', 'unborder-card', 'vertical-card'],
                currentType: 'card'
            }
        },
        methods: {
            fetchPageData () {
                this.$http.get('/api/business/').then(res => {
                    this.businessList = res.data
                    this.isBizAuth = this.businessList[0].is_auth
                })
            },
            applyBizAuth () {
                window.open('https://bkiam.paas-edu.bktencent.com/')
            },
            byteConvert (bytes) {
                if (isNaN(bytes)) {
                    return ''
                }
                const symbols = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
                let exp = Math.floor(Math.log(bytes) / Math.log(2))
                if (exp < 1) {
                    exp = 0
                }
                const i = Math.floor(exp / 10)
                bytes = bytes / Math.pow(2, 10 * i)
 
                if (bytes.toString().length > bytes.toFixed(2).toString().length) {
                    bytes = bytes.toFixed(2)
                }
                return bytes + ' ' + symbols[i]
            },
            applyAuth (row) {
                this.$http.get(`/api/make_host_apply_url/${row.bk_biz_id.replace(',', '')}/${row.bk_set_id.split(',')[0]}/${row.bk_module_id.split(',')[0]}/${row.bk_host_id}/`).then(res => {
                    window.open(res.data)
                })
            },
            selectable (row, index) {
                return row.is_auth
            },
            handleReset () {
                this.bkSetId = null
                this.bkModuleId = null
                this.multipleSelection = this.selectData
                this.pagination.current = 1
                this.get_filter_hosts()
                this.get_sets_of_business()
            },
            doSeclectHosts () {
                this.selectData = this.multipleSelection
                this.treeVisible = false
            },
            businessChange (id) {
                this.businessList.forEach(item => {
                    if (item.bk_biz_id === id) {
                        this.curBusiness = item
                    }
                })
                this.bkSetId = null
                this.bkModuleId = null
                this.selectData = []
                this.formData = {}
                this.resultData = []
                this.loadingProcess = 1
                this.isError = false
                this.isSearch = false
                clearInterval(this.interval)
                this.get_sets_of_business()
                this.pagination.current = 1
                this.get_filter_hosts()
            },
            addHosts () {
                if (!this.bkBizId) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请先选择业务'),
                        offset: '80'
                    })
                    return
                }
                this.bkSetId = null
                this.bkModuleId = null
                this.multipleSelection = this.selectData
                this.pagination.current = 1
                this.get_filter_hosts()

                this.treeVisible = true
            },
            rowMultipleChecked () {
                this.multipleSelection.forEach(item => {
                    this.data.forEach(ele => {
                        if (ele.bk_host_id === item.bk_host_id) {
                            this.$refs.hostTable.toggleRowSelection(ele, true)
                        }
                    })
                })
            },
            clearHosts () {
                this.selectData = []
            },
            selectHost (item) {
                this.multipleSelection = this.arrayNonRepeatfy(this.multipleSelection.concat(item))
                const dataId = []
                this.data.forEach(ele => {
                    dataId.push(ele.bk_host_id)
                })
                const multipleSelectionId = []
                this.multipleSelection.forEach(ele => {
                    multipleSelectionId.push(ele.bk_host_id)
                })
                const itemId = []
                item.forEach(ele => {
                    itemId.push(ele.bk_host_id)
                })
              
                dataId.forEach(ele => {
                    const index = multipleSelectionId.indexOf(ele)
                    if (index !== -1 && itemId.indexOf(ele) === -1) {
                        this.multipleSelection[index] = ''
                    }
                })
                this.multipleSelection = this.multipleSelection.filter(ele => {
                    return ele !== ''
                })
            },
            getRowKeys (row) {
                return row.bk_host_id
            },
            remove (row) {
                const index = this.selectData.indexOf(row)
                if (index !== -1) {
                    this.selectData.splice(index, 1)
                }
            },
            backupFile (row) {
                row.isBackup = true
                const data = {
                    bk_biz_id: this.bkBizId,
                    ip_list: [row.ip],
                    file_suffix: this.formData.file_suffix1,
                    file_list: row.file_list.split(','),
                    file_directory: row.file_directory,
                    os_type: row.os_type
                }
                this.$http.post('/api/backup_host_files/', data).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            theme: 'success',
                            message: this.$t('开始备份'),
                            offset: '80'
                        })
                    } else {
                        this.$bkMessage({
                            theme: 'warning',
                            message: this.$t('该目录禁止备份'),
                            offset: '80'
                        })
                    }
                })
            },
            searchHostFiles () {
                this.formData.bk_biz_id = this.bkBizId
                this.formData.os_type = this.osType
                this.formData.ip_list = []
                this.selectData.forEach(ele => {
                    this.formData.ip_list.push({
                        ip: ele.bk_host_innerip,
                        bk_cloud_id: ele.bk_cloud_id
                    })
                })
                if (!this.bkBizId) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请先选择业务'),
                        offset: '80'
                    })
                    return
                }
                if (this.formData.ip_list.length === 0) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请至少选择一台主机'),
                        offset: '80'
                    })
                    return
                }
                if (!this.formData.file_path) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请输入文件目录'),
                        offset: '80'
                    })
                    return
                }
                if (this.formData.file_path.indexOf('\\') !== -1) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('windows和linux文件分隔符请使用/'),
                        offset: '80'
                    })
                    return
                }
                if (!this.formData.file_suffix1) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请输入文件后缀'),
                        offset: '80'
                    })
                    return
                }
                if (this.formData.file_suffix1 === '.*') {
                    this.formData.file_suffix = "''"
                } else {
                    this.formData.file_suffix = this.formData.file_suffix1
                }
                this.isSearch = true
                this.isError = false
                this.errInfo = []
                this.resultData = []
                this.$http.post('/api/search_host_files/', this.formData).then(res => {
                    this.loadingProcess = 2
                    let count = 0
                    this.interval = setInterval(() => {
                        this.$http.get(`/api/search_host_files_result/${res.data}/`).then(res => {
                            count++
                            if (count >= 100) {
                                clearInterval(this.interval)
                            }
                            if (res.result) {
                                if (res.data.fail_host_info.length !== 0) {
                                    this.isError = true
                                    this.errInfo = res.data.fail_host_info
                                }

                                res.data.file_list.forEach(ele => {
                                    ele.isBackup = false
                                    this.resultData.push(ele)
                                })
                                this.loadingProcess = 4
                                this.isSearch = false
                                clearInterval(this.interval)
                                this.$bkMessage({
                                    theme: 'primary',
                                    message: this.resultData.length + this.$t('台成功/') + this.errInfo.length + this.$t('台失败'),
                                    offset: '80'
                                })
                            }
                        })
                    }, 2000)
                })
            },
            treeDataChange (event) {
                const that = this
                if (event.level === 0) {
                    this.bkSetId = event.id
                    this.bkModuleId = null
                    this.pagination.current = 1
                    this.get_filter_hosts()
                    this.$http.get(`/api/modules_of_set/${this.bkBizId}/${event.id}/`).then(res => {
                        const data = res.data
                        const node = that.$refs.tree.getNodeById(event.id)
                        if (node.children.length === 0) {
                            that.$refs.tree.addNode(data, event.id)
                        }
                    })
                }
                if (event.level === 1) {
                    that.bkModuleId = event.data.bk_module_id
                    that.bkSetId = event.parent.id
                    this.pagination.current = 1
                    that.get_modules_of_set()
                    that.get_filter_hosts()
                }
            },
            arrayNonRepeatfy (arr) {
                const map = new Map()
                const array = [] // 数组用于返回结果
                for (let i = 0; i < arr.length; i++) {
                    if (map.has(arr[i].bk_host_id)) { // 如果有该key值
                        map.set(arr[i].bk_host_id, true)
                    } else {
                        map.set(arr[i].bk_host_id, false) // 如果没有该key值
                        array.push(arr[i])
                    }
                }
                return array
            },
            handlePageChange (page) {
                this.pagination.current = page
                this.get_filter_hosts()
            },
            handleLimitChange (limit) {
                this.pagination.limit = limit
                this.pagination.current = 1
                this.get_filter_hosts()
            },
            get_business_info () {
                this.$http.get('/api/business/').then(res => {
                    this.businessList = res.data
                })
            },
            get_sets_of_business () {
                this.$store.commit('setCurBusiness', this.curBusiness)
                this.$http.get(`/api/sets_of_business/${this.bkBizId}/`).then(res => {
                    this.treeData = res.data
                    this.setList = res.data
                })
            },
            get_modules_of_set () {
                this.$http.get(`/api/modules_of_set/${this.filterCondition.bk_biz_id}/${this.filterCondition.bk_set_id}/`).then(res => {
                    this.moduleList = res.data
                })
            },
            get_filter_hosts () {
                this.filterCondition.bk_biz_id = this.bkBizId
                this.filterCondition.bk_set_id = this.bkSetId
                this.filterCondition.bk_module_id = this.bkModuleId
                this.filterCondition.start = (this.pagination.current - 1) * this.pagination.limit
                this.filterCondition.limit = this.pagination.limit
                this.data = []
                this.isDataLoading = true
                this.$store.commit('setCurBusiness', this.curBusiness)
                this.$http.post(`/api/filter_hosts/?start=${this.filterCondition.start}&limit=${this.pagination.limit}`, this.filterCondition).then(res => {
                    if (res.code !== 403) {
                        this.pagination.count = res.count
                        this.data = res.data
                        setTimeout(this.rowMultipleChecked(), 500)
                    }
                    this.isDataLoading = false
                })
            }
        }
    }
</script>
<style lang="postcss" scoped>
.host-sea-content{
    display: flex;
    width: 100%;
}
.my-form {
    margin: 30px 0;
    width: 50%;
}
.my-search-result{
    width: 50%;
    margin: 0 auto;
    height: calc(100vh - 800px);
}
.my-step{
    width: 80%;
    margin: 30px auto;
}
.my-tree{
    height: 100%;
    width: 250px;
    flex-shrink:0;
    overflow-y: auto;
}
.select-items{
    float: left;
}
.my-host-table{
    flex:1;
    margin: 10px;
    position: relative;
    .my-host-table-content{
        position:absolute;
        width:100%;
        height: calc(100vh - 450px);
    }
}
.strong {
    font-weight: 700;
    color: #3a84ff;
}
.number {
    padding: 0 4px;
}
</style>
<style>
.bk-dialog-wrapper .bk-dialog.bk-dialog-fullscreen .bk-dialog-content {
    width: 80vw;
    border-radius: 0;
    position: absolute;
    top: 50px;
    left: 10%;
    bottom: 50px;
    margin-bottom: 0;
}
.bk-textarea-wrapper .bk-form-textarea {
    height: calc(100vh - 450px);
}
.bk-page.bk-page-small .bk-page-selection-count{
    line-height: 32px;
    display: none;
}
</style>
<style lang="postcss">
    .bk-form-radio {
        margin-right: 30px;
    }
</style>
