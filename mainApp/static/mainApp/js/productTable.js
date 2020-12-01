$(document).ready(function() {
    var t = $('#dataTable2').DataTable();
    var counter = 1;
    fetch("http://localhost:8000/default")
	.then(response => {
	  return response.json();
	})
	.then(data => {
	  data.forEach(function(code){
	    t.row.add( [
	    	code['barcode'],
	    	code['productName'],
	    	code['brand'],
	    	code['stockcontrol__location'],
	    	code['stockcontrol__quantity']
	    ] ).draw( false );
	  })
	})
} );


