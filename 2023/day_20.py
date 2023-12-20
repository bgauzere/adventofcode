from abc import abstractmethod, ABC
from typing import Any
from utils import read_content
from dataclasses import dataclass
from tqdm import tqdm
from math import lcm
from collections import deque

import logging

from enum import Enum

class Pulse(Enum):
    HIGH = 1
    LOW = 0

    def __str__(self):
        return "-high-" if self == Pulse.HIGH else "-low-"

@dataclass(frozen=True)
class Message():
    from_who: str
    to_who: str
    content: Pulse

    def __str__(self):
        return f"{self.from_who} {self.content} {self.to_who}"

class Module(ABC):
    def __init__(self, destinations_modules, label):
        self.destinations_modules = destinations_modules
        self.label = label

    @abstractmethod
    def process_pulse(self,pulse:Pulse,from_who:str) -> Message:
        pass

class FlipFlop(Module):
    def __init__(self, destinations_modules, label):
        super().__init__(destinations_modules, label)
        self.status = False
    
    def process_pulse(self,pulse:Pulse,from_who:str):
        messages = []
        if pulse == Pulse.LOW:
            self.status = not self.status 
            pulse_to_send = Pulse.HIGH if self.status else Pulse.LOW
            
            for module in self.destinations_modules:
                messages.append(Message(self.label,module,pulse_to_send))
        return messages

class Conjunction(Module):
    def __init__(self, destinations_modules, label):
        super().__init__(destinations_modules, label)
        self.input_memory = None
        self.input_modules = None

    def set_input(self, input_modules):
        self.input_modules = input_modules
        self.input_memory = {module:Pulse.LOW for module in input_modules}

    def process_pulse(self,pulse:Pulse,from_who:str):
        self.input_memory[from_who] = pulse
        pulse_to_send = Pulse.LOW if all([pulse == Pulse.HIGH for pulse in self.input_memory.values()]) else Pulse.HIGH
        messages = []
        for module in self.destinations_modules:
            messages.append(Message(self.label,module,pulse_to_send))    
        return messages
    


class Broadcaster(Module):
    def __init__(self, destinations_modules, label):
        super().__init__(destinations_modules, label)
        
    def process_pulse(self,pulse:Pulse,from_who:str):
        messages = []
        for module in self.destinations_modules:
            messages.append(Message(self.label,module,pulse))
        return messages
class Button(Module):
    def __init__(self, destinations_modules, label):
        super().__init__(destinations_modules, label)
        
    
    def process_pulse(self,pulse:Pulse,from_who:str):
        raise NotImplementedError


class Dummy(Module):
    def __init__(self, destinations_modules, label):
        super().__init__(destinations_modules, label)
    def process_pulse(self, pulse: Pulse, from_who: str) -> Message:
        if pulse==Pulse.LOW:
            print(f"{cycle = }")
            exit()
        else:
            return [] 


def parse_content(content):
    modules = {}
    conjunction_modules = []
    all_modules_labels = set()
    for l in content:
        modules_dest = [label.strip() for label in l.split("->")[1].split(",")]
        all_modules_labels = all_modules_labels | set(modules_dest)
        
        if l.startswith("broadcaster"):
            broadcaster = Broadcaster(modules_dest,"broadcaster")
            modules["broadcaster"] = broadcaster
        elif l.startswith("%"):
            label = l[1:3]
            flipflop = FlipFlop(modules_dest,label)
            modules[label] = flipflop
        elif l.startswith("&"):
            label = l[1:3]
            conjunction = Conjunction(modules_dest,label)
            modules[label] = conjunction
            conjunction_modules.append(conjunction)
    for conjunction in conjunction_modules:
        conjunction.set_input([module_label for module_label in modules.keys() if conjunction.label in modules[module_label].destinations_modules])
    
    for module_label in all_modules_labels:
        if module_label not in modules.keys():
            logging.info(f"adding {module_label} as Dummy ")
            modules[module_label] = Dummy([],module_label)
    
    return modules

class Detector():
    def __init__(self, messages_to_watch):
        self.to_watch = messages_to_watch
        self.nb_min_cycles = {message: None for message in self.to_watch}

    def detect(self, message:Message, cycle_nb:int):
        logging.error(f"{message} : {cycle_nb}")
        if message in self.to_watch:
            if self.nb_min_cycles[message] is None:
                self.nb_min_cycles[message] = cycle_nb
            # on est arrivés !   
            if all([self.nb_min_cycles[message] is not None for message in self.nb_min_cycles.keys()]):
                print(lcm(*list(self.nb_min_cycles.values())))
                exit()
            
        return
            

def antecedents(modules, module_label):
    return [module for module in modules.keys() if modules[module].destinations_modules and module_label in modules[module].destinations_modules]

def second(content):
    modules = parse_content(content)
    modules["button"] = Button(None,"button")
    antecendts_rx = antecedents(modules,"rx")
    logging.info(f"antecedents de rx : {antecendts_rx}")
    antecendts_kc = antecedents(modules,"kc")
    logging.info(f"antecedents de kc : {antecendts_kc}, {modules['kc']}")
    for ant in antecendts_kc:
        antecendts = antecedents(modules,ant)
        logging.info(f"antecedents de {ant} : {antecendts}")
    #breakpoint()
    # kc est une conjunction. Donc il faut qu'il est reçu un high pulse de chaque antecedent pour envoyer un low pulse
    # Il faut détecter quand il recoit chaque high pusle
    messages_to_watch = [Message(ant,"kc",Pulse.HIGH) for ant in antecendts_kc]
    detector = Detector(messages_to_watch)

    for i in range(1,10000000):
        messages = deque()
        messages.append(Message("button","broadcaster",Pulse.LOW))
    
        while (messages):
            message = messages.popleft()
            detector.detect(message,i)
            logging.info(f"{message}")
            new_messages = modules[message.to_who].process_pulse(message.content,modules[message.from_who].label)
            for next_message in new_messages:
                messages.append(next_message)
                #messages.extend(modules[message.to_who].process_pulse(message.content,modules[message.from_who].label))
    return # never return if dectect



def first(content):
    modules = parse_content(content)
    modules["button"] = Button(None,"button")
    nb_low = 0
    nb_high = 0
    for i in tqdm(range(10000000)):
        messages = [Message("button","broadcaster",Pulse.LOW)]
    
        while (messages):
            message = messages.pop()

            logging.info(f"{message}")
            if message.content == Pulse.LOW:
                nb_low += 1
            else:
                nb_high += 1
            messages.extend(modules[message.to_who].process_pulse(message.content,modules[message.from_who].label))
        logging.info(f"{nb_low = },{nb_high=}")
    return nb_high*nb_low

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format=' %(message)s')
    content = read_content()
    print(second(content))
