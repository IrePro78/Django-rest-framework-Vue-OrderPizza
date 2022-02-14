<template xmlns="http://www.w3.org/1999/html">
    <div v-for="topping of item.product_toppings"></div>
    <tr>
        <td><router-link :to="item.product_variant.product.get_absolute_url">{{ item.product_variant.product.name }}</router-link></td>
        <td>{{item.product_variant.variant.size}}</td>
        <td>{{item.product_variant.price}} PLN</td>
        <td>

          <a @click="decrementQuantity(item) "><i class="fas fa-minus"></i> </a>
          {{ item.quantity }}
          <a @click="incrementQuantity(item) "><i class="fas fa-plus"></i> </a>

        </td>

        <td>
           <label class="ml-2" v-for="topping in item.product_toppings">
              {{ topping.name }} {{ topping.price }}
            </label>
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
            item: this.initialItem
        }
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product_variant.price
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