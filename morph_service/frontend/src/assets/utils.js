
import forEach from 'lodash/forEach';
import config from '@/assets/config.json';

function getMorphologyName(fullString) {
  return fullString.split('/').pop();
}

function sanitizeClassificationResults(classificationJson) {
  const obj = {};
  forEach(classificationJson, (value, key) => {
    const morphology = getMorphologyName(key);
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
  const blob = new Blob([stringFormat], { type: contentType });
  if (window.navigator.msSaveOrOpenBlob) {
    window.navigator.msSaveBlob(blob, name);
  } else {
    const elem = window.document.createElement('a');
    elem.href = window.URL.createObjectURL(blob);
    elem.download = name;
    document.body.appendChild(elem);
    elem.click();
    document.body.removeChild(elem);
  }
}

function isDev() {
  // if is dev remember to change the config.json with the endpoint url
  const { href } = window.location;
  const devHosts = ['localhost', '127.0.0.1', '0.0.0.0', '128.179'];
  return devHosts.some(devHost => href.includes(devHost));
}

function getApiUrlEnv() {
  if (isDev()) return config.devUrl;
  return config.apiUrl;
}

function isExtensionAllowed(fileName, extensions) {
  let isAllowed = false;
  const fileNameLower = fileName.toLowerCase();
  if (typeof extensions === 'string') {
    isAllowed = fileNameLower.endsWith(extensions);
    return !!isAllowed;
  }
  if (Array.isArray(extensions)) {
    isAllowed = extensions.find(ext => fileNameLower.endsWith(ext));
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
