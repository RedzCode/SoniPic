/**
 * Display the uploaded picture
 */
function displayPicture(event) {
    var image = document.getElementById('uploaded');
	image.src = URL.createObjectURL(event.target.files[0]);
    const audioElement1 = document.getElementById("audio-abs");
    const audioElement2 = document.getElementById("audio-cr");
    audioElement1.setAttribute("src", "");
    audioElement2 .setAttribute("src", "");
}

