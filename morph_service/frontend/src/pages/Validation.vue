
<template>
  <div class="complete-page-height">
    <Title
      title="Validation Tool"
      subtitle="Validate your morphologies"
    />

    <section class="section">
      <div class="title is-4">Drop one or more files to get a validation JSON report for each of them</div>

      <div class="title is-5 custom-text-centered">Upload your morphologies</div>
      <DragAndDrop
        :api-url="getApiUrlEnv() + '/validation/api'"
        :extension="['.h5', '.swc', '.asc']"
        @jobFinished="validationDone"
        @fileAdded="createLoadingSpin"
        @removeAll="removeResults"
      />
      <div
        v-if="hasFiles"
        class="section"
      >
        <DisplayReports :reports="reports" />
      </div>
    </section>

    <generic-footer/>

  </div>
</template>


<script>
import DragAndDrop from '@/components/DragAndDrop.vue';
import DisplayReports from '@/components/validation/DisplayReports.vue';
import Title from '@/components/Title.vue';
import GenericFooter from '@/components/GenericFooter.vue';
import { getApiUrlEnv } from '@/assets/utils';
import swal from 'sweetalert2';

export default {
  name: 'Validation',
  components: {
    DragAndDrop,
    DisplayReports,
    Title,
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
