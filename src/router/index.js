import Vue from 'vue'
import Router from 'vue-router'

import Homepage from '@/components/Homepage.vue'
import Dashboard from '@/components/Dashboard.vue'
import Test from '@/components/Test.vue'
import Callback from '@/components/Callback';
import Profile from "@/components/Profile.vue";
import NewTask from "@/components/NewTask.vue";
import axiosAuth from '@/api/axios-auth'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    // TODO: maybe remove?
    base: __dirname,
    routes: [
        {path: '/', component: Homepage},
        {path: '/callback', component: Callback},
        {path: '/newTask', component: NewTask, meta: { requiresAuth: true }},
        {path: '/profile', component: Profile, meta: { requiresAuth: true }},
        {path: '/settings', component: Homepage},
        {path: '/dashboard', component: Dashboard, meta: { requiresAuth: true }},
        {path: '/login', component: Test},
        {path: '*', component: Test}
    ],
});

router.beforeEach((to, from, next) => {
    let token = localStorage.getItem('token');
    let requireAuth = to.matched.some(record => record.meta.requiresAuth);

    if (!requireAuth) {
        next();
    }

    if (requireAuth && !token) {
        next('/login');
    }

    if (to.path === '/login') {
        if (token) {
            axiosAuth.post('/api/v1/login').then(() => {
                next('/dashboard');
            }).catch(() => {
                next();
            });
        }
        else {
            next();
        }
    }

    if (requireAuth && token) {
        axiosAuth.post('/verify-token').then(() => {
            next();
        }).catch(() => {
            next('/login');
        })
    }
});

export default router;
