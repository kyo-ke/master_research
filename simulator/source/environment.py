
class Environment:
    DELTATIME = 1
    TIME = 0
    def __init__(self):
        self.queries = Queue()

    def set_up(self, filename):
        #ハードウェアのセットアップ(from yaml)
        f = open(filename)
        data = yaml.load(f)
        self.number_of_hardware = data["Number_of_hardware"]
        self.hardware_dict = {}
        for i in range(self.number_of_hardware):
            self.hardware_dict[i] = Hardware(i)
        self.service_dict = {}
        for i,d in enumerate(data["Service"]):
            s = Service(self, d)
            self.service_dict[i] = s

    def update(self):
        Environment.TIME += Environment.DELTATIME
        if (self.queries.qsize()) > 0:
            q = self.queries.get()
            q.start()
        for h in self.hardware_dict.values():
            h.update()
        for h in self.hardware_dict.values():
            h.start_next()

    def load_barancer(self):
        pass
