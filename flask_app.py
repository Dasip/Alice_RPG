# импортируем библиотеки
# https://dasip.pythonanywhere.com/post2
from flask import Flask, request
import logging, random
import json
from mech import *

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}

# 1030494/7e258428c42e82021619 - waking
# 1030494/d8b49de67720ead9fef6 - engine room
# 1540737/8fcbe7892a1435df9265 - journal
# 1030494/49cfd903a3238a5ff23d - reactor_broken
# 1540737/b0efdd0a4e8959ab782d - reactor_improoved
# 1030494/1d88827892e9f10d1ac5 - hangar 1
# 1656841/a64bb2790416400791a8 - hangar 2
# 1540737/2936cbd673eb75032788 - rescued

# ===================================|| Локации ||===================================
Start_loc = Location('Перекресток', '''Последнее, что вы помните - взрывы и скрежет металла.
Корабль, должно быть, столкнулся с заброшенной космической станцией, на которой вспыхнула эпидемия неизвестного вируса.
Вы, возможно, последний выживший член экипажа. Вам вдруг становится трудно дышать и вы понимаете,
что на корабле остается мало воздуха. Под рукой вы нащупываете ваш фонарик и кладете его в карман брюк. Вы решаете, что будете делать: ''')
Crossing = Location('Перекресток', 'Вы пришли к перекрестку. Вы можете: ')
Hangar = Location('Ангар', 'Вы вошли в ангар. В дальней части ангара стоит спасательная капсула, но вас от нее отрезает обесточенная шлюзовая дверь. Вы можете: ',)
Engine_room = Location('Реакторный отсек', 'Вы вошли в реакторный отсек. У дальней стены мигает терминал реакторной системы. Вы можете: ')
Engine_terminal = Terminal('Реакторный терминал', '"Мунбридж Хэвикэриэр Мк II" - система заблокирована. Вы можете: ')
Capsule = Location('Капсула', 'Шлюз капсулы загородило крепящей балкой. Возможно, вы могли бы ее отодвинуть подходящим инструментом. Вы можете: ')

Capsule.add_action(Moving('отойти от капсулы', Hangar))
Capsule.add_action(Helpful('справка', '''<Справка> Вам выведен текст и возможные варианты действий.
            Просто введите название действия, которое хотите произвести. Ваша задача - решить
            все головоломки и выбраться с корабля живым.'''))

Start_loc.add_action(Moving('войти в реакторный отсек', Engine_room))
Start_loc.add_action(Moving('войти в ангар', Hangar))
Start_loc.add_action(Helpful('справка', '''<Справка> Вам выведен текст и возможные варианты действий.
            Просто введите название действия, которое хотите произвести. Ваша задача - решить
            все головоломки и выбраться с корабля живым.'''))

Crossing.add_action(Moving('войти в реакторный отсек', Engine_room))
Crossing.add_action(Moving('войти в ангар', Hangar))
Crossing.add_action(Helpful('справка', '''<Справка> Вам выведен текст и возможные варианты действий.
            Просто введите название действия, которое хотите произвести. Ваша задача - решить
            все головоломки и выбраться с корабля живым.'''))

Engine_room.add_action(Moving('вернуться на перекресток', Crossing))
Engine_room.add_action(Moving('подойти к терминалу', Engine_terminal))
Engine_room.add_action(Adding('осмотреть отсек', 'Журнал дежурного инженера',
                              'Вы обнаружили журнал дежурного инженера реакторного отсека. В нем записан код от терминала реакторного терминала. ',
                              {'action': Hacking('запустить аварийные реакторы', 'Вы вводите коды из найденного журнала и успешно входите в систему, запуская аварийные реакторы. ',
                                                 Hangar, Engine_terminal, Capsule),
                               'object': Engine_terminal}))
Engine_room.add_action(Helpful('справка', '''<Справка> Вам выведен текст и возможные варианты действий.
            Просто введите название действия, которое хотите произвести. Ваша задача - решить
            все головоломки и выбраться с корабля живым.'''))

Engine_terminal.add_action(Moving('отойти от терминала', Engine_room))
Engine_terminal.add_action(Helpful('справка', '''<Справка> Вам выведен текст и возможные варианты действий.
            Просто введите название действия, которое хотите произвести. Ваша задача - решить
            все головоломки и выбраться с корабля живым.'''))

Hangar.add_action(Moving('вернуться на перекресток', Crossing))
Hangar.add_action(Helpful('справка', '''<Справка> Вам выведен текст и возможные варианты действий.
            Просто введите название действия, которое хотите произвести. Ваша задача - решить
            все головоломки и выбраться с корабля живым.'''))
Hangar.add_action(Adding('осмотреть отсек', 'магнитный грузоподъемный инструмент',
                         'Вы обнаружили магнитный грузоподъемный инструмент. Его можно использовать для передвижения тяжелых металлических грузов. ',
                        {'action': Cleaning('отодвинуть балку', 'Вы включаете магнит и отодвигаете огромную балку от капсулы. ', Capsule, Capsule,
                                            'Перед вами стоит спасательная капсула - ваш путь на волю. Вы можете: ',
                                            Rescuing('сесть в капсулу', 'Вы сели в капсулу и покинули корабль. Поймав сигналы ближайшего корабля, вы направились к нему. Вы спаслись.')),
                         'object': Capsule}))
# ===================================|| ======= ||===================================

@app.route('/rpg', methods=['POST'])
def main2():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)
 
 
def handle_dialog(res, req):
    
    user_id = req['session']['user_id']
 
    if req['session']['new']:
        res['response']['text'] = '''Система управления транспортным кораблем модели "Мунбридж Хэвикэриэр Мк II",
        назовите свое имя...'''
        sessionStorage[user_id] = {
            'first_name': None
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = \
                'Некорректные данные - повторите ввод данных (имя пользователя)...'
            
        else:
            the_hero = Person(Start_loc)
            sessionStorage[user_id]['first_name'] = first_name
            sessionStorage[user_id]['hero'] = the_hero
            sessionStorage[user_id]['actions'] = [i.text for i in the_hero.location.actions]
            a = sessionStorage[user_id]['hero']
            create_mess(res, {'text': 'Доступ открыт. Добро пожаловать, ' + first_name.title()\
                              + '. ' + a.current_loc()['text'],
                              'actions': sessionStorage[user_id]['actions']
                              })
        
    else:
        action = req['request']['command']
        for i in sessionStorage[user_id]['actions']:
            if i in action:
                action = i
                break
        
        ans = sessionStorage[user_id]['hero'].activate(action)
        create_mess(res, ans)
        if sessionStorage[user_id]['hero'].rescued:
            res['response']['end_session'] = True
        sessionStorage[user_id]['actions'] = ans['actions']
            
def create_mess(res, mess):
    
    #res['response']['card'] = {}
    #res['response']['card']['type'] = 'BigImage'
    #res['response']['card']['image_id'] = mess['pict']   
    #res['response']['card']['title'] = mess['text']
    res['response']['text'] = mess['text']
    res['response']['buttons'] = create_buttons(mess)
            
            
def create_buttons(mess):
    return [
        {
            'title': text,
            'hide': True
            } for text in mess['actions']
        ]       

def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name', то возвращаем её значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)



if __name__ == '__main__':
    app.run()