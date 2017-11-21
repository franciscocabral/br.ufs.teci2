/**
 * Created by Fancisco on 06/11/2016.
 */

var URL = "http://localhost:5000/treat";

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

function getLembreteIndexer(){
    list = localStorage.getItem('lembretes-indexer');
    if(list == null) {
        list = [];
        localStorage.setItem('lembretes-indexer', JSON.stringify(list));
    }
    return JSON.parse(localStorage.getItem('lembretes-indexer'));
}

function addLembrete(data){
    indexer = getLembreteIndexer();
    id = indexer.push(data['text'])-1;
    localStorage.setItem('lembretes-indexer', JSON.stringify(indexer));
    localStorage.setItem('lembrete['+id+']', JSON.stringify(data));
    return id;
}

function getLembrete(id){
    return JSON.parse(localStorage.getItem('lembrete['+id+']'));
}

function setLembrete(id, data){
    localStorage.setItem('lembrete['+id+']', JSON.stringify(data));
    return id;
}

function notificar(id) {
    data = getLembrete(id);
    text = data['text'];
    if (Notification.permission !== "granted")
        Notification.requestPermission();
    else {
        var notification = new Notification('Lembrar-me!', {
            icon: 'icon.png',
            body: text
        });

        notification.onclick = function () {
            window.open("view.html?id="+id);
        };
    }
}
