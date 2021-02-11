from source.service import Microservice
from source.hardware import Hardware
from source.environment import Environment
from queue import Queue
import yaml
import random


class Orchestrator:
    def __init__(self, environment: Environment):
        self.message_queue = Queue()
        self.environment = environment
        self.microservice2hardware = dict()  # str -> str dict

    def choose_replica(self, microservice: str) -> str:
        last_score = 10000  # big number which exceed all possible scores
        for h_name in self.get_hardware(microservice):
            # evaluate each hardware
            h = self.environment.get_hardware(h_name)
            current_score = self.hardware_score(h)
            if(current_score < last_score):
                best_hardware = h
        return best_hardware

    def haerdware_score(self, hardware_name: str) -> float:
        # evaluation logic is implemented here
        return 1.0

    # return Possible list of hardaware for Microservice
    def get_hardware(self, microservice: str) -> list:
        return self.microservice2hardware[microservice]

    def send_message(self, message: Message):
        pass

    def serve_message(self):
        while(not self.message_queue.empty()):
            message = self.message_queue.get()
            to_hardware_name = self.choose_replica(message.to_microservice)
            message.set_target(to_hardware_name)
            send_message(message)
