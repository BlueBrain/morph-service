
<template>
  <div class="morph-filters columns is-multiline">

    <transition name="fade">
      <section
        v-if="!classifier.isLoading"
        class="column is-narrow"
      >
        <div class="flex-centered">
          <span class="circle-number">1</span>
          <span class="subtitle is-3">Choose classifier:</span>
        </div>
        <model-select
          :options="classifier.list"
          :is-error="!classifier.selected"
          v-model="classifier.selected"
          placeholder="Classifier"
        />
      </section>
    </transition>

    <transition name="fade">
      <section
        v-if="classifier.selected"
        class="column is-narrow"
      >
        <div class="flex-centered">
          <span class="circle-number">2</span>
          <span
            class="subtitle is-3"
            title="Number of iterations"
          >
            # Iterations:
          </span>
        </div>
        <input
          v-model="numberOfTrials"
          :class="{'input-error': !isNumberOfTrialsCorrect}"
          class="input custom-height fluid dropdown"
          type="number"
          min="2"
          max="50"
          placeholder="Number of iterations"
        >
      </section>
    </transition>


    <transition name="fade">
      <section
        v-if="isNumberOfTrialsCorrect"
        class="column is-full">
        <div class="flex-centered">
          <span class="circle-number">3</span>
          <span
            class="subtitle is-3"
            title="Morphology type to compare (at least 2)">
            Choose morphology types to classify against:</span>
        </div>
        <MultiSelect
          :options="morphologyTypes.list"
          :selected-options="morphologyTypes.selected"
          :is-error="!morphologyTypes.selected || morphologyTypes.selected.length < 2"
          placeholder="Morphology types"
          @select="onSelect"/>
      </section>
    </transition>

  </div>
</template>


<script>
import map from 'lodash/map';
import filterConfig from '@/assets/filter-config.json';
import { MultiSelect, ModelSelect } from 'vue-search-select';

export default {
  name: 'MorphFilter',
  components: {
    MultiSelect,
    ModelSelect,
  },
  data() {
    return {
      classifier: {
        selected: null,
        list: filterConfig.classifiers,
        isLoading: true,
      },
      morphologyTypes: {
        list: filterConfig.groups,
        selected: null,
      },
      numberOfTrials: null,
    };
  },
  computed: {
    isNumberOfTrialsCorrect() {
      if (this.numberOfTrials > 1 && this.numberOfTrials < 51) {
        return true;
      }
      return false;
    },
  },
  watch: {
    classifier: {
      handler() {
        this.checkRequired();
      },
      deep: true,
    },
    morphologyTypes: {
      handler() {
        this.checkRequired();
      },
      deep: true,
    },
    numberOfTrials() {
      if (this.isNumberOfTrialsCorrect) {
        this.checkRequired();
      }
    },
  },
  mounted() {
    this.$set(this.classifier, 'isLoading', false);
  },
  methods: {
    checkRequired() {
      if (this.classifier.selected
          && this.isNumberOfTrialsCorrect
          && this.morphologyTypes.selected
          && this.morphologyTypes.selected.length > 1) {
        const params = {
          classifier: this.classifier.selected,
          morphtypes: JSON.stringify(map(this.morphologyTypes.selected, 'value')),
          trials: this.numberOfTrials,
        };
        this.$emit('filtersOk', params);
      }
    },
    onSelect(items) {
      this.$set(this.morphologyTypes, 'selected', items);
    },
  },
};
</script>


<style>
  .ui.fluid.dropdown input {
    font-size: 16px;
  }
  .custom-height {
    height: 43px;
  }
  .input-error {
    background: #FFF6F6;
    border-color: #E0B4B4;
    color: #9F3A38;
  }
  .kind-column-margin-bottom section:first-child {
    margin-bottom: 15px;
  }
</style>
