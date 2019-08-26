
<template>
  <div>
    <title-component title="Classification of neurons">
      <h2 class="subtitle">
        <span>Classification using</span>
        <a href="https://link.springer.com/article/10.1007/s12021-017-9341-1">
          Topological Morphology Descriptor (TMD)
          <i class="fas fa-external-link-alt"></i>
        </a>
      </h2>
    </title-component>

    <section class="section">
      <morph-filter @filtersOk="enableDD"/>

      <div class="spaced-bottom"/>

      <transition name="fade">
        <div v-if="!disableDragAndDrop">
          <div class="flex-centered">
            <span class="circle-number">4</span>
            <span class="subtitle is-3">Upload your morphologies:</span>
          </div>
          <drag-and-drop
            :extra-params="extraParams"
            :api-url="getApiUrlEnv() + '/classifier/api'"
            :extension="['.h5', '.swc']"
            @job-finished="classificationDone"
            @file-added="createLoadingSpin"
            @remove-all="removeResults"
          />
          <div class="columns is-multiline">
            <div
              v-for="chart in totalClassifications"
              :key="chart.name"
              class="column is-one-third"
            >
              <pie-chart
                v-if="chart.name"
                :classification="chart"
              />
              <pie-placeholder
                v-if="chart.placeholder"
                :name="chart.placeholder"
              />
            </div>
          </div>
          <div
            v-if="totalClassifications.length > 0 && totalClassifications[0].name"
            class="center-content"
            @click="saveResults"
          >
            <span class="button darker-blue is-medium">Export results as JSON</span>
          </div>
        </div>
      </transition>

    </section>
  </div>
</template>


<script>
import findIndex from 'lodash/findIndex';
import DragAndDrop from '@/components/DragAndDrop.vue';
import PieChart from '@/components/classifier/PieChart.vue';
import PiePlaceholder from '@/components/classifier/PiePlaceholder.vue';
import TitleComponent from '@/components/TitleComponent.vue';
import MorphFilter from '@/components/classifier/MorphFilter.vue';
import { save, sanitizeClassificationResults, getApiUrlEnv } from '@/assets/utils';

export default {
  name: 'Classifier',
  components: {
    DragAndDrop,
    TitleComponent,
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
    classificationDone(results) { // results = {fileSent, response}
      const classification = sanitizeClassificationResults(results.response);
      const index = findIndex(this.totalClassifications, { placeholder: results.fileSent.name });
      const graphData = { name: results.fileSent.name, result: classification };
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
      save('Classifications.json', this.totalClassifications);
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
