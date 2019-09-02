<template>
  <div class="home">
    <Nuage />
    <svg id="grass" height="140" width="100%">
      <ellipse cx="50%" cy="100%" rx="60%" ry="75" style="fill:green;" />
    </svg>
    <Plante />
      <div class="white-box left">
        <span v-if="status.water">{{ status.water.currentHumidity | pourcent }}</span>
        <span v-if="status.water">{{ status.water.isWatering }}</span>
      </div>
      <div class="white-box right">
        <span v-if="status.light">{{ status.light.isOn }}</span>
      </div>
  </div>
</template>
<style lang="scss">
body {
  background-color: rgb(122, 179, 255);
}
.home{
  height: 100%;
  .white-box{
    background-color: rgba(255, 255, 255, 0.349);
    display: flex;
    align-items: center;
    justify-content:center;
    flex-direction: column;
    padding:20px;
    height: 100px;
    width: 100px;
  }
  .left{
    position: absolute;
    left:10%;
    bottom:20%;
    font-size:2em;
  }
  .right{
    position: absolute;
    right:10%;
    bottom:20%;
    font-size:2em;
  }
}
#grass {
  position: absolute;
  bottom: 0;
  content: "";
  height: 150px;
  width: 100%;
}
</style>
<script>
import Nuage from "../components/Nuage.vue";
import Plante from "../components/Plante.vue";

export default {
  name: "home",
  components: {
    Nuage,
    Plante
  },
  
  computed: {
    status() {
      return this.$store.getters.status;
    },
    parameter() {
      return this.$store.getters.parameter;
    }
  }
};
</script>
