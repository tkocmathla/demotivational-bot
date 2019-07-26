<template>
  <div class="container">
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Bot',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/generate?prefix=Innovation&similarity_threshold=0.5&nsamples=1&length=5&temperature=0.9&top_k=1';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
