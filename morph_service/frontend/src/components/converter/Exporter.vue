
<template>
  <div>

    <div class="custom-text-centered">
      <button
        class="button button-with-icon is-info is-medium is-centered"
        @click="exportConvertedMorphology"
      >
        <span>Download modified {{ morphologyWord }}</span>
        <i class="fas fa-download"/>
      </button>
    </div>

  </div>
</template>

<script>
import { save } from '@/assets/utils';
import FileSaver from 'file-saver';
import JSZip from 'jszip';

export default {
  props: ['convertedMorphology'],
  computed: {
    morphologyWord() {
      return (Object.keys(this.convertedMorphology).length > 1) ? 'morphologies' : 'morphology';
    },
  },
  methods: {
    exportConvertedMorphology() {
      const keys = Object.keys(this.convertedMorphology);

      if (keys.length === 1) {
        const info = this.convertedMorphology[keys[0]];
        save(info.convertedName, info.convertedFile);
      } else {
        this.zipFiles(keys);
      }
    },
    zipFiles(keys) {
      const zip = new JSZip();
      // Generate a directory within the Zip file structure
      const folder = zip.folder('ConvertedMorphology');
      keys.forEach((name) => {
        const info = this.convertedMorphology[name];
        // Add a file to the directory, in this case an image with data URI as contents
        folder.file(info.convertedName, info.convertedFile);
      });

      // Generate the zip file asynchronously
      zip.generateAsync({ type: 'blob' })
      .then((content) => {
        // Force down of the Zip file
        FileSaver.saveAs(content, 'converted_morphologies.zip');
      });
    },
  },
};
</script>

<style scoped>
  .custom-spaced .more-spaced {
    margin-right: 100px;
  }
</style>
