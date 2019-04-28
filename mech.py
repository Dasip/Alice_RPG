class Rescuing():
    
    def __init__(self, text, result_text):
        self.actype = 'rescuing'
        self.text = text
        self.result_text = result_text
        
    def do(self, player):
        return player.rescue(self.result_text)
    
    
class Cleaning():
    
    def __init__(self, text, result_text, parent, system, parent_text, new_action):
        self.actype = 'cleaning'
        self.text = text
        self.result_text = result_text
        self.parent = parent
        self.system = system
        self.parent_text = parent_text
        self.new_action = new_action
        
    def do(self, player):
        self.system.text = self.parent_text
        self.system.add_action(self.new_action)
        return player.hack(self.result_text)
    
    
class Helpful():
    
    def __init__(self, text, result_text):
        self.actype = 'helping'
        self.text = text
        self.result_text = result_text
        
    def do(self, player):
        return player.help(self.result_text)
        
        
class Hacking():
    
    def __init__(self, text, result_text, system, parent, unlockable):
        self.actype = 'hacking'
        self.text = text
        self.system = system
        self.result = result_text
        self.parent = parent
        self.unlockable = unlockable
        
    def unlock_hangar(self):
        self.system.text = 'Вы вошли в ангар. В дальней части ангара стоит спасательная капсула. Вы можете: '
        self.system.add_action(Moving('подойти к спасательной капсуле', self.unlockable))    
        
    def do(self, player):
        self.parent.text = '"Мунбридж Хэвикэриэр Мк II" - система функционирует. Вы можете: '
        self.unlock_hangar()
        return player.hack(self.result)
        
        

class Moving():
    
    def __init__(self, text, destination):
        self.actype = 'moving'
        self.text = text
        self.destination = destination
        
    def do(self, player):
        return player.move(self.destination)


class Adding():
    
    def __init__(self, text, item, prize_text, extra_action=None):
        self.actype = 'taking'
        self.text = text
        self.item = item
        self.prize = prize_text
        self.extra_action = extra_action
        
    def do(self, player):
        self.extra_action['object'].add_action(self.extra_action['action'])
        return player.take(self.item, self.prize)
        

class Location():
    
    def __init__(self, name, text, actions=[]):
        self.text = text
        self.name = name
        self.actions = actions[:]
        
    def add_action(self, action):
        self.actions.append(action)
        
    def inform(self):
        return self.text + '; '.join(list(map(lambda x: x.text, self.actions)))
    
    
class Terminal():
    
    def __init__(self, name, text, actions=[]):
        self.name = name
        self.text = text
        self.actions = []
        
    def add_action(self, action):
        self.actions.append(action)    
        
    def inform(self):
        return self.text + '; '.join(list(map(lambda x: x.text, self.actions)))
        

class Person():
    
    def __init__(self, start_loc):
        self.inventory = ['Фонарик']
        self.location = start_loc
        self.rescued = False
        
    def current_loc(self):
        return {
            'text': self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            }        
    
    def hack(self, text):
        return {
            'text': text + self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            }
        
    def move(self, location):
        self.location = location
        return {
            'text': self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            }
    
    def take(self, item, prize_text):
        self.inventory.append(item)
        return {
            'text': prize_text + self.location.inform(),
            'actions': [i.text for i in self.location.actions]
            }
    
    def rescue(self, text):
        self.rescued = True
        return {
            'text': text,
            'actions': []
            }
    
    def help(self, text):
        return {
            'text': text,
            'actions': [i.text for i in self.location.actions]
            }
    
    def activate(self, action):
        if action in list(map(lambda x: x.text, self.location.actions)):
            action = list(filter(lambda x: x.text == action, self.location.actions))[0]
            if action.actype not in ['moving', 'helping']:
                self.location.actions.remove(action)
            return action.do(self)
        else:
            return {
                'text': 'Вы не можете этого сделать. ' + self.location.inform() + '.',
                'actions': [i.text for i in self.location.actions]
                }
     