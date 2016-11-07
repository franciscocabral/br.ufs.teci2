/**
 * Created by Fancisco on 06/11/2016.
 */


var personsSelect = $("#persons").select2({
    tags: true,
    tokenSeparators: [',']
});

var placesSelect = $("#places").select2({
    tags: true,
    tokenSeparators: [',']
});

$(document).ready(function () {

    var id = getUrlParameter('id');
    data = getLembrete(id);

    var text = data['text'];

    var places = data['places'];
    var persons = data['persons'];
    var time = data['time'];
    var date = data['date'];

    if (time.length > 0) time = time[0][1];
    if (date.length > 0) date = date[0][1];

    places = data['newPlaces'] != undefined ? data['newPlaces'] : places;
    persons = data['newPersons'] != undefined ? data['newPersons'] : persons;
    time = [data['newTime'] != undefined ? data['newTime'] : time];
    date = [data['newDate'] != undefined ? data['newDate'] : date];


    $("#text").val(text).trigger("change");

    if (places.length > 0) {
        var tmp = [];
        $.each(places, function (i, v) {
            tmp.push(v);
            placesSelect.append("<option value='" + v + "'>" + v + "</option>");
        });
        placesSelect.val(tmp).trigger("change");
    }
    if (persons.length > 0) {
        var tmp = [];
        $.each(persons, function (i, v) {
            tmp.push(v);
            personsSelect.append("<option value='" + v + "'>" + v + "</option>");
        });
        personsSelect.val(tmp).trigger("change");
    }

    if (time.length > 0) $("#time").val(time[0]).trigger("change");
    if (date.length > 0) $("#date").val(date[0]).trigger("change");

});

$("#save").on("click", function () {
    var id = getUrlParameter('id');
    data = getLembrete(id);

    data['newPlaces'] = placesSelect.val();
    data['newPersons'] = personsSelect.val();
    data['newTime'] = $("#time").val();
    data['newDate'] = $("#date").val();
    setLembrete(id, data);
    window.location.replace("./all.html");
});
