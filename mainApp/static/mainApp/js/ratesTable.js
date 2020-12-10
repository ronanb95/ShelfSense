fetch("http://localhost:8000/getrates")
.then(response => {
  return response.json();
})
.then(data => {
  DJANGO_STATIC_URL = '{{ mainApp/images/icon/market-value/trends-up-icon.png }}';
  contentString = "<tr class='heading-td'> <th>Barcode</th><th>Brand</th><th>Product</th><th>Rate</th></tr>";
  data.forEach(function(code){
    contentString += "<tr><td>" + code['barcode'] + "</td><td>" + code['brand'] + "</td><td>" + code['product'] + "</td><td>" + code['rate']  +"</td></tr>"
  })
  document.getElementById('conversionRates').innerHTML = contentString;
})