<template>
    <div style="height:100%">
        <bk-exception class="exception-wrap-item" type="403" v-if="!isBizAuth">
            <span>{{$t('无业务权限')}}</span>
            <div class="text-subtitle">{{$t('你没有相应业务的访问权限，请前往申请相关业务权限')}}</div>
            <div class="text-wrap">
                <span class="text-btn" @click="applyBizAuth">{{$t('去申请')}}</span>
            </div>
        </bk-exception>
        <div class="my-content" v-if="isBizAuth">
            <div style="position:absolute;">
                <bk-sideslider :is-show.sync="customSettings.isShow" :quick-close="true" :show-mask="false" :width="500" :transfer="true">
                    <div slot="header">{{ $t(customSettings.title) }}</div>
                    <div class="p20" slot="content">
                        <bk-form :label-width="140" :model="filterCondition">
                            <bk-form-item :label="$t('业务')">
                                <bk-select @toggle="businessToggle" v-model="filterCondition.bk_biz_id" searchable @change="formBusinessChange" :placeholder="$t('请选择业务')" :search-with-pinyin="true">
                                    <bk-option v-for="option in businessList"
                                        :key="option.bk_biz_id"
                                        :id="option.bk_biz_id"
                                        :name="option.bk_biz_name"
                                    >
                                        {{option.bk_biz_name}}
                                        <i class="bk-icon icon-lock" v-if="!option.is_auth"></i>
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item
                                :label="$t('集群')"
                                :error-display-type="'normal'">
                                <bk-select v-model="filterCondition.bk_set_id" searchable @toggle="setToggle" @change="formSetChange" :placeholder="$t('请选择集群')" :search-with-pinyin="true">
                                    <bk-option v-for="option in setList"
                                        :key="option.id"
                                        :id="option.id"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item
                                :label="$t('模块')"
                                :error-display-type="'normal'">
                                <bk-select v-model="filterCondition.bk_module_id" searchable @toggle="moduleToggle" @change="formModuleChange" :placeholder="$t('请选择模块')" :search-with-pinyin="true">
                                    <bk-option v-for="option in moduleList"
                                        :key="option.bk_module_id"
                                        :id="option.bk_module_id"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item :label="$t('主机ID')" :desc="customDesc">
                                <bk-input v-model="filterCondition.bk_host_id" :placeholder="$t('请输入完整的主机ID')"></bk-input>
                            </bk-form-item>
                            <bk-form-item :label="$t('主机名称')" :desc="customDesc">
                                <bk-input v-model="filterCondition.bk_host_name" :placeholder="$t('请输入主机名称的关键字')"></bk-input>
                            </bk-form-item>
                            <bk-form-item :label="$t('内网IP')" :desc="customDesc">
                                <bk-input v-model="filterCondition.bk_host_innerip" :placeholder="$t('请输入要查询主机内网IP的前缀')"></bk-input>
                            </bk-form-item>
                            <bk-form-item :label="$t('外网IP')" :desc="customDesc">
                                <bk-input v-model="filterCondition.bk_host_outerip" :placeholder="$t('请输入要查询主机外网IP的前缀')"></bk-input>
                            </bk-form-item>
                            <bk-form-item :label="$t('云区域ID')" :desc="customDesc">
                                <bk-input v-model="filterCondition.bk_cloud_id" :placeholder="$t('请输入完整的云区域ID')"></bk-input>
                            </bk-form-item>
                            <bk-form-item :label="$t('负责人')" :desc="customDesc">
                                <bk-member-selector v-model="operator" :max-data="1" :placeholder="$t('请输入负责人')"></bk-member-selector>
                            </bk-form-item>
                            <bk-form-item :label="$t('备份负责人')" :desc="customDesc">
                                <bk-member-selector v-model="bkBakOperator" :max-data="1" :placeholder="$t('请输入备份负责人')"></bk-member-selector>
                            </bk-form-item>
                        </bk-form>
                    </div>
                    <div slot="footer" style="margin: 30px auto;">
                        <bk-button theme="primary" style="margin-left:30px;" @click="selectHosts">
                            {{$t('查询')}}
                        </bk-button>
                        <bk-button theme="success" style="margin-left:20px;" @click="retData">
                            {{$t('重置')}}
                        </bk-button>
                        <bk-button theme="default" style="margin-left:20px;" @click="customSettings.isShow = false">
                            {{$t('取消')}}
                        </bk-button>
                    </div>
                </bk-sideslider>
            </div>
        
            <div class="my-tree">
                <bk-select v-model="bkBizId" searchable style="margin:10px" @change="businessChange" @toggle="businessToggle" :search-with-pinyin="true">
                    <bk-option v-for="option in businessList"
                        :key="option.bk_biz_id"
                        :id="option.bk_biz_id"
                        :name="option.bk_biz_name"
                    >
                        {{option.bk_biz_name}}
                        <i class="bk-icon icon-lock" v-if="!option.is_auth"></i>
                    </bk-option>
                </bk-select>
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
                    <div>
                        <bk-button theme="primary" @click="customSettings.isShow = true" style="margin-left:15px;margin-bottom:15px">{{$t('填写查询条件')}}</bk-button>
                        <bk-button theme="primary" @click="syncBusiness('sync_all')" :loading="syncLoading" style="margin-left:15px;margin-bottom:15px">{{$t('同步所有业务')}}</bk-button>
                        <bk-button theme="primary" @click="syncBusiness('sync_single')" :loading="syncLoading" style="margin-left:15px;margin-bottom:15px" v-if="filterCondition.bk_biz_id">{{$t('同步业务')}}:{{businessName}}</bk-button>
                    </div>
                    <bk-table
                        :data="data"
                        :max-height="'calc(100vh - 250px)'"
                        :height="'calc(100vh - 250px)'"
                        :pagination="pagination"
                        @page-change="handlePageChange"
                        @page-limit-change="handleLimitChange">
                        <bk-table-column type="index" :label="$t('序列')" width="70" align="center"></bk-table-column>
                        <bk-table-column :label="$t('主机ID')" prop="bk_host_id" align="center">
                            <template slot-scope="props">
                                <bk-button class="mr10" theme="primary" text @click="lookDetail(props.row)">{{props.row.bk_host_id}}</bk-button>
                            </template>
                        </bk-table-column>
                        <bk-table-column :label="$t('主机名称')" prop="bk_host_name" align="center"></bk-table-column>
                        <bk-table-column :label="$t('内网IP')" prop="bk_host_innerip" align="center"></bk-table-column>
                        <bk-table-column :label="$t('外网IP')" prop="bk_host_outerip" align="center"></bk-table-column>
                        <bk-table-column :label="$t('云区域')" prop="bk_cloud_id" align="center"></bk-table-column>
                        <bk-table-column :label="$t('负责人')" prop="operator" align="center"></bk-table-column>
                        <bk-table-column :label="$t('备份负责人')" prop="bk_bak_operator" align="center"></bk-table-column>
                        <!-- <bk-table-column :label="$t('操作')" align="center">
                            <template slot-scope="props">
                                <bk-button class="mr10" theme="primary" text @click="applyAuth(props.row)" v-if="!props.row.is_auth">{{$t('权限申请')}}</bk-button>
                            </template>
                        </bk-table-column> -->
                    </bk-table>
                </div>
    
            </div>
            <section>
                <bk-sideslider :is-show.sync="exampleSetting4.visible" :quick-close="true" :show-mask="false" :width="500" :transfer="true">
                    <div slot="header">{{ $t(exampleSetting4.title) }}</div>
                    <div class="p20" slot="content">
                        <div v-for="(item,index) in hostInfo" :key="item.bk_property_id">
                            <bk-alert type="success" style="margin: 10px;" v-if="item.bk_property_value !== null && item.bk_property_value !== '' && index % 2 ">
                                <div slot="title">{{$t(item.bk_property_name)}} : {{item.bk_property_value}}</div>
                            </bk-alert>
                            <bk-alert type="info" style="margin: 10px;" v-if="item.bk_property_value !== null && item.bk_property_value !== '' && !(index % 2) ">
                                <div slot="title">{{$t(item.bk_property_name)}} : {{item.bk_property_value}}</div>
                            </bk-alert>
                        </div>
                    </div>
                </bk-sideslider>
            </section>
        </div>
    </div>
