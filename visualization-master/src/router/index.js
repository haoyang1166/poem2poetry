import Vue from 'vue'
import Router from 'vue-router'
import Visualization from '@/views/visualization'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'visualization',
      component: Visualization
    }
  ]
})
