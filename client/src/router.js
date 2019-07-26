import Vue from 'vue';
import Router from 'vue-router';
import Bot from './components/Bot.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Bot',
      component: Bot,
    },
  ],
});
