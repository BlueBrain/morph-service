
<template>
  <div id="app">
    <nav
      class="navbar darker-blue"
      role="navigation"
      aria-label="main navigation">
      <div class="navbar-brand">
        <a
          role="button"
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
        >
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
        </a>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <router-link
            v-for="(value, key) in navItems"
            :key="key"
            :to="key"
            :class="{'is-active': isActive(key)}"
            class="navbar-item"
          >
            {{ value }}
          </router-link>
        </div>
      </div>

    </nav>
    <router-view/>
  </div>
</template>

<script>
import 'bulma/css/bulma.css';
import '@/assets/style.css';

export default {
  name: 'App',
  data() {
    return {
      navItems: {
        '/': 'MorphService',
        classifier: 'TMD Classifier',
        annotations: 'Annotations',
      },
    };
  },
  methods: {
    isActive(route) {
      return this.$route.fullPath.endsWith(route);
    },
  },
};
</script>


<style scoped>
  .darker-blue .navbar-menu a {
    color: #fff;
  }
  .darker-blue .navbar-menu a.is-active {
    background-color: #156ca5;
  }
  .darker-blue .navbar-menu a:hover {
    background-color: #156ca5;
  }
</style>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  /*height: 100vh;*/
}
</style>
