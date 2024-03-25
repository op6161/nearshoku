var lat,lng;
window.initMap = function () {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: current_lat, lng: current_lng},
        zoom: 13,
    });
    map.addListener("click",function(e){ // click event listener
        placeMarkerAndPanTo(e.latLng, map);
        console.log(e.latLng)
        lat = e.latLng.lat();
        lng = e.latLng.lng();
        document.getElementById('selected_lat').value = lat
        document.getElementById('selected_lng').value = lng
        })
    function placeMarkerAndPanTo(latLng, map){
        new google.maps.Marker({ // mark click on pan
            position: latLng,
            map: map,
        });
        map.panTo(latLng); // screen move to pan
    }
};//스크립트 파일 분리시 template변수를 읽지 못해 오작동, hidden이랑 연계하면 해결가능할지도
//마커가 계속 찍히는 문제가 있음 (정상적인 기능이지만 수정하고싶음)
