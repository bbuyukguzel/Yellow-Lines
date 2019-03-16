import Vue from 'vue'
import Router from 'vue-router'

import Homepage from '@/components/Homepage.vue'
import Dashboard from '@/components/Dashboard.vue'
import Test from '@/components/Test.vue'
import Callback from '@/components/Callback';

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: __dirname,
  routes: [
    { path: '/', component: Homepage },
    { path: '/callback', component: Callback },
    { path: '/settings', component: Homepage },
    { path: '/dashboard', component: Dashboard},
    { path: '/login', component: Test },
    { path: '*', component: Test }
  ]
})
