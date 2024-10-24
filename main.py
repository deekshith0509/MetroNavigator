import os
import heapq
from collections import defaultdict, namedtuple
import random
import matplotlib.pyplot as plt
import networkx as nx

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
import matplotlib.pyplot as plt
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from collections import defaultdict
# Named tuple to store the neighboring station's name, time in minutes, and distance in meters.
Pairs = namedtuple('Pairs', ['station', 'time', 'distance'])
from kivy.uix.scatter import Scatter

from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Rectangle
from kivy.graphics import RoundedRectangle, Color, Rectangle
from kivy.core.window import Window

from kivy.utils import get_color_from_hex


from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

from kivy.utils import platform
if platform == 'android':
    from android.storage import app_storage_path
    self.user_data_dir = os.path.join(app_storage_path(), 'cache')
    os.environ['MPLCONFIGDIR'] = self.user_data_dir
    if not os.path.exists(os.environ['MPLCONFIGDIR']):
        os.makedirs(os.environ['MPLCONFIGDIR'])
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class CustomScatter(Scatter):
    def on_touch_down(self, touch):
        # Check if the touch is within the bounds of the back button
        if self.parent.children[0].collide_point(*touch.pos):
            return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        # Ensure touch events are processed by the scatter only if not on the back button
        if self.parent.children[0].collide_point(*touch.pos):
            return False  # Don't allow the scatter to handle this touch
        return super().on_touch_move(touch)



class JourneyDetailScreen(Screen):
    def __init__(self, **kwargs):
        super(JourneyDetailScreen, self).__init__(**kwargs)

        # Background setup (black background)
        with self.canvas.before:
            Color(0, 0, 0, 1)  # black background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header setup (header color can remain unchanged)
        header = BoxLayout(size_hint_y=None, height=50)
        with header.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # header color
            self.header_gradient = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header_gradient, pos=self._update_header_gradient)
        header.add_widget(Label(text='Journey Details', font_size='24sp', bold=True, color=(1, 1, 1, 1)))  # White text

        self.layout.add_widget(header)

        # Scrollable view for journey details
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 500))
        self.detail_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.detail_layout.bind(minimum_height=self.detail_layout.setter('height'))
        self.scroll_view.add_widget(self.detail_layout)

        # Back button setup (button text color can remain unchanged)
        back_button = Button(text='Back', size_hint_y=None, height=40, background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), bold=True)
        back_button.bind(on_release=self.go_back)

        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)

    def update_journey_info(self, journey_info):
        self.detail_layout.clear_widgets()

        # Customize these values as needed
        char_width = 8  # Adjust based on font and design
        line_height = 50  # Line height for the labels
        row_spacing = 80  # Distance between rows

        for info in journey_info:
            detail_label = Label(
                text=info,
                size_hint_y=None,
                color=(1, 1, 1, 1),  # White text
                halign='left',
                valign='top',
                height=line_height  # Set initial height
            )
            
            # Set the desired width for the label
            detail_label.width = char_width * len(info)  # Width based on character count

            # Bind size to text_size
            detail_label.bind(size=detail_label.setter('text_size'))

            # Add padding for line height
            detail_label.height = detail_label.texture_size[1] + row_spacing  # Add spacing

            self.detail_layout.add_widget(detail_label)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _update_header_gradient(self, instance, value):
        self.header_gradient.pos = instance.pos
        self.header_gradient.size = instance.size

    def go_back(self, instance):
        # Set the transition effect
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'

