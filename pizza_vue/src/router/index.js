import {createRouter, createWebHistory} from 'vue-router'
import store from "@/store";
import Home from '@/views/Home.vue'

import Product from '@/views/Product.vue'
import Category from '@/views/Category.vue'
import Cart from '@/views/Cart.vue'
import LogIn from '@/views/LogIn.vue'
import LogOut from '@/views/LogOut.vue'
import SignUp from '@/views/SignUp.vue'
import MyAccount from '@/views/MyAccount.vue'
import Checkout from '@/views/Checkout.vue'
import Success from '@/views/Success.vue'
import Delivery from '@/views/Delivery.vue';
import EditProfile from "@/views/EditProfile";

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
    {
        path: '/edit-profile',
        name: 'EditProfile',
        component: EditProfile,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/cart',
        name: 'Cart',
        component: Cart
    },
    {
        path: '/cart/success',
        name: 'Success',
        component: Success
    },
    {
        path: '/cart/checkout',
        name: 'Checkout',
        component: Checkout,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/:category_slug/:product_slug',
        name: 'Product',
        component: Product
    },
    {
        path: '/:category_slug',
        name: 'Category',
        component: Category
    },
    {
        path: '/delivery',
        name: 'Delivery',
        component: Delivery
    }

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
