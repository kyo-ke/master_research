from source.service import Service, Microservice
from source.hardware import Hardware
from source.orchestrator import Orchestrator
from source.util import Util
from queue import Queue


class Environment:
    DELTATIME = 1
    TIME = 0

    def __init__(self):
        # unused
        self.queries = Queue()
        self.orchestrator = Orchestrator(self)

    def set_up(self, filename):
        # ハードウェアのセットアップ(from yaml)
        self.number_of_hardware, services = Util.load_config(filename)
        self.hardware_dict = {}
        # hardware name should be chaged to str
        for i in range(self.number_of_hardware):
            self.hardware_dict[i] = Hardware(i)
        self.service_dict = {}
        for i, d in enumerate(services):
            s = Service(self, d)
            self.service_dict[i] = s
            # deploy
            for m_name in s.microservices.keys():
                for rep_dict in s.hardware_map[m_name]:
                    for rep_num, harsware_num in rep_dict.items():
                        name = m_name + "_" + str(rep_num)
                        microservice = Microservice(
                            self.harsware_dict[hardware_num],
                            name,
                            s.jobs_of_service[m_name],
                            s.jobs)
                        self.hardware_dict[hardware_num].deploy(
                            microservice, name)

    def update(self):
        Environment.TIME += Environment.DELTATIME
        self.orchestrator.serve_message()
        for h in eslf.hardware_dict.values():
            h.move_message()
        for h in eslf.hardware_dict.values():
            h.run(Environment.DELTATIME)

    def get_orchestrator(self):
        return self.orchestrator

    def get_hardware(self, hardware_name: str) -> Hardware:
        return self.hardware_dict[hardware_name]

    def load_barancer(self):
        pass
