<template>
  <div class="home">
    <section class="hero is-small is-dark mb-6">
        <div class="hero-body has-text-centered">
            <p class="title mb-6">
                Welcome to Pizza ordering online
            </p>
            <p class="subtitle">
                The best pizza store online
            </p>
        </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class="is-size-2 has-text-centered">Popular products</h2>
      </div>

      <ProductBox
        v-for="product in popularProducts"
        v-bind:key="product.id"
        v-bind:product="product" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox'
export default {
  name: 'Home',
  data() {
    return {
      popularProducts: []
    }
  },
  components: {
    ProductBox
  },
  mounted() {
    this.getPopularProducts()
    document.title = 'Home | OrderPizza'
  },
  methods: {
    async getPopularProducts() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/popular-products/')
        .then(response => {
          this.popularProducts = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>