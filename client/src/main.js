import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { store } from './store/store'
import './registerServiceWorker'
import axios from 'axios'
import VueApexCharts from 'vue-apexcharts'

Vue.config.productionTip = false
Vue.component('apexchart', VueApexCharts)

const $axios = axios.create({
  baseURL: 'http://192.168.1.246:8080/api/v1/',
  timeout: 1000,
  headers: {'KEY':'1234'}
});
window.axios = $axios

Vue.filter('pourcent', function (value) {
  return Math.floor(value*100) + " %"
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
