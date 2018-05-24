
<template>
  <div>
    <section class="hero is-info darker-blue">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            {{ title }}
          </h1>
          <h2
            v-if="subtitle"
            class="subtitle">
            {{ subtitle }}
          </h2>
          <slot/>
        </div>
      </div>
    </section>
  </div>
</template>


<script>
export default {
  name: 'TitleComponent',
  props: ['title', 'subtitle'],
};
</script>


<style scoped>
  .darker-blue {
    background-color: #1b84ca;
  }
  .title {
    margin-bottom: 10px;
  }
</style>
