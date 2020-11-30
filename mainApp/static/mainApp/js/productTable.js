fetch("http://localhost:8000/default")
.then(response => {
  return response.json();
})
.then(data => {
  data.forEach(function(code){
    console.log(code)
  })
})

