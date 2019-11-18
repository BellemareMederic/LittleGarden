<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Accueil</router-link>
      <router-link to="/data">Data</router-link>
      <router-link to="/parametre" class="gear"><img alt="Vue logo" src="./assets/icons/settings.svg"></router-link>
    </div>
    <router-view/>
  </div>
</template>
<script>
import "./assets/scss/style.scss";
export default {
  created() {
    setInterval(() => {
      this.$store.dispatch("fetchData");
    }, 1000);
  },
}
</script>