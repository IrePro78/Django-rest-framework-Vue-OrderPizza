<template>
  <div class="page-product">
    <div class="columns is-multiline">
      <div class="column is-9">
        <figure class="image mb-6">
          <img v-bind:src="product.get_image">
        </figure>

        <h1 class="title">{{ product.name }}</h1>

        <p>{{ product.description }}</p>
      </div>
      <div class="column is-3">
        <h2 class="subtitle">Information</h2>

        <p><strong>Price: </strong>{{ totalPrice.toFixed(2) }} PLN </p>

        <div class="field has-addons mt-5">
          <div class="control">
            <input type="number" class="input" min="1" v-model="quantity">
          </div>
          <div class="control">
            <a class="button is-dark" @click="addToCart(selected_variant, selected_toppings, selected_sauces)">Add to cart</a>
          </div>
        </div>
        <br>
        <p><strong>{{ show_size }}</strong></p>
        <div class="radio mt-2">
          <div v-for="variant in product_variant" :key="variant.id">
            <label>
            <input type="radio" id="variant"
                   :value="variant"
                   v-model="selected_variant">
            {{ variant.variant.size }} {{ variant.variant.description }}</label>
          </div>
        </div>
        <br>
        <br>
         <p><strong>{{ show_topp }}</strong></p>
        <div class="checkbox_topping mt-2">
            <div v-for="topping in product_toppings" :key="topping.id">
              <label>
              <input type="checkbox" id="topping"
                     :value="topping"
                     v-model="selected_toppings">
              {{ topping.name }} - {{topping.price}} PLN</label>
          </div>
        </div>
        <br>
        <p><strong>{{ show_sauce }}</strong></p>
        <div class="checkbox_sauce mt-2">
            <div v-for="sauce in product_sauces" :key="sauce.id">
              <label>
              <input type="checkbox" id="sauce"
                     :value="sauce"
                     v-model="selected_sauces">
              {{ sauce.name }} - {{sauce.price}} PLN</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import ProductBox from "@/components/ProductBox";
import {uuid} from "uuidv4";

export default {
  name: 'Product',
  components: {
        ProductBox
    },
  data() {
    return {
      product: {},
      product_variant: {},
      selected_variant: {},
      product_toppings: [],
      selected_toppings: [],
      product_sauces: [],
      selected_sauces: [],
      contents: {},
      quantity: 1,
      show_topp:'',
      show_size:'',
      show_sauce:'',
      uuid: '',

    }

  },

  mounted() {
    this.getProduct()

  },
  methods: {
    async getProduct() {
      this.$store.commit('setIsLoading', true)
      const category_slug = this.$route.params.category_slug
      const product_slug = this.$route.params.product_slug
      await axios
          .get(`/api/v1/products/${category_slug}/${product_slug}`)
          .then(response => {
            this.product = response.data
            this.getVariantsProduct(product_slug)
            if (category_slug === 'pizza') {
              this.getToppingsProduct()
              this.getSaucesProduct()
              this.show_topp = 'Toppings:'
              this.show_size = 'Size:'
              this.show_sauce = 'Sauces:'
            } else {
              this.show_size = 'Capacity:'
              }

            document.title = this.product.name + ' | OrderPizza'
          })
          .catch(error => {
            console.log(error)
          })

      this.$store.commit('setIsLoading', false)
    },

    async getVariantsProduct(product_slug) {
      this.$store.commit('setIsLoading', true)
      await axios
          .get(`/api/v1/variants/${product_slug}`)
          .then(response => {
            this.product_variant = response.data
            this.selected_variant = response.data.find(i => i.is_default)
          })
          .catch(error => {
            console.log(error)
          })

      this.$store.commit('setIsLoading', false)
    },

    async getToppingsProduct() {
      this.$store.commit('setIsLoading', true)
      await axios
          .get(`/api/v1/toppings/`)
          .then(response => {
            this.product_toppings = response.data
          })
          .catch(error => {
            console.log(error)
          })

      this.$store.commit('setIsLoading', false)
    },

    async getSaucesProduct() {
      this.$store.commit('setIsLoading', true)
      await axios
          .get(`/api/v1/sauces/`)
          .then(response => {
            this.product_sauces = response.data

          })
          .catch(error => {
            console.log(error)
          })

      this.$store.commit('setIsLoading', false)
    },

    addToCart(variant, toppings, sauces) {
      if (isNaN(this.quantity) || this.quantity < 1) {
        this.quantity = 1
      }

      const item = {
        uuid: uuid(),
        contents: {
          product_variant: variant,
          product_toppings: toppings,
          product_sauces: sauces,
        },
        quantity: this.quantity,
      }
      this.$store.commit('addToCart', item)
      toast({
        message: 'The product was added to the cart',
        type: 'is-success',
        dismissible: true,
        pauseOnHover: true,
        duration: 2000,
        position: 'bottom-right',
      })
    }
  },
  computed: {
    totalPrice() {
        return (this.selected_variant.price * this.quantity ) + (this.selected_toppings.reduce((acc, curVal) => {
          return acc += curVal.price * 1
        }, 0))+ this.selected_sauces.reduce((acc, curVal) => {
          return acc += curVal.price * 1
        }, 0)
    }
  }
}
</script>