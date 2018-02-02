<template>
<b-media tag="li" class="mb-3">
  <b-img slot="aside" :src="product.photo" height="96" alt="product" />
  <h3 class="mt-0 mb-1 text-left">{{ product.name }}</h3>
  <b-row class="">
    <b-col cols="10">
      <p class="text-left">{{ product.description }}</p>
    </b-col>
    <b-col cols="2">
      <h4>&#36;{{ product.price }}</h4>
      <b-button @click="createCartProduct" variant="primary">Add to cart</b-button>
    </b-col>
  </b-row>
</b-media>
</template>

<script>
import Cookies from 'js-cookie';
import _ from 'lodash';

export default {
  name: 'Products',
  props: {
    product: {
      url: String,
      name: String,
      description: String,
      photo: String,
      price: String,
      created: String,
      updated: String,
    },
  },
  methods: {
    createCartProduct: _.debounce(function () {
      fetch('/api/cart/products/', {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken'),
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        method: 'POST',
        body: JSON.stringify({
          product: this.product.url,
          quantity: 1,
        }),
      })
        .then((result) => {
          if (result.status === 201) {
            this.$emit('fetchCartEvent');
          } else if (result.status === 409) {
            this.$notify({
              group: 'shop',
              type: 'error',
              title: 'Error',
              text: 'This product is already in your cart',
            });
          } else {
            // TODO: Handle error?
          }
          return result.json();
        })
        .then((json) => {
          if (_.has(json, 'cart') && !_.has(json, 'product')) {
            this.$notify({
              group: 'shop',
              type: 'error',
              title: 'Error',
              text: json.cart[0],
            });
          }
        });
    }, 500, { leading: true, trailing: true }),
  },
};
</script>
