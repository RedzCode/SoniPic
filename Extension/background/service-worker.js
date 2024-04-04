let imagesUrl = [];

/**
 * Start the script when the page is loaded
 */
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (tab) {
    execScript(tab);
  } else {
    console.log("There are no active tabs");
  }
});

/**
 * Execute grabImages() function on a web page,
 * opened on specified tab and on all frames of this page
 * @param tab - A tab to execute script on
 */
function execScript(tab) {
  chrome.scripting
    .executeScript({
      target: { tabId: tab.id, allFrames: true },
      func: grabImages,
    })
    .then((injectionResults) => {
      for (const frameResult of injectionResults) {
        const { frameId, result } = frameResult;
        imagesUrl = result;
      }
    });
}

/**
 * Get all the url of frames of a page
 * @returns 
 */
function grabImages() {
  const images = document.querySelectorAll("img");

  let frames = Array.from(images).map((image) => image.src.replace(/'[^\x00-\x7F]'/gi, ''));
  if (!frames || !frames.length) {
    console.log("Could not retrieve images from this page");
    return;
  }
  frames = frames.filter(url => !(url.includes("svg") || url.includes("png")));
  return frames;
}

/**
 * Handle requests from the popup and send a response
 */
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "getNbImages") {
    sendResponse({ nb: imagesUrl.length });
  }
  if (request.getURL != null) sendResponse({ url: imagesUrl[request.getURL] });
});
