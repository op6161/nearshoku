function init()
{
    window.navigator.geolocation.getCurrentPosition(get_latlng);
    console.log("init_get_geo");
}
/**
 *
 * @param position
 */
function get_latlng(position)
{
    console.log("get_latlng");
    let lat = position.coords.latitude;
    let lng = position.coords.longitude;
    // window.lat = lat
    // window.lng = lng
}

window.addEventListener('load', init);