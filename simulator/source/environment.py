from source.hardware import Hardware
from source.orchestrator import Orchestrator


class Environment:
    DELTATIME = 1
    TIME = 0

    def __init__(self):
        self.queries = Queue()
        self.orchestrator = Orchestrator()

    def set_up(self, filename):
        # ハードウェアのセットアップ(from yaml)
        f = open(filename)
        data = yaml.load(f)
        self.number_of_hardware = data["Number_of_hardware"]
        self.hardware_dict = {}
        #hardware name should be chaged to str
        for i in range(self.number_of_hardware):
            self.hardware_dict[i] = Hardware(i)
        self.service_dict = {}
        for i, d in enumerate(data["Service"]):
            s = Service(self, d)
            self.service_dict[i] = s

    def update(self):
        Environment.TIME += Environment.DELTATIME
        self.orchestrator.serve_message():
        for h in eslf.hardware_dict.values():
            h.move_message()
         for h in eslf.hardware_dict.values():
            h.run()

    def get_hardware(self, hardware_name: str) -> Hardware:
        return self.hardware_dict[hardware_name]

    def load_barancer(self):
        pass
