from queue import Queue


class Message:
    def __init__(self,
                 message_type,
                 to_hardware,
                 to_microservice,
                 to_job_type=None,
                 to_job_id=None,
                 from_hardware=None,
                 from_microservice=None,
                 from_job_type=None,
                 from_job_id=None,
                 relation=None):
        self.type = message_type  # 1: generate job, 2: count finished children
        self.to_hardware = to_hardware  # name of hardware(string)
        self.to_microservice = to_microservice  # name of microservice(string)
        self.to_job_type = to_job_type
        self.to_job_id = to_job_id
        self.from_hardware = from_hardware
        self.from_microservice = from_microservice
        self.from_job_type = from_job_type
        self.from_job_id = from_job_id
        self.relation = relation

    def set_target(self, hardware_name):
        self.to_hardware = hardware_name

class Job:
    # microservice: Microservice(real istance)
    def __init__(self, microservice, parent_info, job_dict, job_id):
        self.microservice = microservice
        self.parent_hardware = parent_info["parent_hardware"]  # str
        self.parent_microservice = parent_info["parent_microservice"]  # str
        self.parent_job_id = parent_info["parent_job_id"]
        # cpu pressure for this job　これいらん
        self.cpu_pressure = job_dict["cpu_pressure"]
        # memory pressure of this job
        self.memory_pressure = job_dict["memory_pressure"]
        # remaining time for this job
        self.remain_time = job_dict["remain_time"]
        self.jobname = job_dict["jobname"]
        self.next_jobs = job_dict["next_jobs"]
        self.number_of_next_jobs = job_dict["number_of_next_jobs"]
        self.count = 0
        # ここにid持たせる意味あるかはわからん
        self.job_id = job_id
        # 0 : stop, 1 : running, 2 : wating
        self.status = 1

    def run(self, deltatime) -> int:
        if (self.remain_time > deltatime):
            self.remain_time -= deltatime
            return 0
        else:
            self.send_message()
            return deltatime - self.remain_time

    def get_hardware_id(self):
        return self.microservice.get_hardware().get_id()

    def get_microservice_id(self):
        return self.microservice.get_id()
    # flag = 1 終了のサイン
    #flag = 2
    def generate_message(self, flag: int) -> Message:
        # when job is finished
        if flag == 2:
            message = Message(message_type=2,
                              to_hardware=self.parent_hardware,
                              to_microservice=self.parent_microservice,
                              to_job_id=self.parent_job_id
                              )
            return message
        # when job start wating
        elif flag == 1:
            message_list = list()
            for j in self.next_jobs.values():
                message = Message(message_type=1,
                                  to_microservcie = j["servicename"],
                                  to_job_type =j["jobname"],
                                  from_hardware = self.get_hardware_id(),
                                  from_microservice = self.get_microservice_id(),
                                  from_job_id = self.job_id)
                message_list.append(message)
            return message_list

    def send_message(self, message: Message):
        # send message to orchestrator
        # this work should done by kernel or service orchestrator
        hardware = self.microservice.hardware
        environment = hardware.get_env()
        orchestrator = environment.orchestrator
        orchestrator.recieve_message(message)

    def count(self):
        self.count+=1

    def isend(self):
        return self.count >= self.number_of_next_jobs

    def end(self):
        message = self.generate_message(1)
        self.send_message(message)


    def wait(self):
        message_list = self.generate_message(2)
        for message in message_list:
            self.send_message(message)


