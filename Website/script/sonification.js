
async function sonifyImage(){
    blobImg = document.getElementById("picture-input").files[0];
    var formData = new FormData();
    // Append the file to FormData
    formData.append('image', blobImg);
/*     var reader = new FileReader
    reader.readAsDataURL(blobImg)
    var data = reader.result;
    data = data.split(",").pop(); */
    paths = await postImage(formData)
}

async function loadAudios(){
    img = document.getElementById("uploaded")
    await postImage(img)
}

async function postImage(data){

return fetch("http://127.0.0.1:5000/post-sound/", {
    method: "POST",
    body: data,
    })
    .then((response) => response.json())
    .then(async (json) => {    
        paths = json.path
        pathVisualisation = paths.pathVisu
        pathListen = paths.pathListen
        await getSound(pathVisualisation, "audio-visu")
        await getSound(pathListen, "audio-listen")
    }
);
    
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