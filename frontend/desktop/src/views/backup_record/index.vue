<template>
    <div>
        <div style="height:50px">
            
        </div>
        <div class="mr30 ml30">
            <bk-table
                :data="data"
                :max-height="'calc(100vh - 250px)'"
                :height="'calc(100vh - 250px)'"
                :pagination="pagination"
                @page-change="handlePageChange"
                @page-limit-change="handleLimitChange"
            >
                <bk-table-column type="index" :label="$t('序列')" width="70" align="center"></bk-table-column>
                <bk-table-column :label="$t('主机IP')" prop="bk_host_innerip" align="center">
                </bk-table-column>
                <bk-table-column :label="$t('文件目录')" prop="backup_directory" align="center" :show-overflow-tooltip="true"></bk-table-column>
                <bk-table-column :label="$t('文件名后缀')" prop="file_suffix" align="center"></bk-table-column>
                <bk-table-column :label="$t('备份文件名')" prop="backup_file_name" align="center" :show-overflow-tooltip="true">
                    <template slot-scope="props">
                        <span v-if="props.row.backup_file_name.indexOf('/data/wheel_test') !== -1">{{props.row.backup_file_name}}</span>
                    </template>
                </bk-table-column>
                <bk-table-column :label="$t('状态')" prop="backup_file_name" align="center">
                    <template slot-scope="props">
                        <bk-tag theme="success" type="filled" v-if="props.row.backup_file_name.indexOf('/data/wheel_test') !== -1">{{$t('执行成功')}}</bk-tag>
                        <bk-tag theme="danger" type="filled" v-else>{{$t('执行失败')}}</bk-tag>
                    </template>
                </bk-table-column>
                <bk-table-column :label="$t('备份时间')" prop="backup_time" align="center">
                    <template slot-scope="props">
                        {{formatDate(props.row.backup_time)}}
                    </template>
                </bk-table-column>
                <bk-table-column :label="$t('备份人')" prop="backup_operator" align="center"></bk-table-column>
                <bk-table-column :label="$t('操作')" align="center">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" text @click="goDetail(props.row)">{{$t('作业详情')}}</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>
        
    </div>
</template>

<script>

    export default {
        
        data () {
            return {
                data: [],
                pagination: {
                    current: 1,
                    count: 100,
                    limit: 10
                }
            }
        },
        methods: {
            fetchPageData () {
                this.get_backup_records()
            },
            handlePageChange (page) {
                this.pagination.current = page
                this.get_backup_records()
            },
            rowstyle ({ row, rowIndex }) {
                const stylejson = {}
                if (row.backup_file_name.indexOf('wheelwang') === -1) {
                    stylejson.background = '#e0838f'// 背景颜色
                    // 也可以修改文字颜色
                    stylejson.color = 'green'
                    return stylejson
                } else {
                    return ''
                }
            },
            formatDate (time) {
                const date = new Date(time)

                const year = date.getFullYear()
                const month = date.getMonth() + 1; const // 月份是从0开始的
                    day = date.getDate()
                const hour = date.getHours()
                const min = date.getMinutes()
                const sec = date.getSeconds()
                const newTime = year + '-'
                    + (month < 10 ? '0' + month : month) + '-'
                    + (day < 10 ? '0' + day : day) + ' '
                    + (hour < 10 ? '0' + hour : hour) + ':'
                    + (min < 10 ? '0' + min : min) + ':'
                    + (sec < 10 ? '0' + sec : sec)

                return newTime
            },

            handleLimitChange (limit) {
                this.pagination.limit = limit
                this.pagination.current = 1
                this.get_backup_records()
            },
            goDetail (row) {
                window.open(`https://job.paas-edu.bktencent.com/${row.bk_biz_id}/execute/task/${row.job_instance_id}?from=historyList`)
            },
            get_backup_records () {
                const start = (this.pagination.current - 1) * this.pagination.limit
                this.$http.get(`/api/backup_records/?start=${start}&limit=${this.pagination.limit}`).then(res => {
                    this.data = res.data
                    this.pagination.count = res.data
                })
            }
        }
    }
</script>
<style lang="postcss" scoped>
.my-content{
    height: 100%;
    width: 100%;
}

</style>
