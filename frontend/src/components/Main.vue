<template>
<b-row>
  <b-col lg="8" sm="10"><products v-on:fetchCartEvent="fetchCart" /></b-col>
  <b-col lg="4" sm="10"><cart /></b-col>
</b-row>
</template>

<script>
import Cart from '@/components/Cart';
import Products from '@/components/Products';

export default {
  name: 'Main',
  data() {
    return {
    };
  },
  components: {
    cart: Cart,
    products: Products,
  },
  methods: {
    fetchCart() {
      this.$emit('fetchCartEvent');
    },
  },
};
</script>

