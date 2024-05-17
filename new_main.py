import base64
import socket
import json
import os
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.core.window import Window
import chardet
# from jnius import autoclass

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error

    # type: ignore
    request_permissions([Permission.CAMERA, Permission.INTERNET])

Builder.load_string('''
<LoadingScreen>:
    FloatLayout:
        Image:
            source: root.get_load_image()
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

<RegistrationScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 5
        padding: [50, 50]
        canvas.before:
            Color:
                rgba: (0.53, 0.00, 0.11, 1)  
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'Registration'
            font_size: 200
            color: (1, 1, 1, 1)
            halign: 'center'
            valign: 'middle'
            padding: [0, 60]  # Use padding instead of padding_y
            bold: True

        TextInput:
            id: user_first_name_input
            hint_text: 'user_first_name'
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.1)  
            pos_hint: {'center_x': 0.5, 'center_y': 0.8}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
            font_size: 50

        TextInput:
            id: user_last_name_input
            hint_text: 'user_last_name'
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.1)  
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
            font_size: 50

        TextInput:
            id: email_input
            hint_text: 'email'
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.1)  
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
            font_size: 50

        TextInput:
            id: age_input
            hint_text: 'age'
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.1)  
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
            font_size: 50

        TextInput:
            id: password_input
            hint_text: 'password'
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.1) 
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
            font_size: 50

        Button:
            text: 'Sign up'
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.2)  
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            background_color: (1, 1, 1, 1)
            color: (0, 0, 0, 1)  # Text color: black
            on_release: root.register(None)
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)  # Outline color: white
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [5]  # Rounded corners radius
                Color:
                    rgba: (0, 0, 0, 0)  # Background color: transparent
                RoundedRectangle:
                    pos: self.x + 5, self.y + 5
                    size: self.width - 6, self.height - 6
                    radius: [8]  # Rounded corners radius

<AuthenticationScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 5
        padding: [50, 50]
        canvas.before:
            Color:
                rgba: (0.53, 0.00, 0.11, 1)
            Rectangle:
                pos: self.pos
                size: self.size

        Image:
            id: logo_image
            source: 'Images_screen/logo.png'
            size_hint_y: None
            height: root.height * 0.4
            pos_hint: {'center_x': 0.5}

        TextInput:
            id: fname_input
            hint_text: 'First name'
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.15)
            pos_hint: {'center_x': 0.5}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)
            font_size: 100

        TextInput:
            id: lname_input
            hint_text: 'Last name'
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.15)
            pos_hint: {'center_x': 0.5}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)
            font_size: 100
        TextInput:
            id: password_input
            hint_text: 'Enter the password'
            password: True
            multiline: False
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.15)
            pos_hint: {'center_x': 0.5}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)
            font_size: 100
        Button:
            text: 'Ready'
            size_hint: (None, None)
            size: (root.width * 0.8, root.height * 0.15)
            pos_hint: {'center_x': 0.5}
            background_color: (1, 1, 1, 1)
            color: (0, 0, 0, 1)
            on_release: root.login(None)
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [5]
                Color:
                    rgba: (0, 0, 0, 0)
                RoundedRectangle:
                    pos: self.x + 5, self.y + 5
                    size: self.width - 6, self.height - 6
                    radius: [8]

<CameraScreen>:
    name: 'camera'
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            resolution: (root.width, root.height)
            play: True
            canvas.before:
                PushMatrix:
                Rotate:
                    angle: -90
                    origin: self.center
            canvas.after:
                PopMatrix
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '100dp'
            on_press: root.capture()

<ResultScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            font_size: 140
            id: date_label
            text: ''
        Label:
            font_size: 140
            id: time_label
            text: ''
        Label:
            font_size: 120
            id: digits_label
            text: ''
        Widget:
            size_hint_y: None
            height: root.height * 0.1  

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: root.height * 0.2  
            spacing: 5  
            pos_hint: {'center_x': 0.5}  

            Button:
                text: 'Save'
                size_hint_x: None
                width: root.width * 0.33  
                on_release: root.save_info()
                font_size: 60

            Button:
                text: 'Retake picture'
                size_hint_x: None
                width: root.width * 0.33  
                on_release: root.retake_photo()
                font_size: 60

            Button:
                text: 'Exit'
                size_hint_x: None
                width: root.width * 0.34
                on_release: app.stop()
                font_size: 60

<SaveResultScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 50]
        Label:
            id: result_label
            text: ''
            font_size: 60
            color: (1, 1, 1, 1)  # Text color: white
            text_size: self.size
            halign: 'center'
            valign: 'middle'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: root.height * 0.2  
            spacing: 5  
            pos_hint: {'center_x': 0.5}  

            Button:
                text: 'Retry again'
                size_hint_x: None
                width: root.width * 0.5  
                on_release: root.try_again()
                font_size: 60    

            Button:
                text: 'Exit'
                size_hint_x: None
                width: root.width * 0.5
                on_release: app.stop()
                font_size: 60
''')


