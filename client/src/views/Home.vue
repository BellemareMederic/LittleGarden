<template>
  <div class="home">
    <Nuage />
    <svg id="grass" height="140" width="100%">
      <ellipse cx="50%" cy="100%" rx="60%" ry="75" style="fill:green;" />
    </svg>
    <Plante />
      <div class="white-box left">
        <span v-if="status.water">{{ status.temperature.temperature }} °C</span>
        <span v-if="status.water">{{ status.water.currentHumidity | pourcent }}</span>
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
    display: flex;
    align-items: center;
    justify-content:center;
    font-size:4em;
    flex-direction: column;
    padding:20px;
    color:rgba(255, 255, 255, 0.5);
  }
  .left{
    position: absolute;
    left:10%;
    bottom:20%;
    min-width: 15;
    @media only screen and (max-width: 600px) {
      padding:10px;
      left:0;
    }
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
    Plante,
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
