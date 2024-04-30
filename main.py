from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
import os
import time
from predict import digit_detection

Builder.load_string('''
<LoadingScreen>:
    FloatLayout:
        Image:
            source: 'load_image.png'  # путь к вашей иконке
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

<MainScreen>:
    Label:
        text: 'Main Screen'

''')


# Экран загрузки
class LoadingScreen(Screen):
    def on_enter(self, *args):
        # Запланировать переход на главный экран через 3 секунды
        Clock.schedule_once(self.go_to_camera_screen, 15)

    def go_to_camera_screen(self, dt):
        self.manager.current = 'camera'


# Главный экран
class MainScreen(Screen):
    pass


# Экран камеры
class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)

        # Получить разрешение экрана
        screen_width, screen_height = Window.size

        # Вычислить границы второй части
        part_height = screen_height // 5
        top = part_height
        bottom = part_height * 4

        # Создать прямоугольник для отображения области
        with self.canvas:
            Color(1, 1, 1, 1)  # Белый цвет
            self.rectangle = Rectangle(pos=(0, top), size=(screen_width - 50, part_height))

        # Создать камеру с указанным разрешением и индексом
        self.camera = Camera(resolution=(1920, 1080), play=True, index=0)

        # Изменить размер и положение камеры
        self.camera.size_hint = (1, part_height / screen_height)
        self.camera.pos_hint = {'center_x': 0.5, 'y': 0.5 + (screen_height - part_height) / (2 * screen_height)}

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.camera)

        capture_button = Button(background_normal='siskipiski.png', size_hint=(None, None), size=(150, 150))
        capture_button.pos_hint = {'center_x': 0.5, 'y': 0}
        capture_button.bind(on_press=self.capture)
        layout.add_widget(capture_button)

        self.add_widget(layout)

    def capture(self, instance):
        app_path = os.path.dirname(os.path.abspath(__file__))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        photo_name = f"photo_{timestamp}.jpg"
        photo_path = os.path.join(app_path, photo_name)
        self.camera.export_to_png(photo_path)
        print("Снимок сохранен в:", photo_path)
        digit_array = digit_detection(photo_name)
        print(digit_array)


# Запуск приложения
class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(CameraScreen(name='camera'))
        return sm


if __name__ == '__main__':
    MainApp().run()
