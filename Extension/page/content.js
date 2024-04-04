/**
 * Handle requests from the popup and send a response
 */
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if(request.action === 'showImage') {
    displayModal(request.url)
    sendResponse({ state: "open"});
  }
  if(request.action === 'hideImage') {
    closeModal(request.url)
    sendResponse({ state: "close"});
  }
});

/**
 * Insert modal in the code source of the page
 * Display the image on the page in a popup window (modal)
 * @param {*} src url image 
 */
function displayModal(src){

  const divModal = document.createElement("div");
  divModal.classList.add("modal")
  divModal.setAttribute("id","img-modal");

  const imgModal = document.createElement("img");
  imgModal.classList.add("modal-content")
  imgModal.setAttribute("id","img-show");
  divModal.appendChild(imgModal)

  document.body.appendChild(divModal); 
  
  modal = document.getElementById("img-modal");
  modalImg = document.getElementById("img-show");
  modal.style.display = "block";
  modalImg.src = src;

  modalImg.onclick = function() { 
    modal.style.display = "none";
  }
}

/**
 * Close the opened modal
 * @param {*} src url image
 */
function closeModal(src){
  
  modal = document.getElementById("img-modal");
  modalImg = document.getElementById("img-show");
  modal.style.display = "none";
  modalImg.src = src;
}
