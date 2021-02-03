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
        self.job_id = job_id
        self.status = 1  # 0 : stop, 1 : running, 2 : wating

    def run(self):
        pass

    def send_message(self):
        pass

    def end(self):
        pass

    def start(self):
        pass


class Message(self):
    def __init__(self):
        pass
