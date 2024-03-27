function init()
{
    window.navigator.geolocation.getCurrentPosition(get_latlng);
}

function get_latlng(position)
{
    let lat = position.coords.latitude;
    let lng = position.coords.longitude;
    // $('#current_lat_geo').text(lat)
    // $('#current_lng_geo').text(lng)
    $('#current_lat').val(lat)
    $('#current_lng').val(lng)
    $('#current_lat_s').val(lat)
    $('#current_lng_s').val(lng)
}

window.addEventListener('load', init);