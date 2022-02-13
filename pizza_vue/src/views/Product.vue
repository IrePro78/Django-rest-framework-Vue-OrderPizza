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

        <p><strong>Price: </strong>{{ selected_variant.price }} PLN </p>

        <div class="field has-addons mt-6">
          <div class="control">
            <input type="number" class="input" min="1" v-model="quantity">
          </div>

          <div class="control">
            <a class="button is-dark" @click="addToCart(selected_variant)">Add to cart</a>
          </div>

        </div>
        <br>

        <div class="radio">
          <div v-for="variant in product_variant" :key="variant.id">
            <input type="radio" id="variant"
                   :value="variant"
                   v-model="selected_variant">
            <label class="ml-2" for="variant">{{ variant.variant.size }} {{ variant.variant.description }}</label>
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
      quantity: 1

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
            this.getVariantProduct(product_slug)
            document.title = this.product.name + ' | OrderPizza'
          })
          .catch(error => {
            console.log(error)
          })

      this.$store.commit('setIsLoading', false)
    },

    async getVariantProduct(product_slug) {
      this.$store.commit('setIsLoading', true)
      await axios
          .get(`/api/v1/variants/${product_slug}`)
          .then(response => {
            this.product_variant = response.data
            this.selected_variant = response.data.find(i => i.is_default)
            console.log(this.selected_variant)
          })
          .catch(error => {
            console.log(error)
          })

      this.$store.commit('setIsLoading', false)
    },

    addToCart(variant) {
      if (isNaN(this.quantity) || this.quantity < 1) {
        this.quantity = 1
      }
      const item = {
        product_variant: variant,
        quantity: this.quantity,
      }
      console.log(item.product_variant)
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
  }
}
</script>