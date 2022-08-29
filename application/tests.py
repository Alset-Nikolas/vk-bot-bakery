from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock
from vk_api.bot_longpoll import VkBotMessageEvent
import settings
from bot.bot import Bot


class Test1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'message': {'date': 1600102810, 'from_id': 548199338, 'id': 89, 'out': 0,
                               'peer_id': 0, 'text': 'м', 'conversation_message_id': 88,
                               'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
                               'is_hidden': False},
                   'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'],
                                   'keyboard': True, 'inline_keyboard': True, 'carousel': False, 'lang_id': 0}},
        'group_id': 198507410, 'event_id': '7eaa4ff72c79d802328422c91cde763d6ee5b4a5'}

    def test_run(self):
        count = 5
        events = [{}] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch("bot.bot.vk_api.VkApi"):
            with patch("bot.bot.VkBotLongPoll", return_value=long_poller_listen_mock):
                bot = Bot("", 0)
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()
                bot.on_event.assert_called_with({})
                assert bot.on_event.call_count == count

    INPUTS = [
        "Привет",
        "/help",
        "bakery",
        "чай",
        "Хлеб",
        "чай",
        "Батон Нарезной",
        '/bakery',
        'Выход',
        '/bakery',
        'Торты',
        'Выход',
        '/bakery',
        'Вафли',
        'Назад',
        'Вафли',
        'Выход',
        '/bakery',
        'Хлеб',
        'Назад',
        'Торты',
        'Назад',
        'Вафли',
        'Вафли Шоколадные',

    ]
    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.HELP_ANSWER,
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["failure_text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step3"]["failure_text"],
        'Описание:\nХлеб — всему голова! Приготовленный с любовью из натуральных'
        ' продуктов он станет основой для вкусного завтрака, '
        'дополнением к сытному обеду, удачным сочетанием для перекуса '
        'на работе или в дороге. Попробуйте подсушить ломтики батона в тостере, '
        'поджарить на сковороде с яйцом или сделать нарядные сэндвичи с мясом и овощами.',
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        'Досрочное завершение сценария.',
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["text"],
        'Досрочное завершение сценария.',
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["text"],
        'Досрочное завершение сценария.',
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step1"]["text"],
        settings.SCENARIOS["/bakery"]["steps"]["step2"]["text"],
        'Описание:\nПриумножь сладкое удовольствие!'
        ' Хрустящие воздушные вафли и восхитительная шоколадная начинка.'
        ' Мы объединили две сладости в одну, чтобы вам было ещё вкуснее во время чаепития.'
        ' Вафли имеют приятный аромат, который достигается за счёт приготовления на натуральном кокосовом масле.'

    ]

    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event["object"]['message']["text"] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch("bot.bot.VkBotLongPoll", return_value=long_poller_mock):
            bot = Bot("", 0)
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()
        # assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            if kwargs["message"] is None:
                print('---------')
                print(kwargs)
                print('-----------')
            real_outputs.append(kwargs["message"])
        for real, expec in zip(real_outputs, self.EXPECTED_OUTPUTS):
            if real != expec:
                print('test_ans=', real)
                print('-' * 50)
                print('expected=', expec)
                print('_' * 50)
        assert real_outputs == self.EXPECTED_OUTPUTS
