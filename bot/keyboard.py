from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
import typing


class Keyboard:
    def __init__(self, items, item_in_line=2):
        self.keyboard: VkKeyboard = VkKeyboard(one_time=False)
        self.items: typing.List[str] = items
        self.item_in_line: int = item_in_line

    def add_callback(self):
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Назад', color=VkKeyboardColor('primary'), payload='back')

    def create(self):
        for i, item in enumerate(self.items):
            if i != 0 and i != len(self.items):
                if i % self.item_in_line == 0:
                    self.keyboard.add_line()
            self.keyboard.add_callback_button(label=item, color=VkKeyboardColor('primary'), payload=item)
        self.add_callback()
        return self.keyboard.get_keyboard()
