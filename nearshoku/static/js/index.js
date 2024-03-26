var lat,lng;

/////// init google map ///////
window.initMap = function () {
    // google map setting
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: current_lat, lng: current_lng},
        zoom: 13,
    });

    // current location marker setting
    var marker = new google.maps.Marker({
            position: { lat: current_lat, lng: current_lng},
            map: map,
        });

    /////// map onclick events ///////
    map.addListener("click",function(e){// click event listener
        // clear previous marker
        marker.setMap(null);
        // new marker
        placeMarkerAndPanTo(e.latLng, map);

        // get values from api
        lat = e.latLng.lat();
        lng = e.latLng.lng();

        // set values
        $("#selected_lat").val(lat);
        $("#selected_lng").val(lng);
        $("#submitSelectedLocation").attr('disabled',false);
        $("#submitSelectedLocation").val("Search By Selected Location");
        })


    function placeMarkerAndPanTo(latLng, map){
        marker = new google.maps.Marker({
            position: latLng,
            map: map,
        });
        // move screen to marker
        map.panTo(latLng);
    }
};//스크립트 파일 분리시 template변수를 읽지 못해 오작동, hidden이랑 연계하면 해결가능할지도
//마커가 계속 찍히는 문제가 있음 (정상적인 기능이지만 수정하고싶음)
