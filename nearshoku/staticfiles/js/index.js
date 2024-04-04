/**
* Initializes the Google Map and handles map-related interactions
 *
 * set center to current location
 * set pin to center
 * map click event : place new pin, move screen center to pin, set selected location
 * Note: This function requires google map API script.
*/
function initMap() {
    navigator.geolocation.getCurrentPosition(async function(position){
        let selected_lng
        let selected_lat

        // Create a LatLng object to use current position
        let latlng = await new google.maps.LatLng(position.coords.latitude, position.coords.longitude)

        // Create a GoogleMap object centered at current position
        const map = await new google.maps.Map(document.getElementById("map"), {
            center: latlng,
            zoom: 13,

            // Add code to replace Marker to AdvancedMarkerElemnt
            mapId: "DEMO_MAP_ID", // Map ID is required for advanced markers.
            // It must be a new mapID on production
            // https://developers.google.com/maps/documentation/javascript/advanced-markers/start
        });

        // Create a Marker at current position on GoogleMap
        // It replaced from google.maps.Marker
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker")
        let marker = await new google.maps.marker.AdvancedMarkerElement({position: latlng, map: map,});

        /**
        * Set the current location data to sent to views
        *
        * @param {dictionary} latlng - current latitude dict
        */
        function get_latlng(latlng) {
            let lat = latlng['lat']
            let lng = latlng['lng']
            $('#current_lat').val(lat)
            $('#current_lng').val(lng)
        }

        // Add a click event listener to the map
        map.addListener("click", function (e) {
            // Delete existing Marker
            marker.setMap(null);
            // Place a new Marker and move the screen center to it
            placeMarkerAndPanTo(e.latLng, map);

            // Set the selected location data to sent to views
            // And active submit by-selected-location button
            selected_lat = e.latLng.lat();
            selected_lng = e.latLng.lng();
            set_select(selected_lat, selected_lng)
        })

        /**
         * Set place marker and move screen center to marker
         * @event click
         * @param {dict} latLng - The latlng dictionary
         * @param {google.maps.Map} map - The google.maps.Map object
         */
        function placeMarkerAndPanTo(latLng, map) {
            // Set marker on clicked
            // It replaced from google.maps.Marker
            marker = new google.maps.marker.AdvancedMarkerElement({position: latLng, map: map,});
            // Move screen to set marker
            map.panTo(latLng);
        }

        /**
         * Set the selected-location data to send views
          * set selected-location
          * active by-selected-search button
         * @param {number} lat - The selected latitude
         * @param {number} lng - The current longitude
         */
        function set_select(lat, lng){
            // set selected-location
            $("#selected_lat").val(lat);
            $("#selected_lng").val(lng);
            // active search-by-selected-location submit button
            $("#submitSelectedLocation").attr('disabled',false);
            $("#submitSelectedLocation").text("Search By Selected Location");
        }
    })
}




