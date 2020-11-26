//Form to set up the monitor of stock//
barcodes = []
products = []
locations = []

fetch("http://localhost:8000/selectLocation")
.then(response => {
  return response.json();
})
.then(data => {
  data.forEach(function(code){
    locations.push(code.pk)
  })
})


fetch("http://localhost:8000/all")
.then(response => {
	return response.json();
})
.then(data => {
	data.forEach(function(code){
		barcodes.push(code.pk)
	})
})

barcode1 = 0;
barcode2 = 0;
barcode3 = 0;
barcode4 = 0;
barcode5 = 0;


monitorForm = document.getElementById("monitorForm");

document.getElementById('locationCode').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      var entryLoc = document.getElementById('locationCode').value;
      if (locations.includes(entryLoc)){
        document.getElementById('barcode1').style.display="block";
        document.getElementById('startbtn').style.display="block";
      } else {
        alert("Error, this location is not recognised")
      }
    }
});

document.getElementById('barcode1').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      var entry = document.getElementById('barcode1').value;
      if (barcodes.includes(entry)){
      	document.getElementById('barcode2').style.display="block";
        barcode1 = entry;
      }
      else{
      	//document.getElementById('barcode1').value = "Error, there is no product registered with this barcode..."
        alert("product not in database, please register before monitoring")
      }
    }
});

document.getElementById('barcode2').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      document.getElementById('barcode3').style.display="block";
      entry = document.getElementById('barcode2').value;
      barcode2 = entry;
    }
});

document.getElementById('barcode3').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      document.getElementById('barcode4').style.display="block";
      entry = document.getElementById('barcode3').value;
      barcode3 = entry
    }
});

document.getElementById('barcode4').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      document.getElementById('barcode5').style.display="block";
      entry = document.getElementById('barcode4').value;
      barcode4 = entry
    }
});

document.getElementById('barcode5').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      entry = document.getElementById('barcode5').value;
      barcode5 = entry
    }
});

document.getElementById('startbtn').addEventListener('click', function(event){
  if(document.getElementById('barcode1').value === ""){
    alert("You must enter at least one product barcode")
  } else {
    fetch("http://localhost:8000/startMonitoringProcess/?barcode1="+barcode1+"&barcode2="+barcode2+"&barcode3="+barcode3+"&barcode4="+barcode4+"&barcode5="+barcode5)
    .then(response => {
      return response.json()
    })
    .then(data =>{
      document.getElementById('innerMessage').innerHTML = "<h1>" + data + "</h1>"
    })
  }
})




// fetch("http://localhost:8000/startMonitoringProcess/?barcode1="+barcode1+"&barcode2="+barcode2+"&barcode3="+barcode3+"&barcode4="+barcode4+"&barcode5="+barcode5)
// .then(response => {
//   return response.json()
// })
// .then(data =>{
//   console.log(data)
//})


//var input = document.createElement("input");
//input.setAttribute('type', 'text');
//monitorForm.append(input);