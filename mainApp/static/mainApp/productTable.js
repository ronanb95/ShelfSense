fetch("http://localhost:8000/all")
.then(response => {
  return response.json();
})
.then(data => {
  data.forEach(function(code){
    console.log(data)
  })
})

function noLoader(){
    setTimeout(function () {
        document.getElementById('preloader').style.display = "none";
    }, 2500);
}

noLoader();