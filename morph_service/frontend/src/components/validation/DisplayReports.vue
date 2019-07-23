
<template>
  <div>
    <div class="buttons is-centered custom-spaced">
      <button
        class="button button-with-icon is-info is-medium"
        @click="exportReports"
      >
        <span>Get report(s)</span>
        <i class="fas fa-download"/>
      </button>
    </div>

  </div>
</template>

<script>
import { save, changeFileName } from '@/assets/utils';
import FileSaver from 'file-saver';
import JSZip from 'jszip';
import get from 'lodash/get';

export default {
  props: ['reports'],
  methods: {
    exportReports() {
      const keys = Object.keys(this.reports);

      if (keys.length === 1) {
        const validationContent = get(this, `reports['${keys[0]}']`);
        save(this.filenameReports(keys[0]), validationContent);
      } else {
        this.zipFiles();
      }
    },
    zipFiles() {
      const zip = new JSZip();
      // Generate a directory within the Zip file structure
      const folder = zip.folder('reports');
      const keys = Object.keys(this.reports);
      keys.forEach((name) => {
        folder.file(this.filenameReports(name), JSON.stringify(this.reports[name], null, 2));
      });

      // Generate the zip file asynchronously
      zip.generateAsync({ type: 'blob' })
      .then((content) => {
        // Force download of the Zip file
        FileSaver.saveAs(content, 'reports.zip');
      });
    },
    filenameReports(name) {
      return changeFileName(name, 'report', 'json');
    },
  },
};
</script>

<style scoped>
  .custom-spaced .more-spaced {
    margin-right: 100px;
  }
</style>
