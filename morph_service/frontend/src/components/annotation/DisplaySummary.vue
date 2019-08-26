
<template>
  <div>
    <div class="title is-4 custom-text-centered">Annotations summary</div>
    <div class="columns is-multiline">
      <div
        v-for="element in summaryArray"
        :key="element.name"
        class="column is-one-third"
      >
        <ul class="menu-list">
          <li>
            <span class="title is-6">{{ element.name }}</span>
            <ul>
              <li
                v-for="(key, item) in element.summary"
                :key="element.name + item"
              >
                <span>{{ item }} : {{ key }}</span>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>

    <div
      class="buttons is-centered custom-spaced">
      <button
        class="button button-with-icon is-info is-medium more-spaced"
        @click="exportSummary"
      >
        <span>Summary</span>
        <i class="fas fa-download"/>
      </button>
      <button
        class="button button-with-icon is-info is-medium"
        @click="exportAnnotations"
      >
        <span>Annotated file(s)</span>
        <i class="fas fa-download"/>
      </button>
    </div>

  </div>
</template>


<script>
import FileSaver from 'file-saver';
import JSZip from 'jszip';
import { save, changeFileName } from '@/assets/utils';

export default {
  props: ['summaryArray', 'annotations'],
  methods: {
    exportSummary() {
      const tmp = {};
      this.summaryArray.forEach((elem) => {
        tmp[elem.name] = elem.summary;
      });
      save('summary.json', JSON.stringify(tmp));
    },
    exportAnnotations() {
      const keys = Object.keys(this.annotations);

      if (keys.length === 1) {
        save(this.filenameAnnotations(keys[0]), this.annotations[keys[0]]);
      } else {
        this.zipFiles();
      }
    },
    zipFiles() {
      const zip = new JSZip();
      // Generate a directory within the Zip file structure
      const folder = zip.folder('annotations');
      const keys = Object.keys(this.annotations);
      keys.forEach((name) => {
        // Add a file to the directory, in this case an image with data URI as contents
        folder.file(this.filenameAnnotations(name), this.annotations[name]);
      });

      // Generate the zip file asynchronously
      zip.generateAsync({ type: 'blob' })
      .then((content) => {
        // Force down of the Zip file
        FileSaver.saveAs(content, 'annotation_archive.zip');
      });
    },
    filenameAnnotations(name) {
      return changeFileName(name, 'annotated', 'asc');
    },
  },
};
</script>


<style scoped>
  .custom-spaced .more-spaced {
    margin-right: 100px;
  }
</style>
