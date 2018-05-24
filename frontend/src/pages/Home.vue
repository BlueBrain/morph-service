<template>
  <div>
    <Title title="Select one tool"/>
    <div class="section custom-card-container">
      <router-link
        class="card custom-card"
        to="/tmd">
        <div class="title">Classify morphologies using Topological Morphology Descriptor (TMD)</div>
      </router-link>
      <router-link
        class="card custom-card"
        to="/annotation">
        <div class="title">Annotate morphologies</div>
      </router-link>
    </div>
  </div>
</template>

<script>
import Title from '@/components/Title';
export default {
  name: 'Home',
  components: {
    Title,
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
  }
</style>
