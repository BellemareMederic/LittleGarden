<template>
  <div class="home">
    <Nuage status="status.water"/>
    <svg id="grass" height="140" width="100%">
      <ellipse cx="50%" cy="100%" rx="60%" ry="75" style="fill:green;" />
    </svg>
    <Plante :status="status.water"/>
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
import Nuage from '../components/Nuage.vue'
import Plante from '../components/Plante.vue'

export default {
  name: 'home',
  components: {
    Nuage,
    Plante
  },
  data: function() {
    return {
      status: 'pas mis a jour'
    }
  },
  created(){
    this.fetchData();
  },
  methods: {
    fetchData: function() {
      this.status ={
        "light": {
          "isForceLight": false,
          "isOn": false
        },
        "serverTime": "Tue, 27 Aug 2019 18:45:02 GMT",
        "temperature": {
          "temperature": 0
        },
        "water": {
          "currentHumidity": 0.07,
          "isForceWatering": false,
          "isWatering": true
        }
      }
    }
  }
}
</script>
