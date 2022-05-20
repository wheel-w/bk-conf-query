<template>
    <div class="monitor-navigation">
        <bk-navigation
            :header-title="nav.navId"
            :side-title="nav.title"
            :default-open="true"
            :hover-width="260"
            :head-height="64"
            :navigation-type="curNav.nav"
            :need-menu="curNav.needMenu"
            @toggle="handleToggle">
            <template slot="side-header">
                <div class="side-header-content">
                    <img style="vertical-align: middle;width:49px" src="data:image/svg+xml;base64,PHN2ZyBpZD0i5Zu+5bGCXzEiIGRhdGEtbmFtZT0i5Zu+5bGCIDEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHZpZXdCb3g9IjAgMCAxOSAxNyI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJsaW5lYXItZ3JhZGllbnQiIHgxPSI2LjEzIiB5MT0iMy43IiB4Mj0iNy4wMiIgeTI9IjIuMTYiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiMwMGE2ZmQiLz48c3RvcCBvZmZzZXQ9IjAuNDQiIHN0b3AtY29sb3I9IiMyYTg3ZjAiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMwMGM3ZGIiLz48L2xpbmVhckdyYWRpZW50PjxsaW5lYXJHcmFkaWVudCBpZD0ibGluZWFyLWdyYWRpZW50LTIiIHgxPSI2LjgyIiB5MT0iMTQuODgiIHgyPSIxMy40NSIgeTI9IjMuNCIgeGxpbms6aHJlZj0iI2xpbmVhci1ncmFkaWVudCIvPjwvZGVmcz48dGl0bGU+bG9nb+WbvuaghzwvdGl0bGU+PHBhdGggZD0iTTUuNjEsMy44NGExLjMyLDEuMzIsMCwwLDEsMS4yNC40N3MwLS4xNywwLS4xNmExLjUyLDEuNTIsMCwwLDEsLjY4LTEuMDdjLjEtLjA3LjA2LS40NS4wNi0uNTRTNy41OCwyLDcuNTcsMmExLjg3LDEuODcsMCwwLDAtLjc2LDEuMzljMC0uMDUsMC0uMSwwLS4xNWExLjMsMS4zLDAsMCwwLTEuMjQtLjQ4Yy0uMTUsMCwwLDEuMDgsMCwxLjA4WiIgc3R5bGU9ImZpbGw6dXJsKCNsaW5lYXItZ3JhZGllbnQpIi8+PHBhdGggZD0iTTE1LjczLDEzSDUuMzNBMi4zOSwyLjM5LDAsMCwxLDMuNTQsMTJjLS44OC0xLjEzLS40Ny0yLjc2LDAtNCwuNjgtMS45LDEuOTMtMy4zMyw0LTMuMTVBNC4yMSw0LjIxLDAsMCwxLDExLDguOTFjLjA1LDIuMSwxLjU2LDQsMy43MiwzLjQ0YTQsNCwwLDAsMCwyLjQyLTIuODdBMy44MSwzLjgxLDAsMCwwLDE2LDYuMTFhMy45MSwzLjkxLDAsMCwwLTEuNjEtMWMtLjMzLS4xLS4yNC0uMTUtLjI3LS40OWEzLjM0LDMuMzQsMCwwLDAtLjI4LTEsMi43MywyLjczLDAsMCwwLTMuMjgtMS4zNEE0LjYyLDQuNjIsMCwwLDAsOC42NiwzLjg3Yy0uNDQuNDkuMzMtLjE4LjQ1LS4zMSwxLjExLTEuMjUsMy0uNDYsMy44Ni42MmEyLjgzLDIuODMsMCwwLDEsLjQ2LDEuNDdjMCwuMzEsMS4wOC42MiwxLjQyLjg1YTMuOTEsMy45MSwwLDAsMSwxLjYzLDMuMDgsMi42NCwyLjY0LDAsMCwxLS41NywxLjg2Yy0uMy4zMS0xLjI0LjI5LTEuNi4yNy0yLS4xNC0yLjM4LTIuNTYtMi42LTQuMThhNC4wOCw0LjA4LDAsMCwwLTQtMy40OGMtMy4yNCwwLTUuNzIsNC42Mi01LjQsNy41M0EyLjU2LDIuNTYsMCwwLDAsNSwxMy44SDE1Yy4yOSwwLC41Ny0uNzcuNzQtLjc3WiIgc3R5bGU9ImZpbGw6dXJsKCNsaW5lYXItZ3JhZGllbnQtMikiLz48L3N2Zz4=">
                    <strong style="white-space:nowrap;font: 18px sans-serif;;vertical-align: middle; line-height: 31px;padding-left: 5px;color:rgb(19,145,236);">
                        {{$t('服务器文件备份系统')}}</strong>
                        
                </div>
            </template>
            <template slot="header">
                <div class="monitor-navigation-header">
                    <ol class="header-nav" v-if="curNav.nav === 'top-bottom'">
                        <bk-popover v-for="(item,index) in header.list" :key="item.id" theme="light navigation-message" :arrow="false" offset="0, -5" placement="bottom" :tippy-options="{ 'hideOnClick': false, flipBehavior: ['bottom'] }">
                            <li v-show="item.show" class="header-nav-item" :class="{ 'item-active': index === header.active }">
                                {{item.name}}
                            </li>
                            <template slot="content">
                                <ul class="monitor-navigation-nav">
                                    <li class="nav-item" v-for="headerNavItem in curHeaderNav.navList" :key="headerNavItem.id">
                                        {{headerNavItem.name}}
                                    </li>
                                </ul>
                            </template>
                        </bk-popover>
                    </ol>
                    <div v-else class="header-title">
                        <span class="header-title-icon">
                            <svg class="icon" style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4756"><path d="M416 480h320v64H416l96 96-48 48-176-176 176-176 48 48-96 96z" p-id="4757"></path></svg>
                        </span>
                        {{nav.navId}}
                    </div>
                    <bk-select class="header-select" :class="{ 'is-left': curNav.nav === 'left-right' }" v-model="header.bizId" :clearable="false" searchable>
                        <bk-option v-for="option in header.selectList"
                            :key="option.id"
                            :id="option.id"
                            :name="option.name">
                        </bk-option>
                    </bk-select>
                    <div class="my-language">
                        <bk-dropdown-menu @show="dropdownShow" @hide="dropdownHide" ref="dropdown" font-size="large">
                            <div class="dropdown-trigger-btn" style="padding-left: 19px;" slot="dropdown-trigger">
                                <span>{{$t('语言')}}: {{$t(language)}}</span>
                                <i :class="['bk-icon icon-angle-down',{ 'icon-flip': isDropdownShow }]"></i>
                            </div>
                            <ul class="bk-dropdown-list" slot="dropdown-content">
                                <li><a @click="changeLanguage('Chinese')" :key="ch" class="bk-dropdown-list-li"> {{$t('中文')}}</a></li>
                                <li><a @click="changeLanguage('English')" :key="en" class="bk-dropdown-list-li">{{$t('英文')}}</a></li>
                            </ul>
                        </bk-dropdown-menu>
                    </div>
                    
                    <bk-popover theme="light navigation-message" :arrow="false" offset="-20, 10" placement="bottom-start" :tippy-options="{ 'hideOnClick': false }">
                        <div class="header-user" :class="{ 'is-left': curNav.nav === 'left-right' }">
                            {{user.username}}
                        </div>
                    </bk-popover>
                </div>
            </template>
            <template slot="menu">
                <bk-navigation-menu
                    ref="menu"
                    @select="handleNavSelect"
                    :default-active="nav.navId"
                    :unique-opened="open"
                    :before-nav-change="beforeNavChange"
                    :toggle-active="nav.toggle">
                    <bk-navigation-menu-group
                        v-for="item in nav.list2"
                        :key="item.name"
                        :group-name="$t(item.name)">
                        <bk-navigation-menu-item
                            :key="child.name"
                            v-for="child in item.children"
                            :id="child.name"
                            :disabled="child.disabled"
                            :icon="child.icon"
                            :href="child.href"
                            :has-child="child.children && !!child.children.length"
                            :default-active="child.active">
                            <span>{{$t(child.name)}}</span>
                            <div slot="child">
                                <bk-navigation-menu-item
                                    :key="set.name"
                                    v-for="set in child.children"
                                    :id="set.name"
                                    :disabled="set.disabled"
                                    :href="set.href"
                                    :default-active="set.active">
                                    <span>{{$t(set.name)}}</span>
                                </bk-navigation-menu-item>
                            </div>
                        </bk-navigation-menu-item>
                    </bk-navigation-menu-group>
                </bk-navigation-menu>
            </template>
            <div class="monitor-navigation-content">
                <router-view :key="$route.path"></router-view>
            </div>
            <template slot="footer">
                <div class="monitor-navigation-footer">
                    Copyright © 2012-{{new Date().getFullYear()}} Tencent BlueKing. All Rights Reserved. 腾讯蓝鲸 版权所有
                </div>
            </template>
        </bk-navigation>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex'
    import { bkNavigation, bkNavigationMenu, bkNavigationMenuItem, bkNavigationMenuGroup, bkSelect, bkOption, bkPopover, lang, locale } from 'bk-magic-vue'
    export default {
        name: 'monitor-navigation',
        components: {
            bkNavigation,
            bkNavigationMenu,
            bkNavigationMenuItem,
            bkNavigationMenuGroup,
            bkSelect,
            bkOption,
            bkPopover
        },
        data () {
            return {
                position: 'middle',
                showNav: true,
                navActive: 1,
                isDropdownShow: false,
                isLargeDropdownShow: false,
                language: '中文',
                navMap: [
                    {
                        nav: 'left-right',
                        needMenu: true,
                        name: '左右结构导航'
                    },
                    {
                        nav: 'top-bottom',
                        needMenu: true,
                        name: '上下结构导航'
                    },
                    {
                        nav: 'top-bottom',
                        needMenu: false,
                        name: '上下结构无侧栏导航'
                    }
                ],
                nav: {
                    list2: [
                        {
                            name: '配置平台',
                            children: [
                                {
                                    name: '业务拓扑',
                                    href: 'businessTopology',
                                    icon: 'icon-sitemap'
                                }
                            ]
                        },
                        {
                            name: '作业平台',
                            children: [
                                {
                                    name: '服务器文件查询',
                                    href: 'hostSearch',
                                    active: true,
                                    icon: 'icon-tree-application-shape'
                                },
                                {
                                    name: '备份记录查看',
                                    title: true,
                                    href: 'backup_record',
                                    icon: 'icon-tree-application-shape'
                                }
                            ]
                        }
                    ],
                    navId: '集群',
                    toggle: false,
                    submenuActive: false,
                    title: '配置查询系统'
                },
                header: {
                    list: [
                        {
                            name: '作业平台',
                            id: 1,
                            show: false
                        },
                        {
                            name: '配置平台',
                            id: 2,
                            show: false
                        },
                        {
                            name: '监控平台',
                            id: 3,
                            show: false,
                            navList: [
                                {
                                    name: '插件管理',
                                    id: 1
                                },
                                {
                                    name: '采集配置',
                                    id: 2
                                },
                                {
                                    name: '策略配置',
                                    id: 3
                                },
                                {
                                    name: '事件中心',
                                    id: 4
                                }
                            ],
                            navActive: 2
                        },
                        {
                            name: '蓝盾平台',
                            id: 4,
                            show: false
                        }
                    ],
                    selectList: [
                        {
                            name: '英雄联盟',
                            id: 1
                        },
                        {
                            name: '和平精英',
                            id: 2
                        },
                        {
                            name: '王者荣耀',
                            id: 3
                        }
                    ],
                    active: 2,
                    bizId: 1
                },
                message: {
                    list: [
                      
                    ]
                },
                userSelect: {
                    list: [
                        '项目管理',
                        '权限中心',
                        '退出'
                    ]
                }
            }
        },
        computed: {
            ...mapGetters(['user']),
            curNav () {
                return this.navMap[this.navActive]
            },
            curHeaderNav () {
                return this.header.list[this.header.active] || {}
            }
        },
        created () {
            // 国际化配置
            const currentLanguage = localStorage.getItem('curLang') || 'zhCN'
            locale.use(lang[currentLanguage])
            if (currentLanguage === 'zhCN') {
                this.language = '中文'
            }
            if (currentLanguage === 'enUS') {
                this.language = '英文'
            }
            this.$i18n.locale = currentLanguage
        },
        methods: {
            changeLanguage (language) {
                if (language === 'Chinese') {
                    this.language = '中文'
                    localStorage.setItem('curLang', 'zhCN')
                }
                if (language === 'English') {
                    this.language = '英文'
                    localStorage.setItem('curLang', 'enUS')
                }
                this.$nextTick(() => {
                    window.location.reload()
                })
                this.$refs.dropdown.hide()
            },
            dropdownShow () {
                this.isDropdownShow = true
            },
            dropdownHide () {
                this.isDropdownShow = false
            },
            triggerHandler () {
                this.$refs.dropdown.hide()
            },
            handleNavSelect (id, item) {
                this.nav.navId = id
                const finishPage = 'businessTopology hostSearch backup_record'
                if (finishPage.indexOf(item.href) === -1) {
                    this.$bkMessage({
                        message: this.$t('敬请期待'),
                        theme: 'success'
                    })
                    return
                }
                this.$router.push({
                    name: item.href
                })
            },
            handleToggle (v) {
                this.nav.toggle = v
            },
            beforeNavChange (newId, oldId) {
                console.info(newId, oldId)
                return true
            },
            handleChangeNav () {
                this.navActive = (this.navActive + 1) % 3
            }
        }
    }
