/**
* A function init google map
 * set center to received location
 * set pin to center
 * map click event : place new pin, move screen center to pin, set selected location
* requires google map api script
*/
function initMap() {
    // 35.6812362,139.7671248
    // test value Tokyo Station
    var selected_lng
    var selected_lat

    navigator.geolocation.getCurrentPosition(async function(position){
        // var latlng = new google.maps.LatLng(35.6812362, 139.7671248)

        var latlng = await new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
        const map = await new google.maps.Map(document.getElementById("map"), {center: latlng, zoom: 13,});
        var marker = await new google.maps.Marker({position: latlng, map: map,});



        function get_latlng(latlng) {
            var lat = latlng['lat']
            var lng = latlng['lng']
            $('#current_lat').val(lat)
            $('#current_lng').val(lng)
            // by selected
            $('#current_lat_s').val(lat)
            $('#current_lng_s').val(lng)
        }
        /**
         * map click event
          * place new pin
          * move screen center to pin
          * set selected location
         */
        map.addListener("click", function (e) {
            marker.setMap(null);
            placeMarkerAndPanTo(e.latLng, map);
            selected_lat = e.latLng.lat();
            selected_lng = e.latLng.lng();
            set_select(selected_lat, selected_lng)
        })
        /**
         * place marker and move screen center to marker
         * @event click
         * @param {dict} latLng latlng dictionary
         * @param {google.maps.Map} map google map object
         */
        function placeMarkerAndPanTo(latLng, map) {
            // set marker on clicked
            marker = new google.maps.Marker({position: latLng, map: map,});
            // move screen to set marker
            map.panTo(latLng);
        }
    })
}



/**
 * A function set selected location data to send views
  * set selected location
  * active by selected search button
 * @param {number} lat selected latitude
 * @param {number} lng current longitude
 */
function set_select(lat, lng){
    $("#selected_lat").val(lat);
    $("#selected_lng").val(lng);
    $("#submitSelectedLocation").attr('disabled',false);
    $("#submitSelectedLocation").val("Search By Selected Location");
}

/**
 * A function set current location data to send views
 * @param {number} lat current latitude
 * @param {number} lng current longitude
 */

function set_current(){
    window.navigator.geolocation.getCurrentPosition(get_latlng)

}