from kivy.lang import Builder
class MetroMapApp(MDApp):

    def build(self):
        self.metro_map = self.add_metro_map()
        self.str_to_num = self.map_stations_to_numbers(self.metro_map)
        self.num_to_str = self.map_numbers_to_stations(self.str_to_num)
        self.current_path = None
        self.suppress_popup = False
        self.current_mode = None

        print(self.user_data_dir)
        # Ensure directory exists
        os.makedirs(self.user_data_dir, exist_ok=True)

        # Create the screen manager
        self.root = ScreenManager()

        # Main layout with improved styling
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Information section at the top
        info_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        info_layout.add_widget(Label(text='Metro Map Application', font_size='20sp', bold=True))
        info_layout.add_widget(Label(text='Developed by: Your Name', font_size='16sp'))
        # In your build function, replace the info_layout section with:
        info_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        info_layout.add_widget(Label(text='Metro Map Application', font_size='20sp', bold=True))

        # Create clickable labels
        email_label = Label(text='Email: deekshith.bh0509@gmail.com', font_size='16sp', color=(0, 0, 1, 1))
        email_label.bind(on_touch_down=lambda instance, touch: self.open_link('mailto:deekshith.bh0509@gmail.com') if instance.collide_point(*touch.pos) else None)

        projects_label = Label(text=' Projects:Some of my projects', font_size='16sp', color=(0, 0, 1, 1))
        projects_label.bind(on_touch_down=lambda instance, touch: self.open_link('https://github.com/deekshith0509?tab=repositories') if instance.collide_point(*touch.pos) else None)

        github_label = Label(text='GitHub: github.com/deekshith0509', font_size='16sp', color=(0, 0, 1, 1))
        github_label.bind(on_touch_down=lambda instance, touch: self.open_link('https://github.com/deekshith0509/') if instance.collide_point(*touch.pos) else None)

        resume_label = Label(text='Resume: Open Resume', font_size='16sp', color=(0, 0, 1, 1))
        resume_label.bind(on_touch_down=lambda instance, touch: self.open_link('https://drive.google.com/file/d/1274cxCrj52NG1dDgo7aGmvjRbl1ahmGo/view') if instance.collide_point(*touch.pos) else None)

        portfolio_label = Label(text='Portfolio: My Info', font_size='16sp', color=(0, 0, 1, 1))
        portfolio_label.bind(on_touch_down=lambda instance, touch: self.open_link('https://deekshith0509.github.io/Portfolio.html') if instance.collide_point(*touch.pos) else None)

        # Add labels to the layout
        info_layout.add_widget(email_label)
        info_layout.add_widget(projects_label)
        info_layout.add_widget(github_label)
        info_layout.add_widget(resume_label)
        info_layout.add_widget(portfolio_label)
        # ScrollView for the info section
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 200))
        scroll_view.add_widget(info_layout)
        self.layout.add_widget(scroll_view)

        # Source Station Dropdown
        self.source_dropdown = DropDown()
        for station in self.str_to_num.keys():
            btn = Button(text=station, size_hint_y=None, height=44, background_color=(0.8, 0.8, 0.8, 1))
            btn.bind(on_release=lambda btn: self.source_dropdown.select(btn.text))
            self.source_dropdown.add_widget(btn)

        self.source_button = Button(text='Select Source Station', size_hint_y=None, height=44)
        self.source_button.bind(on_release=self.source_dropdown.open)
        self.source_dropdown.bind(on_select=lambda instance, x: setattr(self.source_button, 'text', x))

        # Destination Station Dropdown
        self.destination_dropdown = DropDown()
        for station in self.str_to_num.keys():
            btn = Button(text=station, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.destination_dropdown.select(btn.text))
            self.destination_dropdown.add_widget(btn)

        self.destination_button = Button(text='Select Destination Station', size_hint_y=None, height=44)
        self.destination_button.bind(on_release=self.destination_dropdown.open)
        self.destination_dropdown.bind(on_select=lambda instance, x: setattr(self.destination_button, 'text', x))

        # Mode Selection Dropdown
        self.mode_dropdown = DropDown()
        for option in ['Distance', 'Time']:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.mode_dropdown.select(btn.text))
            self.mode_dropdown.add_widget(btn)

        self.mode_button = Button(text='Select Mode', size_hint_y=None, height=44)
        self.mode_button.bind(on_release=self.mode_dropdown.open)
        self.mode_dropdown.bind(on_select=lambda instance, x: self.set_mode(x))

        # Find Path Button
        find_path_button = Button(text='Find Path', size_hint_y=None, height=44)
        find_path_button.bind(on_release=self.find_path)

        # Visualize Button
        visualize_button = Button(text='Visualize Path', size_hint_y=None, height=44)
        visualize_button.bind(on_release=self.visualize_metro_map)

        # Add all widgets to the main layout
        self.layout.add_widget(self.source_button)
        self.layout.add_widget(self.destination_button)
        self.layout.add_widget(self.mode_button)
        self.layout.add_widget(find_path_button)
        self.layout.add_widget(visualize_button)

        # Main screen
        main_screen = Screen(name='main')
        main_screen.add_widget(self.layout)
        self.root.add_widget(main_screen)

        # Create the journey detail screen
        self.journey_detail_screen = JourneyDetailScreen(name='journey_details')
        self.root.add_widget(self.journey_detail_screen)

        # Create the visualization screen
        self.visualization_screen = Screen(name='visualization')
        self.root.add_widget(self.visualization_screen)

        # Create the visualization page
        self.create_visualization_page()

        # Style all buttons
        self.style_buttons([
            self.source_button,
            self.destination_button,
            self.mode_button,
            find_path_button,
            visualize_button,
        ])

        return self.root

    def style_buttons(self, buttons):
        for button in buttons:
            button.background_normal = ''
            button.background_color = (0.2, 0.6, 0.8, 1)  # Base color
            button.bind(on_enter=lambda instance: setattr(instance, 'background_color', (0.3, 0.7, 0.9, 1)))  # Hover color
            button.bind(on_leave=lambda instance: setattr(instance, 'background_color', (0.2, 0.6, 0.8, 1)))  # Revert color

            with button.canvas.before:
                Color(0.2, 0.6, 0.8, 1)  # Button color
                button.rect = RoundedRectangle(size=button.size, pos=button.pos, radius=[10])

            button.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))
            button.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))

            # Add shadow effect
            with button.canvas.after:
                Color(0, 0, 0, 0.2)  # Shadow color
                button.shadow = Rectangle(size=(button.width, button.height), pos=(button.x + 2, button.y - 2))

            button.bind(size=lambda instance, value: setattr(instance.shadow, 'size', value))
            button.bind(pos=lambda instance, value: setattr(instance.shadow, 'pos', (button.x + 2, button.y - 2)))


    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)






    def set_mode(self, mode):
        if self.current_mode is None:
            self.current_mode= "time"
        else:
            self.current_mode = mode  # Store the selected mode
        print(f"Current mode set to: {self.current_mode}")  # Optional feedback

    def create_visualization_page(self):
        # Create a new screen for visualization
        visualization_page = Screen(name='visualization_page')

        # Create a layout for the visualization page with a modern design
        self.visualization_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Create a top layout for the title
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)

        # Add a title label with modern styling
        title_label = Label(
            text='Visualization',
            size_hint_y=None,
            height=50,
            font_size='24sp',
            bold=True,
            color=(0, 0, 0, 1)  # Black text
        )
        top_layout.add_widget(title_label)

        # Create a main layout to combine the top layout and visualization layout
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(top_layout)
        main_layout.add_widget(self.visualization_layout)

        # Add a separator line for better visual separation
        with main_layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)  # Light grey color
            Rectangle(pos=(0, 50), size=(main_layout.width, 2))  # Line below the top layout

        # Add the main layout to the visualization page
        visualization_page.add_widget(main_layout)

        # Add a back button with modern styling
        back_button = Button(
            text='Back',
            size_hint=(None, None),
            size=(100, 50),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),  # White text
            bold=True,
            font_size='16sp',
            pos_hint={'x': 0, 'top': 1}  # Position the button to the top-left corner
        )
        back_button.bind(on_release=self.go_back_to_main)

        # Add the back button to the visualization page directly
        visualization_page.add_widget(back_button)

        # Add the new screen to the screen manager
        self.root.add_widget(visualization_page)

        # Optionally switch to the visualization page here
        # self.root.current = 'visualization_page'



    def go_back_to_main(self, instance):
        # Clear the visualization layout
        self.visualization_layout.clear_widgets()

        # Switch back to the main screen
        self.root.transition = SlideTransition(direction='right')
        self.root.current = 'main'

        
    def create_journey_detail_page(self):
        # Similar structure as visualization
        self.journey_detail_layout = BoxLayout(orientation='vertical')

        # Create a small back button
        back_button = Button(text='←', size_hint=(None, None), size=(84, 84))
        back_button.bind(on_release=self.go_to_main)

        # Create a horizontal layout for the back button and main content
        top_layout = BoxLayout(size_hint_y=None, height=44)
        top_layout.add_widget(back_button)  # Add back button to the top layout

        # Add the top layout to the main layout
        self.journey_detail_layout.add_widget(top_layout)

        # Add a label for the journey details title
        self.journey_detail_label = Label(text='Journey Details', size_hint_y=None, height=44)
        self.journey_detail_layout.add_widget(self.journey_detail_label)

        # Placeholder for journey details content
        self.journey_detail_content = Label(text='[Journey Details Here]', size_hint_y=None, height=200)
        self.journey_detail_layout.add_widget(self.journey_detail_content)

        # Create a new screen for journey details if it doesn't exist
        if 'journey_details' not in [screen.name for screen in self.root.screens]:
            self.journey_detail_screen = Screen(name='journey_details')
            self.journey_detail_screen.add_widget(self.journey_detail_layout)
            self.root.add_widget(self.journey_detail_screen)
        else:
            self.journey_detail_screen = self.root.get_screen('journey_details')
            self.journey_detail_screen.clear_widgets()  # Clear existing widgets to refresh
            self.journey_detail_screen.add_widget(self.journey_detail_layout)


    def add_metro_map(self):
        metro_map = defaultdict(list)
    # Adding Red Line stations
        red_line_stations = [
            # (station1, station2, time, distance)
            ('Miyapur', 'JNTU_College', 2, 2000),
            ('JNTU_College', 'KPHB_Colony', 3, 2200),
            ('KPHB_Colony', 'Kukatpally', 2, 1800),
            ('Kukatpally', 'Balanagar', 4, 3200),
            ('Balanagar', 'Moosapet', 3, 2500),
            ('Moosapet', 'Bharatnagar', 3, 2600),
            ('Bharatnagar', 'Erragadda', 2, 1900),
            ('Erragadda', 'ESI_Hospital', 3, 2100),
            ('ESI_Hospital', 'SR_Nagar', 2, 1800),
            ('SR_Nagar', 'Ameerpet', 3, 2300),
            ('Ameerpet', 'Punjagutta', 2, 1800),
            ('Punjagutta', 'Errum_Manzil', 3, 2400),
            ('Errum_Manzil', 'Khairatabad', 2, 1600),
            ('Khairatabad', 'Lakdi_Ka_Pul', 2, 1800),
            ('Lakdi_Ka_Pul', 'Assembly', 3, 2200),
            ('Assembly', 'Nampally', 3, 2100),
            ('Nampally', 'Gandhi_Bhavan', 2, 1500),
            ('Gandhi_Bhavan', 'Osmania_Medical_College', 2, 1700),
            ('Osmania_Medical_College', 'MG_Bus_Station', 2, 1600),
            ('MG_Bus_Station', 'Malakpet', 3, 2000),
            ('Malakpet', 'New_Market', 2, 1600),
            ('New_Market', 'Musarambagh', 2, 1700),
            ('Musarambagh', 'Dilsukhnagar', 3, 2300),
            ('Dilsukhnagar', 'Chaitanyapuri', 2, 1600),
            ('Chaitanyapuri', 'Victoria_Memorial', 2, 1800),
            ('Victoria_Memorial', 'LB_Nagar', 3, 2500),
        ]
        
        # Adding Blue Line stations
        blue_line_stations = [
            ('Raidurg', 'Hitec_City', 2, 1600),
            ('Hitec_City', 'Durgam_Cheruvu', 2, 1600),
            ('Durgam_Cheruvu', 'Madhapur', 2, 1700),
            ('Madhapur', 'Peddamma_Temple', 2, 1800),
            ('Peddamma_Temple', 'Jubilee_Hills_Check_Post', 3, 2100),
            ('Jubilee_Hills_Check_Post', 'Jubilee_Hills_Road_No_5', 2, 1700),
            ('Jubilee_Hills_Road_No_5', 'Yousufguda', 2, 1600),
            ('Yousufguda', 'Madhura_Nagar', 2, 1600),
            ('Madhura_Nagar', 'Ameerpet', 3, 2200),
            ('Ameerpet', 'Begumpet', 3, 2000),
            ('Begumpet', 'Prakash_Nagar', 2, 1700),
            ('Prakash_Nagar', 'Rasoolpura', 2, 1800),
            ('Rasoolpura', 'Paradise', 3, 2200),
            ('Paradise', 'JBS_Parade_Ground', 3, 2200),
            ('JBS_Parade_Ground', 'Secunderabad_East', 2, 1500),
            ('Secunderabad_East', 'Mettuguda', 3, 2100),
            ('Mettuguda', 'Tarnaka', 2, 1600),
            ('Tarnaka', 'Habsiguda', 3, 2200),
            ('Habsiguda', 'NGRI', 2, 1800),
            ('NGRI', 'Stadium', 2, 1700),
            ('Stadium', 'Uppal', 3, 2200),
            ('Uppal', 'Nagole', 3, 2300),
        ]
        
        # Adding Green Line stations
        green_line_stations = [
            ('JBS_Parade_Ground', 'Secunderabad_West', 2, 1500),
            ('Secunderabad_West', 'Gandhi_Hospital', 2, 1600),
            ('Gandhi_Hospital', 'Musheerabad', 3, 2000),
            ('Musheerabad', 'RTC_Cross_Roads', 2, 1700),
            ('RTC_Cross_Roads', 'Chikkadpally', 2, 1500),
            ('Chikkadpally', 'Narayanguda', 2, 1600),
            ('Narayanguda', 'Sultan_Bazaar', 2, 1600),
            ('Sultan_Bazaar', 'MG_Bus_Station', 3, 2200),
        ]
       
        # Helper function to add connections
        def add_connections(stations):
            for station1, station2, time, distance in stations:
                metro_map[station1].append(Pairs(station2, time, distance))
                metro_map[station2].append(Pairs(station1, time, distance))
        
        # Add all lines to the map
        add_connections(red_line_stations)
        add_connections(blue_line_stations)
        add_connections(green_line_stations)
        return metro_map

    def map_stations_to_numbers(self, metro_map):
        station_names = list(metro_map.keys())
        return {station: index for index, station in enumerate(station_names)}

    def map_numbers_to_stations(self, str_to_num):
        return {index: station for station, index in str_to_num.items()}


    def find_path(self, instance):
        source = self.source_button.text
        destination = self.destination_button.text
        
        if source not in self.str_to_num or destination not in self.str_to_num:
            self.show_popup("Error", "Invalid station names.")
            return

        source_num = self.str_to_num[source]
        destination_num = self.str_to_num[destination]
        self.current_mode = 'distance' if self.mode_button.text == 'Distance' else 'time'
        
        distance, path = self.cached_shortest_path(source_num, destination_num, self.current_mode)

        if distance != float('inf') and path is not None:
            self.current_path = path
            
            journey_details = []
            total_distance = 0
            total_time = 0
            
            for i in range(len(path) - 1):
                station_a = path[i]
                station_b = path[i + 1]
                leg_distance = self.get_distance_between_stations(station_a, station_b)
                leg_time = self.get_time_between_stations(station_a, station_b)
                
                journey_details.append(f"{station_a} to {station_b}: Distance = {leg_distance}m, Time = {leg_time} min")
                total_distance += leg_distance
                total_time += leg_time
            
            journey_summary = f"Total Distance: {total_distance}m, Total Time: {total_time} min"
            journey_details.append(journey_summary)

            # Update the journey detail screen and navigate to it
            self.journey_detail_screen.update_journey_info(journey_details)
            self.root.transition = SlideTransition(direction='left')
            self.root.current = 'journey_details'
            
        else:
            self.current_path = None
            self.show_popup("Result", "No path found.")

    def get_distance_between_stations(self, station_a, station_b):
        for connection in self.metro_map[station_a]:
            if connection.station == station_b:
                return connection.distance
        return float('inf')  # Return infinity if no connection exists

    def get_time_between_stations(self, station_a, station_b):
        for connection in self.metro_map[station_a]:
            if connection.station == station_b:
                return connection.time
        return float('inf')  # Return infinity if no connection exists


    class CustomPopup(Popup):
        def __init__(self, title, message, **kwargs):
            super().__init__(**kwargs)
            self.title = title
            self.content = self.create_content(message)
            self.size_hint = (0.8, 0.5)

        def create_content(self, message):
            layout = BoxLayout(orientation='vertical', padding=10)

            # Close button (X)
            close_button = Button(text='✖', size_hint_y=None, height=40)
            close_button.bind(on_release=self.dismiss)

            # Message label
            message_label = Label(text=message, size_hint_y=None, height=100)

            layout.add_widget(close_button)
            layout.add_widget(message_label)

            return layout

    # Usage
    def show_popup(self, title, message):
        popup = self.CustomPopup(title=title, message=message)
        popup.open()




    def visualize_metro_map(self, instance):
        self.suppress_popup = True  # Prevent popups during this operation
        self.find_path(instance)  # Try to find the path

        if self.current_path is None or len(self.current_path) == 0:
            self.suppress_popup = False  # Reset the flag
            return

        self.suppress_popup = False  # Reset flag for future calls

        try:
            self.visualization_layout.clear_widgets()  # Clear previous visualizations
            G = nx.Graph()

            # Define node colors for different metro lines
            line_colors = {
                'red': {'Miyapur', 'JNTU_College', 'KPHB_Colony', 'Kukatpally', 'Balanagar', 'Moosapet',
                         'Bharatnagar', 'Erragadda', 'ESI_Hospital', 'SR_Nagar', 'Ameerpet',
                         'Punjagutta', 'Errum_Manzil', 'Khairatabad', 'Lakdi_Ka_Pul', 'Assembly',
                         'Nampally', 'Gandhi_Bhavan', 'Osmania_Medical_College', 'MG_Bus_Station',
                         'Malakpet', 'New_Market', 'Musarambagh', 'Dilsukhnagar', 'Chaitanyapuri',
                         'Victoria_Memorial', 'LB_Nagar'},
                'blue': {'Raidurg', 'Hitec_City', 'Durgam_Cheruvu', 'Madhapur', 'Peddamma_Temple',
                          'Jubilee_Hills_Check_Post', 'Jubilee_Hills_Road_No_5', 'Yousufguda',
                          'Madhura_Nagar', 'Ameerpet', 'Begumpet', 'Prakash_Nagar', 'Rasoolpura',
                          'Paradise', 'JBS_Parade_Ground', 'Secunderabad_East', 'Mettuguda',
                          'Tarnaka', 'Habsiguda', 'NGRI', 'Stadium', 'Uppal', 'Nagole'},
                'green': {'JBS_Parade_Ground', 'Secunderabad_West', 'Gandhi_Hospital', 'Musheerabad',
                           'RTC_Cross_Roads', 'Chikkadpally', 'Narayanguda', 'Sultan_Bazaar',
                           'MG_Bus_Station'},
                'interchange': {'MG_Bus_Station', 'JBS_Parade_Ground', 'Ameerpet'}
            }

            # Add edges to the graph
            for station, neighbors in self.metro_map.items():
                for neighbor in neighbors:
                    weight = neighbor.distance if self.current_mode == 'distance' else neighbor.time
                    G.add_edge(station, neighbor.station, weight=weight, distance=neighbor.distance, time=neighbor.time)

            # Define positions for nodes
            pos = self.get_node_positions()  # Assume this function is defined elsewhere

            # Draw all nodes in light gray
            nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=10, edgecolors='black')
            nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray', width=1.5, arrows=False)

            # Initialize total distance and time
            total_distance = 0
            total_time = 0
            for i in range(len(self.current_path) - 1):
                node = self.current_path[i]
                next_node = self.current_path[i + 1]
                edge_data = G.get_edge_data(node, next_node)
                if edge_data:
                    total_distance += edge_data['distance']
                    total_time += edge_data['time']

            # Draw path edges
            path_edges = list(zip(self.current_path, self.current_path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='cyan', width=2, alpha=0.6, arrows=False)

            # Adjust label positions to the right of the nodes
            labels = {node: node for node in G.nodes()}
            label_pos = {node: (x + 0.1, y) for node, (x, y) in pos.items()}  # Shift labels to the right

            # Draw labels
            nx.draw_networkx_labels(G, label_pos, labels, font_size=6, verticalalignment='center')

            # Print distances to the console
            distance_legend = []
            for (node1, node2) in path_edges:
                edge_data = G.get_edge_data(node1, node2)
                if edge_data:
                    dist = edge_data['distance']
                    distance_legend.append(f"{node1} to {node2}: {dist} m")

            print("Distances between path nodes:")
            for entry in distance_legend:
                print(entry)
            print(f"Total distance: {total_distance} m")

            # Add total time and total distance to legend
            legend_text = f'Total Distance: {total_distance} m\nTotal Time: {total_time} min'

            plt.text(0.95, 0.95, legend_text, transform=plt.gca().transAxes, fontsize=10,
                     verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.8))

            plt.title('Metro Map Visualization')
            plt.axis('off')

            # Save the visualization using self.user_data_dir
            visualization_path = os.path.join(self.user_data_dir, 'metro_map_visualization.png')
            plt.savefig(visualization_path, bbox_inches='tight', dpi=150)
            plt.close()
            print(self.user_data_dir)

            # Clear the old visualization layout
            self.visualization_layout.clear_widgets()

            # Create a new Image widget to display the visualization
            self.visualization_image = Image(source=visualization_path, allow_stretch=True, keep_ratio=True)

            # Adjust image size based on dimensions
            self.adjust_image_size()

            # Wrap the image in a Scatter widget for zooming functionality
            scatter = Scatter(do_scale=True, do_rotation=False, do_translation=True)
            scatter.add_widget(self.visualization_image)

            # Add to visualization layout
            self.visualization_layout.add_widget(scatter)

            # Force the image to reload
            self.visualization_image.reload()

            # Switch to the visualization page
            self.root.transition = SlideTransition(direction='left')
            self.root.current = 'visualization_page'
        except Exception as e:
            import traceback
            traceback.print_exc()  # Print full stack trace
            self.suppress_popup = False
            self.show_popup("Error", f"Visualization error: {str(e)}")
            return

    def adjust_image_size(self):
        try:
            image_path = os.path.join(self.user_data_dir, 'metro_map_visualization.png')
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at {image_path}")
                
            # Load image with error handling
            image = plt.imread(image_path)
            if image is None:
                raise ValueError("Failed to load image")
                
            image_height, image_width = image.shape[0], image.shape[1]
            
            # Release memory
            del image
            
            # Rest of your sizing code
            if image_height > image_width:
                self.visualization_image.size_hint = (None, 1)
                self.visualization_image.size = (self.root.width * image_width / image_height, self.root.height)
            else:
                self.visualization_image.size_hint = (1, None)
                self.visualization_image.size = (self.root.width, self.root.height * image_height / image_width)
        except Exception as e:
            print(f"Error in adjust_image_size: {e}")

            
    def get_node_positions(self):
        # Define positions for nodes
        scale_x = 1
        scale_y = 2
        return {                # Example positions for Red Line nodes (scaled)
                    'Miyapur': (0 * scale_x, 21 * scale_y),
                    'JNTU_College': (1 * scale_x, 20 * scale_y),
                    'KPHB_Colony': (2 * scale_x, 19 * scale_y),
                    'Kukatpally': (2 * scale_x, 18 * scale_y),
                    'Balanagar': (2 * scale_x, 17 * scale_y),
                    'Moosapet': (2 * scale_x, 16 * scale_y),
                    'Bharatnagar': (2 * scale_x, 15 * scale_y),
                    'Erragadda': (3 * scale_x, 14 * scale_y),
                    'ESI_Hospital': (4 * scale_x, 13 * scale_y),
                    'SR_Nagar': (5 * scale_x, 12 * scale_y),
                    'Ameerpet': (6 * scale_x, 11 * scale_y),
                    'Punjagutta': (7 * scale_x, 10 * scale_y),
                    'Errum_Manzil': (7 * scale_x, 9 * scale_y),
                    'Khairatabad': (7 * scale_x, 8 * scale_y),
                    'Lakdi_Ka_Pul': (7 * scale_x, 7 * scale_y),
                    'Assembly': (8 * scale_x, 6 * scale_y),
                    'Nampally': (9 * scale_x, 5 * scale_y),
                    'Gandhi_Bhavan': (10 * scale_x, 4 * scale_y),
                    'Osmania_Medical_College': (10 * scale_x, 2.5 * scale_y),
                    'MG_Bus_Station': (12 * scale_x, 2 * scale_y),
                    'Malakpet': (13 * scale_x, 1* scale_y),
                    'New_Market': (14 * scale_x, 0 * scale_y),
                    'Musarambagh': (15 * scale_x, -1* scale_y),
                    'Dilsukhnagar': (15 * scale_x, -2 * scale_y),
                    'Chaitanyapuri': (15 * scale_x, -3 * scale_y),
                    'Victoria_Memorial': (16 * scale_x, -4 * scale_y),
                    'LB_Nagar': (17 * scale_x, -5 * scale_y),

                    # Example positions for Blue Line nodes (scaled)
                    'Raidurg': (0 * scale_x, 0 * scale_y),
                    'Hitec_City': (1 * scale_x, 1 * scale_y),
                    'Durgam_Cheruvu': (2 * scale_x, 2 * scale_y),
                    'Madhapur': (2 * scale_x, 3 * scale_y),
                    'Peddamma_Temple': (2 * scale_x, 4 * scale_y),
                    'Jubilee_Hills_Check_Post': (2 * scale_x, 5 * scale_y),
                    'Jubilee_Hills_Road_No_5': (3 * scale_x, 6 * scale_y),
                    'Yousufguda': (3 * scale_x, 7.3 * scale_y),
                    'Madhura_Nagar': (3.5 * scale_x, 9.4 * scale_y),
                    'Ameerpet': (6 * scale_x, 11 * scale_y),
                    'Begumpet': (8 * scale_x, 12 * scale_y),
                    'Prakash_Nagar': (9 * scale_x, 11 * scale_y),
                    'Rasoolpura': (10 * scale_x, 12 * scale_y),
                    'Paradise': (11 * scale_x, 12.5 * scale_y),
                    'JBS_Parade_Ground': (12 * scale_x, 11 * scale_y),
                    'Secunderabad_East': (13 * scale_x, 12 * scale_y),
                    'Mettuguda': (14 * scale_x, 11 * scale_y),
                    'Tarnaka': (15 * scale_x, 10* scale_y),
                    'Habsiguda': (16 * scale_x, 8 * scale_y),
                    'NGRI': (17 * scale_x, 7 * scale_y),
                    'Stadium': (18 * scale_x, 6 * scale_y),
                    'Uppal': (19 * scale_x, 5 * scale_y),
                    'Nagole': (20 * scale_x, 4 * scale_y),

                    # Example positions for Green Line nodes (scaled)
                    'JBS_Parade_Ground': (12 * scale_x, 11 * scale_y),
                    'Secunderabad_West': (12 * scale_x, 10 * scale_y),
                    'Gandhi_Hospital': (12 * scale_x, 9 * scale_y),
                    'Musheerabad': (12 * scale_x, 8 * scale_y),
                    'RTC_Cross_Roads': (12 * scale_x, 7 * scale_y),
                    'Chikkadpally': (12 * scale_x, 6 * scale_y),
                    'Narayanguda': (12 * scale_x, 5 * scale_y),
                    'Sultan_Bazaar': (12 * scale_x, 4 * scale_y),
                    'MG_Bus_Station': (12 * scale_x, 2 * scale_y),
                }



    def display_random_quote(self):
        quote = random.choice(quotes)
        self.ids.quote_label.text = quote  # Ensure 'quote_label' is defined in the VisualizationPage



    def cached_shortest_path(self, source_num, destination_num, mode):
        queue = []
        heapq.heappush(queue, (0, source_num))  # (cost, station)
        
        distances = {source_num: 0}
        previous_nodes = {source_num: None}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_distance > distances.get(current_node, float('inf')):
                continue

            for neighbor in self.metro_map[self.num_to_str[current_node]]:
                distance = current_distance + (neighbor.distance if mode == 'distance' else neighbor.time)
                neighbor_num = self.str_to_num[neighbor.station]

                if distance < distances.get(neighbor_num, float('inf')):
                    distances[neighbor_num] = distance
                    previous_nodes[neighbor_num] = current_node
                    heapq.heappush(queue, (distance, neighbor_num))

        path = []
        current = destination_num
        while current is not None:
            path.append(self.num_to_str[current])
            current = previous_nodes.get(current)

        path.reverse()  # Reverse the path to get it from source to destination

        return distances.get(destination_num, float('inf')), path if distances.get(destination_num, float('inf')) < float('inf') else None

    def go_back_to_main(self, instance):
        try:
            # Clear matplotlib resources
            plt.close('all')
            
            # Clear widgets
            if self.visualization_layout:
                self.visualization_layout.clear_widgets()
            
            # Clear image cache
            if hasattr(self, 'visualization_image'):
                self.visualization_image.source = ''
                
            # Switch back
            self.root.transition = SlideTransition(direction='right')
            self.root.current = 'main'
            
            # Force garbage collection
            gc.collect()
        except Exception as e:
            print(f"Error in go_back_to_main: {e}")

if __name__ == '__main__':
    try:
        MetroMapApp().run()
    except Exception as e:
        print(f"Application error: {e}")
