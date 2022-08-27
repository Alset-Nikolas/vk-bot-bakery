import os

DEFAULT_ANSWER = "Не знаю как на это ответить.\n" \
                 "Напишите  /help"
HELP_ANSWER = '''
Рад вас приветсвовать в этом чате.
Сейчас я умею отвечать на команды :
/bakery: Помжет найти вам интересующую продукцию
/help: Напишу вам это же сообщение
Общаюсь я с помошью клавиатуры. 
'''

INTENTS = [
    {
        "name": 'Информация о продукте',
        "tokens": ("/start", "/bakery"),
        "scenario_name": "/bakery",
        "answer": None
    },
    {
        "name": 'Написать возможности бота',
        "tokens": ("/help",),
        "scenario_name": "/help",
        "answer": None
    }
]
SCENARIOS = {
    "/bakery": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Какой раздел вас интересует?",
                "handler_response_text": None,
                "handler_user_text": None,
                'failure_text': None,
                "keyboard": {
                    "items_handler": 'get_all_section',
                    "add_back_btn": False,
                },
                "next_step": "step2",
                'jump_back_step': None
            },
            "step2": {
                "text": "Какой продукт вас интересует?",
                "handler_response_text": None,
                "handler_user_text": 'handlers_section',
                'failure_text': 'Ошибка',
                "keyboard": {
                    "items_handler": 'get_product_by_section',
                    "add_back_btn": True,
                },
                "next_step": "step3",
                'jump_back_step': None
            },
            "step3": {
                "text": None,
                "handler_response_text": 'send_product_info',
                "handler_user_text": 'handlers_product',
                'failure_text': 'Ошибка',
                "keyboard": None,
                "next_step": None,
                'jump_back_step': 'step1'
            },

        }
    },
    '/help': {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": HELP_ANSWER,
                "handler_response_text": None,
                "handler_user_text": None,
                'failure_text': None,
                "image": None,
                "keyboard": None,
                "next_step": None,
                'jump_back_step': None
            },
        }
    }

}

SECTIONS = [
    {'name': 'Хлеб'},
    {'name': 'Торты'},
    {'name': 'Вафли'}
]

PRODUCTS = [
    {'name': 'Батон Нарезной',
     'description': 'Хлеб — всему голова! Приготовленный с любовью из '
                    'натуральных продуктов он станет основой для вкусного завтрака, '
                    'дополнением к сытному обеду, удачным сочетанием для перекуса на работе или в дороге.'
                    ' Попробуйте подсушить ломтики батона в тостере, поджарить на сковороде с яйцом'
                    ' или сделать нарядные сэндвичи с мясом и овощами.',
     'photo_url': os.path.join('photo', 'bread1.jpg'),
     'section_name': SECTIONS[0]['name']
     },
    {
        'name': 'Хлеб Сергеевский',
        'description': 'Мягкий «Сергеевский» хлеб выпечен из смеси пшеничной и ржаной муки'
                       ' по особому рецепту на натуральной ржаной закваске.'
                       ' У него пышный ароматный мякиш и тонкая золотистая корочка.',
        'photo_url': os.path.join('photo', 'bread2.jpg'),
        'section_name': SECTIONS[0]['name']
    },
    {
        'name': 'Хлеб Кукурузный',
        'description': 'Ароматный и воздушный, с хрустящей корочкой из запеченного сыра, '
                       'кукурузный хлеб является низкокалорийным продуктом, '
                       'обладающим высоким содержанием клетчатки и насыщенными жирными кислотами.',
        'photo_url': os.path.join('photo', 'bread3.jpg'),
        'section_name': SECTIONS[0]['name']
    },
    {
        'name': 'Торт Ягодный',
        'description': 'Нежным веером раскрывается вкус этого десерта.'
                       ' Сначала вы ощущаете тонкие сливочные ноты крема,'
                       ' напоминающие пломбир, затем легкую ягодную кислинку садовой голубики, '
                       'а завершает эту гармонию вкуса классический светлый бисквит. '
                       'BOCCONTO – наслаждение, тающее во рту!',
        'photo_url': os.path.join('photo', 'cake1.jpg'),
        'section_name': SECTIONS[1]['name']
    },
    {
        'name': 'Чизкейк',
        'description': 'Роскошный десерт для важного события! '
                       'Шёлковый бисквит, покрытый нежным сливочно-сырным кремом,'
                       ' с ягодами голубики и черники, придающими вкусу яркую и '
                       'приятную кислинку, станет прекрасным завершением праздничного вечера.'
                       ' BOCCONTO – наслаждение, тающее во рту!',
        'photo_url': os.path.join('photo', 'cake2.jpg'),
        'section_name': SECTIONS[1]['name']
    },
    {
        'name': 'Торт Шоколадно-Трюфельный',
        'description': 'Идеальный десерт для вашего праздника!'
                       ' Торт «Шоколадно-трюфельный» - это насыщенный шоколадный крем, '
                       'напоминающий по своей текстуре суфле, с нежной сливочной прослойкой,'
                       ' расположенный на темном, с нотками какао, бисквите.'
                       ' Сверху торт украшен витиеватой шоколадной стружкой.',
        'photo_url': os.path.join('photo', 'cake3.jpg'),
        'section_name': SECTIONS[1]['name']
    },
    {
        'name': 'Вафли Сливочные',
        'description': 'Приумножь сладкое удовольствие!'
                       ' Хрустящие воздушные вафли и нежная сливочная начинка.'
                       ' Мы объединили две сладости в одну, чтобы вам было ещё вкуснее во время чаепития.'
                       ' Вафли имеют приятный аромат, '
                       'который достигается за счёт приготовления на натуральном кокосовом масле.',
        'photo_url': os.path.join('photo', 'waffles1.jpg'),
        'section_name': SECTIONS[2]['name']
    },
    {
        'name': 'Вафли Шоколадные',
        'description': 'Приумножь сладкое удовольствие! '
                       'Хрустящие воздушные вафли и восхитительная шоколадная начинка.'
                       ' Мы объединили две сладости в одну, чтобы вам было ещё вкуснее во время чаепития.'
                       ' Вафли имеют приятный аромат,'
                       ' который достигается за счёт приготовления на натуральном кокосовом масле.',
        'photo_url': os.path.join('photo', 'waffles2.jpg'),
        'section_name': SECTIONS[2]['name']
    },
    {
        'name': 'Вафли Шоколадно-Ореховые',
        'description': 'Приумножь сладкое удовольствие!'
                       ' Хрустящие воздушные вафли и восхитительная шоколадно-ореховая начинка. '
                       'Мы объединили две сладости в одну, чтобы вам было ещё вкуснее во время чаепития.'
                       ' Вафли имеют приятный аромат, '
                       'который достигается за счёт приготовления на натуральном кокосовом масле.',
        'photo_url': os.path.join('photo', 'waffles3.jpg'),
        'section_name': SECTIONS[2]['name']
    }
]
