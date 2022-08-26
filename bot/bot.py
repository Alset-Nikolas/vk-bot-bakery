import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from log import logger
from keyboard import Keyboard
import settings

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

    def on_event(self, event):
        '''
        :param event: VkBotMessageEvent
        '''
        user_id = event.object['message']['peer_id']

        if event.type != VkBotEventType.MESSAGE_EVENT:
            logger.info(f'не умею обрабатывать {event.type}')
            print(event.object.payload)
            return self.send_text(text_to_send=settings.DEFAULT_ANSWER, user_id=user_id)
        print()
        key = Keyboard(items=['1', '2', '3', '4'], item_in_line=2)
        keyboard = key.create()
        text = event.obj['message']["text"]
        self.send_text('cc', user_id, keyboard)
        # state = UserState.get(user_id=str(user_id))
        # if state is not None:
        #     # continue scenario
        #     self.continue_scenario(text=text, state=state, user_id=user_id)
        # else:
        #     # serch intent
        #
        #     for intent in settings.INTENTS:
        #         log.debug(f"User gets {intent}")
        #         if any(token in text.lower() for token in intent["tokens"]):
        #             # run intent
        #             if intent["answer"]:
        #                 self.send_text(intent["answer"], user_id)
        #             else:
        #                 self.start_scenario(user_id, intent["scenario"], text)
        #             break
        #     else:
        #         self.send_text(settings.DEFAULT_ANSWER, user_id)

    def send_text(self, text_to_send, user_id, keyboard=None):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id,
            keyboard=keyboard
        )
