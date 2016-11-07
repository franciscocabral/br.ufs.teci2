/**
 * Created by Fancisco on 06/11/2016.
 */



$(document).ready(function () {
    var text = getUrlParameter('text');
    if(text != undefined){
        $("[name=text]").val(text);
    }
});

$(".submit").on('click', function () {
    var text = $("[name=text]").val();
    $.ajax({
        url: URL + text,
    }).done(function (result) {
        var id = addLembrete(result);
        window.location.replace("./view.html?id="+id);
    });
});


