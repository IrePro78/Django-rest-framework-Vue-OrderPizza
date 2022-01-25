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

                <p><strong>Price: </strong>{{ product.price }} PLN -- {{ picked }}</p>

                <div class="field has-addons mt-6">
                    <div class="control">
                        <input type="number" class="input" min="1" v-model="quantity">
                    </div>

                    <div class="control">
                        <a class="button is-dark" @click="addToCart()">Add to cart</a>
                    </div>

                </div>
                <br>
                <div>
                  <input type="radio" id="small" value="small" v-model="picked">
                  <label for="small">  Small (20 cm)</label>
                  <br>
                  <input type="radio" id="medium" value="medium" v-model="picked">
                  <label for="medium">  Medium (30 cm)</label>
                  <br>
                  <input type="radio" id="large" value="large" v-model="picked">
                  <label for="large">  Large (40 cm)</label>
                  <br>
                  <input type="radio" id="x-large" value="x-large" v-model="picked">
                  <label for="x-large">  X-Large (50 cm)</label>


                </div>

            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
    name: 'Product',
    data() {
        return {
            product: {},
            quantity: 1,
            picked: 'medium'
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
                    console.log(response.data)
                    document.title = this.product.name + ' | OrderPizza'
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },
        addToCart() {
            if (isNaN(this.quantity) || this.quantity < 1) {
                this.quantity = 1
            }
            const item = {
                product: this.product,
                size: this.picked,
                quantity: this.quantity

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
    }
}
</script>