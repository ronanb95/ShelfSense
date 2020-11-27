/////////////Form to set up the monitor of stock///////////
barcodes = []
products = []
locations = []

//Get current locations to check user location entry is correct
fetch("http://localhost:8000/selectLocation")
.then(response => {
  return response.json();
})
.then(data => {
  data.forEach(function(code){
    locations.push(code.pk)
  })
})

//Get current barcodes to check user barcode entry is correct
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

b1 = document.getElementById('barcode1')
b2 = document.getElementById('barcode2')
b3 = document.getElementById('barcode3')
b4 = document.getElementById('barcode4')
b5 = document.getElementById('barcode5')

locerror = document.getElementById('locerror')
error1 = document.getElementById('error1')
error2 = document.getElementById('error2')
error3 = document.getElementById('error3')
error4 = document.getElementById('error4')
error5 = document.getElementById('error5')

monitorForm = document.getElementById("monitorForm");

//Check location entry and display rest of form
document.getElementById('locationCode').addEventListener('keyup', function(event) {
    if (event.code === 'Enter') {
      var entryLoc = document.getElementById('locationCode').value;
      if (locations.includes(entryLoc)){
        locerror.style.display = "none";
        document.getElementById('barcode1').style.display="block";
        document.getElementById('startbtn').style.display="block";
        document.getElementById('addbtn').style.display="block";
      } else {
        locerror.style.display = "block";
        document.getElementById('locationCode').value = ""
      }
    }
});

//Check each barcode entry when adding more products
document.getElementById('addbtn').addEventListener('click', function(event){
  if(b1.value !== ""){
    if(barcodes.includes(b1.value)){
      b2.style.display = "block";
      error1.style.display = "none";
    } else {
      error1.style.display = "block";
      b1.value = ""
    }
  }
  if(b2.value !== ""){
    if(barcodes.includes(b2.value)){
      b3.style.display = "block";
      error2.style.display = "none";
    } else {
      error2.style.display = "block";
      b2.value = ""
    }
  }
  if(b3.value !== ""){
    if(barcodes.includes(b3.value)){
      b4.style.display = "block";
      error3.style.display = "none";
    } else {
      error3.style.display = "block";
      b3.value = ""
    }
  }
  if(b4.value !== ""){
    if(barcodes.includes(b4.value)){
      b5.style.display = "block";
      error4.style.display = "none";
      document.getElementById('addbtn').style.display = "none";
    } else {
      error4.style.display = "block";
      b4.value = ""
    }
  }
});


//Check first barcode entered and final barcode entry (others checked above) is fine and pass information to backend to start monitoring
document.getElementById('startbtn').addEventListener('click', function(event){
  if (b1.value == ""){
    alert("Please enter at least one barcode to start monitoring")
  } else if (b5.value != "" && barcodes.includes(b5.value) == false){
    error5.style.display = "block";
    b5.value = "";
  } else {
    if (b1.value != "" && barcodes.includes(b1.value) == false){
      b1.value = ""
      error1.style.display = "block";
    } else if (b2.value != "" && barcodes.includes(b2.value) == false){
      b2.value = ""
      error2.style.display = "block";
    } else if (b3.value != "" && barcodes.includes(b3.value) == false){
      b3.value = ""
      error3.style.display = "block";
    } else if (b4.value != "" && barcodes.includes(b4.value) == false){
      b4.value = ""
      error4.style.display = "block";
    } else {
      barcode1 = b1.value;
      barcode2 = b2.value;
      barcode3 = b3.value;
      barcode4 = b4.value;
      barcode5 = b5.value;
      error1.style.display = "none";
      error2.style.display = "none";
      error3.style.display = "none";
      error4.style.display = "none";
      error5.style.display = "none";
      //Actual passing of all the information
      fetch("http://localhost:8000/startMonitoringProcess/?barcode1="+barcode1+"&barcode2="+barcode2+"&barcode3="+barcode3+"&barcode4="+barcode4+"&barcode5="+barcode5)
      .then(response => {
        return response.json()
      })
      .then(data =>{
        monitorForm.innerHTML = "<h1>" + data + "</h1>";
        addbtn.style.display = "none";
        startbtn.style.display = "none";
      })
    }
  }
});



// document.getElementById('barcode1').addEventListener('keyup', function(event) {
//     if (event.code === 'Enter') {
//       var entry = document.getElementById('barcode1').value;
//       if (barcodes.includes(entry)){
//       	document.getElementById('barcode2').style.display="block";
//         barcode1 = entry;
//       }
//       else{
//       	//document.getElementById('barcode1').value = "Error, there is no product registered with this barcode..."
//         alert("product not in database, please register before monitoring")
//       }
//     }
// });

// document.getElementById('barcode2').addEventListener('keyup', function(event) {
//     if (event.code === 'Enter') {
//       document.getElementById('barcode3').style.display="block";
//       entry = document.getElementById('barcode2').value;
//       barcode2 = entry;
//     }
// });

// document.getElementById('barcode3').addEventListener('keyup', function(event) {
//     if (event.code === 'Enter') {
//       document.getElementById('barcode4').style.display="block";
//       entry = document.getElementById('barcode3').value;
//       barcode3 = entry
//     }
// });

// document.getElementById('barcode4').addEventListener('keyup', function(event) {
//     if (event.code === 'Enter') {
//       document.getElementById('barcode5').style.display="block";
//       entry = document.getElementById('barcode4').value;
//       barcode4 = entry
//     }
// });

// document.getElementById('barcode5').addEventListener('keyup', function(event) {
//     if (event.code === 'Enter') {
//       entry = document.getElementById('barcode5').value;
//       barcode5 = entry
//     }
// });

// document.getElementById('startbtn').addEventListener('click', function(event){
//   if(document.getElementById('barcode1').value === ""){
//     alert("You must enter at least one product barcode")
//   } else {
//     fetch("http://localhost:8000/startMonitoringProcess/?barcode1="+barcode1+"&barcode2="+barcode2+"&barcode3="+barcode3+"&barcode4="+barcode4+"&barcode5="+barcode5)
//     .then(response => {
//       return response.json()
//     })
//     .then(data =>{
//       document.getElementById('innerMessage').innerHTML = "<h1>" + data + "</h1>"
//     })
//   }
// })





fetch("http://localhost:8000/startMonitoringProcess/?barcode1="+barcode1+"&barcode2="+barcode2+"&barcode3="+barcode3+"&barcode4="+barcode4+"&barcode5="+barcode5)
.then(response => {
  return response.json()
})
.then(data =>{
  console.log(data)
})


