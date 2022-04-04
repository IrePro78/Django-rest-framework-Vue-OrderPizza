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
            <th>Sauces</th>
            <th>Total</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <CartItem
              v-for="item in cart.items"
              v-bind:key="item.uuid"
              v-bind:initialItem="item"
              v-on:removeFromCart="removeFromCart"

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
      this.cart.items = this.cart.items.filter(i => i.uuid !== item.uuid)
    }
  },
  computed: {
    cartTotalLength() {
      return this.cart.items.reduce((acc, curVal) => {
        return acc += curVal.quantity
      }, 0)
    },

    cartTotalPrice() {
      const items = this.cart.items;
      let itemPrice = 0
      let toppingsPrice = 0
      let saucesPrice = 0

      items.forEach(item => {
        itemPrice += item.contents.product_variant.price * item.quantity
        item.contents.product_toppings.forEach(topping => {
          toppingsPrice += topping.price * item.quantity
        })
        item.contents.product_sauces.forEach(sauce => {
          saucesPrice += sauce.price * item.quantity
        })
      })
      return itemPrice + toppingsPrice + saucesPrice
    }
  }
}
</script>