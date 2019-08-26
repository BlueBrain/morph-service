import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
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
      component: () => import(/* webpackChunkName: "anotation" */ '@/pages/Annotation.vue'),
      name: 'Annotations',
    },
    {
      path: '/classifier',
      component: () => import(/* webpackChunkName: "tmd" */ '@/pages/Classifier.vue'),
      name: 'Topological Morphology Descriptor',
    },
    {
      path: '/converter',
      component: () => import(/* webpackChunkName: "converter" */ '@/pages/Converter.vue'),
      name: 'Morphology converter',
    },
    {
      path: '/validation',
      component: () => import(/* webpackChunkName: "validation" */ '@/pages/Validation.vue'),
      name: 'Validation',
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
