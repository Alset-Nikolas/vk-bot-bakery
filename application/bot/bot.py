import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent
import random
from log import logger
from bot.keyboard import Keyboard
import settings
import models.user as  user_model
import models.handlers as model_handlers
import bot.handlers_user_answer as handler_user
import bot.handler_bot_answer as handler_bot
from models import UserState
import typing


class Bot:

    def __init__(self, token: str, group_id: int, key_word_end='Выход'):
        """
        :param group_id: group id из группы vk
        :param token: секретный токен
        """
        self.token: str = token
        self.group_id: int = group_id
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.token)
        self.long_poller: VkBotLongPoll = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api = self.vk.get_api()

        self.key_word_end_scenario = key_word_end

    def run(self):
        """
            Запуск бота
        """
        for event in self.long_poller.listen():
            logger.info(f"полученло событие event={event}")
            try:
                self.on_event(event)
            except Exception as er:
                logger.exception(f'Ошибка в обработке события: {er}')

    def check_key_words_start_scenario(self, text_user: str) -> str:
        """
            Проверяем текст пользователя на ключевые солова
        """
        for intent in settings.INTENTS:
            if any(token in text_user.lower() for token in intent["tokens"]):
                return intent["scenario_name"]

    def on_event(self, event: VkBotMessageEvent) -> None:
        """
            Обработка события event
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id: int = event.object['message']['peer_id']
            text_user: str = event.object['message']['text']
            state_user: UserState = user_model.get_state_user(user_id)
            if state_user is not None:
                # Идти дальше по сценарию
                self.continue_scenario(text_user, user_id)
            else:
                # Проверим хочет ли пользователь начать сценарий по ключевому слову
                scenario_name: str = self.check_key_words_start_scenario(text_user)
                if scenario_name is not None:
                    self.start_scenario(user_id, scenario_name)
                    return self.continue_scenario(text_user, user_id)
                return self.send_msg(text_to_send=settings.DEFAULT_ANSWER, user_id=user_id,
                                     keyboard=Keyboard.get_empty_keyboard())
        logger.info(f'Не умею отвечать на  тип {event.type}')

    def start_scenario(self, user_id: int, scenario: str) -> None:
        """
            У пользователя user_id начинается сценарий scenario
        """
        logger.info(f'start_scenario user={user_id}')
        first_step: str = settings.SCENARIOS[scenario]['first_step']
        if user_model.get_state_user(user_id) is None:
            user_model.registration(user_id, scenario, first_step)

    def check_answer_user(self, text_user: str, user_id: int, step_user: typing.Dict[str, str]) -> bool:
        """
           Проверяем валидность ответа пользователя 1 из обработчиков handlers_user_answer
        """
        if step_user['handler_user_text'] is None:
            return True
        handler_user_text: typing.Callable = getattr(handler_user, step_user['handler_user_text'])
        return handler_user_text(text_user, user_id)

    def create_keyboard(self, state_user: UserState, settings_keyboard: typing.Dict[str, typing.Any]) -> Keyboard:
        """
           Создаем клавиатуру
        """
        if settings_keyboard:
            get_items_keyboard: typing.Callable = getattr(model_handlers, settings_keyboard['items_handler'])
            if get_items_keyboard:
                items: typing.List[str] = get_items_keyboard(state_user.context)
                keyboard_obj: Keyboard = Keyboard(items=items,
                                                  back_btn=settings_keyboard['add_back_btn'],
                                                  exit_btn=settings_keyboard['add_exit_btn'])
                return keyboard_obj.create()
        return Keyboard.get_empty_keyboard()

    def continue_scenario(self, text_user: str, user_id: int) -> None:
        """
           Проход по сценарию
        """
        state_user: UserState = user_model.get_state_user(user_id)
        steps: typing.Dict[str, typing.Any] = settings.SCENARIOS[state_user.scenario_name]["steps"]
        step_user: typing.Dict[str, typing.Any] = steps[state_user.step_name]
        if not self.express_end_scenario(text_user, user_id):
            if self.check_answer_user(text_user, user_id, step_user):
                step_user: typing.Dict[str, typing.Any] = steps[state_user.step_name]
                keyboard: Keyboard = self.create_keyboard(state_user, step_user['keyboard'])
                self.send_response(user_id, step_user, keyboard)
                user_model.next_step(user_id)
            else:
                self.send_msg(step_user['failure_text'], user_id)

    def express_end_scenario(self, text_user: str, user_id: int) -> bool:
        """
           Обработка выхода из сценария
        """
        if text_user.lower() == self.key_word_end_scenario.lower():
            self.send_msg('Досрочное завершение сценария.', user_id, keyboard=Keyboard.get_empty_keyboard())
            user_model.delete_user_state(user_id)
            return True
        return False

    def send_response(self, user_id: int, step_user: typing.Dict[str, typing.Any], keyboard: Keyboard) -> None:
        """
            Обработка сложного (через handler_bot_answer) ответа пользователю
        """
        if step_user['text']:
            self.send_msg(step_user['text'], user_id, keyboard)

        handler_response: typing.Optional[str] = step_user['handler_response_text']
        if handler_response:
            handler: typing.Callable = getattr(handler_bot, handler_response)
            params: typing.Dict[str, typing.Any] = handler(user_id)
            attachment = None
            if 'image' in params:
                attachment = self.send_image(params['image'])
            if 'text' in params:
                self.send_msg(params['text'], user_id, keyboard, attachment)


    def send_image(self, image_path: str) -> str:
        """
            Обработка сложного (через handler_bot_answer) ответа пользователю
        """
        upload: vk_api.VkUpload = vk_api.VkUpload(self.api)
        photo = upload.photo_messages(image_path)
        owner_id: int = photo[0]['owner_id']
        photo_id: int = photo[0]['id']
        access_key: str = photo[0]['access_key']
        attachment: str = f'photo{owner_id}_{photo_id}_{access_key}'
        return attachment

    def send_msg(self, text_to_send: str, user_id: int, keyboard: Keyboard = None, attachment: str = None):
        """
        Отправка сообщения
        """
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id,
            keyboard=keyboard,
            attachment=attachment
        )
