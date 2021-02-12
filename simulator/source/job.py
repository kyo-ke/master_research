from queue import Queue


class Job:
    def __init__(self, job_dict, job_id):
        # cpu pressure for this job
        self.cpu_pressure = job_dict["cpu_pressure"]
        # memory pressure of this job
        self.memory_pressure = job_dict["memory_pressure"]
        # remaining time for this job
        self.remain_time = job_dict["remain_time"]
        self.jobname = job_dict["jobname"]
        self.next_jobs = job_dict["next_jobs"]
        # ここにid持たせる意味あるかはわからん
        self.job_id = job_id
        #self.microservice = microservice
        # 0 : stop, 1 : running, 2 : wating
        self.status = 1

    def run(self, deltatime) -> int:
        if (self.remain_time > deltatime):
            self.remain_time -= deltatime
            return 0
        else:
            self.send_message()
            return deltatime - self.remain_time

    def send_message(self):
        pass

    def count(self):
        pass

    def end(self):
        pass


class Message:
    def __init__(self, message_type, to_hardware, from_hardware, from_microservice, relation=None, to_microservice=None, to_job_type=None, to_job_id=None, from_job_type=None, from_job_id=None):
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