def get_encoding(text):
    encoding = chardet.detect(text.encode())
    return encoding['encoding']


def convert_encoding(text, from_encoding='cp1251', to_encoding='utf-8'):
    try:
        text = text.encode(from_encoding, 'strict')
        text = text.decode(from_encoding, 'strict')
        text = text.encode(to_encoding, 'strict')
        text = text.decode(to_encoding, 'strict')
        return text
    except UnicodeEncodeError as e:
        print(f"Error: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Error: {e}")
        return None

'''
# Get the Camera.Parameters class from the Android API
Camera = autoclass('android.hardware.Camera')
CameraParameters = autoclass('android.hardware.Camera$Parameters')


def get_best_camera_resolution():
    # Open the first back-facing camera on the device
    camera = Camera.open(0)

    # Get the camera parameters
    parameters = camera.getParameters()

    # Get the supported preview sizes
    supported_preview_sizes = parameters.getSupportedPreviewSizes()

    # Find the largest preview size that matches the screen aspect ratio
    screen_aspect_ratio = Window.size[0] / Window.size[1]
    best_preview_size = None
    for size in supported_preview_sizes:
        if abs(size.width / size.height - screen_aspect_ratio) < 0.1:
            if best_preview_size is None or size.width * size.height > best_preview_size.width * best_preview_size.height:
                best_preview_size = size

    # Close the camera
    camera.release()

    return best_preview_size.width, best_preview_size.height
'''

class DatabaseClient:
    def __init__(self, host="192.168.0.12", port=7000):
        self.host = host
        self.port = port

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            # Convert the request to a JSON string
            json_data = json.dumps(request)

            # Add a header to the JSON data (which contains the length of the JSON data)
            header = f"{len(json_data)}".ljust(10)
            data = header.encode() + json_data.encode()

            # Send the data to the server
            s.sendall(data)

            # Receive the response from the server
            response_data = s.recv(1024)
            if response_data:
                try:
                    response = json.loads(response_data.decode())
                    print(response)
                except json.JSONDecodeError:
                    response = {'status': 'error', 'message': 'Server response is not a valid JSON'}
                    print(response)
            else:
                response = {'status': 'error', 'message': 'Server did not respond'}
                print(response)
        return response


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.height_screen = None
        self.width_screen = None
        self.check_file()

    def get_load_image(self):
        self.width_screen = Window.size[0]
        self.height_screen = Window.size[1]
        if self.width_screen == 1080 and self.height_screen == 2400:
            return 'Images_screen/load_image2400x1080.png'
        else:
            return 'Images_screen/load_image.png'

    def check_file(self):
        if os.path.exists("data_about_user.txt"):
            with open("data_about_user.txt", "r") as f:
                content = f.readline()
                if len(content) == 1:
                    Clock.schedule_once(self.go_to_registration_screen, 3)
                elif len(content) > 1:
                    Clock.schedule_once(self.go_to_auth_screen, 3)
                f.close()
        else:
            Clock.schedule_once(self.go_to_registration_screen, 3)

    def go_to_registration_screen(self, dt):
        self.manager.current = 'register'

    def go_to_auth_screen(self, dt):
        self.manager.current = 'auth'


class RegistrationScreen(Screen):
    def register(self, dt):
        client = DatabaseClient(host="192.168.0.12", port=7000)
        first_name = convert_encoding(self.ids.user_first_name_input.text)
        last_name = convert_encoding(self.ids.user_last_name_input.text)
        email_input = convert_encoding(self.ids.email_input.text)
        age_input = convert_encoding(self.ids.age_input.text)
        password_input = convert_encoding(self.ids.password_input.text)

        if not first_name or not last_name or not email_input or not age_input or not password_input:
            print("All fields must be filled in")
            return

        request = {
            'action': 'register',
            'first_name': first_name,
            'last_name': last_name,
            'email': email_input,
            'age': age_input,
            'password': password_input
        }

        response = client.send_request(request)
        if response['status'] == 'success':
            with open("data_about_user.txt", "w") as f:
                f.write("1\n")
                f.write(f"{first_name}\n")
                f.write(f"{last_name}\n")
                f.write(f"{password_input}\n")
                f.write(f"{str(response['current_user_id'])}")
            self.manager.current = 'auth'
        elif response['status'] == 'error':
            print(response['message'])


class AuthenticationScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthenticationScreen, self).__init__(**kwargs)
        if os.path.exists("data_about_user.txt"):
            with open("data_about_user.txt", "r") as f:
                _ = f.readline().strip()
                first_name = f.readline().strip()
                last_name = f.readline().strip()
                password = f.readline().strip()
            self.ids.fname_input.text = first_name
            self.ids.lname_input.text = last_name
            self.ids.password_input.text = password

    def login(self, dt):
        client = DatabaseClient(host="192.168.0.12", port=7000)
        first_name = convert_encoding(self.ids.fname_input.text)
        last_name = convert_encoding(self.ids.lname_input.text)
        password = convert_encoding(self.ids.password_input.text)

        if not first_name or not last_name or not password:
            print("All fields must be filled in")
            return

        first_name = convert_encoding(first_name, "cp1251", "utf-8")
        last_name = convert_encoding(last_name, "cp1251", "utf-8")
        password = convert_encoding(password, "cp1251", "utf-8")
        request = {
            'action': 'login',
            'first_name': first_name,
            'last_name': last_name,
            'password': password
        }

        response = client.send_request(request)
        if response['status'] == 'success':
            self.manager.current = 'camera'
        elif response['status'] == 'error':
            print(response['message'])


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.user_id = None
        #best_resolution = get_best_camera_resolution()
        self.ids.camera.resolution = (1920, 1080)

    def capture(self):
        app_path = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(app_path, "images_dir")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        photo_name = f"photo_{timestamp}.jpg"
        photo_path = os.path.join(images_dir, photo_name)
        self.ids.camera.export_to_png(photo_path)
        print("Photo saved in:", photo_path)

        client = DatabaseClient(host="192.168.0.12", port=7000)
        with open("data_about_user.txt") as f:
            content = f.readlines()
            content = content[4]
            self.user_id = content
        with open(photo_path, 'rb') as file:
            image_data = file.read()
            image_data_base64 = base64.b64encode(image_data).decode('utf-8')
            image_data_length = len(image_data)

        request = {
            'action': 'process_image',
            'user_id': self.user_id,
            'image_data': image_data_base64,
            'image_data_length': str(image_data_length)
        }

        response = client.send_request(request)

        digit_array = response['digit_array']

        result_screen = self.manager.get_screen('result')
        result_screen.update_info(timestamp, digit_array)
        self.manager.current = 'result'


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.date_value = ""
        self.time_value = ""
        self.digits_array = ""
        self.user_id = ""

    def update_info(self, instance, digit_array):
        date_label = self.ids.date_label
        time_label = self.ids.time_label
        digits_label = self.ids.digits_label
        self.date_value = time.strftime("%d.%m.%Y")
        self.time_value = time.strftime("%H:%M")
        self.digits_array = digit_array
        date_label.text = f"Date: {self.date_value}"
        time_label.text = f"Time: {self.time_value}"
        digits_label.text = f"Glucose: {digit_array}"

    def save_info(self):
        client = DatabaseClient(host="192.168.0.12", port=7000)
        with open("data_about_user.txt", "r") as f:
            content = f.readlines()
            self.user_id = content[4]
            request = {
                'action': 'insert_data',
                'user_id': self.user_id,
                'date': self.date_value,
                'time': self.time_value,
                'measurement': self.digits_array
            }
            response = client.send_request(request)
            if response is not None:
                save_result_screen = self.manager.get_screen('save_result')
                if response['status'] == 'success':
                    save_result_screen.ids.result_label.text = 'Success'
                else:
                    save_result_screen.ids.result_label.text = 'Error'
                self.manager.current = 'save_result'

    def retake_photo(self):
        self.manager.current = 'camera'


class SaveResultScreen(Screen):
    def __init__(self, **kwargs):
        super(SaveResultScreen, self).__init__(**kwargs)

    def try_again(self):
        self.manager.current = 'camera'


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(RegistrationScreen(name='register'))
        sm.add_widget(AuthenticationScreen(name='auth'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(SaveResultScreen(name='save_result'))
        return sm


if __name__ == '__main__':
    MainApp().run()