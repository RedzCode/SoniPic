
/**
 * Get the uploaded image and get the paths 
 */
async function sonifyImage(){
    blobImg = document.getElementById("picture-input").files[0];
    if(blobImg){
        text = document.getElementById("waiting-sonify");
        text.innerText = "En attente ..."
        var formData = new FormData();
        formData.append('image', blobImg);
        paths = await postImage(formData)
    }
}

/**
 * Send the image to the server to generate audio files
 * And then get the audio files from the server
 * @param {*} data image uploaded
 */
async function postImage(data){
return fetch("http://127.0.0.1:5000/post-sound/", {
    method: "POST",
    body: data,
    })
    .then((response) => response.json())
    .then((json) => json).then(async (paths) => {
        pathVisualisation = paths.pathVisu
        pathListen = paths.pathListen
        await getSound(pathVisualisation, "audio-abs")
        await getSound(pathListen, "audio-cr")
    }).then(() => {    
        text = document.getElementById("waiting-sonify")
        text.innerText = ""
    });
    
}

/**
 * Get the audio file from the server 
 * and set the audio file to the audio player
 * @param {*} path of the audio file
 * @param {*} idPlayer selected audio player
 */
async function getSound(path, idPlayer){
    fetch("http://127.0.0.1:5000/get-sound/"+path, {
    method: "GET",
    })
    .then((response) => response.blob())
    .then((blob) => {
        blob = new Blob([blob], { type: 'audio/wav' });
        soundUrl = URL.createObjectURL(blob);
        const audioElement = document.getElementById(idPlayer);
        audioElement.setAttribute("src", soundUrl);
    })
    .catch(error => {
    console.error('Error fetching the audio file:', error);
    });
}