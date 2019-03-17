import Vue from 'vue'
import Router from 'vue-router'
import auth from "../auth/authService";

import Homepage from '@/components/Homepage.vue'
import Dashboard from '@/components/Dashboard.vue'
import Test from '@/components/Test.vue'
import Callback from '@/components/Callback';
import Profile from "@/components/Profile.vue";
import NewTask from "@/components/NewTask.vue";

Vue.use(Router)

const router = new Router({
    mode: 'history',
    // TODO: maybe remove?
    base: __dirname,
    routes: [
        {path: '/', component: Homepage},
        {path: '/callback', component: Callback},
        {path: '/newTask', component: NewTask},
        {path: '/profile', component: Profile},
        {path: '/settings', component: Homepage},
        {path: '/dashboard', component: Dashboard},
        {path: '/login', component: Test},
        {path: '*', component: Test}
    ],
});

router.beforeEach((to, from, next) => {
    if (to.path === "/" || to.path === "/callback" || auth.isAuthenticated()) {
        return next();
    }

    // Specify the current path as the customState parameter, meaning it
    // will be returned to the application after auth
    auth.login({target: to.path});
});

export default router;
