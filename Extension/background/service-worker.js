let imagesUrl = [];

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (tab) {
    execScript(tab);
  } else {
    alert("There are no active tabs");
  }
});

/**
 * Execute a grabImages() function on a web page,
 * opened on specified tab and on all frames of this page
 * @param tab - A tab to execute script on
 */
function execScript(tab) {
  // Execute a function on a page of the current browser tab
  // and process the result of execution
  chrome.scripting
    .executeScript({
      target: { tabId: tab.id, allFrames: true },
      func: grabImages,
    })
    .then((injectionResults) => {
      // console.log(injectionResults);
      for (const frameResult of injectionResults) {
        const { frameId, result } = frameResult;
        console.log(`Frame ${frameId} result:`, result);
        imagesUrl = result;
      }
    });
}

function grabImages() {
  const images = document.querySelectorAll("img");
  let frames = Array.from(images).map((image) => image.src);
  // If script execution failed on the remote end
  // and could not return results
  if (!frames || !frames.length) {
    alert("Could not retrieve images from specified page");
    return;
  }
  return frames;
}

function getImagesUrl() {
  console.log("show");
}

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "getNbImages") {
    sendResponse({ nb: imagesUrl.length });
  }
  if (request.getURL != null) sendResponse({ url: imagesUrl[request.getURL] });
});
