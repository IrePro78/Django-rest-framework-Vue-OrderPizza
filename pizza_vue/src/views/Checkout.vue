<template>
  <div class="page-checkout">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Checkout</h1>
      </div>

      <div class="column is-12 box">
        <table class="table is-fullwidth">
          <thead>
          <tr>
            <th>Product</th>
            <th>Size</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Toppings</th>
            <th>Sauces</th>
            <th>Total</th>
          </tr>
          </thead>

          <tbody>
          <tr
              v-for="item in cart.items"
              v-bind:key="item.contents.product_variant.id"
          >
            <td>{{ item.contents.product_variant.product.name }}</td>
            <td>{{ item.contents.product_variant.variant.size }}</td>
            <td>{{ item.contents.product_variant.price }} PLN</td>
            <td>{{ item.quantity }}</td>
            <td>
              <em class="ml-2" v-for="topping in item.contents.product_toppings">
                {{ topping.name }}-{{ topping.price }}
              </em>
            </td>
            <td>
              <em class="ml-2" v-for="sauce in item.contents.product_sauces">
                {{ sauce.name }}-{{ sauce.price }}
              </em>
            </td>
            <td>{{ getItemTotal(item).toFixed(2) }} PLN</td>
          </tr>
          </tbody>
          <tfoot>

          <td colspan="3">Total</td>
          <td>{{ cartTotalLength }}</td>
          <td colspan="2"></td>
          <td>{{ cartTotalPrice.toFixed(2) }} PLN</td>
          </tfoot>
        </table>
      </div>

      <div class="column is-12 box">
        <h2 class="subtitle">Shipping details</h2>

        <p class="has-text-grey mb-4">* All fields are required</p>

        <div class="columns is-multiline">
          <div class="column is-6">
            <div class="field">
              <label>First name*</label>
              <div class="control">
                <input type="text" class="input" v-model="first_name">
              </div>
            </div>

            <div class="field">
              <label>Last name*</label>
              <div class="control">
                <input type="text" class="input" v-model="last_name">
              </div>
            </div>

            <div class="field">
              <label>E-mail*</label>
              <div class="control">
                <input type="email" class="input" v-model="email">
              </div>
            </div>

            <div class="field">
              <label>Phone*</label>
              <div class="control">
                <input type="text" class="input" v-model="phone">
              </div>
            </div>
          </div>

          <div class="column is-6">
            <div class="field">
              <label>Address*</label>
              <div class="control">
                <input type="text" class="input" v-model="address">
              </div>
            </div>

            <div class="field">
              <label>Post code*</label>
              <div class="control">
                <input type="text" class="input" v-model="postcode">
              </div>
            </div>

            <div class="field">
              <label>Place*</label>
              <div class="control">
                <input type="text" class="input" v-model="place">
              </div>
            </div>
          </div>
        </div>

        <div class="notification is-danger mt-4" v-if="errors.length">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
        </div>

        <hr>

        <div id="card-element" class="mb-5"></div>

        <template v-if="cartTotalLength">
          <hr>

          <button class="button is-dark" @click="submitForm">Send order</button>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'


export default {
  name: 'Checkout',
  data() {
    return {
      cart: {
        items: []
      },
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      address: '',
      postcode: '',
      place: '',
      errors: []
    }
  },
  mounted() {
    document.title = 'Checkout | OrderPizza'
    this.cart = this.$store.state.cart


  },
  methods: {

    getItemTotal(item) {
      return (item.quantity * item.contents.product_variant.price)
          + (item.contents.product_toppings.reduce((acc, curVal) => {
            return acc += curVal.price * item.quantity
          }, 0)) + item.contents.product_sauces.reduce((acc, curVal) => {
            return acc += curVal.price * item.quantity
          }, 0)
    },

    submitForm() {
      this.errors = []
      if (this.first_name === '') {
        this.errors.push('The first name field is missing!')
      }
      if (this.last_name === '') {
        this.errors.push('The last name field is missing!')
      }
      if (this.email === '') {
        this.errors.push('The email field is missing!')
      }
      if (this.phone === '') {
        this.errors.push('The phone field is missing!')
      }
      if (this.address === '') {
        this.errors.push('The address field is missing!')
      }
      if (this.postcode === '') {
        this.errors.push('The post code field is missing!')
      }
      if (this.place === '') {
        this.errors.push('The place field is missing!')
      }
      if (!this.errors.length) {

        this.$store.commit('setIsLoading', true)
        const items = []
        this.cart.items.forEach(item => {

          const obj = {
            contents: {
              product_variant: item.contents.product_variant,
              toppings: item.contents.product_toppings,
              sauces: item.contents.product_sauces,
            },
            quantity: item.quantity,
            total_price: this.getItemTotal(item)
          }
          items.push(obj)

        })
        const data = {
          'first_name': this.first_name,
          'last_name': this.last_name,
          'email': this.email,
          'address': this.address,
          'postcode': this.postcode,
          'place': this.place,
          'phone': this.phone,
          'items': items

        }
        axios
            .post('/api/v1/checkout/', data)
            .then(response => {
              console.log(response.data)
              this.$store.commit('clearCart')
              this.$router.push('/cart/success')

            })
            .catch(error => {
              this.errors.push('Something went wrong. Please try again')
              console.log(error)
            })
        this.$store.commit('setIsLoading', false)
      }
    }
  },
  computed: {
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
    },
    cartTotalLength() {
      return this.cart.items.reduce((acc, curVal) => {
        return acc += curVal.quantity
      }, 0)
    }
  }
}
</script>