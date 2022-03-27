<template>
    <div class="my-content">
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
                                    :name="option.bk_biz_name">
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
                    :name="option.bk_biz_name">
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
        <div class="my-host-table">
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
                        <!-- <template slot-scope="props">
                            <bk-button class="mr10" theme="primary" text @click="lookDetail(props.row)">{{props.row.bk_host_id}}</bk-button>
                        </template> -->
                    </bk-table-column>
                    <bk-table-column :label="$t('主机名称')" prop="bk_host_name" align="center"></bk-table-column>
                    <bk-table-column :label="$t('内网IP')" prop="bk_host_innerip" align="center"></bk-table-column>
                    <bk-table-column :label="$t('外网IP')" prop="bk_host_outerip" align="center"></bk-table-column>
                    <bk-table-column :label="$t('云区域')" prop="bk_cloud_id" align="center"></bk-table-column>
                    <bk-table-column :label="$t('负责人')" prop="operator" align="center"></bk-table-column>
                    <bk-table-column :label="$t('备份负责人')" prop="bk_bak_operator" align="center"></bk-table-column>
                </bk-table>
            </div>
            
        </div>
        <section>
            <bk-sideslider :is-show.sync="exampleSetting4.visible" :quick-close="true" :show-mask="false" :width="500" :transfer="true">
                <div slot="header">{{ exampleSetting4.title }}</div>
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
                hostInfo: [],
                syncLoading: false,
                businessList: [],
                setList: [],
                moduleList: [],
                bkBizId: 1,
                bkSetId: null,
                bkModuleId: null,
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
                this.filterCondition.bk_biz_id = this.bkBizId
                this.businessName = '测试业务'
                this.get_business_info()
                this.get_sets_of_business()
                this.get_filter_hosts()
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
                    }
                })
                this.bkSetId = null
                this.bkModuleId = null
                this.filterCondition.bk_biz_id = id
                this.filterCondition.bk_set_id = null
                this.filterCondition.bk_module_id = null
                this.get_sets_of_business()
                this.get_filter_hosts()
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
                    business: {
                        'bk_biz_id': this.filterCondition.bk_biz_id,
                        'bk_biz_name': this.businessName
                    }
                }
                this.$http.post('/api/sync_host_data/', command).then(res => {
                    this.syncLoading = false
                    if (res.result === true) {
                        this.$bkMessage({
                            theme: 'success',
                            message: this.$t('开始同步CMDB业务信息'),
                            offset: '80'
                        })
                    } else {
                        this.$bkMessage({
                            theme: 'warning',
                            message: this.$t('CMDB业务信息正在同步'),
                            offset: '80'
                        })
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
                    this.hostInfo = res.data
                    this.exampleSetting4.visible = true
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
                const bkHostId = this.filterCondition.bk_host_id
                const bkCloudId = this.filterCondition.bk_cloud_id
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
                this.$http.post(`/api/filter_hosts/?start=${this.filterCondition.start}&limit=${this.pagination.limit}`, this.filterCondition).then(res => {
                    this.pagination.count = res.count
                    this.data = res.data
                    if (this.data.length === 0) {
                        this.$bkMessage({
                            theme: 'warning',
                            message: this.$t('查询结果为空'),
                            offset: '80'
                        })
                    }
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
