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

<style lang="scss">
  body{
    margin:0;
    overflow:hidden;
    font-family: "Manjari";
  }
  #app {
    color: #2c3e50;
    height: 100vh;
  }
  #nav {
    background-color:rgb(240, 240, 240);
    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    display: flex;
    height: 40px;
    justify-content: space-around;
    a {
      display: flex;
      align-items: center;
      justify-content: center;
      
      width: 100%;
      text-decoration: none;
      color:black;
      &.gear{
        width: 200px;
      }
      &.router-link-exact-active,&:hover{
        background-color:rgb(200, 200, 200);
      }
      img{
        height: 100%;
      }
      @media only screen and (max-width: 600px) {
        & {
          padding: 10px;
        }
      }
    }
  }
</style>

<script>
export default {
  created() {
    setInterval(() => {
      this.$store.dispatch("fetchData");
    }, 1000);
  },
}
</script>