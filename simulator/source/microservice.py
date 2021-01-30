from queue import Queue
import yaml
import random
#yamlファイルとかにセットアップ情報書く？


"""
Environentにいくつかのハードウェア がある
その上でServiceが動いてる
"""
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
        

class Service:
    def __init__(self, environment, service_dict):
        self.environment = environment
        self.service_id = service_dict["service_id"]
        self.query_types = service_dict["query"]
        self.microservice_dict = {}
        for t in service_dict["microservices"].items():
            self.microservice_dict[t[0]] = {}
            for j in range(1,t[1] + 1):
                m = Microservice(self.environment, self, t[0], t[1], self.environment.hardware_dict[service_dict["hardware_map"][t[0]][j]])
                self.microservice_dict[m.microservice_id][m.replication_id] = m
        self.start_dict = {}
        self.end_dict = {}
    
    def generate_query_id(self):
        return random.randrange(10)

    def generate_next(self, generated_query, query_data, s_n):
        node = Service_node(self, generated_query, self.microservice_dict[s_n][map_service()], query_data["nodes"][s_n]["cpu_pressure"], query_data["nodes"][s_n]["memory_pressure"], query_data["nodes"][s_n]["remain_time"])
        for n_s_n in query_data["nodes"][s_n]["next_nodes"]:
            if(n_s_n is not None):
                node.next_nodes.append(self.generate_next(generated_query, query_data, n_s_n))
        return node

    def generate_query(self, query_id):
        #replicaまで決めたクエリの作成をする
        query_data = self.query_types[query_id]
        generated_query = Query(self, self.generate_query_id(),query_data["number_of_service"])
        for s_n in query_data["start_nodes"]:
            node = Service_node(self, generated_query, self.microservice_dict[s_n][map_service()], query_data["nodes"][s_n]["cpu_pressure"], query_data["nodes"][s_n]["memory_pressure"], query_data["nodes"][s_n]["remain_time"])
            for n_s_n in query_data["nodes"][s_n]["next_nodes"]:
                node.next_nodes.append(self.generate_next(generated_query, query_data, n_s_n))
            generated_query.start_service_nodes.append(node)
        return generated_query

def map_service():
    return 1

class Microservice:
    def __init__(self, environment, service, microservice_id,replication_id, hardware):
        self.environment = environment
        self.service = service
        self.microservice_id = microservice_id
        self.replication_id = replication_id
        self.hardware = hardware


class Hardware:
    def __init__(self, hardware_id):
        self.hardware_id = hardware_id
        self.cpu_pressure = 0
        self.memory_pressure = 0
        self.service_node_queue = Queue()
        self.service_node_end_queue = Queue()
    
    def append_service_node(self, service_node):
        self.service_node_queue.put(service_node)

    def update(self):
        for i in range(self.service_node_queue.qsize()):
            s = self.service_node_queue.get()
            s.remain_time -= Environment.DELTATIME
            if s.remain_time > 0:
                self.service_node_queue.put(s)
            else:
                self.service_node_end_queue.put(s)
    
    def start_next(self):
        while self.service_node_end_queue.qsize() > 0:
            s = self.service_node_end_queue.get()
            s.end_service_node()


class Service_node:
    def __init__(self, service, query, microservice, cpu_pressure, memory_pressure, remain_time):
        self.service = service
        self.query = query
        self.microservice = microservice
        self.cpu_pressure = cpu_pressure
        self.memory_pressure = memory_pressure
        self.remain_time = remain_time
        self.next_nodes = []#list of service_node
        self.wait_time = 0
    
    def start_nextservice(self):
        print(Environment.TIME)
        for node in self.next_nodes:
            node.start_service_node()

    def start_service_node(self):
        h = self.microservice.hardware
        h.append_service_node(self)
        h.cpu_pressure += self.cpu_pressure
        h.memory_pressure += self.memory_pressure
    
    def end_service_node(self):
        h = self.microservice.hardware
        h.cpu_pressure -= self.cpu_pressure
        h.memory_pressure -= self.memory_pressure
        self.start_nextservice()
        self.query.number_of_remaining_service -= 1
        if(self.query.number_of_remaining_service == 0):
            self.query.finish()

#どのレプリカを走らせるか決定した後のクエリ
class Query:
    def __init__(self, service , query_id, number_of_service):
        self.service = service
        self.query_id = query_id
        self.number_of_remaining_service = number_of_service
        self.start_service_nodes = []
    
    def start(self):
        self.service.start_dict[self.query_id] = Environment.TIME
        for node in self.start_service_nodes:
            node.start_service_node()

    def finish(self):
        self.service.end_dict[self.query_id] = Environment.TIME
    


if __name__ == "__main__":
    filename = "/Users/kariyagouyuu/Desktop/Master_Research/master_research/simulator/config/test_service.yml"
    ENV = Environment()
    ENV.set_up(filename)
    print(ENV.hardware_dict)
    for m_dict in ENV.service_dict[0].microservice_dict.values():
        for m in m_dict.values():
            print("name : {}, replication : {}, hardware : {}".format(m.microservice_id, m.replication_id, m.hardware.hardware_id))
    service = ENV.service_dict[0]
    q = service.generate_query(0)
    ENV.queries.put(q)
    for i in range(10):
        ENV.update()
    service = ENV.service_dict[0]
    print(service.end_dict)




"""
serviceごとにクラスにする？
service.query(num,root) -> hardware.cpu,hardware.memory が変更されるような仕様にしたい

通信コストの実装
通信コスト自体の計算をO(n)で計算できる設定？O(1)
もし全部メモったら2^n
クエリ実行 -> 　クエリ終了　-> ハードウェア状態変化
ハードウェアにpriority_queue

linked listにする？
複数結合のlinkedlistとか？
クエリ->レプレプリカも指定したクエリ->実行

基本的に1秒毎の実装がいいかも
"""
