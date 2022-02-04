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

        <p><strong>Price: </strong>{{}} PLN -- {{ }}</p>

        <div class="field has-addons mt-6">
          <div class="control">
            <input type="number" class="input" min="1" v-model="quantity">
          </div>

          <div class="control">
            <a class="button is-dark" @click="addToCart()">Add to cart</a>
          </div>

        </div>
        <br>

        <div id="list-rendering">
            <div v-for="variantId in this.product_variant"
              v-bind:key="variantId.id">
                <input type="radio" id="variant" :value="variantId"  v-model="size">
                <label for="variant">{{variantId.variant}} </label>
            </div>
        </div>




<!--              <input type="radio" id="variant" :value="id" v-model="size">-->
<!--            <label for="variant"> Small (20 cm)</label>-->



<!--        <template v-if="this.$route.params.category_slug === 'pizza'">-->
<!--            <input type="radio" id="variant" :value="id" v-model="size">-->
<!--            <label for="variant"> Small (20 cm)</label>-->
<!--            <br>-->
<!--            <input type="radio" id="medium" :value="product_variant" v-model="size">-->
<!--            <label for="medium"> Medium (30 cm)</label>-->
<!--            <br>-->
<!--            <input type="radio" id="large" value="LARGE" v-model="size">-->
<!--            <label for="large"> Large (40 cm)</label>-->
<!--            <br>-->
<!--            <input type="radio" id="giant" value="GIANT" v-model="size">-->
<!--            <label for="giant"> Giant (50 cm)</label>-->
<!--        </template>-->
<!--        <template v-else>-->
<!--            <input type="radio" id="0,3L" value=0.3 v-model="size">-->
<!--            <label for="variant"> 0,3 L</label>-->
<!--            <br>-->
<!--            <input type="radio" id="0,5L" value=0.5 v-model="size">-->
<!--            <label for="medium"> 0,5 L</label>-->
<!--            <br>-->
<!--            <input type="radio" id=")1,0L" value=1.0 v-model="size">-->
<!--            <label for="large"> 1,0 L</label>-->
<!--            <br>-->
<!--        </template>-->

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'

export default {
  name: 'Product',
  data() {
    return {
      product: {},
      product_variant: {},
      quantity: 1,
      size: this.product_variant,
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
            console.log(response.data)
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
            console.log(response.data)
          })
          .catch(error => {
            console.log(error)
          })

      this.$store.commit('setIsLoading', false)
    },

    addToCart(id) {
      if (isNaN(this.quantity) || this.quantity < 1) {
        this.quantity = 1
      }
      const item = {
        product: this.product_variant.filter(({ id: variantId })  => id === variantId),
        quantity: this.quantity,


        // product: this.product,
        // size: this.product.size.size,
        // quantity: this.quantity

      }
      console.log(item.product)


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