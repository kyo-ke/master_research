from source.job import Job
from collections import deque


class Service:
    def __init__(self):
        pass


class Microservice:
    def __init__(self, hardware, job_list, job_dict):
        self.job_dict = dict()
        for job_name in job_list:
            self.job_dict[job_name] = job_dict[job_name]
        self.run_job_dict = dict()
        self.job_deque = deque()
        self.hardware = hardware
        self.next_id = 0

    def make_job(self, job_type):
        current_id = self.generate_id()
        j = Job(self.job_dict[job_type], current_id)
        # add new job to dict and deque
        #dict for running or wating jobs
        self.run_job_dict[current_id] = j
        #deque for wating jobs
        self.job_deque.append(j)

    def generate_id(self) -> int:
        self.next_id += 1
        return self.next_id

    def run(self, deltatime):
        remain_time = deltatime
        while(remain_time != 0):
            if(self.job_deque.empty()):
                break
            else:
                current_job = self.job_deque.popleft()
                remain_time = current_job.run(remain_time)
                if(remain_time < 0):
                    self.job_deque.appendleft(current_job)
