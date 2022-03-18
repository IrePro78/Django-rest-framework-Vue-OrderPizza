import {createStore} from 'vuex'
import _ from "lodash";

export default createStore({
    state: {
        cart: {
            items: [],
        },
        isAuthenticated: false,
        token: '',
        isLoading: false,
        user: {
            id: 0,
            username: '',
            email: ''
        }
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('cart')) {
                state.cart = JSON.parse(localStorage.getItem('cart'))
            } else {
                localStorage.setItem('cart', JSON.stringify(state.cart))
            }

            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
                state.user.id = localStorage.getItem('userid')
                state.user.username = localStorage.getItem('username')
                state.user.email = localStorage.getItem('email')


            } else {
                state.token = ''
                state.isAuthenticated = false
                state.user.id = 0
                state.user.username = ''
                state.user.email = ''
            }
        },

        addToCart(state, item) {

            const exists = state.cart.items.filter(i => i.contents.product_variant.id === item.contents.product_variant.id)

            let result = false;
            let exist_index = 0
            exists.forEach(function(exist, index) {
              if (_.isEqual(exist.contents,item.contents)) {
                result = true;
                exist_index = index;
              }
            });
            console.log(result, exist_index);

            if (result) {
                exists[exist_index].quantity = parseInt(exists[exist_index].quantity) + parseInt(item.quantity)
            } else {
                state.cart.items.push(item)
            }

            localStorage.setItem('cart', JSON.stringify(state.cart))

        },

        setIsLoading(state, status) {
            state.isLoading = status
        },
        setToken(state, token) {
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state) {
            state.token = ''
            state.isAuthenticated = false
        },
        setUser(state, user) {
            state.user = user
        },
        clearCart(state) {
            state.cart = {items: []}
            localStorage.setItem('cart', JSON.stringify(state.cart))
        },

    },
    actions: {},
    modules: {}
})
