<template>
<div>
  <ul class="list-unstyled" v-if="cartReadyForCheckout">
    <cart-product v-on:fetchCartEvent="fetchCart"
                  v-for="cartProduct in cart.cart_products"
                  :key="cartProduct.url"
                  :cartProduct="cartProduct" />
  </ul>
  <h5 v-else>Cart is empty</h5>
  <h2 v-if="cartReadyForCheckout">Subtotal: &#36;{{ subtotal }}</h2>
  <b-button @click="checkout" variant="success" v-if="cartReadyForCheckout">Checkout</b-button>
  <b-button @click="deleteCart" variant="danger" v-if="cartReadyForCheckout">Clear</b-button>
</div>
</template>

<script>
import fetch from 'isomorphic-fetch';
import Cookies from 'js-cookie';
import CartProduct from '@/components/CartProduct';
import _ from 'lodash';

export default {
  name: 'Cart',
  data: () => ({
    cart: null,
  }),
  created() {
    this.$parent.$on('fetchCartEvent', this.fetchCart);
    this.fetchCart();
  },
  beforeDestroy() {
    this.$parent.$off('fetchCartEvent', this.fetchCart);
  },
  methods: {
    fetchCart() {
      fetch('/api/cart/', { credentials: 'same-origin' })
        .then(result => result.json())
        .then((json) => {
          this.cart = json;
        });
    },
    deleteCart() {
      return fetch('/api/cart/', {
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken'),
        },
        method: 'DELETE',
        // TODO: Handle possible error
      }).then(() => this.fetchCart());
    },
    checkout() {
      this.$notify({
        group: 'shop',
        type: 'success',
        title: 'Success',
        text: 'We received your order!',
      });
      this.deleteCart();
    },
  },
  computed: {
    cartReadyForCheckout() {
      return (!_.isNull(this.cart) && this.cart.cart_products.length > 0);
    },
    subtotal() {
      return this.cart.cart_products.map(
        cartProduct => cartProduct.quantity * parseFloat(cartProduct.product.price))
        .reduce((a, b) => a + b).toFixed(2);
    },
  },
  components: {
    'cart-product': CartProduct,
  },
};
</script>
