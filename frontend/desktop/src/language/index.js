import zhCN from './zh-hans.json'
import enUS from './en.json'
import { lang } from 'bk-magic-vue'

export const messages = {
    'zhCN': Object.assign(lang.zhCN, zhCN),
    'enUS': Object.assign(lang.enUS, enUS)
}
