/**
 * Created by Fancisco on 07/11/2016.
 */

$(document).ready(function () {
    indexer = getLembreteIndexer();
    $.each(indexer, function (i, v) {
        var id = i;
        var text = v;
        var html = '<div class="fourteen wide column field">' +
            '<div class="ui left input middle">' +
            '<span>'+text+'</span>' +
            '</div>' +
            '</div>' +
            '<div class="two wide column">' +
            '<div class="ui fluid green button right visualizar" data-id="'+id+'">' +
            'Abrir</div>' +
            '</div>';
        $('.lembretes').append(html);
    });
});

$(document).on( "click",".visualizar", function(){
    var id = $(this).data('id');
    window.location.replace("./view.html?id="+id);
});