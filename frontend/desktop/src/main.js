/**
 * @file main entry
 * @author wheel-w
 */

import './public-path'
import Vue from 'vue'

import App from '@/App'
import router from '@/router'
import store from '@/store'
import { injectCSRFTokenToHeaders } from '@/api'
import auth from '@/common/auth'
import Img403 from '@/images/403.png'
import Exception from '@/components/exception'
import { bus } from '@/common/bus'
import AuthComponent from '@/components/auth'
import bkMagicVue from 'bk-magic-vue'
import VueI18n from 'vue-i18n'
import Cookie from 'js-cookie'
import { messages } from '@/language/index.js'

// 国际化配置
Vue.use(VueI18n)
Vue.use(bkMagicVue)
const locale = Cookie.get('blueking_language') || 'zhCN'
const i18n = new VueI18n({
    locale,
    messages
})
bkMagicVue.locale.i18n((key, value) => i18n.t(key, value))
Vue.component('app-exception', Exception)
Vue.component('app-auth', AuthComponent)

auth.requestCurrentUser().then(user => {
    injectCSRFTokenToHeaders()
    if (user.isAuthenticated) {
        global.bus = bus
        global.mainComponent = new Vue({
            el: '#app',
            i18n,
            router,
            store,
            components: { App },
            template: '<App/>'
        })
    }
}, err => {
    let message
    if (err.status === 403) {
        message = 'Sorry，您的权限不足!'
        if (err.data && err.data.msg) {
            message = err.data.msg
        }
    } else {
        message = '无法连接到后端服务，请稍候再试。'
    }

    const divStyle = ''
        + 'text-align: center;'
        + 'width: 400px;'
        + 'margin: auto;'
        + 'position: absolute;'
        + 'top: 50%;'
        + 'left: 50%;'
        + 'transform: translate(-50%, -50%);'

    const h2Style = 'font-size: 20px;color: #979797; margin: 32px 0;font-weight: normal'

    const content = ``
        + `<div class="bk-exception bk-exception-center" style="${divStyle}">`
        + `<img src="${Img403}"><h2 class="exception-text" style="${h2Style}">${message}</h2>`
        + `</div>`

    document.write(content)
})
