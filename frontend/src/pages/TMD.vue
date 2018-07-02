<template>
  <div>
    <Title title="Classification of neurons">
      <h2>
      <span>Classification using</span>
      <a href="https://link.springer.com/article/10.1007/s12021-017-9341-1">
      Topological Morphology Descriptor (TMD)
      <i class="fas fa-external-link-alt"></i>
      </a>
      </h2>
    </Title>
    <section class="section">
      <MorphFilter @filtersOk="enableDD"/>

      <div class="spaced-bottom"/>

      <transition name="fade">
        <div v-if="!disableDragAndDrop">
          <div class="flex-centered">
            <span class="circle-number">4</span>
            <span class="subtitle is-3">Upload your morphologies:</span>
          </div>
          <DragAndDrop
            :extra-params="extraParams"
            :api-url="getApiUrlEnv() + '/classifier/api'"
            :extension="['.h5', '.swc']"
            @jobFinished="classificationDone"
            @fileAdded="createLoadingSpin"
            @removeAll="removeResults"/>
          <div class="columns is-multiline">
            <div
              v-for="chart in totalClassifications"
              :key="chart.name"
              class="column is-one-third">
              <PieChart
                v-if="chart.name"
                :classification="chart"/>
              <PiePlaceholder
                v-if="chart.placeholder"
                :name="chart.placeholder"/>
            </div>
          </div>
          <div
            v-if="totalClassifications.length > 0 && totalClassifications[0].name"
            class="center-content"
            @click="saveResults">
            <span class="button darker-blue is-medium">Export results as JSON</span>
          </div>
        </div>
      </transition>

    </section>
  </div>
</template>

<script>
import DragAndDrop from '@/components/DragAndDrop.vue';
import PieChart from '@/components/classifier/PieChart.vue';
import PiePlaceholder from '@/components/classifier/PiePlaceholder.vue';
import Title from '@/components/Title.vue';
import MorphFilter from '@/components/classifier/MorphFilter.vue';
import findIndex from 'lodash/findIndex';
import { save, sanitizeClassificationResults, getApiUrlEnv } from '@/assets/utils';

export default {
  name: 'Tmd',
  components: {
    DragAndDrop,
    Title,
    PieChart,
    MorphFilter,
    PiePlaceholder,
  },
  data() {
    return {
      totalClassifications: [],
      disableDragAndDrop: true, // first select filters
      extraParams: {},
      getApiUrlEnv,
    };
  },
  methods: {
    classificationDone(results) { // results = {file, response}
      const classification = sanitizeClassificationResults(results.response);
      const index = findIndex(this.totalClassifications, { placeholder: results.file.name });
      const graphData = { name: results.file.name, result: classification };
      // replace placeholder for chart
      this.$set(this.totalClassifications, index, graphData);
    },
    enableDD(params) {
      this.extraParams = params;
      this.disableDragAndDrop = false;
    },
    createLoadingSpin(fileName) {
      this.totalClassifications.push({ placeholder: fileName });
    },
    saveResults() {
      save('Classifications.json', JSON.stringify(this.totalClassifications));
    },
    removeResults() {
      this.totalClassifications = [];
    },
  },
};
</script>

<style scoped>
  .spaced-bottom {
    margin-bottom: 40px;
  }
  .darker-blue {
    color: white;
  }
  .center-content {
    display: flex;
    justify-content: center;
  }
</style>
