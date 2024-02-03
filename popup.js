document.addEventListener("DOMContentLoaded", function () {
  chrome.runtime.sendMessage(
    {
      action: "getNbImages",
    },
    function (response) {
      console.log(response);
    }
  );
});
