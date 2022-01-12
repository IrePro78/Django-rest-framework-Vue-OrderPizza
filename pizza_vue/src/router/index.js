import {createRouter, createWebHistory} from 'vue-router'
import store from "../store";
import Home from '../views/Home.vue'
import LogIn from '../views/LogIn.vue'
import LogOut from '../views/LogOut.vue'
import SignUp from '../views/SignUp.vue'
import MyAccount from '../views/MyAccount.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/log-in',
        name: "LogIn",
        component: LogIn,
    },
    {
        path: '/sign-up',
        name: "SignUp",
        component: SignUp,
    },
    {
        path: '/log-out',
        name: "LogOut",
        component: LogOut,
    },
    {
        path: '/my-account',
        name: 'MyAccount',
        component: MyAccount,
        meta: {
            requireLogin: true
        }
    },

]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
        next('/log-in')
    } else {
        next()
    }
})

export default router
