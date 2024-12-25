import os

import kivy
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarker
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.camera import Camera
import geocoder
kivy.require('1.9.0')
# Set the application icon
Config.set('kivy', 'window_icon', 'C:/Simple/camera.png')  # Change this path to your icon file

KV = '''
BoxLayout:
    orientation: 'vertical'

    MapView:
        id: map_view
        lat: 37.7749  # Default latitude
        lon: -122.4194  # Default longitude
        zoom: 12

    BoxLayout:
        size_hint_y: None
        height: dp(300)  # Set height for camera view
        padding: dp(10)

        Camera:
            id: camera
            resolution: (640, 480)
            play: True  # Start camera preview

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        padding: dp(10)

        MDRaisedButton:
            text: "Take Picture"
            on_release: app.take_picture()

        MDRaisedButton:
            text: "Set Location"
            on_release: app.set_location()

        MDLabel:
            id: location_label
            text: "Location: "
'''


class MainApp(MDApp):
    def build(self):
        self.marker = None
        self.root = Builder.load_string(KV)
        return self.root

    def set_location(self):
        # Get the user's current location using geocoder
        g = geocoder.ip('me')  # Get location based on IP address

        if g.ok:
            lat = g.latlng[0]  # Latitude
            lon = g.latlng[1]  # Longitude
            self.update_map(lat, lon)
            self.root.ids.map_view.zoom = 15  # Set zoom level after updating location
        else:
            self.root.ids.location_label.text = "Unable to determine location."

    def update_map(self, lat, lon):
        self.root.ids.map_view.lat = lat
        self.root.ids.map_view.lon = lon

        if not self.marker:
            self.marker = MapMarker(lat=lat, lon=lon)
            self.root.ids.map_view.add_marker(self.marker)
        else:
            self.marker.lat = lat
            self.marker.lon = lon

        self.root.ids.location_label.text = f"Location: {lat}, {lon}"

    def take_picture(self):
        camera = self.root.ids.camera  # Access the camera widget from the layout
        camera.export_to_png("picture.png")
        print("Picture taken and saved as picture.png")


if __name__ == '__main__':
    MainApp().run()
