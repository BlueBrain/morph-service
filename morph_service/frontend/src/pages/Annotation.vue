
<template>
  <div class="complete-page-height">
    <title-component
      title="Annotation Tool"
      subtitle="Annotate your morphologies"
    />

    <section class="section">
      <div class="title is-4">Choose a Neurolucida file and then you will be able to download a copy of this file(s) with the annotations appended at the end</div>
      <div class="inline">
        <span>There are 5 types of supported annotations:</span>
        <div class="tags">
          <span
            class="tag is-light is-medium tooltip"
            data-tooltip="Check if there are jumps (large movements along the z axis)">Z-jump</span>
          <span
            class="tag is-light is-medium tooltip"
            data-tooltip="Check if neurites have a narrow start">Narrow start</span>
          <span
            class="tag is-light is-medium tooltip"
            data-tooltip="Check if leaf points are too large">Fat end</span>
          <span
            class="tag is-light is-medium tooltip"
            data-tooltip="Check if the neuron has dangling neurites">Dangling branch</span>
          <span
            class="tag is-light is-medium tooltip"
            data-tooltip="Check if the neuron has sections with only one child section">Single child</span>
          <span
            class="tag is-light is-medium tooltip"
            data-tooltip="Check if the neuron has sections with more than two child sections">Multifurcation</span>
        </div>
      </div>

      <div class="title is-5 custom-text-centered">Upload your morphologies</div>
      <drag-and-drop
        :api-url="getApiUrlEnv() + '/annotations/api'"
        extension=".asc"
        @job-finished="annotationDone"
        @file-added="createLoadingSpin"
        @remove-all="removeResults"
      />
      <div
        v-if="hasFiles"
        class="section"
      >
        <display-summary
          :summary-array="summary"
          :annotations="annotations"
        />
      </div>
    </section>

    <generic-footer>
      <p>For more information about the annotation computation see: <a href="https://github.com/BlueBrain/NeuroM/blob/master/neurom/check/neuron_checks.py">https://github.com/BlueBrain/NeuroM/blob/master/neurom/check/neuron_checks.py</a></p>
    </generic-footer>

  </div>
</template>


<script>
import swal from 'sweetalert2';
import DragAndDrop from '@/components/DragAndDrop.vue';
import DisplaySummary from '@/components/annotation/DisplaySummary.vue';
import TitleComponent from '@/components/TitleComponent.vue';
import GenericFooter from '@/components/GenericFooter.vue';
import { getApiUrlEnv } from '@/assets/utils';

export default {
  name: 'Annotation',
  components: {
    DragAndDrop,
    DisplaySummary,
    TitleComponent,
    GenericFooter,
  },
  data() {
    return {
      hasFiles: false,
      annotations: {},
      summary: [],
      getApiUrlEnv,
    };
  },
  methods: {
    annotationDone(result) {
      // result {file, response {file, summary}}
      this.hasFiles = true;
      this.summary.push({
        name: result.fileSent.name,
        summary: result.response.summary,
      });
      this.annotations[result.fileSent.name] = result.response.file;
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


<style scoped>
  .inline {
    display: inline-flex;
    align-items: center;
  }
</style>
