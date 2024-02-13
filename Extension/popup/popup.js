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

function getURL(indexImage) {
  chrome.runtime.sendMessage(
    //Send message to the background script
    {
      getURL: indexImage,
    },
    async function (message) {
      //Get the answer of the background
      fetch("http://127.0.0.1:5000/post-sound/", {
        method: "POST",
        body: JSON.stringify({
          url: message.url
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
      .then((response) => response.json())
      .then((json) => encoded(json));
      
      function encoded(json){
        console.log(json);
        console.log(json.encodedSound);
      
      }
      /* var snd = new Audio("data:audio/x-wav;base64"+soundBase64);
      snd.play(); */
      
    }
  );
}

function handleActiveButton(button){
  activeButton = document.getElementsByClassName("active")[0]
  activeButton.classList.remove("active")

  button.classList.add("active")

  index = button.getAttribute('data-idBtt')

  getURL(index)
}

