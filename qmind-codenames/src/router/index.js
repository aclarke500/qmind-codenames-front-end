import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DesignBoardView from '@/views/DesignBoardView.vue'

const routes = [
  {
    path: '/:customBoard?:',
    name: 'home',
    component: HomeView
  },
  {
    path:'/design-board/',
    name:'design-board', 
    component: DesignBoardView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
