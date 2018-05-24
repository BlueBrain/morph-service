
import {forEach} from 'lodash';
import config from '@/assets/config.json';

function getMorphologyName(fullString) {
  return fullString.split('/').pop();
}

function sanitizeClassificationResults(classificationJson) {
  let obj = {};
  forEach(classificationJson, (value, key) => {
    let morphology = getMorphologyName(key);
    obj[morphology] = value * 100;
  });
  return obj;
}

function save(name, fileContent) {
  // saves the content to a file. Extension is required.
  let contentType = 'text/plain';
  if (name.endsWith('.json')) contentType = 'text/json';
  let stringFormat = null;
  if (fileContent && Array.isArray(fileContent)) {
    stringFormat = fileContent.join('\n');
  } else {
    stringFormat = fileContent;
  }
  let blob = new Blob([stringFormat], {type: contentType});
  if (window.navigator.msSaveOrOpenBlob) {
    window.navigator.msSaveBlob(blob, name);
  } else {
    let elem = window.document.createElement('a');
    elem.href = window.URL.createObjectURL(blob);
    elem.download = name;
    document.body.appendChild(elem);
    elem.click();
    document.body.removeChild(elem);
  }
}

function getApiUrlEnv() {
  if (isDev()) return config.devUrl;
  return config.apiUrl;
}

function isDev() {
  return window.location.href.includes('localhost') ||
    window.location.href.includes('127.0.0.1') ||
    window.location.href.includes('0.0.0.0');
}

function isExtensionAllowed(fileName, extensions) {
  let isAllowed = false;
  if (typeof extensions === 'string') {
    isAllowed = fileName.endsWith(extensions);
    return !!isAllowed;
  }
  if (Array.isArray(extensions)) {
    isAllowed = extensions.find((ext) => fileName.endsWith(ext));
    return !!isAllowed;
  }
  return !!isAllowed;
}

export {
  isExtensionAllowed,
  getApiUrlEnv,
  isDev,
  sanitizeClassificationResults,
  save,
};
