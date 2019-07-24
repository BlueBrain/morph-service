
<template>
  <div class="pie-placeholder">
    <div>Classifying {{ name }}</div>
    <div>
      <i class="fas fa-sync spin"/>
    </div>
  </div>
</template>


<script>
export default {
  name: 'PiePlaceholder',
  props: ['name'],
};
</script>


<style scoped>
  .spin {
    font-size: 40px;
  }
  .pie-placeholder {
    min-height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
  }
</style>
