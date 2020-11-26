//Form to set up the monitor of stock//
barcodes = []
products = []


fetch("http://localhost:8000/all")
.then(response => {
	return response.json();
})
.then(data => {
	data.forEach(function(code){
		barcodes.push(code.pk)
	})
})


monitorForm = document.getElementById("monitorForm");

document.getElementById('locationCode').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      document.getElementById('barcode1').style.display="block";
    }
});

document.getElementById('barcode1').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      var entry = document.getElementById('barcode1').value;
      if (barcodes.includes(entry)){
      	document.getElementById('barcode2').style.display="block";
      }
      else{
      	entry.value = "Error, there is no product registered with this barcode..."
      }
    }
});

document.getElementById('barcode2').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      document.getElementById('barcode3').style.display="block";
    }
});

document.getElementById('barcode3').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      document.getElementById('barcode4').style.display="block";
    }
});

document.getElementById('barcode4').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      document.getElementById('barcode5').style.display="block";
    }
});



fetch("http://localhost:8000/routes/api/realtime/?stopid="+marker.id)


//var input = document.createElement("input");
//input.setAttribute('type', 'text');
//monitorForm.append(input);