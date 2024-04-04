var currentBlob = ""
var pathAbstract = ""
var pathConcrete = ""
var currUrl = ""
var stateModal = "close"
var server = "https://sonipic-maefortune.pythonanywhere.com/"

/**
 * Start when the DOM load
 */
document.addEventListener("DOMContentLoaded", function () {
  var query = { active: true, currentWindow: true };
  chrome.tabs.query(query, checkPermissions);

  // Get the number of images from the background script
  chrome.runtime.sendMessage(
    {
      action: "getNbImages",
    },
    function (response) {
      if(response.nb == undefined || response.nb == 0){
        document.getElementById("loading-text").classList.remove("hidden");
      }else{
        document.getElementById("ct-slider").classList.remove("hidden");
        addElementsSlider(response.nb)
      }

    }
  );  

  // Set up buttons
  const btnPlayVisualize = document.getElementById("abstract");
  const btnPlayListen = document.getElementById('concrete');
  const btnSave = document.getElementById('save');
  const btnShow = document.getElementById('show');
  btnPlayVisualize.onclick = function() { playAudio(pathAbstract) };
  btnPlayListen.onclick = function() { playAudio(pathConcrete) };
  btnSave.onclick = function() { saveAudio() };
  btnShow.onclick = function() { handleModal() };

});

/**
 *  Check if the extension is allowed on the opened tab
 *  Do not work with every navigator version 
 * @param {*} tabs list of navigator tabs
 */
function checkPermissions(tabs) {
  var currentTab = tabs[0];
  chrome.permissions.contains({
    origins: [currentTab.url]
  }, function(result) {
    if (result) {
      console.log("permission");
    } else {
      console.log("no permission");
    }
  });
  
}

/**
 * Create as much buttons as the number of elements
 * @param {*} nbElements number of images in the page
 */
function addElementsSlider(nbElements) {
  
  for (let index = 0; index < nbElements; index++) {
    const button = document.createElement("button");

    const indexButton = document.createTextNode((index+1)+"");

    button.appendChild(indexButton);

    button.classList.add("item")

    button.setAttribute('data-idBtt' , index);      

    button.onclick = function() { handleActiveButton(this) };

    const container = document.getElementById("slider");
    container.appendChild(button)
    
  }
 
}

/**
 * Process the image and set up the sound
 * @param {*} indexImage of the selected image
 */
function processUrl(indexImage) {
  chrome.runtime.sendMessage(
    {
      getURL: indexImage,
    },
    async function (message) {
      //Get the answer of the background
      currUrl =  message.url.replace(/'[^\x00-\x7F]'/gi, '');
      paths = await postImage(currUrl)         
      pathAbstract = paths.pathAbstract
      pathConcrete = paths.pathConcrete
      
    }
  );
}

/**
 * Handle action of the selected image
 * @param {*} button 
 */
function handleActiveButton(button){
  currentBlob = ""
  pathAbstract = ""
  pathConcrete = ""
  currUrl = ""

  if(stateModal == "open")
    handleModal()

  const optionsAudio = document.getElementById("ct-audio")
  if(!optionsAudio.classList.contains("hidden")){
    optionsAudio.classList.add("hidden");
  }

  activeButton = document.getElementsByClassName("active")[0]
  if(activeButton != undefined )
    activeButton.classList.remove("active")

  button.classList.add("active")

  index = button.getAttribute('data-idBtt')

  options = document.getElementById("options")
  if( options != null || options.classList.contains("hidden")){
    options.style.visibility = "visible"
  }

  processUrl(index)
}

/**
 * Call flask server to process the image and save it on the serv
 * @param {*} url of the image
 * @returns the name of the wav file saved
 */
async function postImage(url){

 return fetch(server+"post-sound/", {
    method: "POST",
    body: JSON.stringify({
      url: url
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
  .then((response) => response.json())
  .then((json) => json);
  
}

/**
 * Call flask server to get the audio file and transform it as a blob data
 * Set up the received audio file into the audio element
 * @param {*} path name of the wav file
 */
async function getSound(path){
  fetch(server+"get-sound/"+path, {
    method: "GET",
  })
  .then((response) => response.blob())
  .then((blob) => {
    currentBlob = new Blob([blob], { type: 'audio/wav' });
    soundUrl = URL.createObjectURL(currentBlob);
    const audioElement = document.getElementById("audioPlayer");
    audioElement.setAttribute("src", soundUrl);
  })
  .catch(error => {
    console.error('Error fetching the audio file:', error);
  });
}

/**
 * Start the audio
 */
async function playAudio(path){
    currentBlob = ""
    await getSound(path);
    const options = document.getElementById("ct-audio")
    if(options.classList.contains("hidden")){
      options.classList.remove("hidden");
    }
    const audioElement = document.getElementById("audioPlayer");
    audioElement.addEventListener("loadedmetadata", function () {
    });

}

/**
 * Save the audio in the computer
 * @param {*} name 
 */
function saveAudio(name){
  if(currentBlob != ""){
    saveAs(currentBlob, name+'.wav');
  }
}

/**
 * Send a request to the page script to display or close the image modal 
 */
function handleModal(){
  var actionModal = "hideImage"
  if(stateModal == "close"){
    actionModal = "showImage"
  }

  chrome.tabs.query({ active: true, currentWindow: true}, function(activeTabs) {
    chrome.tabs.sendMessage(activeTabs[0].id, { action: actionModal,
    "url":currUrl }, 
    function (response) {
      if(response != undefined)
        stateModal = response.state
    });
  });
}