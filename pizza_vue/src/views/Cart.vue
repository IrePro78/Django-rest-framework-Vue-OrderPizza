<template>
    <div class="page-cart">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Cart</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth" v-if="cartTotalLength">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Size</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Toppings</th>
                            <th>Total</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <CartItem ref="CartItem"
                            v-for="item in cart.items"
                            v-bind:key="item.product_variant.id"
                            v-bind:initialItem="item"
                            v-on:removeFromCart="removeFromCart"
                            v-on:getItemTotal="cartTotalPrice"
                            />
                    </tbody>

                </table>

                <p v-else>You don't have any products in your cart...</p>
            </div>

            <div class="column is-12 box">
                <h2 class="subtitle">Summary</h2>

                <strong>{{ cartTotalPrice.toFixed(2) }} PLN</strong>, {{ cartTotalLength }} items



                <template v-if="cartTotalLength">
                <hr>

                <router-link to="/cart/checkout" class="button is-dark">Proceed to checkout</router-link>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import CartItem from '@/components/CartItem.vue'
export default {
    name: 'Cart',
    components: {
        CartItem
    },
    data() {
        return {
            cart: {
                items: []
            }
        }
    },
    mounted() {
        this.cart = this.$store.state.cart
    },
    methods: {
        removeFromCart(item) {
            this.cart.items = this.cart.items.filter(i => i.product_variant.id !== item.product_variant.id)
        }
    },
    computed: {
        cartTotalLength() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        cartTotalPrice() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.item.product_toppings.reduce()
            }, 0)
        },
      //
      //
      // cartTotalPrice(item) {
      //       return (item.quantity * item.product_variant.price) + item.product_toppings.reduce((acc, curVal) => {
      //       return acc += curVal.price * 1
      //     }, 0)
      //   },


    }
}
</script>