</script>

<style>
.my-info .bk-icon {
    font-size: 200px;
}
/* 以下样式是为了适应例子父级的宽高而设置 */
/* .bk-navigation {
    width:calc(100vw - 530px) !important;
    height:calc(100vh - 140px) !important;
    outline:1px solid #ebebeb;
}
.bk-navigation .bk-navigation-wrapper {
    height:calc(100vh - 252px)!important;
} */
/* 以上样式是为了适应例子父级的宽高而设置 */
.side-header-content{
    position:absolute;
}
.my-api-option{
    position:absolute;
    right: 380px;
    margin:0 20px ;
}
.my-api-option .dropdown-trigger-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 32px;
    min-width: 68px;
    /* border-radius: 2px; */
    font-size:16px ;
    padding: 0 15px;
    color: #e5e7ee;

}
.my-api-option .dropdown-trigger-btn.bk-icon {
    font-size: 18px;
}
.my-api-option .dropdown-trigger-btn .bk-icon {
    font-size: 22px;
}
.my-api-option .dropdown-trigger-btn:hover {
    cursor: pointer;
    border-color: #979ba5;
}
.my-language{
    position:absolute;
    right: 80px;
    margin:0 20px ;
}
.my-language .dropdown-trigger-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 32px;
    min-width: 68px;
    /* border-radius: 2px; */
    font-size:16px ;
    padding: 0 15px;
    color: #e5e7ee;

}
.my-language .dropdown-trigger-btn.bk-icon {
    font-size: 18px;
}
.my-language .dropdown-trigger-btn .bk-icon {
    font-size: 22px;
}
.my-language .dropdown-trigger-btn:hover {
    cursor: pointer;
    border-color: #979ba5;
}
.bk-dropdown-menu .bk-dropdown-list>li>a{
  cursor: pointer;
}

