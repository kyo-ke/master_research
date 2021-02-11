from source.service import Microservice
from source.environment import Environment
from source.job import Message

from queue import Queue


class Hardware:
    def __init__(self, number_of_core: int):
        self.microservice_dict = dict()
        self.cpu_pressure = 0
        self.memory_pressure = 0
        self.number_of_core = number_of_core
        self.message_recieved = Queue()
        self.message_execute = Queue()

    def deploy(self, microservice: Microservice, name: str):
        self.microservice_dict[name] = microservice

    def add_pressure(self, cpu_pressure: int, memory_pressure: int):
        self.cpu_pressure += cpu_pressure
        self.memory_pressure += memory_pressure

    def deal_message(self):
        capacity = self.message_recieved
        while(capacity > 0):
            self.execute_message(self.message_execute.get())

    def execute_message(self, message: Message):
        if(message.type == 1):
            m_service = self.microservice_dict[message.to_microservice]
            m_service.make_job(message.to_job_type)
        else if(message.type == 2):
            m_service = self.microservice_dict[message.to_microservice]
            j = m_service.run_job_dict[message.to_job_id]
            j.count()
        else:
            pass

    def move_message(self):
        while(not self.message_recieved.empty()):
            self.message_execute.put(self.message_recieved.get())

    def assign_time(self):
        #CPUの割り当てはプロセスの要求による
        #最低限microserviceがidleの時は他のをassignできるようにしておく
        return Environment.DELTATIME * self.number_of_core / len(self.microservice_dict)

    def run(self):
        # 本来は何かの指標によってDELTATIMEを分割する(CPUの実行時間の割り当てを行う)
        self.deal_message()
        assign_time = self.assign_time()
        for m_service in self.microservice_dict.values():
            m_service.run(assign_time)
