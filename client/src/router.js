import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'accueil',
      component: Home
    },
    {
      path: '/data',
      name: 'data',
      component: () => import('./views/Data.vue')
    },
    {
      path: '/parametre',
      name: 'parametre',
      component: () => import('./views/Parametre.vue')
    }
  ]
})
