var selected_lat,selected_lng;

function init_index(){
    window.navigator.geolocation.getCurrentPosition(initMap)
}

async function initMap(position)
{
    let latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
    const map = new google.maps.Map(document.getElementById("map"), {center:latlng, zoom: 13,});
    var marker = new google.maps.Marker({position: latlng, map: map,});

    map.addListener("click",function(e) {
        marker.setMap(null);
        placeMarkerAndPanTo(e.latLng, map);
        selected_lat = e.latLng.lat();
        selected_lng = e.latLng.lng();
        $("#selected_lat").val(selected_lat);
        $("#selected_lng").val(selected_lng);
        $("#submitSelectedLocation").attr('disabled',false);
        $("#submitSelectedLocation").val("Search By Selected Location");
    })

    function placeMarkerAndPanTo(latLng, map) {
        marker = new google.maps.Marker({position: latLng, map: map,});
        map.panTo(latLng);// move screen to marker
    }
};

window.addEventListener("load", init_index);