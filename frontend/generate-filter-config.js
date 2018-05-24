
const arrayOfMorphologies = [
  'L2_IPC', 'L2_TPC_A', 'L2_TPC_B',
  'L3_TPC_A', 'L3_TPC_B',
  'L4_SSC', 'L4_TPC', 'L4_UPC',
  'L5_TPC_A', 'L5_TPC_B', 'L5_TPC_C', 'L5_UPC',
  'L6_BPC', 'L6_HPC', 'L6_IPC', 'L6_TPC_A', 'L6_TPC_C', 'L6_UPC',
];
const outputPath = './src/assets/filter-config.json';
const classifiers = [
  'LinearDiscriminantAnalysis',
  'QuadraticDiscriminantAnalysis',
  'DecisionTreeClassifier',
];

const {writeFile, readFile} = require('fs');
const {startCase} = require('lodash');

function createFilters(data) {
  writeFile(outputPath, JSON.stringify(data), function(err) {
    if (err) throw err;
    console.log('Filters configuration was created');
  });
}

function generateGroups(sourceArray, prettify) {
  let totalGroups = [];
  sourceArray.map((value) => {
    // let layer = name.split('_')[0];
    // if (!obj[layer]) obj[layer] = [];
    // obj[layer].push(name);
    let name = value;
    if (prettify) name = startCase(value);
    totalGroups.push({value: value, text: name});
  });
  return totalGroups;
}

let prettify = true;
let processedClassifiers = generateGroups(classifiers, prettify);

let processedGroups = generateGroups(arrayOfMorphologies);

function createFiltersFn() {
  createFilters({
    classifiers: processedClassifiers,
    groups: processedGroups,
  });
};

function getAnnotationVersion() {
  readFile('../morph_service/version.py', 'utf8', function(err, data) {
    if (err) {
      return console.log(err);
    }
    let reg = /.*VERSION.+'(.*)'/;
    let found = data.match(reg);
    if (found.length > 1) console.log(found[1]);
  });
}

module.exports = {
  getAnnotationVersion,
  createFiltersFn,
};
