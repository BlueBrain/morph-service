
<template>
  <div>
    <vue-dropzone
      id="dropzone"
      ref="vueDropzoneComponent"
      :options="dropzoneOptions"
      class="customized-color"
      @vdropzone-success="complete"
      @vdropzone-file-added="changeFlagHasFile"
      @vdropzone-sending="fileAdded"
      @vdropzone-error="errorHandler"
      @vdropzone-canceled="errorHandler"
    />
    <div class="buttons has-addons is-centered">
      <button
        v-if="hasFiles"
        class="button button-with-icon is-rounded is-info is-outlined"
        @click="removeAll"
      >
        <span>Clean All</span>
        <i class="far fa-trash-alt"/>
      </button>
    </div>

  </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';
import { isExtensionAllowed } from '@/assets/utils';
import swal from 'sweetalert2';

export default {
  name: 'DragAndDrop',
  components: {
    vueDropzone: vue2Dropzone,
  },
  props: ['extraParams', 'apiUrl', 'extension'],
  data() {
    return {
      dropzoneOptions: {
        url: this.apiUrl,
        autoDiscover: false,
        createImageThumbnails: false,
        timeout: 300000, // 5 minutes
        parallelUploads: 1,
        previewTemplate: `
          <div class="uploaded-image column">
            <span data-dz-name></span>
            <strong class="dz-size" data-dz-size></strong>
            <div class="dz-error-message" data-dz-errormessage></div>
            <div class="dz-progress">
              <span class="dz-upload" data-dz-uploadprogress></span>
            </div>
          </div>`,
        dictDefaultMessage: `
          <i class="fas fa-cloud-upload-alt dd-title"></i>
          <span class="dd-subtitle">(click to select or drag and drop)</span>`,
      },
      hasFiles: false,
    };
  },
  watch: {
    extraParams() {
      this.setParamsRequest();
    },
  },
  mounted() {
    this.setParamsRequest();
  },
  methods: {
    setParamsRequest() {
      if (!this.extraParams) return;
      this.$refs.vueDropzoneComponent.setOption('params', this.extraParams);
      if (this.extraParams.isBlob) {
        this.$refs.vueDropzoneComponent.setOption('headers', { Accept: 'application/octet-stream' });
      }
    },
    complete(file, response) {
      /* eslint-disable-next-line no-console */
      console.debug('Webservice completed', file.name);
      const finalResponse = this.extraParams.isBlob ? file.xhr.response : response;
      this.$emit('jobFinished', { fileSent: file, response: finalResponse });
    },
    fileAdded(file, xhr) {
      /* eslint-disable no-console,no-param-reassign */
      console.debug('File added', file.status);

      if (this.extraParams.isBlob) {
        console.debug('File is BLOB');
        // overwrite the function (dropzone does not support binary response)
        xhr.responseType = 'blob';
      }
      this.$emit('fileAdded', file.name);
      /* eslint-enable no-console no-param-reassign */
    },
    changeFlagHasFile(file) {
      // this will happen always even if the file has error
      if (!isExtensionAllowed(file.name, this.extension || '')) {
        swal({
          type: 'error',
          title: 'The file format is not supported',
          text: `Please provide a file with ${this.extension} extension`,
        });
        this.$refs.vueDropzoneComponent.removeFile(file);
        return;
      }
      this.hasFiles = true;
    },
    errorHandler(file, message) {
      /*  Clean All cancels the requests and that produces
          some error but it is actually fine */
      if (file.status === 'canceled') return;

      swal({
        type: 'error',
        title: 'There was an error',
        text: message,
      });
      throw Error(message);
    },
    removeAll() {
      this.$refs.vueDropzoneComponent.removeAllFiles(true);
      this.hasFiles = false;
      this.$emit('removeAll');
    },
  },
};
</script>

<style scoped>
.customized-color {
  background-color: #0239ff0d;
  border-style: dashed;
  border-width: 2px;
}
</style>

<style>
.dd-subtitle {
  color: #9596af;
  display: block;
  font-size: 18px;
}
.customized-color .dd-title {
  font-size: 40px;
}
.uploaded-image {
  display: inline-block;
  vertical-align: top;
}
.dz-progress {
  height: 5px;
  display: block;
}
.dz-error-message {
  color: red;
}
.dz-upload {
  display: block;
  height: 100%;
  background: #b7e2b7;
  width: 0;
}
</style>
