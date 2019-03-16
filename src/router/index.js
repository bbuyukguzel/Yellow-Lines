import Vue from 'vue'
import Router from 'vue-router'

import Homepage from '@/components/Homepage.vue'
import Dashboard from '@/components/Dashboard.vue'
import Test from '@/components/Test.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: __dirname,
  routes: [
    { path: '/', component: Homepage },
    { path: '/settings', component: Homepage },
    { path: '/dashboard', component: Dashboard},
    { path: '/login', component: Test },
    { path: '*', component: Test }
  ]
})
