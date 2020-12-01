$(function () {
    
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajax({

        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: 'GET',
        url: '/lowLevelStock/',

        success: function (data) {
            // console.log(data);
            var dataJson = $.parseJSON(data);
            var content = "";
            var icon = trendDownIcon;
            console.log("hiiii");
            content += "<tr class=\"heading-td\">\n" +
                "                                                    <td class=\"mv-icon\">Barcode</td>\n" +
                "                                                    <td class=\"mv-icon\">Brand Name</td>\n" +
                "                                                    <td class=\"coin-name\">Product Name</td>\n" +
                "                                                    <td class=\"buy\">Location</td>\n" +
                "                                                    <td class=\"sell\">Current Stock</td>\n" +
                "                                                    <td class=\"trends\">Low Stock Level</td>\n" +
                "                                                    <td class=\"attachments\">    Store</td>\n" +
                "                                                </tr>";
            var barcode = "";
            for (var i = 0; i < dataJson.length; i++) {
                if (barcode === dataJson[i]["barcode"]){

                }else{
                    barcode = dataJson[i]["barcode"];
                    content += " <tr>\n" + "      <td>";
                content += dataJson[i]["barcode"];
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["barcode__brand"];
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["barcode__productName"];
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["location"];
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["quantity"];


                content += "</td>\n" + "<td>";

                content += dataJson[i]["barcode__lowStockLevel"];
                // content += "</td>\n" + "<td class=\"trends\"><img src=" +icon+" alt=\"icon\"></td>";
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["location__store"];
                content += "</td>"
                }

                // content += "</td>";
            }
            content += "</tr>";
            $("#lowStock").html(content)


        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert("Something Wrong!");
        },
    });
});