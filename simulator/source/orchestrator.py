from source.job import Message
from queue import Queue
import yaml
import random


class Orchestrator:
    def __init__(self, environment):
        #store Message here
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

    def hardware_score(self, hardware_name: str) -> float:
        # evaluation logic is implemented here
        return 1.0

    # return Possible list of hardaware for Microservice
    def get_hardware(self, microservice: str) -> list:
        return self.microservice2hardware[microservice]

    def recieve_message(self, message: Message):
        self.message_queue.put(message)

    def send_message(self, message: Message):
        #get hardware
        service_name = message.to_microservice
        hardware_name = self.choose_replica(service_name)
        hardware = self.environment.get_hardware(hardware_name)
        #これがいるのかは不明
        Message.to_hardware = hardware_name
        #send message
        hardware.recieve_message(message)

    def serve_message(self):
        while(not self.message_queue.empty()):
            message = self.message_queue.get()
            if(message.to_hardware_name is None):
                to_hardware_name = self.choose_replica(message.to_microservice)
                message.set_target(to_hardware_name)
            send_message(message)

    #using this function for testing
    def number_of_message(self):
        return self.message_queue.qsize()
