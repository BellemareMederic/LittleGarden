<template>
    <p>pet</p>
</template>

<script>
export default {
  computed:{
    status() {
      return this.$store.getters.status
    },
    parameter(){
      return this.$store.getters.parameter
    }
  }
};
</script>