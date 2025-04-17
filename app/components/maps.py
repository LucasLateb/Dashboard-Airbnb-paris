import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium

def render_fast_marker_map(df, zoom=12, width=1000, height=600):
    coords = df[["latitude", "longitude", "price", "name", "neighbourhood_cleansed"]].copy()
    center = [coords["latitude"].mean(), coords["longitude"].mean()]
    base_map = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron", control_scale=True)

    data = coords.values.tolist()
    callback = """
    function(row){
        var m = L.marker(new L.LatLng(row[0], row[1]));
        m.bindTooltip(
            `<b>${row[3]}</b><br/>` +
            `${row[4]}<br/>` +
            `<b>${row[2].toFixed(0)} €</b>`,
            {sticky: true}
        );
        return m;
    }
    """
    FastMarkerCluster(data=data, callback=callback).add_to(base_map)

    map_data = st_folium(base_map, width=width, height=height)
    return map_data
