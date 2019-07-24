
<template>
  <div class="pie-custom">
    <div
      id="canvas-holder"
      class="pie-container"
    >
      <canvas id="chart-area"/>
      <div
        id="chartjs-tooltip"
        class="chartjs-tooltip"
      >
        <table/>
      </div>
    </div>
  </div>
</template>


<script>
import Chart from 'chart.js';
import forEach from 'lodash/forEach';
import distinctColors from 'distinct-colors';

export default {
  name: 'PieChart',
  props: {
    classification: Object,
  },
  mounted() {
    this.chart = this.$el.querySelector('#chart-area');
    if (Object.keys(this.classification).length > 0) this.setup();
  },
  methods: {
    setup() {
      /* eslint-disable-next-line no-console */
      console.debug('Classification', this.classification);
      const amount = Object.keys(this.classification.result).length;
      const ctx = this.chart.getContext('2d');

      const palette = distinctColors({ count: amount });

      const morphologyData = {
        data: [],
        backgroundColor: [],
        labels: [],
      };
      let index = 0;
      forEach(this.classification.result, (value, key) => {
        morphologyData.data.push(value);
        morphologyData.backgroundColor.push(palette[index].hex());
        morphologyData.labels.push(key);
        index += 1;
      });

      const config = {
        type: 'pie',
        data: {
          datasets: [{
            data: morphologyData.data,
            backgroundColor: morphologyData.backgroundColor,
          }],
          labels: morphologyData.labels,
        },
        options: {
          responsive: true,
          tooltips: {
            enabled: false,
          },
          title: {
            display: true,
            text: this.classification.name,
            fontSize: 20,
          },
        },
      };

      Chart.defaults.global.tooltips.custom = this.customTooltip;
      // eslint-disable-next-line no-unused-vars
      const myChart = new Chart(ctx, config);
    },
    customTooltip(tooltip) {
      // Tooltip Element
      const tooltipEl = this.$el.querySelector('#chartjs-tooltip');

      // Hide if no tooltip
      if (tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
      }

      // Set caret Position
      tooltipEl.classList.remove('above', 'below', 'no-transform');
      if (tooltip.yAlign) {
        tooltipEl.classList.add(tooltip.yAlign);
      } else {
        tooltipEl.classList.add('no-transform');
      }

      function getBody(bodyItem) {
        return bodyItem.lines;
      }

      // Set Text
      if (tooltip.body) {
        const titleLines = tooltip.title || [];
        const bodyLines = tooltip.body.map(getBody);

        let innerHtml = '<thead>';

        titleLines.forEach((title) => {
          innerHtml += `<tr><th>${title}</th></tr>`;
        });
        innerHtml += '</thead><tbody>';

        bodyLines.forEach((body, i) => {
          const colors = tooltip.labelColors[i];
          let style = `background:${colors.backgroundColor}`;
          style += `; border-color:${colors.borderColor}`;
          style += '; border-width: 2px';
          const span = `<span class="chartjs-tooltip-key" style="${style}"></span>`;
          innerHtml += `<tr><td>${span}${body}%</td></tr>`;
        });
        innerHtml += '</tbody>';

        const tableRoot = tooltipEl.querySelector('table');
        tableRoot.innerHTML = innerHtml;
      }
      const positionY = this.chart.offsetTop;
      const positionX = this.chart.offsetLeft;

      // Display, position, and set styles for font
      tooltipEl.style.opacity = 1;
      tooltipEl.style.left = `${positionX + tooltip.caretX}px`;
      tooltipEl.style.top = `${positionY + tooltip.caretY}px`;
      tooltipEl.style.fontSize = tooltip.bodyFontSize;
      tooltipEl.style.padding = `${tooltip.yPadding}px ${tooltip.xPadding}px`;
    },
  },
};
</script>


<style>
  .pie-custom .pie-container {
    /*width: 50%;*/
    text-align: center;
  }
  .pie-custom .chartjs-tooltip {
    opacity: 1;
    position: absolute;
    background: rgba(0, 0, 0, .7);
    color: white;
    border-radius: 3px;
    -webkit-transition: all .1s ease;
    transition: all .1s ease;
    pointer-events: none;
    -webkit-transform: translate(-50%, 0);
    transform: translate(-50%, 0);
  }
  .pie-custom .chartjs-tooltip-key {
    display: inline-block;
    width: 10px;
    height: 10px;
    margin-right: 10px;
  }
</style>
