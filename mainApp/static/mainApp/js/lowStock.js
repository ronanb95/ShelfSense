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
            console.log(data);
            var dataJson = $.parseJSON(data);
            var content = "";
            var icon = trendDownIcon;
            console.log("hiiii");
            content += "<tr class=\"heading-td\">\n" +
                "                                                    <td class=\"mv-icon\">Brand Name</td>\n" +
                "                                                    <td class=\"coin-name\">Product Name</td>\n" +
                "                                                    <td class=\"buy\">Location</td>\n" +
                "                                                    <td class=\"sell\">Current Stock</td>\n" +
                "                                                    <td class=\"trends\">Low Stock Level</td>\n" +
                "                                                    <td class=\"attachments\">    Trends of Stock</td>\n" +
                "                                                </tr>";
            for (var i = 0; i < dataJson.length; i++) {
                content += " <tr>\n" + "      <td>";
                content += dataJson[i]["brand"];
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["productName"];
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["stockcontrol__location"];
                content += "</td>\n" + "      <td>";
                content += dataJson[i]["stockcontrol__quantity"];


                content += "</td>\n" + "<td>";

                content += dataJson[i]["lowStockLevel"];
                content += "</td>\n" + "<td class=\"trends\"><img src=" +icon+" alt=\"icon\"></td>";
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