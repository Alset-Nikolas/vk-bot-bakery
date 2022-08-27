import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from log import logger
from bot.keyboard import Keyboard
import settings
import models.user as  user_model
import models.handlers as model_handlers
import bot.handlers_user_answer as handler_user
import bot.handler_bot_answer as handler_bot


class Bot:

    def __init__(self, token, group_id):
        """
        :param group_id: group id из группы vk
        :param token: секретный токен
        """
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            logger.info(f"полученло событие event={event}")
            try:
                self.on_event(event)
            except Exception as er:
                logger.exception(f'Ошибка в обработке события: {er}')

    def check_key_words_start_scenario(self, text_user):
        for intent in settings.INTENTS:
            if any((token in text_user.lower()) or (text_user.lower() in token) for token in intent["tokens"]):
                return intent["scenario_name"]

    def on_event(self, event):
        '''
        :param event: VkBotMessageEvent
        '''
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.object['message']['peer_id']
            text_user = event.object['message']['text']
            state_user = user_model.get_state_user(user_id)
            if state_user is not None:
                # Идти дальше по сценарию
                self.continue_scenario(text_user, user_id)
            else:
                # Проверим хочет ли пользователь начать сценарий по ключевому слову
                scenario_name = self.check_key_words_start_scenario(text_user)
                if scenario_name is not None:
                    self.start_scenario(user_id, scenario_name)
                    self.continue_scenario(text_user, user_id)
                    return
                return self.send_text(text_to_send=settings.DEFAULT_ANSWER, user_id=user_id,
                                      keyboard=Keyboard.get_empty_keyboard())
        logger.info(f'Не умею отвечать на  тип {event.type}')

    def start_scenario(self, user_id, scenario):
        logger.info(f'start_scenario user={user_id}')
        first_step = settings.SCENARIOS[scenario]['first_step']
        if user_model.get_state_user(user_id) is None:
            user_model.registration(user_id, scenario, first_step)

    def check_answer_user(self, text_user, user_id, step_user):
        if step_user['handler_user_text'] is None:
            return True
        handler_user_text = getattr(handler_user, step_user['handler_user_text'])
        return handler_user_text(text_user, user_id)

    def create_keyboard(self, state_user, settings_keyboard):
        if settings_keyboard:
            get_items_keyboard = getattr(model_handlers, settings_keyboard['items_handler'])
            if get_items_keyboard:
                items = get_items_keyboard(state_user.context)
                keyboard_obj = Keyboard(items=items, back_btn=settings_keyboard['add_back_btn'])
                return keyboard_obj.create()
        return Keyboard.get_empty_keyboard()

    def continue_scenario(self, text_user, user_id):
        state_user = user_model.get_state_user(user_id)
        steps = settings.SCENARIOS[state_user.scenario_name]["steps"]
        step_user = steps[state_user.step_name]
        if self.check_answer_user(text_user, user_id, step_user):
            step_user = steps[state_user.step_name]
            keyboard = self.create_keyboard(state_user, step_user['keyboard'])
            self.send_response(user_id, step_user, keyboard)
            user_model.next_step(user_id)
        else:
            self.send_text(step_user['failure_text'], user_id)

    def send_response(self, user_id, step_user, keyboard):
        if step_user['text']:
            self.send_text(step_user['text'], user_id, keyboard)

        handler_response = step_user['handler_response_text']
        if handler_response:
            handler = getattr(handler_bot, handler_response)
            params = handler(user_id)
            if 'text' in params:
                self.send_text(params['text'], user_id, keyboard)
            if 'image' in params:
                self.send_image(params['image'], user_id)

    def send_image(self, image_path, user_id):
        upload = vk_api.VkUpload(self.api)
        photo = upload.photo_messages(image_path)
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self.api.messages.send(peer_id=user_id, random_id=random.randint(0, 2 ** 20), attachment=attachment)

    def send_text(self, text_to_send, user_id, keyboard=None):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id,
            keyboard=keyboard
        )
