
import forEach from 'lodash/forEach';
import config from '@/assets/config.json';
import FileSaver from 'file-saver';

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
  let contentType = 'text/plain;charset=utf-8';
  let newFileContent = fileContent;
  if (name.endsWith('.json')) {
    contentType = 'text/json';
    newFileContent = JSON.stringify(fileContent, null, 2);
  }
  if (name.endsWith('.h5')) contentType = 'application/octet-stream';
  const blob = new Blob([newFileContent], { type: contentType });
  FileSaver.saveAs(blob, name);
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

function changeFileName(originalName, suffix, extension) {
  const extensionMatches = originalName.match(/\.([^.]*?)(?=\?|#|$)/);
  if (!extensionMatches || !extensionMatches.length) {
    throw new Error('file extension unknown');
  }
  return originalName.replace(extensionMatches[0], `-${suffix}.${extension}`);
}

export {
  changeFileName,
  isExtensionAllowed,
  getApiUrlEnv,
  isDev,
  sanitizeClassificationResults,
  save,
};
