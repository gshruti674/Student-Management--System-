import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

FILE_NAME = "students.json"


class StudentApp(App):
    title = "Student Management System"

    def build(self):
        self.students = self.load_students()
        self.index = 0

        self.layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.name_label = Label(font_size=24)
        self.roll_label = Label(font_size=20)
        self.course_label = Label(font_size=20)

        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.roll_label)
        self.layout.add_widget(self.course_label)

        self.add_btn = Button(text="Add Student")
        self.edit_btn = Button(text="Edit Student")
        self.delete_btn = Button(text="Delete Student")
        self.prev_btn = Button(text="Previous")
        self.next_btn = Button(text="Next")

        self.add_btn.bind(on_press=self.add_student)
        self.edit_btn.bind(on_press=self.edit_student)
        self.delete_btn.bind(on_press=self.delete_student)
        self.prev_btn.bind(on_press=self.previous_student)
        self.next_btn.bind(on_press=self.next_student)

        self.layout.add_widget(self.add_btn)
        self.layout.add_widget(self.edit_btn)
        self.layout.add_widget(self.delete_btn)
        self.layout.add_widget(self.prev_btn)
        self.layout.add_widget(self.next_btn)

        self.update_student()

        return self.layout

    def load_students(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        return []

    def save_students(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.students, f, indent=4)

    def update_student(self):
        if self.students:
            self.name_label.text = "Name: " + self.students[self.index]["name"]
            self.roll_label.text = "Roll No: " + self.students[self.index]["roll"]
            self.course_label.text = "Course: " + self.students[self.index]["course"]
        else:
            self.name_label.text = "No Students Available"
            self.roll_label.text = ""
            self.course_label.text = ""

    def add_student(self, instance):
        name = TextInput(hint_text="Student Name")
        roll = TextInput(hint_text="Roll Number")
        course = TextInput(hint_text="Course")

        box = BoxLayout(orientation="vertical", spacing=10)

        box.add_widget(name)
        box.add_widget(roll)
        box.add_widget(course)

        save_btn = Button(text="Save")
        box.add_widget(save_btn)

        popup = Popup(
            title="Add Student",
            content=box,
            size_hint=(0.9, 0.7)
        )

        def save_data(btn):
            if not name.text or not roll.text or not course.text:
                return

            self.students.append({
                "name": name.text,
                "roll": roll.text,
                "course": course.text
            })

            self.save_students()
            self.index = len(self.students) - 1
            self.update_student()
            popup.dismiss()

        save_btn.bind(on_press=save_data)
        popup.open()

    def edit_student(self, instance):
        if not self.students:
            return

        name = TextInput(text=self.students[self.index]["name"])
        roll = TextInput(text=self.students[self.index]["roll"])
        course = TextInput(text=self.students[self.index]["course"])

        box = BoxLayout(orientation="vertical", spacing=10)

        box.add_widget(name)
        box.add_widget(roll)
        box.add_widget(course)

        update_btn = Button(text="Update")
        box.add_widget(update_btn)

        popup = Popup(
            title="Edit Student",
            content=box,
            size_hint=(0.9, 0.7)
        )

        def update_data(btn):
            if not name.text or not roll.text or not course.text:
                return

            self.students[self.index]["name"] = name.text
            self.students[self.index]["roll"] = roll.text
            self.students[self.index]["course"] = course.text

            self.save_students()
            self.update_student()
            popup.dismiss()

        update_btn.bind(on_press=update_data)
        popup.open()

    def delete_student(self, instance):
        if not self.students:
            return

        self.students.pop(self.index)

        if self.index >= len(self.students):
            self.index = 0

        self.save_students()
        self.update_student()

    def next_student(self, instance):
        if self.students:
            self.index = (self.index + 1) % len(self.students)
            self.update_student()

    def previous_student(self, instance):
        if self.students:
            self.index = (self.index - 1) % len(self.students)
            self.update_student()


StudentApp().run()