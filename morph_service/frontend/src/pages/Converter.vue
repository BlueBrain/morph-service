
<template>
  <div class="complete-page-height">
    <title-component
      title="Converter"
      subtitle="Convert your morphologies to another format"
    />
    <section class="section">

      <div class="output-selector">
        <span class="circle-number">1</span>
        <span class="bold">Select output format:</span>
        <div class="control has-icons-left">
          <div class="select is-rounded is-small is-info">
            <select v-model="outputExtension">
              <option
                v-for="extension in extensions"
                :key="extension"
              >{{ extension }}</option>
            </select>
          </div>
          <span class="icon is-small is-left">
            <i class="far fa-file"/>
          </span>
        </div>
      </div>

      <transition name="fade">
        <div v-if="outputExtension">
          <div class="elements-margined">
            <span class="circle-number">2</span>
            <span class="title is-5">Upload your morphologies</span>
          </div>
          <drag-and-drop
            ref="dragAndDrop"
            :api-url="getApiUrlEnv() + '/converter/api'"
            :extension="extensions"
            :extra-params="extraParams"
            @job-finished="conversionDone"
            @file-added="createLoadingSpin"
            @remove-all="removeResults"
          />
          <div
            v-if="hasFiles"
            class="section"
          >
            <exporter :converted-morphology="convertedMorphology" />
          </div>
        </div>
      </transition>
    </section>

    <generic-footer/>

  </div>
</template>


<script>
import swal from 'sweetalert2';
import DragAndDrop from '@/components/DragAndDrop.vue';
import Exporter from '@/components/converter/Exporter.vue';
import GenericFooter from '@/components/GenericFooter.vue';
import TitleComponent from '@/components/TitleComponent.vue';
import { getApiUrlEnv } from '@/assets/utils';

export default {
  name: 'Converter',
  components: {
    DragAndDrop,
    Exporter,
    TitleComponent,
    GenericFooter,
  },
  data() {
    return {
      hasFiles: false,
      convertedMorphology: {},
      extensions: ['.h5', '.swc', '.asc'],
      outputExtension: null,
      getApiUrlEnv,
    };
  },
  computed: {
    extraParams() {
      return {
        output_extension: this.outputExtension,
        isBlob: this.outputExtension === '.h5',
      };
    },
  },
  watch: {
    outputExtension() {
      if (Object.keys(this.convertedMorphology).length > 0) {
        this.$refs.dragAndDrop.removeAll();
      }
    },
  },
  methods: {
    conversionDone(result) {
      // result {fileSent, response {file}}
      this.hasFiles = true;
      const converterResult = {
        convertedFile: result.response,
        convertedName: this.getConvertedName(result.fileSent.name, this.outputExtension),
      };
      this.$set(this.convertedMorphology, result.fileSent.name, converterResult);
      setTimeout(() => { swal.close(); }, 500);
    },
    getConvertedName(originalName, outputExtension) {
      return originalName.substr(0, originalName.lastIndexOf('.')) + outputExtension;
    },
    createLoadingSpin() {
      swal.enableLoading();
    },
    removeResults() {
      this.convertedMorphology = {};
      this.hasFiles = false;
    },
  },
};
</script>


<style scoped>
  .title-output {
    display: flex;
    justify-content: space-between;
  }
  .output-selector {
    display: flex;
    align-items: center;
  }
  .output-selector .bold {
    font-weight: 800;
    margin-right: 5px;
    font-size: 1.2em;
  }
  .elements-margined {
    margin: 5px 0;
  }
</style>
