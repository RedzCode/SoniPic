
async function sonifyImage(){
    blobImg = document.getElementById("picture-input").files[0];
    var formData = new FormData();
    // Append the file to FormData
    formData.append('image', blobImg);
    paths = await postImage(formData)
}

async function postImage(data){

return fetch("http://127.0.0.1:5000/post-sound/", {
    method: "POST",
    body: data,
    })
    .then((response) => response.json())
    .then((json) => json).then(async (paths) => {
        console.log(paths);
        pathVisualisation = paths.pathVisu
        pathListen = paths.pathListen
        await getSound(pathVisualisation, "audio-visu")
        await getSound(pathListen, "audio-listen")
    });
    
}

async function getSound(path, idPlayer){
    fetch("http://127.0.0.1:5000/get-sound/"+path, {
    method: "GET",
    })
    .then((response) => response.blob())
    .then((blob) => {
    // Create a new Blob object with the fetched data
    blob = new Blob([blob], { type: 'audio/wav' });
    soundUrl = URL.createObjectURL(blob);
    const audioElement = document.getElementById(idPlayer);
    audioElement.setAttribute("src", soundUrl);
    })
    .catch(error => {
    console.error('Error fetching the audio file:', error);
    });
}