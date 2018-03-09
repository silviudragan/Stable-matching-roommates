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