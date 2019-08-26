
<template>
  <div class="complete-page-height">
    <title-component
      title="Validation Tool"
      subtitle="Validate your morphologies"
    />

    <section class="section">
      <div class="title is-4">Drop one or more files to get a validation JSON report for each of them</div>

      <div class="title is-5 custom-text-centered">Upload your morphologies</div>
      <drag-and-drop
        :api-url="getApiUrlEnv() + '/validation/api'"
        :extension="['.h5', '.swc', '.asc']"
        @job-finished="validationDone"
        @file-added="createLoadingSpin"
        @remove-all="removeResults"
      />
      <div
        v-if="hasFiles"
        class="section"
      >
        <display-reports :reports="reports" />
      </div>
    </section>

    <generic-footer/>

  </div>
</template>


<script>
import swal from 'sweetalert2';
import DragAndDrop from '@/components/DragAndDrop.vue';
import DisplayReports from '@/components/validation/DisplayReports.vue';
import TitleComponent from '@/components/TitleComponent.vue';
import GenericFooter from '@/components/GenericFooter.vue';
import { getApiUrlEnv } from '@/assets/utils';

export default {
  name: 'Validation',
  components: {
    DragAndDrop,
    DisplayReports,
    TitleComponent,
    GenericFooter,
  },
  data() {
    return {
      hasFiles: false,
      reports: {},
      getApiUrlEnv,
    };
  },
  methods: {
    validationDone(result) {
      this.hasFiles = true;
      this.reports[result.fileSent.name] = result.response;
      setTimeout(() => {
        swal.close();
      }, 500);
    },
    createLoadingSpin() {
      swal.enableLoading();
    },
    removeResults() {
      this.reports = {};
      this.hasFiles = false;
    },
  },
};
</script>
