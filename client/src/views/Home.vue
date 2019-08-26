<template>
  <div class="home">
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <svg id="grass" height="140" width="100%">
      <ellipse cx="50%" cy="100%" rx="60%" ry="75"
        style="fill:green;" />
    </svg>
  </div>
</template>
<style lang="scss">
  body{
    background-color:rgb(122, 179, 255);
  }
  #grass{
    position:absolute;
    bottom:0;
    content: "";
    height: 150px;
    width: 100%;
  }
</style>
<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {
    HelloWorld
  }
}
</script>
