from source.job import Job
from collections import deque


class Service:
    def __init__(self):
        pass


class Microservice:
    def __init__(self, hardware, microservice_id, job_list, job_dict):
        self.job_dict = dict()
        for job_name in job_list:
            self.job_dict[job_name] = job_dict[job_name]
        self.run_job_dict = dict()
        self.wait_job_deque = deque()#deque for wating jobs
        self.job_deque = deque()#deque for running job
        self.hardware = hardware
        self.microservice_id = microservice_id#str name of microservice
        self.next_id = 0

    def make_job(self, job_type, parent_info):
        current_id = self.generate_id()
        j = Job(self, parent_info, self.job_dict[job_type], current_id)

        # add new job to dict and deque
        #dict for running or wating jobs
        self.run_job_dict[current_id] = j
        #deque for wating jobs
        self.job_deque.append(j)

    def generate_id(self) -> int:
        self.next_id += 1
        return self.next_id

    def get_id(self):
        return self.microservice_id

    def end_jobs(self):
        num = len(self.wait_job_deque)
        while(num>0):
            current_job = self.wait_job_deque.popleft()
            if(current_job.isend()):
                current_job.end()
            else:
                self.wait_job_deque.append(current_job)

    def run(self, deltatime):
        remain_time = deltatime
        #bag that remain time is positive while deque is empty
        while(remain_time != 0):
            if(self.job_deque.empty()):
                break
            else:
                current_job = self.job_deque.popleft()
                remain_time = current_job.run(remain_time)
                if(remain_time < 0):
                    self.job_deque.appendleft(current_job)
                else:
                    current_job.wait()
                    self.wait_job_deque.appendleft(current_job)

