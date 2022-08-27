from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
import typing


class Keyboard:
    def __init__(self, items, item_in_line=2, back_btn=False):
        self.keyboard: VkKeyboard = VkKeyboard(one_time=False)
        self.items: typing.List[str] = items
        self.item_in_line: int = item_in_line
        self.back_btn = back_btn

    def add_back_btn(self):
        if self.back_btn:
            self.keyboard.add_line()
            self.keyboard.add_button(label='Назад', color=VkKeyboardColor('primary'))

    def create(self):
        for i, item in enumerate(self.items):
            if i != 0 and i != len(self.items):
                if i % self.item_in_line == 0:
                    self.keyboard.add_line()
            self.keyboard.add_button(label=item, color=VkKeyboardColor('primary'))
        self.add_back_btn()
        return self.keyboard.get_keyboard()

    @staticmethod
    def get_empty_keyboard():
        return VkKeyboard().get_empty_keyboard()