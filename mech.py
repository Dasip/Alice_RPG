# ===================================|| События ||===================================


# класс события спасения игрока
class Rescuing():
    
    def __init__(self, text, result_text):
        # actype - тип события
        self.actype = 'rescuing'
        # text - то, как выводится вариант этого события
        self.text = text
        # result_text - текст испольнения действия
        self.result_text = result_text
        
    def do(self, player):
        # игрок спасается - игра заканчивается
        return player.rescue(self.result_text)
    
    
# класс события расчистки места
class Cleaning():
    
    def __init__(self, text, result_text, parent, system, parent_text, new_action):
        
        self.actype = 'cleaning'
        self.text = text
        self.result_text = result_text
        # parent - локация, в которой происходит действие
        self.parent = parent
        # system - локация, в которой происходят изменения-результаты действия
        self.system = system
        # parent_text - новый текст для изменяемой локации
        self.parent_text = parent_text
        # new_action - новое событие, результат действия, появляющийся в изменяемой 
        self.new_action = new_action
        
    def do(self, player):
        # изменение текста и событий изменяемой локации
        self.system.text = self.parent_text
        self.system.add_action(self.new_action)
        # функция hack игрока отвечает за дополнительного текста
        return player.hack(self.result_text)
    
 
# класс справки
class Helpful():
    
    def __init__(self, text, result_text):
        
        self.actype = 'helping'
        self.text = text
        self.result_text = result_text
        
    def do(self, player):
        # выводит текст справки
        return player.help(self.result_text)
        

# класс взлома терминала
class Hacking():
    
    def __init__(self, text, result_text, system, parent, unlockable):
        
        self.actype = 'hacking'
        self.text = text
        # system - локация, претерпевающая изменения
        self.system = system
        self.result = result_text
        self.parent = parent
        # unlockable - открываемая локация
        self.unlockable = unlockable
        
    def unlock_hangar(self):
        
        self.system.text = 'Вы вошли в ангар. В дальней части ангара стоит спасательная капсула. Вы можете: '
        self.system.add_action(Moving('подойти к спасательной капсуле', self.unlockable))    
        
    def do(self, player):
        
        self.parent.text = '"Мунбридж Хэвикэриэр Мк II" - система функционирует. Вы можете: '
        self.unlock_hangar()
        # игрок выводит доп. текст
        return player.hack(self.result)
        
        
# класс движения игрока
class Moving():
    
    def __init__(self, text, destination):
        
        self.actype = 'moving'
        self.text = text
        # destination - локация, в которую перейдет игрок при исполнении
        self.destination = destination
        
    def do(self, player):
        # игрок перемещается в другую локацию
        return player.move(self.destination)


# класс добавления предмета в инвентарь
class Adding():
    
    def __init__(self, text, item, prize_text, extra_action=None):
        
        self.actype = 'taking'
        self.text = text
        # item - добавляемый предмет
        self.item = item
        # prize - текст о добавлении предмета
        self.prize = prize_text
        # extra_action - добавление события в какую-то локацию
        self.extra_action = extra_action
        
    def do(self, player):
        
        self.extra_action['object'].add_action(self.extra_action['action'])
        # в инвентарь игрока добавляется новый предмет
        return player.take(self.item, self.prize)
    
# ===================================|| ======= ||===================================        
# ===================================|| Локации ||===================================

# класс локации
class Location():
    
    def __init__(self, name, text, actions=[]):
        
        self.text = text
        self.name = name
        # Список действий (классов)
        self.actions = actions[:]
        
    # добавление действий в список
    def add_action(self, action):
        
        self.actions.append(action)
        
    # возвращает текст локации и список действий для игрока
    def inform(self):
        
        return self.text + '; '.join(list(map(lambda x: x.text, self.actions)))
    
    
# класс терминала
# уже, честно, непонятно, зачем я его делал
# но я хотел сделать нормальный взлом с вводом пароля в строку
class Terminal():
    
    def __init__(self, name, text, actions=[]):
        
        self.name = name
        self.text = text
        self.actions = []
        
    def add_action(self, action):
        
        self.actions.append(action)    
        
    def inform(self):
        
        return self.text + '; '.join(list(map(lambda x: x.text, self.actions)))
        
# ===================================|| ======= ||===================================    
# ===================================|| Персонаж ||===================================    

# игрок
class Person():
    
    def __init__(self, start_loc):
        
        self.inventory = ['Фонарик']
        self.location = start_loc
        self.rescued = False
        
    # возвращает весь текст своей локации
    # и действия
    def current_loc(self):
        
        return {
            
            'text': self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            
            }    
    
    # возвращает весь текст своей локации и дополнительный текст
    # и действия
    def hack(self, text):
        
        return {
            
            'text': text + self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            
            }
        
    # перемешает игрока в другую локацию
    # сразу же возвращает текст новой локации
    def move(self, location):
        
        self.location = location
        
        return {
            
            'text': self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            
            }
    
    # добавляет новый предмет в инвентарь
    # возвращает текст локации и дополнительный текст
    def take(self, item, prize_text):
        
        self.inventory.append(item)
        
        return {
            
            'text': prize_text + self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            
            }
    
    # Возвращает какой-то текст
    # заканчивает игру
    def rescue(self, text):
        
        self.rescued = True
        
        return {
            
            'text': text,
            'actions': []
            
            }
    
    # возвращает текст справки
    def help(self, text):
        
        return {
            
            'text': text,
            'actions': [i.text for i in self.location.actions]
            
            }
    
    # функция взаимодействия с событиями
    # на вход приходит название события
    def activate(self, action):
        
        # проверяется, если событие есть в списке (по названию)
        if action in list(map(lambda x: x.text, self.location.actions)):
            
            # событие обновляется (используется класс)
            action = list(filter(lambda x: x.text == action, self.location.actions))[0]
            
            # Проверка типа события - передвижения и справки не должны быть удалены из локации
            if action.actype not in ['moving', 'helping']:
                
                # остальные события удаляются из локации при использовании
                self.location.actions.remove(action)
                
            # возвращается исполнение класса события
            return action.do(self)
        
        # события не было в списке
        else:
            
            # возвращаются только текст локации и действия 
            return {
                
                'text': 'Вы не можете этого сделать. ' + self.location.inform() + '.',
                'actions': [i.text for i in self.location.actions]
                
                }
        
# ===================================|| ======== ||===================================   
