document.addEventListener("DOMContentLoaded", function () {
  chrome.runtime.sendMessage(
    //Send message to the background script
    {
      action: "getNbImages",
    },
    function (response) {
      //Get the answer of the background
      console.log(response.nb);
    }
  );

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
        const sound = await resp.json();
        console.log(sound);
        
      }
    );
  }

  document.getElementById("img-btt-0").addEventListener("click", getURL);
});
