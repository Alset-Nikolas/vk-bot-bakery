from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import typing


class Keyboard:
    def __init__(self, items: typing.List[str], item_in_line: int = 2, back_btn: bool = False, exit_btn=False):
        self.keyboard: VkKeyboard = VkKeyboard(one_time=False)
        self.items: typing.List[str] = items
        self.item_in_line: int = item_in_line
        self.back_btn: bool = back_btn
        self.exit_btn: bool = exit_btn

    def add_back_btn(self):
        """
            Метод для добавления кнопки 'Назад'
        """
        if self.back_btn:
            self.keyboard.add_line()
            self.keyboard.add_button(label='Назад', color=VkKeyboardColor('primary'))

    def add_exit_btn(self):
        """
            Метод для добавления кнопки 'Выход'
        """
        if self.exit_btn:
            self.keyboard.add_line()
            self.keyboard.add_button(label='Выход', color=VkKeyboardColor('primary'))

    def create(self):
        """
            Метод создания клавиатуры
        """
        for i, item in enumerate(self.items):
            if i != 0 and i != len(self.items):
                if i % self.item_in_line == 0:
                    self.keyboard.add_line()
            self.keyboard.add_button(label=item, color=VkKeyboardColor('primary'))
        self.add_back_btn()
        self.add_exit_btn()
        return self.keyboard.get_keyboard()

    @staticmethod
    def get_empty_keyboard():
        """
           Метод для удаления клавиатуры
        """
        return VkKeyboard().get_empty_keyboard()
