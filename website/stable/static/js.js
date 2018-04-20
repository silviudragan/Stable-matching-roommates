function showCustomer(str) {
    if(str != ""){
        $.ajax({
            url: '/ajax/validate_username/',
            type: 'get',
            data: {
              'numeColeg': str
            },
            dataType: 'json',
          }).done(function(data){
            var tabel = "<table>";
            for(it in data){
                if(it != "Poza:")
                {
                    tabel += "<tr><td><b>" + it + "</b></td>";
                    tabel += "<td>"  + data[it] + "</td></tr>";
                }
                else
                {
                     $('.result2').html('<img src="/media/' + data[it] + '" height="245" width="180" />');
                }
            }
            tabel += "</table>"
            $('.result').html(tabel);
          });
    }
}

function recenziiFacute(nr_matricol){
    var index = 0;
    var iterator = 0;
    var rez = "";
    $.ajax({
            url: '/ajax/recenzii_facute/',
            type: 'get',
            data: {
              'nr_matricol': nr_matricol
            },
            dataType: 'json',
          }).done(function(data){
            console.log(data);
            var date = [];
            for(it in data){
                if(iterator % 6 == 4){ //nume de la
                    date.push(data[it]);
                }
                iterator = iterator + 1;
            }
            iterator = 0;
            console.log(date);
            for(it in data){

                console.log(iterator%6);
                if(iterator % 6 == 1){ //nume de la
                    rez += "<h5><span class='glyphicon glyphicon-time'></span> Post by " + data[it] + ", " + date[index] + ".</h5>";
                    index = index + 1;
                }
                if(iterator % 6 == 2){ //nume pt rec
                    rez += "<h5>To:"+ data[it] + "</h5>";
                }
                if(iterator % 6 == 3){ //nume
                    rez += "<h5><span class='label label-danger'>Coleg</span> <span class='label label-primary'>C12</span></h5>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 6 == 5){ //nume
                    rez += "<h5><span class='glyphicon glyphicon-star'></span>" + data[it] + "/5</h5>";
                    rez += "<hr>";
                }
                iterator = iterator + 1;
            }


            $('.recenziiRealizate').html(rez);
          });
}

function recenziiPrimite(nr_matricol){
    var index = 0;
    var iterator = 0;
    var rez = "";
    $.ajax({
            url: '/ajax/recenzii_primite/',
            type: 'get',
            data: {
              'nr_matricol': nr_matricol
            },
            dataType: 'json',
          }).done(function(data){
            console.log(data);
            var date = [];
            for(it in data){
                if(iterator % 6 == 4){ //nume de la
                    date.push(data[it]);
                }
                iterator = iterator + 1;
            }
            iterator = 0;
            console.log(date);
            for(it in data){

                console.log(iterator%6);
                if(iterator % 6 == 1){ //nume de la
                    rez += "<h5><span class='glyphicon glyphicon-time'></span> Post by " + data[it] + ", " + date[index] + ".</h5>";
                    index = index + 1;
                }
                if(iterator % 6 == 2){ //nume pt rec
                    rez += "<h5>To:"+ data[it] + "</h5>";
                }
                if(iterator % 6 == 3){ //text
                    rez += "<h5><span class='label label-danger'>Coleg</span> <span class='label label-primary'>C12</span></h5>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 6 == 5){ //stele
                    rez += "<h5><span class='glyphicon glyphicon-star'></span>" + data[it] + "/5</h5>";
                    rez += "<hr>";
                }
                iterator = iterator + 1;
            }


            $('.recenziiRealizate').html(rez);
          });
}

function toateRecenziile(){
    var index = 0;
    var iterator = 0;
    var rez = "";
    $.ajax({
            url: '/ajax/toate_recenziile/',
            type: 'get',
            dataType: 'json',
          }).done(function(data){
            console.log(data);
            var date = [];
            for(it in data){
                if(iterator % 6 == 4){ //nume de la
                    date.push(data[it]);
                }
                iterator = iterator + 1;
            }
            iterator = 0;
            console.log(date);
            for(it in data){

                console.log(iterator%6);
                if(iterator % 6 == 1){ //nume de la
                    rez += "<h5><span class='glyphicon glyphicon-time'></span> Post by " + data[it] + ", " + date[index] + ".</h5>";
                    index = index + 1;
                }
                if(iterator % 6 == 2){ //nume pt rec
                    rez += "<h5>To:"+ data[it] + "</h5>";
                }
                if(iterator % 6 == 3){ //text
                    rez += "<h5><span class='label label-danger'>Coleg</span> <span class='label label-primary'>C12</span></h5>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 6 == 5){ //stele
                    rez += "<h5><span class='glyphicon glyphicon-star'></span>" + data[it] + "/5</h5>";
                    rez += "<hr>";
                }
                iterator = iterator + 1;
            }


            $('.recenziiRealizate').html(rez);
          });
}

function showCustomer(str) {
    if(str != ""){
        $.ajax({
            url: '/ajax/validate_username/',
            type: 'get',
            data: {
              'numeColeg': str
            },
            dataType: 'json',
          }).done(function(data){
            var tabel = "<table>";
            for(it in data){
                if(it != "Poza:")
                {
                    tabel += "<tr><td><b>" + it + "</b></td>";
                    tabel += "<td>"  + data[it] + "</td></tr>";
                }
                else
                {
                     $('.result2').html('<img src="/media/' + data[it] + '" height="245" width="180" />');
                }
            }
            tabel += "</table>"
            $('.result').html(tabel);
          });
    }
}

