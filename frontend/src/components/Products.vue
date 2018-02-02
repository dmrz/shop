<template>
<div>
  <ul class="list-unstyled">
    <product v-for="product in products"
             v-on:fetchCartEvent="fetchCart"
             :key="product.url"
             :product="product" />
  </ul>
</div>
</template>

<script>
import fetch from 'isomorphic-fetch';
import Product from '@/components/Product';

export default {
  name: 'Products',
  data: () => ({
    products: [],
  }),
  created() {
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      fetch('/api/products/', { credentials: 'same-origin' })
        .then(result => result.json())
        .then((json) => {
          this.products = json;
        });
    },
    fetchCart() {
      this.$emit('fetchCartEvent');
    },
  },
  components: {
    product: Product,
  },
};
</script>
