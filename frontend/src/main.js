import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';
import Annotation from '@/pages/Annotation.vue';
import TMD from '@/pages/TMD.vue';
import Home from '@/pages/Home.vue';

Vue.use(VueRouter);

Vue.config.productionTip = false;

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Home,
      name: 'MorphoTools',
    },
    {
      path: '/annotations',
      component: Annotation,
      name: 'Annotations',
    },
    {
      path: '/classifier',
      component: TMD,
      name: 'Topological Morphology Descriptor',
    },
  ],
});

router.afterEach((to) => {
  document.title = to.name;
});

new Vue({
  render: h => h(App),
  router,
}).$mount('#app');
