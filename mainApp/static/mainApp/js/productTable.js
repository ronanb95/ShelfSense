$(document).ready(function() {
    var t = $('#dataTable2').DataTable();
    var counter = 1;
    fetch("http://localhost:8000/default")
	.then(response => {
	  return response.json();
	})
	.then(data => {
		unseenProducts = []
	  data.forEach(function(code){
	  	if(unseenProducts.includes(code['barcode']) == false){
	  		unseenProducts.push(code['barcode'])
	  		t.row.add([code['brand'], code['productName'], code['barcode'], code['stockcontrol__quantity'],code['stockcontrol__location']]).draw(false);
	  	}
	  })
	})
} );


