<template>
    <div class="box mb-4">
        <h3 class="is-size-4 mb-2">Order #{{ order.id }} </h3>
        <h3 class="is-size-6 mb-6">Date of order : {{order.created_at}} </h3>

        <h4 class="is-size-5">Products</h4>

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
                    <th></th>
                </tr>
            </thead>

            <tbody>
                <tr
                    v-for="item in order.items"
                    v-bind:key="item.contents.id"
                >
                    <td>{{ item.contents.product_variant.product.name}}</td>
                    <td>{{ item.contents.product_variant.variant.size }}</td>
                    <td>{{ item.contents.product_variant.price }} PLN</td>
                    <td>{{ item.contents.quantity }}</td>
                    <td>
                      <em class="ml-2" v-for="topping in item.contents.toppings">
                        {{ topping.name }}-{{ topping.price }}
                      </em>
                    </td>
                    <td>
                      <em class="ml-2" v-for="sauce in item.contents.sauces">
                        {{ sauce.name }}-{{ sauce.price }}
                      </em>
                    </td>

                    <td>{{ getItemTotal(item).toFixed(2) }} PLN</td>
                </tr>
            </tbody>

            <tfoot>
                <tr>
                    <td colspan="3">Total</td>
                    <td>{{ orderTotalLength(order) }}</td>
                    <td colspan="2"></td>
                    <td>{{ orderTotalPrice(order).toFixed(2) }} PLN</td>

                </tr>
            </tfoot>

        </table>
    </div>
</template>

<script>
export default {
    name: 'OrderSummary',
    props: {
        order: Object
    },
    methods: {
        getItemTotal(item) {
          return (item.quantity * item.contents.product_variant.price) + (item.contents.toppings.reduce((acc, curVal) => {
            return acc += curVal.price * 1
          }, 0)) + item.contents.sauces.reduce((acc, curVal) => {
          return acc += curVal.price * 1
        }, 0)
        },

        orderTotalLength(order) {
            return order.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        orderTotalPrice(order) {
      return order.items.reduce((acc, curVal) => {
        return acc += curVal.contents.product_variant.price * curVal.quantity
      }, 0) + order.items.reduce((acc, curVal) => {
        return acc += curVal.contents.toppings.reduce((acc, curVal) => {
          return acc += curVal.price * 1
        }, 0)
      }, 0) +  order.items.reduce((acc, curVal) => {
        return acc += curVal.contents.sauces.reduce((acc, curVal) => {
          return acc += curVal.price * 1
        }, 0)
      }, 0)
    },

    }
}
</script>