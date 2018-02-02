<template>
<b-media tag="li" class="mb-3">
  <b-img slot="aside" :src="cartProduct.product.photo" height="32" alt="placeholder" />
  <b-row>
    <b-col cols="6">
      <h6 class="text-left mt-1 mb-0">{{ cartProduct.product.name }}</h6>
    </b-col>
    <b-col cols="4">
      <b-input-group>
        <b-input-group-prepend>
          <b-btn @click="decrementQuantity" variant="outline-danger">&ndash;</b-btn>
        </b-input-group-prepend>

        <b-form-input size="sm" class="text-center" :value="cartProduct.quantity" readonly>
        </b-form-input>

        <b-input-group-append>
          <b-btn v-if="!productsMaxExceeded" @click="incrementQuantity" variant="outline-success">
            &#43;
          </b-btn>
          <b-btn v-if="productsMaxExceeded" disabled variant="outline-success">
            &#43;
          </b-btn>
        </b-input-group-append>
      </b-input-group>
    </b-col>
    <b-col cols="1">
      <b-btn size="sm" v-on:click="deleteCartProduct" variant="danger">Delete</b-btn>
    </b-col>
  </b-row>
</b-media>
</template>

<script>
import Cookies from 'js-cookie';
import _ from 'lodash';

export default {
  name: 'CartProduct',
  props: {
    cartProduct: {
      url: String,
      quantity: Number,
      product: {
        name: String,
        description: String,
        photo: String,
        price: String,
        created: String,
        updated: String,
      },
    },
  },
  watch: {
    'cartProduct.quantity': function () {
      this.updateQuantity();
    },
  },
  computed: {
    productsMaxExceeded() {
      return this.cartProduct.quantity >= 10;
    },
  },
  methods: {
    decrementQuantity() {
      if (this.cartProduct.quantity > 1) {
        this.cartProduct.quantity -= 1;
      } else {
        this.deleteCartProduct();
      }
    },
    incrementQuantity() {
      this.cartProduct.quantity += 1;
    },
    updateQuantity: _.debounce(function () {
      fetch((new URL(this.cartProduct.url)).pathname, {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken'),
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        method: 'PATCH',
        body: JSON.stringify({ quantity: this.cartProduct.quantity }),
      })
        .then((result) => {
          if (result.status !== 200) {
            // TODO: Handle error?
          }
        });
    }, 500, { leading: true, trailing: true }),
    deleteCartProduct() {
      fetch((new URL(this.cartProduct.url)).pathname, {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken'),
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        method: 'DELETE',
      })
        .then((result) => {
          if (result.status === 204) {
            this.$emit('fetchCartEvent');
          } else {
            // TODO: Handle error?
          }
        });
    },
  },
};
</script>
