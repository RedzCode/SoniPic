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

function closeModal(src){
  
  modal = document.getElementById("img-modal");
  modalImg = document.getElementById("img-show");
  modal.style.display = "none";
  modalImg.src = src;
}
