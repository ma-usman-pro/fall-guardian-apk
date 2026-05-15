"""
screens/contacts_screen.py
Manage emergency contacts.
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.toast import toast

KV = """
<ContactItem>:
    text: root.name
    secondary_text: root.phone + " (" + root.relation + ")"
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    secondary_theme_text_color: "Custom"
    secondary_text_color: 0.533, 0.573, 0.643, 1

    IconLeftWidget:
        icon: "account"
        theme_text_color: "Custom"
        text_color: 0, 0.831, 1, 1

    IconRightWidget:
        icon: "trash-can-outline"
        theme_text_color: "Custom"
        text_color: 1, 0.231, 0.361, 1
        on_release: root.delete_callback(root.contact_id)

<ContactsScreen>:
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.102, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: "vertical"

        # ── Top Bar ──
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(60)
            padding: [dp(8), dp(8)]
            md_bg_color: 0.067, 0.094, 0.161, 1

            MDIconButton:
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: 0, 0.831, 1, 1
                on_release: root.go_back()

            MDLabel:
                text: "Emergency Contacts"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            MDIconButton:
                icon: "plus"
                theme_text_color: "Custom"
                text_color: 0, 0.902, 0.463, 1
                on_release: root.show_add_dialog()

        ScrollView:
            MDList:
                id: contacts_list
                padding: dp(10)
"""
Builder.load_string(KV)


class ContactItem(TwoLineAvatarIconListItem):
    def __init__(self, contact_id, name, phone, relation, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.relation = relation
        self.delete_callback = delete_callback


# ── THE FIX: Give the dialog content strict height and spacing ──
class AddContactContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(15)
        self.size_hint_y = None
        self.height = dp(220)  # This prevents the overlapping!

        self.name_field = MDTextField(
            hint_text="Full Name", 
            mode="rectangle"
        )
        self.phone_field = MDTextField(
            hint_text="Phone (e.g. 03001234567)", 
            mode="rectangle"
        )
        self.relation_field = MDTextField(
            hint_text="Relation (Family/Friend)", 
            mode="rectangle"
        )
        
        self.add_widget(self.name_field)
        self.add_widget(self.phone_field)
        self.add_widget(self.relation_field)


class ContactsScreen(Screen):
    dialog = None

    def on_enter(self):
        self.app = App.get_running_app()
        self.refresh_list()

    def refresh_list(self):
        self.ids.contacts_list.clear_widgets()
        contacts = self.app.storage.get_contacts()
            
        for c in contacts:
            item = ContactItem(
                contact_id=c["id"],
                name=c["name"],
                phone=c["phone"],
                relation=c.get("relation", "Family"),
                delete_callback=self.delete_contact
            )
            self.ids.contacts_list.add_widget(item)

    def show_add_dialog(self):
        self.dialog_content = AddContactContent()
        self.dialog = MDDialog(
            title="Add Emergency Contact",
            type="custom",
            content_cls=self.dialog_content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=(1, 0.231, 0.361, 1),
                    on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text="ADD CONTACT",
                    md_bg_color=(0, 0.831, 1, 1),
                    on_release=self.save_contact
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def save_contact(self, *args):
        name = self.dialog_content.name_field.text.strip()
        phone = self.dialog_content.phone_field.text.strip()
        relation = self.dialog_content.relation_field.text.strip()

        if not name or not phone:
            toast("Name and Phone are required!")
            return

        self.app.storage.add_contact(name, phone, relation)
        self.refresh_list()
        self.close_dialog()
        toast(f"Added {name} to contacts")

    def delete_contact(self, contact_id):
        self.app.storage.delete_contact(contact_id)
        self.refresh_list()
        toast("Contact deleted")

    def go_back(self):
        self.manager.current = "home"