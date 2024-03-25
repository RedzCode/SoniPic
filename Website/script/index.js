function displayPicture(event) {
    var image = document.getElementById('uploaded');
	image.src = URL.createObjectURL(event.target.files[0]);
}

