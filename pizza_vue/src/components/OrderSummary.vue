<template>
    <div class="box mb-4">
        <h3 class="is-size-4 mb-2">Order #{{ order.id }} </h3>
        <h3 class="is-size-6 mb-6">Date of order : {{order.created_at}} </h3>

        <h4 class="is-size-5">Products</h4>

        <table class="table is-fullwidth">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                </tr>
            </thead>

            <tbody>
                <tr
                    v-for="item in order.items"
                    v-bind:key="item.product.id"
                >
                    <td>{{ item.product.name }}</td>
                    <td>{{ item.product.price }} PLN</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ getItemTotal(item).toFixed(2) }} PLN</td>
                </tr>
            </tbody>

            <tfoot>
                <tr>
                    <td colspan="2">Total</td>
                    <td>{{ orderTotalLength(order) }}</td>
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
            return item.quantity * item.product.price
        },
        orderTotalLength(order) {
            return order.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        orderTotalPrice(order) {
            return order.items.reduce((acc, curVal) => {
                return acc += curVal.product.price * curVal.quantity
            }, 0)
        },

    }
}
</script>