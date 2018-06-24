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

function detaliiColeg(str) {
    if(str != ""){
        $.ajax({
            url: '/ajax/validate_username/',
            type: 'get',
            data: {
              'numeColeg': str
            },
            dataType: 'json',
          }).done(function(data){
            var nume = "";
            var an = "";
            var grupa = "";
            for(it in data){
                if(it == "Nume:")
                {
                    nume = data[it];
                    $('.nume').html(data[it]);
                }
                if(it == "An:")
                {
                    $('.an').html(data[it]);
                }
                if(it == "Grupa:")
                {
                    $('.grupa').html(data[it]);
                }
                if(it == "Poza:")
                {
                    $('.result2').html('<br><br><img src="/media/' + data[it] + '" height="200" width="200" />');
                }
            }
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
            rez += "<center><h2> Recenzii făcute </h2></center>";
            var nume_expeditor = "";
            var nume_destinatar = "";
            var mesaj = "";
            var camin = "";
            for(it in data){
                if(iterator % 8 == 0) // numa camin
                {
                    camin = data[it];
                }
                if(iterator % 8 == 1){ // poza expeditor
                    rez += "<div class='sticker'>";
                    rez += "<div class='col-md-3 col-sm-3'>";
                    rez += "<center><img src='/media/" + data[it] + "' height='100' width='100' />";
                    index = index + 1;
                }
                if(iterator % 8 == 2){ // nume expeditor
                    rez += "<p style='font-size:12px;'>" + data[it] + "</p></center>";
                    nume_expeditor = data[it];
                }
                if(iterator % 8 == 3){ // poza destinatar
                    rez += "<center><img src='/media/" + data[it] + "' height='100' width='100' />";
                }
                if(iterator % 8 == 4){ // nume destinatar
                    rez += "<p style='font-size:12px;'>" + data[it] + "</p></center></div>";
                    nume_destinatar = data[it];
                }
                if(iterator % 8 == 5){ // mesaj
                    mesaj = data[it];
                }
               if(iterator % 8 == 6){ // data recenziei
                    rez += "<div class='col-md-3 col-sm-3'><br>";
                    rez += "<h5> Expeditor</h5>";
                    rez += "<p>Destinatar</p><p>Data</p><p>Rating</p><p>Mesaj</p>";
                    rez += "</div>";
                    rez += "<div class='col-md-6 col-sm-6'><br>";
                    rez += "<h5>" + nume_expeditor + "</h5>";
                    rez += "<p>" + nume_destinatar + "</p>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 8 == 7){ // stele
                    rez += "<p>" + data[it] + "/5 <span class='glyphicon glyphicon-star'></span></p>";
                    rez += "<p>" + mesaj + "</p>";
                    rez += "</div></div><br>";
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
                if(iterator % 8 == 6){ //nume de la
                    date.push(data[it]);
                }
                iterator = iterator + 1;
            }
            iterator = 0;
            console.log(date);

            rez += "<center><h2> Recenzii primite </h2></center>";
            var nume_expeditor = "";
            var nume_destinatar = "";
            var mesaj = "";
            var camin = "";
            for(it in data)
            {
                if(iterator % 8 == 0)
                {
                    camin = data[it];
                }
                if(iterator % 8 == 1){ // poza expeditor
                    rez += "<div class='sticker'>";
                    rez += "<div class='col-md-3 col-sm-3'>";
                    rez += "<center><img src='/media/" + data[it] + "' height='100' width='100' />";
                    index = index + 1;
                }
                if(iterator % 8 == 2){ // nume expeditor
                    rez += "<p style='font-size:12px;'>" + data[it] + "</p></center>";
                    nume_expeditor = data[it];
                }
                if(iterator % 8 == 3){ // poza destinatar
                    rez += "<center><img src='/media/" + data[it] + "' height='100' width='100' />";
                }
                if(iterator % 8 == 4){ // nume destinatar
                    rez += "<p style='font-size:12px;'>" + data[it] + "</p></center></div>";
                    nume_destinatar = data[it];
                }
                if(iterator % 8 == 5){ // mesaj
                    mesaj = data[it];
                }
               if(iterator % 8 == 6){ // data recenziei
                    rez += "<div class='col-md-3 col-sm-3'><br>";
                    rez += "<h5> Expeditor</h5>";
                    rez += "<p>Destinatar</p><p>Data</p><p>Rating</p><p>Mesaj</p>";
                    rez += "</div>";
                    rez += "<div class='col-md-6 col-sm-6'><br>";
                    rez += "<h5>" + nume_expeditor + "</h5>";
                    rez += "<p>" + nume_destinatar + "</p>";
                    rez += "<p>" + data[it] + "</p>";
                }
                if(iterator % 8 == 7){ // stele
                    rez += "<p>" + data[it] + "/5 <span class='glyphicon glyphicon-star'></span></p>";
                    rez += "<p>" + mesaj + "</p>";
                    rez += "</div></div><br>";
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
            $('.recenziiRealizate').html();
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

function salvareFavoriti(numar_matricol){
    console.log("aaaaaaa" + numar_matricol);
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

function stergeDate(){
    $.ajax({
        url: '/ajax/sterge_date/',
        type: 'get',
        data: {},
        dataType: 'json',
    }).done(function(data){
        console.log(data);
        console.log("silviuuu");
    });
}