function recenziiFacute(nr_matricol){
    var index = 0;
    var iterator = 0;
    var rez = "";
    $.ajax({
            url: '/ajax/recenzii_facute/',
            type: 'get',
            data: {
              'nr_matricol': nr_matricol
            },
            dataType: 'json',
          }).done(function(data){
            console.log(data);
            var date = [];
            for(it in data){
                if(iterator % 6 == 4){ //nume de la
                    date.push(data[it]);
                }
                iterator = iterator + 1;
            }
            iterator = 0;
            console.log(date);
            for(it in data){

                if(iterator % 6 == 1){ //nume de la
                    rez += "<h5><span class='glyphicon glyphicon-time'></span> Post by " + data[it] + ", " + date[index] + ".</h5>";
                    index = index + 1;
                }
                if(iterator % 6 == 2){ //nume pt rec
                    rez += "<h5>To:"+ data[it] + "</h5>";
                }
                if(iterator % 6 == 3){ //nume
                    rez += "<h5><span class='label label-danger'>Coleg</span> <span class='label label-primary'>C12</span></h5>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 6 == 5){ //nume
                    rez += "<h5><span class='glyphicon glyphicon-star'></span>" + data[it] + "/5</h5>";
                    rez += "<hr>";
                }
                iterator = iterator + 1;
            }

            $( "testare" ).empty();
            $('.recenziiRealizate').html(rez);
          });
}

function recenziiPrimite(nr_matricol){
    var index = 0;
    var iterator = 0;
    var rez = "";
    $.ajax({
            url: '/ajax/recenzii_primite/',
            type: 'get',
            data: {
              'nr_matricol': nr_matricol
            },
            dataType: 'json',
          }).done(function(data){
            console.log(data);
            var date = [];
            for(it in data){
                if(iterator % 6 == 4){ //nume de la
                    date.push(data[it]);
                }
                iterator = iterator + 1;
            }
            iterator = 0;
            console.log(date);
            for(it in data){

                if(iterator % 6 == 1){ //nume de la
                    rez += "<h5><span class='glyphicon glyphicon-time'></span> Post by " + data[it] + ", " + date[index] + ".</h5>";
                    index = index + 1;
                }
                if(iterator % 6 == 2){ //nume pt rec
                    rez += "<h5>To:"+ data[it] + "</h5>";
                }
                if(iterator % 6 == 3){ //text
                    rez += "<h5><span class='label label-danger'>Coleg</span> <span class='label label-primary'>C12</span></h5>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 6 == 5){ //stele
                    rez += "<h5><span class='glyphicon glyphicon-star'></span>" + data[it] + "/5</h5>";
                    rez += "<hr>";
                }
                iterator = iterator + 1;
            }


            $('.recenziiRealizate').html(rez);
          });
}

function toateRecenziile(){
    var index = 0;
    var iterator = 0;
    var rez = "";
    $.ajax({
            url: '/ajax/toate_recenziile/',
            type: 'get',
            dataType: 'json',
          }).done(function(data){
            console.log(data);
            var date = [];
            for(it in data){
                if(iterator % 6 == 4){ //nume de la
                    date.push(data[it]);
                }
                iterator = iterator + 1;
            }
            iterator = 0;
            console.log(date);
            for(it in data){

                if(iterator % 6 == 1){ //nume de la
                    rez += "<h5><span class='glyphicon glyphicon-time'></span> Post by " + data[it] + ", " + date[index] + ".</h5>";
                    index = index + 1;
                }
                if(iterator % 6 == 2){ //nume pt rec
                    rez += "<h5>To:"+ data[it] + "</h5>";
                }
                if(iterator % 6 == 3){ //text
                    rez += "<h5><span class='label label-danger'>Coleg</span> <span class='label label-primary'>C12</span></h5>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 6 == 5){ //stele
                    rez += "<h5><span class='glyphicon glyphicon-star'></span>" + data[it] + "/5</h5>";
                    rez += "<hr>";
                }
                iterator = iterator + 1;
            }


            $('.recenziiRealizate').html(rez);
          });
}

function adaugareFavorit() {

    var nameValue = document.getElementById("studenti").value;
    var studenti = document.getElementById("studenti");
    studenti.remove(studenti.selectedIndex);
    var x = document.getElementById("favoriti");
    options = x.getElementsByTagName("option");

    var c = document.createElement("option");

    if(nameValue.length > 0){
        c.text = nameValue;
        x.options.add(c, options.length);
    }

//    var queryString = document.getElementById("favoriti");
//    options = queryString.getElementsByTagName("option");
//    console.log(options[1].text);
}

function eliminareFavorit(){
    var nameValue = document.getElementById("favoriti").value;
    var studenti_alesi = document.getElementById("favoriti");
    studenti_alesi.remove(studenti_alesi.selectedIndex);

    var studenti = document.getElementById("studenti");
    options = studenti.getElementsByTagName("option");

    var c = document.createElement("option");
    if(nameValue.length > 0){
        c.text = nameValue;
        studenti.options.add(c, 0);
    }
}

function salvareFavoriti(){

    var queryString = document.getElementById("favoriti");
    options = queryString.getElementsByTagName("option");

    var nume_preferinte = "";
    for(i = 0; i < options.length; i++){
        nume_preferinte += options[i].text + "+";
    }
    console.log(nume_preferinte);

    if(options.length > 0){
        $.ajax({
                url: '/ajax/preferinte_student/',
                type: 'get',
                data: {
                  'nume_preferinte': nume_preferinte,
                },
                dataType: 'json',
              }).done(function(data){
                    console.log(data);
                });
    }
    console.log(nume_preferinte);
}
