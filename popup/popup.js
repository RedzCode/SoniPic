document.addEventListener("DOMContentLoaded", function () {
  chrome.runtime.sendMessage(
    //Send message to the background script
    {
      action: "getNbImages",
    },
    function (response) {
      //Get the answer of the background
      console.log(response);
    }
  );
});
