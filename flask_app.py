from flask import Flask, render_template, render_template_string,\
    request, url_for, redirect
from friends import get_friends_list
import geopy
import folium
import urllib.error


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map', methods=['POST'])
def create_map():
    accname = request.form['name']
    try:
        friends_info = get_friends_list(accname)
    except urllib.error.HTTPError:
        return render_template('failure.html')
    locations = dict()
    for friend in friends_info:
        if friend['location'] not in locations:
            locations[friend['location']] = [friend['name']]
        else:
            locations[friend['location']].append(friend['name'])

    followers_map = folium.Map()
    fg = folium.FeatureGroup(name='Friends')
    geocoder = geopy.geocoders.ArcGIS(timeout=5)
    for location in locations:
        try:
            loc = geocoder.geocode(location)
            assert loc
        except (geopy.exc.GeocoderTimedOut, AssertionError):
            continue
        popup = '</li><li>'.join(locations[location])
        popup = '<style>.leaflet-popup-content {margin-left:0 !important} ul {padding-left: 30px}</style><div><ul><li>' + popup + '</li></ul></div>'
        fg.add_child(folium.Marker(location=(loc.latitude,loc.longitude),
                                   popup=popup, icon=folium.Icon()))
    followers_map.add_child(fg)
    html_string = followers_map.get_root().render()
    return render_template_string(html_string)


if __name__ == '__main__':
    app.run(debug=True)
