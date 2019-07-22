
<template>
  <footer class="custom-footer">
    <div class="content has-text-centered">
      <slot/>
      <p>Contact: <a href="mailto:bbp-ou-nse@epfl.ch">bbp-ou-nse@epfl.ch</a></p>
      <p>Version: {{ version }}</p>
    </div>
  </footer>
</template>


<script>
export default {
  name: 'GenericFooter',
  data() {
    return {
      version: process.env.VUE_APP_MORPH_SERVICE_VERSION,
    };
  },
};
</script>


<style>
.custom-footer {
  position: sticky;
  text-align: center;
  width: 100%;
  top: 95vh;
  font-size: 12px;
}
</style>
