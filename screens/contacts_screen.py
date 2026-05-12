"""
screens/contacts_screen.py
Add, view, delete emergency contacts.
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivy.clock import Clock

KV = """
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
                theme_icon_color: "Custom"
                icon_color: 0, 0.831, 1, 1
                on_release: root.go_back()

            MDLabel:
                text: "Emergency Contacts"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            MDIconButton:
                icon: "plus"
                theme_icon_color: "Custom"
                icon_color: 0, 0.831, 1, 1
                on_release: root.show_add_dialog()

        # ── Contacts List ──
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: [dp(16), dp(12)]
                spacing: dp(10)
                adaptive_height: True

                MDLabel:
                    text: "EMERGENCY CONTACTS"
                    font_style: "Overline"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(24)

                MDLabel:
                    id: empty_label
                    text: "No contacts added yet.\\nTap + to add emergency contacts."
                    font_style: "Body1"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.533, 0.573, 0.643, 1
                    size_hint_y: None
                    height: dp(80)

                MDBoxLayout:
                    id: contacts_container
                    orientation: "vertical"
                    spacing: dp(8)
                    adaptive_height: True

                # ── Info Card ──
                MDCard:
                    md_bg_color: 0, 0.831, 1, 0.08
                    radius: [dp(12)]
                    padding: [dp(16), dp(12)]
                    size_hint_y: None
                    height: dp(90)
                    margin: [0, dp(20), 0, 0]

                    MDBoxLayout:
                        spacing: dp(12)
                        MDIconButton:
                            icon: "information"
                            theme_icon_color: "Custom"
                            icon_color: 0, 0.831, 1, 1
                            size_hint_x: None
                            width: dp(40)
                        MDLabel:
                            text: "Add family or friends who should be alerted if a fall is detected. Use international format for phone numbers (e.g. +923001234567)."
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.533, 0.573, 0.643, 1
"""

Builder.load_string(KV)


class ContactsScreen(Screen):

    def on_enter(self):
        self.app = App.get_running_app()
        Clock.schedule_once(lambda dt: self._refresh_contacts(), 0.1)

    def _refresh_contacts(self):
        container = self.ids.contacts_container
        container.clear_widgets()

        contacts = self.app.storage.get_contacts()
        self.ids.empty_label.opacity = 1 if not contacts else 0

        for contact in contacts:
            self._add_contact_widget(contact)

    def _add_contact_widget(self, contact: dict):
        from kivymd.uix.card import MDCard
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDIconButton

        card = MDCard(
            md_bg_color=(0.067, 0.094, 0.161, 1),
            radius=[12],
            padding=12,
            size_hint_y=None,
            height=80,
        )

        row = MDBoxLayout(orientation="horizontal", spacing=12)

        icon_box = MDBoxLayout(size_hint_x=None, width=48,
                               pos_hint={"center_y": 0.5})
        from kivymd.uix.button import MDIconButton
        icon = MDIconButton(
            icon="account",
            theme_icon_color="Custom",
            icon_color=(0, 0.831, 1, 1),
        )
        icon_box.add_widget(icon)

        info = MDBoxLayout(orientation="vertical", spacing=4)
        name_label = MDLabel(
            text=contact.get("name", ""),
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Body1",
            size_hint_y=None,
            height=28,
        )
        phone_label = MDLabel(
            text=f"{contact.get('phone','')}  •  {contact.get('relation','')}",
            theme_text_color="Custom",
            text_color=(0.533, 0.573, 0.643, 1),
            font_style="Caption",
            size_hint_y=None,
            height=20,
        )
        info.add_widget(name_label)
        info.add_widget(phone_label)

        delete_btn = MDIconButton(
            icon="delete",
            theme_icon_color="Custom",
            icon_color=(1, 0.231, 0.361, 0.7),
            size_hint_x=None,
            width=40,
        )
        cid = contact["id"]
        delete_btn.bind(on_release=lambda btn, c=cid: self._confirm_delete(c))

        row.add_widget(icon_box)
        row.add_widget(info)
        row.add_widget(delete_btn)
        card.add_widget(row)
        self.ids.contacts_container.add_widget(card)

    def show_add_dialog(self):
        from kivymd.uix.boxlayout import MDBoxLayout

        content = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
            height=220,
            padding=[0, 10, 0, 0],
        )

        self._name_field  = MDTextField(hint_text="Full Name *", mode="rectangle")
        self._phone_field = MDTextField(
            hint_text="Phone (+923001234567) *",
            mode="rectangle",
            input_type="number",
        )
        self._rel_field   = MDTextField(hint_text="Relation (Family/Friend)", mode="rectangle")

        content.add_widget(self._name_field)
        content.add_widget(self._phone_field)
        content.add_widget(self._rel_field)

        self._dialog = MDDialog(
            title="Add Emergency Contact",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self._dialog.dismiss()
                ),
                MDRaisedButton(
                    text="ADD CONTACT",
                    md_bg_color=(0, 0.831, 1, 1),
                    on_release=lambda x: self._save_contact()
                ),
            ],
        )
        self._dialog.open()

    def _save_contact(self):
        name  = self._name_field.text.strip()
        phone = self._phone_field.text.strip()
        rel   = self._rel_field.text.strip() or "Family"

        if not name or not phone:
            self._name_field.error = not name
            self._phone_field.error = not phone
            return

        self.app.storage.add_contact(name, phone, rel)
        self._dialog.dismiss()
        self._refresh_contacts()

    def _confirm_delete(self, contact_id: int):
        dialog = MDDialog(
            title="Delete Contact?",
            text="This contact will no longer receive emergency alerts.",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(1, 0.231, 0.361, 1),
                    on_release=lambda x: [
                        self.app.storage.delete_contact(contact_id),
                        dialog.dismiss(),
                        self._refresh_contacts()
                    ]
                ),
            ]
        )
        dialog.open()

    def go_back(self):
        self.manager.current = "home"
