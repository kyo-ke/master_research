import unittest
import sys
sys.path.append("./")
from source.service import Microservice, Service
from source.hardware import Hardware
from source.environment import Environment
from source.util import Util

class TestMicroservice(unittest.TestCase):

    def __init__(self,*args, **kwargs):
        super(TestMicroservice, self).__init__(*args, **kwargs)
        env = Environment()
        # make Hardware instance
        self.hardware_id = 0
        number_of_core = 1
        self.hardware = Hardware(env, self.hardware_id, number_of_core)
        # make Microservice instance
        _, services = Util.load_config("config/test.yml")
        s = services[0]
        _, microservices, _, jobs_of_service, _, jobs = Util.parse_service(s)
        self.microservice_id = list(microservices.keys())[0]
        self.job_list = jobs_of_service[self.microservice_id]
        self.job_dict = jobs

    def test_make_job(self):
        microservice = Microservice(self.hardware, self.microservice_id, self.job_list, self.job_dict)
        parent_info = dict()
        parent_info["parent_hardware"] = "parent_hardware_name"
        parent_info["parent_microservice"] = "parent_microservice_name"
        parent_info["parent_job_id"] = "parent_id"
        microservice.make_job(list(microservice.job_dict.keys())[0], parent_info)
        self.assertEqual(len(microservice.job_deque), 1)
        self.assertEqual(len(microservice.run_job_dict), 1)

    def test_generate_id(self):
        microservice = Microservice(self.hardware, self.microservice_id, self.job_list, self.job_dict)
        self.assertEqual(microservice.next_id, 0)
        self.assertEqual(microservice.generate_id(),1)
        self.assertEqual(microservice.generate_id(),2)

    def test_get_id(self):
        microservice = Microservice(self.hardware, self.microservice_id, self.job_list, self.job_dict)
        self.assertEqual(microservice.get_id(), self.microservice_id)

    def test_get_hardware(self):
        microservice = Microservice(self.hardware, self.microservice_id, self.job_list, self.job_dict)
        self.assertEqual(microservice.get_hardware(), self.hardware)

    def test_get_hardware_id(self):
        microservice = Microservice(self.hardware, self.microservice_id, self.job_list, self.job_dict)
        self.assertEqual(microservice.get_hardware_id(), self.hardware_id)

    def test_end_jobs(self):
        microservice = Microservice(self.hardware, self.microservice_id, self.job_list, self.job_dict)
        parent_info = dict()
        parent_info["parent_hardware"] = "parent_hardware_name"
        parent_info["parent_microservice"] = "parent_microservice_name"
        parent_info["parent_job_id"] = "parent_id"
        microservice.make_job(list(microservice.job_dict.keys())[0], parent_info)
        microservice.make_job(list(microservice.job_dict.keys())[0], parent_info)
        self.assertEqual(microservice.run(20), 0)
        self.assertEqual(len(microservice.job_deque),0)
        self.assertEqual(len(microservice.wait_job_deque),2)
        job = microservice.wait_job_deque.pop()
        for i in range(job.number_of_next_jobs):
            job.count_up()
        microservice.wait_job_deque.append(job)
        self.assertEqual(len(microservice.wait_job_deque),2)
        microservice.end_jobs()
        self.assertEqual(len(microservice.wait_job_deque),1)



    def test_run(self):
        microservice = Microservice(self.hardware, self.microservice_id, self.job_list, self.job_dict)
        parent_info = dict()
        parent_info["parent_hardware"] = "parent_hardware_name"
        parent_info["parent_microservice"] = "parent_microservice_name"
        parent_info["parent_job_id"] = "parent_id"
        microservice.make_job(list(microservice.job_dict.keys())[0], parent_info)
        microservice.make_job(list(microservice.job_dict.keys())[0], parent_info)
        self.assertEqual(microservice.run(10), 0)
        self.assertEqual(len(microservice.job_deque),1)
        self.assertEqual(len(microservice.wait_job_deque),1)
        self.assertEqual(microservice.run(30), 20)

if __name__ == "__main__":
    unittest.main()
