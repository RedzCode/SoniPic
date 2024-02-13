document.addEventListener("DOMContentLoaded", function () {
  chrome.runtime.sendMessage(
    //Send message to the background script
    {
      action: "getNbImages",
    },
    function (response) {
      //Get the answer of the background
      console.log(response.nb);
      addElementsSlider(response.nb)
    }
  );

});

// create as much buttons as the number of images in the page
function addElementsSlider(nbElements) {
  
  for (let index = 1; index <= nbElements; index++) {
    const button = document.createElement("button");

    const indexButton = document.createTextNode(index+"");

    button.appendChild(indexButton);

    button.classList.add("item")

    if(index == 1){
      button.classList.add("active")
    }

    button.setAttribute('data-idBtt' , index);      

    button.onclick = function() { handleActiveButton(this) };

    const container = document.getElementById("slider");
    container.appendChild(button)
    
  }
 
}

function getURL() {
  chrome.runtime.sendMessage(
    //Send message to the background script
    {
      getURL: 10,
    },
    async function (message) {
      //Get the answer of the background
      //
      //console.log(response.url);
      let url = message.url.replaceAll('/', '.SN.')
      const resp = await fetch("http://127.0.0.1:5000/get-sound/"+url);
      const soundBase64 = await resp.json();
      console.log(JSON.stringify(soundBase64));
/*         var snd = new Audio("data:audio/x-wav;base64"+soundBase64);
      snd.play(); */
      
    }
  );
}

function handleActiveButton(element){
  activeButton = document.getElementsByClassName("active")[0]
  activeButton.classList.remove("active")

  element.classList.add("active")
}

