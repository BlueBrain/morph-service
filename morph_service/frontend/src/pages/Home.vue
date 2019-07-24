
<template>
  <div>
    <title-component title="Select one tool"/>
    <div class="section custom-card-container">
      <router-link
        class="card custom-card"
        to="classifier"
      >
        <div class="subtitle">Classify morphologies using Topological Morphology Descriptor (TMD)</div>
      </router-link>
      <router-link
        class="card custom-card"
        to="annotations"
      >
        <div class="subtitle">Annotate morphologies</div>
      </router-link>
      <router-link
        class="card custom-card"
        to="converter"
      >
        <div class="subtitle">Convert morphologies</div>
      </router-link>
      <router-link
        class="card custom-card"
        to="validation"
      >
        <div class="subtitle">Validate morphologies</div>
      </router-link>
    </div>
  </div>
</template>


<script>
import TitleComponent from '@/components/TitleComponent.vue';

export default {
  name: 'Home',
  components: {
    TitleComponent,
  },
};
</script>


<style scoped>
  .custom-card {
    background-color: #0239ff0d;
    margin: 20px;
    text-align: center;
    padding: 50px;
  }
  .custom-card-container {
    display: flex;
    flex-direction: column;
    max-width: 1100px;
    margin: 0 auto;
  }
</style>
