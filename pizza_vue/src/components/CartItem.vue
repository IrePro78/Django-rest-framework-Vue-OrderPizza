<template xmlns="http://www.w3.org/1999/html">
    <tr>
        <td><router-link :to="item.contents.product_variant.product.get_absolute_url">{{ item.contents.product_variant.product.name }}</router-link></td>
        <td>{{item.contents.product_variant.variant.size}}</td>
        <td>{{item.contents.product_variant.price}} PLN</td>
        <td>

          <a @click="decrementQuantity(item) "><i class="fas fa-minus"></i> </a>
          {{ item.quantity }}
          <a @click="incrementQuantity(item) "><i class="fas fa-plus"></i> </a>

        </td>

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
        <td><button class="delete" @click="removeFromCart(item)"></button></td>
    </tr>
</template>

<script>
export default {
    name: 'CartItem',
    props: {
        initialItem: Object
    },
    data() {
        return {
            item: this.initialItem,
        }
    },
    methods: {
        getItemTotal(item) {
          return (item.contents.product_variant.price * item.quantity) + (item.contents.product_toppings.reduce((acc, curVal) => {
            return acc += curVal.price * item.quantity
          }, 0))+ item.contents.product_sauces.reduce((acc, curVal) => {
          return acc += curVal.price * item.quantity
        }, 0)
        },
        decrementQuantity(item) {
            item.quantity -= 1
            if (item.quantity === 0) {
                this.$emit('removeFromCart', item)
            }
            this.updateCart()
        },
        incrementQuantity(item) {
            item.quantity += 1
            this.updateCart()
        },
        updateCart() {
            localStorage.setItem('cart', JSON.stringify(this.$store.state.cart))
        },

        removeFromCart(item) {
            this.$emit('removeFromCart', item)
            this.updateCart()
        },
    },
}
</script>