var dropZone = document.getElementById('drag-and-drop-box');
var input = document.getElementById('fileControl');
var annotateButton = document.getElementById('annotate-btn');
var timeout = 120000; // 2 minutes


var canvas = document.querySelector('canvas');
var context = canvas.getContext('2d');
var count = document.getElementById('count');
/*          var destinationUrl = document.getElementById('url');*/
var list = [];
var totalSize = 0;
var totalProgress = 0;
var processedFiles = new Set();
var annotations = {};



function updateSummary(){
    annotateButton.disabled = (Object.keys(annotations).length < 1);
    var myNode = document.getElementById('summary-div');
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }

    var newSummaryDiv = document.createElement('div');
    for(var f in annotations){
        var summary = annotations[f].summary;
        var div = document.createElement('li');
        div.innerHTML = f;
        var l = document.createElement('ul');
        div.appendChild(l);
        for(var key in summary){
            var item = document.createElement('li');
            item.innerHTML += key + ': ' + summary[key];
            l.appendChild(item);
        }
        newSummaryDiv.appendChild(div);
        myNode.appendChild(newSummaryDiv);
    }

}

input.onchange = function () {
    processFiles(input.files);
};



$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


// Optional.   Show the copy icon when dragging over.  Seems to only work for chrome.
dropZone.addEventListener('dragover', function(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
});


// Get file data on drop
dropZone.addEventListener('drop', function(e) {
    e.stopPropagation();
    e.preventDefault();
    processFiles(e.dataTransfer.files);

});

// draw progress
function drawProgress(progress) {
    context.clearRect(0, 0, canvas.width, canvas.height); // clear context
    if(progress < 1){
        context.beginPath();
        context.strokeStyle = '#4B9500';
        context.fillStyle = '#4B9500';
        context.fillRect(0, 0, progress * 500, 20);
        context.closePath();
        // draw progress (as text)
        context.font = '16px Verdana';
        context.fillStyle = '#000';
        context.fillText('Progress: ' + Math.floor(progress*100) + '%', 50, 15);
    }
}
function exportSummary(){
    var tmp = {};
    for(var k in annotations){
        tmp[k] = annotations[k].summary;
    }
    offerDownload(JSON.stringify(tmp), "summary.json");
}


function offerDownload(object, filename){
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(object);
    var dlAnchorElem = document.getElementById('downloadAnchorElem');
    dlAnchorElem.setAttribute("href",     dataStr     );
    dlAnchorElem.setAttribute("download", filename);
    dlAnchorElem.click();
}

function zipFiles(files) {
    var zip = new JSZip();

    // Generate a directory within the Zip file structure
    var folder = zip.folder("annotations");

    for(var name in files) {
        // Add a file to the directory, in this case an image with data URI as contents
        folder.file(filenameAnnotations(name), files[name].file);
    }

    // Generate the zip file asynchronously
    zip.generateAsync({type:"blob"})
        .then(function(content) {
            // Force down of the Zip file
            saveAs(content, "archive.zip");
        });
}

function filenameAnnotations(name) {
    return name.replace(".asc", '-annotated.asc').replace(".ASC", '-annotated.asc');
}


function exportAnnotations(){
    var zip = new JSZip();
    var size = Object.keys(annotations).length;

    if(size == 1){
        offerDownload(annotations[0].file, filenameAnnotations(annotations[0]));
    } else {
        zipFiles(annotations);
    }

}

function resetAllFields(){
    annotations = {};
    input.value = "";
    processedFiles = new Set();
    updateSummary();
}


function processFiles(filelist) {
	  if (!filelist || !filelist.length || list.length) return;
	  totalSize = 0;
	  totalProgress = 0;
	  for (var i = 0; i < filelist.length && i < 5; i++) {
        if(!processedFiles.has(filelist[i].name)){
	          list.push(filelist[i]);
	          totalSize += filelist[i].size;
        }
	  }
	  uploadNext();
}

// on complete - start next file
function handleComplete(file) {
    totalProgress += file.size;
    drawProgress(totalProgress / totalSize);
    processedFiles.add(file.name);
    updateSummary();
    uploadNext();
}
// update progress
function handleProgress(event) {
    var progress = totalProgress + event.loaded;
    drawProgress(progress / totalSize);
}
// upload file
function uploadFile(file, status) {
    var formData = new FormData();
	  formData.append('myfile', file);

    $.ajax(
        {method: 'POST', url: "/annotations/api",
         cache: false,
         contentType: false,
         processData: false,
         data: formData,
         success: function(data){handleComplete(file);},
         error: function(data){
             alert("Something went wrong for file: "+file.name+"\n"+data.responseJSON.error);
             handleComplete(file);
         },
         success: function(data){
             annotations[file.name] = data;
             handleComplete(file);
         }
        });
}

// upload next file
function uploadNext() {
    if (list.length) {
        dropZone.className = 'uploading';
        var nextFile = list.shift();
        uploadFile(nextFile, status);
    } else {
        dropZone.className = '';
    }
}
