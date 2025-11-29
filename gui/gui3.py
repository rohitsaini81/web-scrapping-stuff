from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        label = Label(text="Hello Kivy!")
        layout.add_widget(label)

        def show_popup(instance):
            popup = Popup(title='Hello',
                          content=Label(text='Welcome to Kivy GUI!'),
                          size_hint=(0.6, 0.4))
            popup.open()

        button = Button(text="Click Me")
        button.bind(on_press=show_popup)
        layout.add_widget(button)

        return layout

if __name__ == "__main__":
    MyApp().run()

