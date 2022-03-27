<template>
    <div>
        <main class="main-content" v-bkloading="{ isLoading:
            mainContentLoading, opacity: 1 }">
            <router-view :key="routerKey" v-show="!mainContentLoading" />
        </main>
        <app-auth ref="bkAuth"></app-auth>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex'

    import { bus } from '@/common/bus'

    export default {
        name: 'app',
        data () {
            return {
                routerKey: +new Date(),
                systemCls: 'mac'
            }
        },
        computed: {
            ...mapGetters(['mainContentLoading'])
        },
        watch: {
        },
        created () {
            const platform = window.navigator.platform.toLowerCase()

            if (platform.indexOf('win') === 0) {
                this.systemCls = 'win'
            }
        },
        mounted () {
            const self = this
            bus.$on('show-login-modal', data => {
                self.$refs.bkAuth.showLoginModal(data)
            })
            bus.$on('close-login-modal', () => {
                self.$refs.bkAuth.hideLoginModal()
                setTimeout(() => {
                    window.location.reload()
                }, 0)
            })
        }
    }
</script>