</template>
<script>
    import { bkBigTree, bkTable, bkTableColumn } from 'bk-magic-vue'
    
    export default {
        components: {
            bkBigTree,
            bkTable,
            bkTableColumn
        },
        data () {
            return {
                filterCondition: {},
                exampleSetting4: {
                    fullscreen: true,
                    visible: false,
                    title: ''
                },
                isBizAuth: true,
                isDataLoading: true,
                hostInfo: [],
                syncLoading: false,
                businessList: [],
                setList: [],
                moduleList: [],
                bkBizId: null,
                bkSetId: null,
                bkModuleId: null,
                curBusiness: null,
                operator: [],
                bkBakOperator: [],
                treeData: [],
                data: [],
                pagination: {
                    current: 1,
                    count: 100,
                    limit: 20
                },
                customSettings: {
                    isShow: false,
                    title: '查询参数填写'
                }
            }
        },
        methods: {
            fetchPageData () {
                this.$http.get('/api/business/').then(res => {
                    this.businessList = res.data
                    if (this.businessList[0].is_auth) {
                        this.businessName = this.businessList[0].bk_biz_name
                        this.bkBizId = this.businessList[0].bk_biz_id
                        this.filterCondition.bk_biz_id = this.bkBizId
                        this.get_sets_of_business()
                        this.isDataLoading = true
                        this.get_filter_hosts()
                    } else {
                        this.isBizAuth = false
                    }
                })
            },
            applyBizAuth () {
                window.open('https://bkiam.paas-edu.bktencent.com/')
            },
            applyAuth (row) {
                this.$axios.get(`/make_host_apply_url/${row.bk_biz_id.replace(',', '')}/${row.bk_set_id.split(',')[0]}/${row.bk_module_id.split(',')[0]}/${row.bk_host_id}/`).then(res => {
                    window.open(res.data.data)
                })
            },
            businessToggle (flag) {
                if (!flag) {
                    return
                }
                this.get_business_info()
            },
            businessChange (id) {
                this.businessList.forEach(item => {
                    if (item.bk_biz_id === id) {
                        this.businessName = item.bk_biz_name
                        this.curBusiness = item
                    }
                })
                this.bkSetId = null
                this.bkModuleId = null
                this.filterCondition.bk_biz_id = id
                this.filterCondition.bk_set_id = null
                this.filterCondition.bk_module_id = null
                this.treeData = []
                this.setList = []
                this.data = []

                if (id !== '') {
                    this.get_sets_of_business()
                    this.get_filter_hosts()
                }
            },
            formBusinessChange (id) {
                this.bkBizId = id
                this.businessList.forEach(item => {
                    if (item.bk_biz_id === id) {
                        this.businessName = item.bk_biz_name
                    }
                })
                this.filterCondition.bk_set_id = null
                this.filterCondition.bk_module_id = null
            },
            formSetChange (id) {
                this.filterCondition.bk_module_id = null
                this.filterCondition.bk_set_id = id
                this.bkSetId = id
                const that = this
                if (id) {
                    this.get_filter_hosts()
                    this.get_modules_of_set()
                    this.$http.get(`/api/modules_of_set/${this.bkBizId}/${id}/`).then(res => {
                        const data = res.data
                        const node = that.$refs.tree.getNodeById(id)
                        if (node.children.length === 0) {
                            that.$refs.tree.addNode(data, id)
                        }
                    })
                    this.$refs.tree.setSelected(id)
                }
            },
            formModuleChange (id) {
                if (id) {
                    this.bkModuleId = id
                    this.$refs.tree.setSelected(`module${id}`)
                    this.get_filter_hosts()
                }
            },
            setToggle (flag) {
                if (!flag) {
                    return
                }
                if (!this.filterCondition.bk_biz_id) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请先选择业务'),
                        offset: '80'
                    })
                }
            },
            moduleToggle (flag) {
                if (!flag) {
                    return
                }
                if (!this.filterCondition.bk_set_id) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请先选择集群'),
                        offset: '80'
                    })
                }
            },
            retData () {
                this.filterCondition = {}
                this.operator = []
                this.bkBakOperator = []
            },
            selectHosts () {
                this.get_filter_hosts()
            },
            syncBusiness (value) {
                if (value === 'sync_single' && this.businessName === '') {
                    this.$bkMessage({
                        theme: 'error',
                        message: this.$t('请选择要同步的业务'),
                        offset: '80'
                    })
                    return
                }
                this.syncLoading = true
                const command = {
                    value: value,
                    bk_biz_id: this.filterCondition.bk_biz_id,
                    business: {
                        'bk_biz_id': this.filterCondition.bk_biz_id,
                        'bk_biz_name': this.businessName
                    }
                }
                if (value === 'sync_single') {
                    this.$store.commit('setCurBusiness', this.curBusiness)
                }
                if (value === 'sync_all') {
                    this.$store.commit('setCurBusiness', {})
                }
                this.$http.post('/api/sync_host_data/', command).then(res => {
                    this.syncLoading = false
                    if (res.data.code !== 403) {
                        if (res.data.result === true) {
                            this.$bkMessage({
                                theme: 'success',
                                message: this.$t('开始同步CMDB业务信息'),
                                offset: '80'
                            })
                        } else {
                            this.$bkMessage({
                                theme: 'warning',
                                message: this.$t('CMDB业务信息正在同步,可通过切换API获取最新数据'),
                                offset: '80'
                            })
                        }
                    }
                })
            },
            treeDataChange (event) {
                const that = this
                if (event.level === 0) {
                    this.bkSetId = event.id
                    this.bkModuleId = null
                    this.get_filter_hosts()
                    this.filterCondition.bk_set_id = this.bkSetId
                    this.filterCondition.bk_module_id = null
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
                    that.filterCondition.bk_set_id = that.bkSetId
                    that.filterCondition.bk_module_id = that.bkModuleId
                    that.get_modules_of_set()
                    that.get_filter_hosts()
                }
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
            lookDetail (row) {
                this.exampleSetting4.title = this.$t('主机详情[') + row.bk_host_id + ']'
                this.$http.get(`/api/host_base_info/${row.bk_host_id}/`).then(res => {
                    if (res.code !== 403) {
                        this.hostInfo = res.data.data
                        this.exampleSetting4.visible = true
                    }
                })
            },
            retFilterCondition () {
                this.filterCondition.bk_host_name = null
                this.filterCondition.bk_host_id = null
                this.filterCondition.bk_host_innerip = null
                this.filterCondition.bk_host_outerip = null
                this.filterCondition.operator = null
                this.filterCondition.bk_bak_operator = null
                this.filterCondition.bk_cloud_id = null
            },
            get_business_info () {
                this.$http.get('/api/business/').then(res => {
                    this.businessList = res.data
                })
            },
            get_sets_of_business () {
                this.$store.commit('setCurBusiness', this.curBusiness)
                this.$http.get(`/api/sets_of_business/${this.bkBizId}/`).then(res => {
                    this.treeData = []
                    this.setList = []
                    if (res.data.code !== 403) {
                        this.treeData = res.data
                        this.setList = res.data
                    }
                })
            },
            get_modules_of_set () {
                this.$http.get(`/api/modules_of_set/${this.filterCondition.bk_biz_id}/${this.filterCondition.bk_set_id}/`).then(res => {
                    this.moduleList = res.data
                })
            },
            get_filter_hosts () {
                const bkHostId = this.filterCondition.bk_host_id
                const bkCloudId = this.filterCondition.bk_cloud_id
                if (!this.filterCondition.bk_biz_id) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('请选择业务'),
                        offset: '80'
                    })
                    return
                }
                if (isNaN(Number(bkHostId)) && this.filterCondition.bk_host_id) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('主机ID请输入整形数据'),
                        offset: '80'
                    })
                    return
                }
                if (isNaN(Number(bkCloudId)) && this.filterCondition.bk_cloud_id) {
                    this.$bkMessage({
                        theme: 'warning',
                        message: this.$t('云区域ID请输入整形数据'),
                        offset: '80'
                    })
                    return
                }
                this.filterCondition.start = (this.pagination.current - 1) * this.pagination.limit
                this.filterCondition.limit = this.pagination.limit
                this.filterCondition.operator = this.operator.join('')
                this.filterCondition.bk_bak_operator = this.bkBakOperator.join('')
                this.data = []
                this.isDataLoading = true
                this.$store.commit('setCurBusiness', this.curBusiness)
                this.$http.post(`/api/filter_hosts/?start=${this.filterCondition.start}&limit=${this.pagination.limit}`, this.filterCondition).then(res => {
                    if (res.code !== 403) {
                        this.pagination.count = res.data.count
                        this.data = res.data
                        if (this.data.length === 0) {
                            this.$bkMessage({
                                theme: 'warning',
                                message: this.$t('查询结果为空'),
                                offset: '80'
                            })
                        }
                    }
                    this.isDataLoading = false
                })
            }
          
        }
    }
</script>
<style lang="postcss" scoped>
.my-content{
    height: 100%;
    width: 100%;
    display: flex;
}
.my-tree{
    height: 100%;
    width: 250px;
    flex-shrink:0;
    overflow-y: auto;
}
.my-host-table{
    flex:1;
    margin: 10px;
    position: relative;
    .my-host-table-content{
        position:absolute;
        width:100%;
        height: calc(100vh - 260px);
    }
}
</style>
<style lang="postcss">
.exception-wrap-item {
    border: 1px solid #DCDEE5;
    margin: 10px;
    height: calc(100% - 20px);
    width: calc(100% - 20px);
    padding-top: 22px;
}
.exception-wrap-item .text-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3A84FF;
    font-size: 14px;
    margin-top: 12px;
}
.exception-wrap-item .text-subtitle {
    color: #979BA5;
    font-size: 14px;
    text-align: center;
    margin-top: 14px;
}
.text-wrap .text-btn {
    margin: 0 5px;
}
.text-wrap .text-btn:hover {
    cursor: pointer;
}
</style>
