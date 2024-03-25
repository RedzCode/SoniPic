

async function postImage(url){

return fetch("http://127.0.0.1:5000/post-sound/", {
    method: "POST",
    body: JSON.stringify({
        url: url
    }),
    headers: {
        "Content-type": "application/json; charset=UTF-8"
    }
    })
    .then((response) => response.json())
    .then((json) => json.path);
    
}

async function getSound(path){
    fetch("http://127.0.0.1:5000/get-sound/"+path, {
    method: "GET",
    })
    .then((response) => response.blob())
    .then((blob) => {
    // Create a new Blob object with the fetched data
    blob = new Blob([blob], { type: 'audio/wav' });
    soundUrl = URL.createObjectURL(blob);
    const audioElement = document.getElementById("audioPlayer");
    audioElement.setAttribute("src", soundUrl);
    })
    .catch(error => {
    console.error('Error fetching the audio file:', error);
    });
}