(document).ready(function () {
    var index = [];
    var t = $('#dataTable2').DataTable();
    fetch("http://127.0.0.1:8000/default").then(response => {
        return response.json();
    }).then(data => {
        data.forEach(function (code) {
            if (!~index.indexOf(code['barcode'])) {
                t.row.add([code['brand'], code['productName'], code['stockcontrol__location'], code['barcode'], code['stockcontrol__quantity']]).draw(false);
            }
            index.push(code['barcode']);
        })
    })
});


