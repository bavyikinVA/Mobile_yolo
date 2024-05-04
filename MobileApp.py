import os
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen
from predict import digit_detection
import database
Builder.load_string('''
<LoadingScreen>:
    FloatLayout:
        Image:
            source: 'Images_screen/load_image.png'  # путь к вашей иконке
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

<RegistrationScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 50]
        canvas.before:
            Color:
                rgba: (0.53, 0.00, 0.11, 1)  # Background color: 88001B
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'Регистрация'
            font_size: 22
            color: (1, 1, 1, 1)  # Text color: white
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            padding_y: 50
        TextInput:
            id: user_first_name_input
            hint_text: 'user_first_name'
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
            
        TextInput:
            id: user_last_name_input
            hint_text: 'user_last_name'
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
        TextInput:
            id: email_input
            hint_text: 'email'
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
        TextInput:
            id: age_input
            hint_text: 'age'
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
        TextInput:
            id: password_input
            hint_text: 'password'
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: black
        Button:
            text: 'Зарегистрироваться'
            size_hint: (None, None)
            size: (200, 60)
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
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
        padding: [50, 50]
        canvas.before:
            Color:
                rgba: (0.53, 0.00, 0.11, 1)  # Background color: 88001B
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            source: 'Images_screen/logo.png'  # путь к вашему логотипу
            height: self.texture_size[1]  # Keep the original height of the image
            width: self.texture_size[0]  # Keep the original width of the image
            pos_hint: {'center_x': 0.5, 'top': 1.0}  # Position in the first third of the screen

        TextInput:
            id: fname_input
            hint_text: 'Имя'
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: white

        TextInput:
            id: lname_input
            hint_text: 'Фамилия'
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: white

        TextInput:
            id: password_input
            hint_text: 'Введите пароль'
            password: True
            multiline: False
            size_hint: (None, None)
            size: (250, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            background_color: (1, 1, 1, 1)
            foreground_color: (0, 0, 0, 1)  # Text color: white
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, None)
            height: self.minimum_height
            padding: [dp(50), dp(50)]
            CheckBox:
                id: remember_me
                group: 'remember'
                active: False
                size_hint: (None, None)
                size: (dp(40), dp(40))
            Label:
                text: 'Запомнить'
                size_hint: (None, None)
                size: (dp(100), dp(40))
                color: (0, 0, 0, 1)  # Text color: white
                font_size: 20
        Button:
            text: 'Начать'
            size_hint: (None, None)
            size: (200, 60)
            pos_hint: {'center_x': 0.5, 'center_y': 0.3} 
            background_color: (1, 1, 1, 1)
            color: (0, 0, 0, 1)  # Text color: white
            on_release: root.login(None)
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


<ResultScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: date_label
            text: ''
        Label:
            id: time_label
            text: ''
        Label:
            id: digits_label
            text: ''
        Button:
            text: 'Сохранить измерения'
            pos_hint: {'center_x': 0.5}
            size_hint: (None, None)
            size: (200, 70)
            on_release: root.save_info()
        Button:
            pos_hint: {'center_x': 0.5}
            text: 'Сделать фото заново'
            size_hint: (None, None)
            size: (dp(200), dp(70))
            on_release: root.retake_photo()
''')


# Экран загрузки
class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.check_file()

    def check_file(self):
        with open("data_about_user.txt", "r") as f:
            content = f.readline()
            if len(content) == 1:
                Clock.schedule_once(self.go_to_registration_screen, 7)
            elif len(content) > 1:
                Clock.schedule_once(self.go_to_auth_screen, 7)
            f.close()

    def go_to_registration_screen(self, dt):
        self.manager.current = 'register'

    def go_to_auth_screen(self, dt):
        self.manager.current = 'auth'


class RegistrationScreen(Screen):
    def register(self, dt):
        database.create_db()
        # database_operations.create_local_db()
        fname = self.ids.user_first_name_input.text
        lname = self.ids.user_last_name_input.text
        email_input = self.ids.email_input.text
        age_input = self.ids.age_input.text
        password_input = self.ids.password_input.text
        registered, current_user_id = database.add_new_user_to_db(fname, lname, email_input, age_input, password_input)
        if registered == "Успешно":
            with (open("data_about_user.txt", "r+") as f):
                content = f.read().strip()
                new_content = f"{str(int(content) + 1)}\n{fname}\n{lname}\n{password_input}\n{str(current_user_id)}"
                f.seek(0)
                f.write(new_content)
                f.truncate()
            self.manager.current = 'auth'


# Экран авторизации
class AuthenticationScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthenticationScreen, self).__init__(**kwargs)
        if os.path.exists("remembered_user.txt"):
            with open("remembered_user.txt", "r") as f:
                fname = f.readline().strip()
                lname = f.readline().strip()
                password = f.readline().strip()
            self.ids.fname_input.text = fname
            self.ids.lname_input.text = lname
            self.ids.password_input.text = password
            self.ids.remember_me.active = True

    def login(self, dt):
        fname = self.ids.fname_input.text
        lname = self.ids.lname_input.text
        password = self.ids.password_input.text
        check_auth, current_user_id = database.authenticate_user(fname, lname, password)
        if check_auth == "Успешно":
            if self.ids.remember_me.active:
                with open("remembered_user.txt", "w") as f:
                    f.write(f"{fname}\n{lname}\n{password}\n{current_user_id}")
            self.manager.current = 'camera'
        elif check_auth == "Ошибка ввода данных":
            self.manager.current = 'auth'


# Экран камеры
class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        # request_permissions([Permission.CAMERA])
        self.camera = Camera(resolution=(1920, 1080), play=True, index=0)
        self.camera.size_hint = (1, 1)
        self.camera.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.camera)

        capture_button = Button(background_normal='Images_screen/button_photo.png', size_hint=(None, None),
                                size=(110, 110))
        capture_button.pos_hint = {'center_x': 0.5, 'y': 0}
        capture_button.bind(on_press=self.capture)
        layout.add_widget(capture_button)

        self.add_widget(layout)

    def capture(self, instance):
        app_path = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(app_path, "images_dir")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        photo_name = f"photo_{timestamp}.jpg"
        photo_path = os.path.join(images_dir, photo_name)
        self.camera.export_to_png(photo_path)
        print("Снимок сохранен в:", photo_path)
        digit_array = digit_detection(photo_path)
        print(digit_array)
        # переход на экран информации
        result_screen = self.manager.get_screen('result')
        result_screen.update_info(timestamp, digit_array)
        self.manager.current = 'result'


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.date_value = ""
        self.time_value = ""
        self.digits_array = ""

    def update_info(self, instance, digit_array):
        date_label = self.ids.date_label
        time_label = self.ids.time_label
        digits_label = self.ids.digits_label
        self.date_value = time.strftime("%d.%m.%Y")
        self.time_value = time.strftime("%H:%M")
        self.digits_array = digit_array
        date_label.text = f"Дата: {self.date_value}"
        time_label.text = f"Время: {self.time_value}"
        digits_label.text = f"Показатели: {digit_array}"

    def save_info(self):
        with open("remembered_user.txt", "r+") as f:
            content = f.readlines()
            user_id = content[3]
            database.insert_data(user_id, self.date_value, self.time_value, self.digits_array)
            # database_operations.add_data_in_dimens_table(self.date_value, self.time_value, self.digits_array)

    def retake_photo(self):
        self.manager.current = 'camera'


# Запуск приложения
class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(RegistrationScreen(name='register'))
        sm.add_widget(AuthenticationScreen(name='auth'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(ResultScreen(name='result'))
        return sm


if __name__ == '__main__':
    MainApp().run()
