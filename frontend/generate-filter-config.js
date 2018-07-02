
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

const { writeFile, readFile } = require('fs');
const { startCase } = require('lodash');

function createFilters(data) {
  writeFile(outputPath, JSON.stringify(data), (err) => {
    if (err) throw err;
  });
}

function generateGroups(sourceArray, prettify) {
  const totalGroups = [];
  sourceArray.forEach((value) => {
    let name = value;
    if (prettify) name = startCase(value);
    totalGroups.push({ value, text: name });
  });
  return totalGroups;
}

const prettify = true;
const processedClassifiers = generateGroups(classifiers, prettify);

const processedGroups = generateGroups(arrayOfMorphologies);

function createFiltersFn() {
  // this will create a JSON with with morphologies and labels
  createFilters({
    classifiers: processedClassifiers,
    groups: processedGroups,
  });
}

function getAnnotationVersion() {
  readFile('../morph_service/version.py', 'utf8', (err, data) => {
    if (err) throw err;
    const reg = /.*VERSION.+'(.*)'/;
    const found = data.match(reg);
    if (found.length > 1) console.log(found[1]);
  });
}

module.exports = {
  getAnnotationVersion,
  createFiltersFn,
};
