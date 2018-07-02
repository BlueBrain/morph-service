<template>
  <div class="complete-page-height">
    <Title
      title="Annotation Tool"
      subtitle="Annotate your morphologies"/>
    <section class="section">
      <div class="title is-3">Choose a Neurolucida file and then you will be able to download a copy of this file(s) with the annotations appended at the end</div>
      <div>
        <span>There are 5 types of supported annotations:</span>
        <span
          class="tag is-light is-medium tooltip is-tooltip-multiline"
          data-tooltip="Check if there are jumps (large movements along the z axis)">Z-jump</span>
        <span
          class="tag is-light is-medium tooltip is-tooltip-multiline"
          data-tooltip="Check if neurites have a narrow start">Narrow start</span>
        <span
          class="tag is-light is-medium tooltip is-tooltip-multiline"
          data-tooltip="Check if leaf points are too large">Fat end</span>
        <span
          class="tag is-light is-medium tooltip is-tooltip-multiline"
          data-tooltip="Check if the neuron has dangling neurites">Dangling branch</span>
        <span
          class="tag is-light is-medium tooltip is-tooltip-multiline"
          data-tooltip="Check if the neuron has sections with only one child section">Single child</span>
      </div>
    </section>
    <div class="title is-4 custom-text-centered">Upload your morphologies</div>
    <DragAndDrop
      :api-url="getApiUrlEnv() + '/annotations/api'"
      extension=".asc"
      @jobFinished="annotationDone"
      @fileAdded="createLoadingSpin"
      @removeAll="removeResults"/>
    <div
      v-if="hasFiles"
      class="section">
      <DisplaySummary
        :summary-array="summary"
        :annotations="annotations"/>
    </div>

    <footer class="custom-footer">
      <div class="content has-text-centered">
        <p>For more information about the annotation computation see: <a href="https://github.com/BlueBrain/NeuroM/blob/master/neurom/check/neuron_checks.py">https://github.com/BlueBrain/NeuroM/blob/master/neurom/check/neuron_checks.py</a></p>
        <p>Contact: <a href="mailto:bbp-ou-nse@epfl.ch">bbp-ou-nse@epfl.ch</a></p>
        <p>Version: {{ version }}</p>
      </div>
    </footer>

  </div>
</template>

<script>
import 'bulma-extensions/bulma-tooltip/dist/bulma-tooltip.min.css';
import 'bulma-extensions/bulma-divider/dist/bulma-divider.min.css';
import DragAndDrop from '@/components/DragAndDrop.vue';
import DisplaySummary from '@/components/annotation/DisplaySummary.vue';
import Title from '@/components/Title.vue';
import { getApiUrlEnv } from '@/assets/utils';
import swal from 'sweetalert2';

export default {
  name: 'Annotation',
  components: {
    DragAndDrop,
    DisplaySummary,
    Title,
  },
  data() {
    return {
      hasFiles: false,
      annotations: {},
      summary: [],
      getApiUrlEnv,
      version: process.env.VUE_APP_ANNOTATION_VERSION,
    };
  },
  methods: {
    annotationDone(result) {
      // result {file, response {file, summary}}
      this.hasFiles = true;
      this.summary.push({
        name: result.file.name,
        summary: result.response.summary,
      });
      this.annotations[result.file.name] = result.response.file;
      setTimeout(() => {
        swal.close();
      }, 500);
    },
    createLoadingSpin() {
      swal.enableLoading();
    },
    removeResults() {
      this.annotations = {};
      this.summary = [];
      this.hasFiles = false;
    },
  },
};
</script>

<style>
.tooltip.is-tooltip-multiline::before {
  font-size: 16px;
  min-width: 150px;
}
.custom-footer {
  position: sticky;
  text-align: center;
  width: 100%;
  top: 90vh;
  font-size: 12px;
}
</style>
