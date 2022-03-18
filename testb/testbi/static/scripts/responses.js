


function getBotResponse(input) {
    //rock paper scissors
    //var djangoData = $('#my-data').data("var_name");
    //var dat = JSON.parse("{{var_name | tojson | safe}}");
   // alert(input);
   var var_name = $("#here").text();
    mes = var_name
    $.ajax({
        url: '',
        type:'get',
        data: {
            'input':input,
        },
    });
    $.ajax({
        url: "index.html",
        data: {
          id:$(this).attr('id')
        },
        cache: false,
        success: function(html){
            $('#list-content').html(data);
        }
      })
    // Simple responses
    if (mes == mes) {
        return mes;
    } 
}