btn = document.getElementById('maintbtn');


btn.addEventListener('click', function(event){
	btn.style.display = 'none';
	fetch("http://localhost:8000/checkMaintenance")
	.then(response => {
		return response.json();
	})
	.then(data => {
		if (data == 1){
			document.getElementById('successinner').style.display = 'block';
		}
		else {
			document.getElementById('noSuccessinner').style.display = 'block';
		}
	})
});