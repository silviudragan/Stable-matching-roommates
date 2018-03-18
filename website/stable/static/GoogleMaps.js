function myMap() {
    var fii = {lat: 47.1740032, lng: 27.5748576};
    var mapOptions = {
        center: fii,
        zoom: 15,
        mapTypeId: google.maps.MapTypeId.HYBRID
    }

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    var C1 = {lat: 47.1882123, lng: 27.5625704};
    var C2 = {lat: 47.1882123, lng: 27.5625704};
    var C3 = {lat: 47.1886243, lng: 27.5621144};
    var C4 = {lat: 47.188692, lng: 27.563088};
    var C5 = {lat: 47.176098, lng: 27.570003};
    var C6 = {lat: 47.1758367, lng: 27.569249};
    var C7 = {lat: 47.175478, lng: 27.56946};
    var C8 = {lat: 47.174839, lng: 27.569413};
    var C10 = {lat: 47.1775, lng: 27.573786};
    var C11 = {lat: 47.176655, lng: 27.572409};
    var C12 = {lat: 47.176953, lng: 27.572231};
    var C13 = {lat: 47.177031, lng: 27.574232};
    var Akademos = {lat: 47.1694349, lng: 27.5743529};
    var Gaudeamus = {lat: 47.1778824, lng: 27.5711426};

    var marker = new google.maps.Marker({
        position: fii,
        map: map,
        title: 'Facultatea de Informatică'
    });

    var marker = new google.maps.Marker({
        position: C1,
        map: map,
        title: 'Cămin C1'
    });

    var marker = new google.maps.Marker({
        position: C2,
        map: map,
        title: 'Cămin C2'
    });

    var marker = new google.maps.Marker({
        position: C3,
        map: map,
        title: 'Cămin C3'
    });

    var marker = new google.maps.Marker({
        position: C4,
        map: map,
        title: 'Cămin C4'
    });

    var marker = new google.maps.Marker({
        position: C5,
        map: map,
        title: 'Cămin C5'
    });

    var marker = new google.maps.Marker({
        position: C6,
        map: map,
        title: 'Cămin C6'
    });

    var marker = new google.maps.Marker({
        position: C7,
        map: map,
        title: 'Cămin C7'
    });

    var marker = new google.maps.Marker({
        position: C8,
        map: map,
        title: 'Cămin C8'
    });

    var marker = new google.maps.Marker({
        position: C10,
        map: map,
        title: 'Cămin C10'
    });

    var marker = new google.maps.Marker({
        position: C11,
        map: map,
        title: 'Cămin C11'
    });

    var marker = new google.maps.Marker({
        position: C12,
        map: map,
        title: 'Cămin C12'
    });

    var marker = new google.maps.Marker({
        position: C13,
        map: map,
        title: 'Cămin C13'
    });

    var marker = new google.maps.Marker({
        position: Gaudeamus,
        map: map,
        title: 'Gaudeamus'
    });

    var marker = new google.maps.Marker({
        position: Akademos,
        map: map,
        title: 'Akademos'
    });
}