.monitor-navigation-header {
    -webkit-box-flex:1;
    -ms-flex:1;
    flex:1;
    height:100%;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    font-size:14px;
}
.monitor-navigation-header .header-nav {
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    padding:0;
    margin:0;
}
.monitor-navigation-header .header-nav-item {
    list-style:none;
    height:50px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    margin-right:40px;
    color:#96A2B9;
    min-width:56px
}
.monitor-navigation-header .header-nav-item.item-active {
    color:#FFFFFF !important;
}
.monitor-navigation-header .header-nav-item:hover {
    cursor:pointer;
    color:#D3D9E4;
}
.monitor-navigation-header .header-title {
    color:#63656E;
    font-size:16px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    margin-left:-6px;
}
.monitor-navigation-header .header-title-icon {
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    width:28px;
    height:28px;
    font-size:28px;
    color:#3A84FF;
    cursor:pointer;
}
.monitor-navigation-header .header-select {
    width:240px;
    margin-left:auto;
    margin-right:34px;
    border:none;
    background:#252F43;
    color:#D3D9E4;
    -webkit-box-shadow:none;
    box-shadow:none;
    visibility:hidden
}
.monitor-navigation-header .header-select.is-left {
    background:#F0F1F5;
    color:#63656E;
}
.monitor-navigation-header .header-mind {
    color:#768197;
    font-size:16px;
    position:relative;
    height:32px;
    width:32px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    -webkit-box-pack:center;
    -ms-flex-pack:center;
    justify-content:center;
    margin-right:8px
}
.monitor-navigation-header .header-mind.is-left {
    color:#63656E;
}
.monitor-navigation-header .header-mind.is-left:hover {
    color:#3A84FF;
    background:#F0F1F5
}
.monitor-navigation-header .header-mind-mark {
    position:absolute;
    right:8px;
    top:8px;
    height:7px;
    width:7px;
    border:1px solid #27334C;
    background-color:#EA3636;
    border-radius:100%
}
.monitor-navigation-header .header-mind-mark.is-left {
    border-color:#F0F1F5;
}
.monitor-navigation-header .header-mind:hover {
    background:-webkit-gradient(linear,right top, left top,from(rgba(37,48,71,1)),to(rgba(38,50,71,1)));
    background:linear-gradient(270deg,rgba(37,48,71,1) 0%,rgba(38,50,71,1) 100%);
    border-radius:100%;
    cursor:pointer;
    color:#D3D9E4;
}
.monitor-navigation-header .header-help {
    color:#768197;
    font-size:16px;
    position:relative;
    height:32px;
    width:32px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    -webkit-box-pack:center;
    -ms-flex-pack:center;
    justify-content:center;
    margin-right:8px
}
.monitor-navigation-header .header-help.is-left {
    color:#63656E;
}
.monitor-navigation-header .header-help.is-left:hover {
    color:#3A84FF;
    background:#F0F1F5
}
.monitor-navigation-header .header-help:hover {
    background:-webkit-gradient(linear,right top, left top,from(rgba(37,48,71,1)),to(rgba(38,50,71,1)));
    background:linear-gradient(270deg,rgba(37,48,71,1) 0%,rgba(38,50,71,1) 100%);
    border-radius:100%;
    cursor:pointer;
    color:#D3D9E4;
}
.monitor-navigation-header .header-user {
    height:100%;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    -webkit-box-pack:center;
    -ms-flex-pack:center;
    justify-content:center;
    color:#96A2B9;
    margin-left:8px;
}
.monitor-navigation-header .header-user .bk-icon {
    margin-left:5px;
    font-size:12px;
}
.monitor-navigation-header .header-user.is-left {
    color:#63656E;
}
.monitor-navigation-header .header-user.is-left:hover {
    color:#3A84FF
}
.monitor-navigation-header .header-user:hover {
    cursor:pointer;
    color:#D3D9E4;
}
.monitor-navigation-content {
    height:calc(100% - 84px);
    background:#FFFFFF;
    -webkit-box-shadow:0px 2px 4px 0px rgba(25,25,41,0.05);
    box-shadow:0px 2px 4px 0px rgba(25,25,41,0.05);
    border-radius:2px;
    border:1px solid rgba(220,222,229,1);
}
.monitor-navigation-footer {
    height:52px;
    width:100%;
    margin:32px 0 0;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    -webkit-box-pack:center;
    -ms-flex-pack:center;
    justify-content:center;
    border-top:1px solid #DCDEE5;
    color:#63656E;
    font-size:12px;
}
.monitor-navigation-message {
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-orient:vertical;
    -webkit-box-direction:normal;
    -ms-flex-direction:column;
    flex-direction:column;
    width:360px;
    background-color:#FFFFFF;
    border:1px solid #E2E2E2;
    border-radius:2px;
    -webkit-box-shadow:0px 3px 4px 0px rgba(64,112,203,0.06);
    box-shadow:0px 3px 4px 0px rgba(64,112,203,0.06);
    color:#979BA5;
    font-size:12px;
}
.monitor-navigation-message .message-title {
    -webkit-box-flex:0;
    -ms-flex:0 0 48px;
    flex:0 0 48px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    color:#313238;
    font-size:14px;
    padding:0 20px;
    margin:0;
    border-bottom:1px solid #F0F1F5;
}
.monitor-navigation-message .message-list {
    -webkit-box-flex:1;
    -ms-flex:1;
    flex:1;
    max-height:450px;
    overflow:auto;
    margin:0;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-orient:vertical;
    -webkit-box-direction:normal;
    -ms-flex-direction:column;
    flex-direction:column;
    padding:0;
}
.monitor-navigation-message .message-list-item {
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    width:100%;
    padding:0 20px;
}
.monitor-navigation-message .message-list-item .item-message {
    padding:13px 0;
    line-height:16px;
    min-height:42px;
    -webkit-box-flex:1;
    -ms-flex:1;
    flex:1;
    -ms-flex-wrap:wrap;
    flex-wrap:wrap;
    color:#63656E;
}
.monitor-navigation-message .message-list-item .item-date {
    padding:13px 0;
    margin-left:16px;
    color:#979BA5;
}
.monitor-navigation-message .message-list-item:hover {
    cursor:pointer;
    background:#F0F1F5;
}
.monitor-navigation-message .message-footer {
    -webkit-box-flex:0;
    -ms-flex:0 0 42px;
    flex:0 0 42px;
    border-top:1px solid #F0F1F5;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    -webkit-box-pack:center;
    -ms-flex-pack:center;
    justify-content:center;
    color:#3A84FF;
}
.monitor-navigation-nav {
    width:150px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-orient:vertical;
    -webkit-box-direction:normal;
    -ms-flex-direction:column;
    flex-direction:column;
    background:#FFFFFF;
    border:1px solid #E2E2E2;
    -webkit-box-shadow:0px 3px 4px 0px rgba(64,112,203,0.06);
    box-shadow:0px 3px 4px 0px rgba(64,112,203,0.06);
    padding:6px 0;
    margin:0;
    color:#63656E;
}
.monitor-navigation-nav .nav-item {
    -webkit-box-flex:0;
    -ms-flex:0 0 32px;
    flex:0 0 32px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    padding:0 20px;
    list-style:none
}
.monitor-navigation-nav .nav-item:hover {
    color:#3A84FF;
    cursor:pointer;
    background-color:#F0F1F5;
}
.monitor-navigation-admin {
    width:170px #63656E;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-orient:vertical;
    -webkit-box-direction:normal;
    -ms-flex-direction:column;
    flex-direction:column;
    background:#FFFFFF;
    border:1px solid #E2E2E2;
    -webkit-box-shadow:0px 3px 4px 0px rgba(64,112,203,0.06);
    box-shadow:0px 3px 4px 0px rgba(64,112,203,0.06);
    padding:6px 0;
    margin:0;
    color:#63656E;
}
.monitor-navigation-admin .nav-item {
    -webkit-box-flex:0;
    -ms-flex:0 0 32px;
    flex:0 0 32px;
    display:-webkit-box;
    display:-ms-flexbox;
    display:flex;
    -webkit-box-align:center;
    -ms-flex-align:center;
    align-items:center;
    padding:0 20px;
    list-style:none
}
.monitor-navigation-admin .nav-item:hover {
    color:#3A84FF;
    cursor:pointer;
    background-color:#F0F1F5;
}
.tippy-popper .tippy-tooltip.navigation-message-theme {
    padding:0;
    border-radius:0;
    -webkit-box-shadow:none;
    box-shadow:none;
}
</style>
