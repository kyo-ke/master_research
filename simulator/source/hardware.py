from source.service import Microservice
from source.job import Message

from queue import Queue


class Hardware:
    def __init__(self, environment, hardware_id, number_of_core: int):
        self.hardware_id = hardware_id
        #koredokodetukatteru??
        self.environment = environment
        self.microservice_dict = dict()
        self.cpu_pressure = 0
        self.memory_pressure = 0
        self.number_of_core = number_of_core
        self.message_recieved = Queue()

    def get_env(self):
        return self.environment

    def get_id(self):
        return self.hardware_id

    def deploy(self, microservice: Microservice, name: str):
        self.microservice_dict[name] = microservice

    def recieve_message(self, message: Message):
        self.message_recieved.put(message)

    def deal_message(self):
        capacity = self.message_recieved
        while(capacity > 0):
            self.execute_message(self.message_recieved.get())
            capacity -= 1

    def execute_message(self, message: Message):
        if(message.type == 1):
            m_service = self.microservice_dict[message.to_microservice]
            parent_info = dict()
            parent_info["parent_hardware"] = message.from_hardware
            parent_info["parent_microservice"] = message.from_microservice
            parent_info["parent_job_id"] = message.from_job_id
            m_service.make_job(message.to_job_type, parent_info)
        elif(message.type == 2):
            m_service = self.microservice_dict[message.to_microservice]
            j = m_service.run_job_dict[message.to_job_id]
            j.count_up()
        else:
            pass

    def assign_time(self, envtime):
        # CPUの割り当てはプロセスの要求による
        # 最低限microserviceがidleの時は他のをassignできるようにしておく
        return envtime * self.number_of_core / len(self.microservice_dict)

    def run(self, envtime):
        # 本来は何かの指標によってDELTATIMEを分割する(CPUの実行時間の割り当てを行う)
        self.deal_message()
        assign_time = self.assign_time(envtime)
        for m_service in self.microservice_dict.values():
            m_service.run(assign_time)


if __name__ == "__main__":
    h = Hardware(2)
