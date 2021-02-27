import unittest
import sys
sys.path.append("./")
from source.environment import Environment
from source.hardware import Hardware
from source.service import Microservice
from source.job import Job
from source.util import Util


class TestJob(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestJob, self).__init__(*args, **kwargs)
        # make Environment instance
        env = Environment()
        # make Hardware instance
        self.hardware_id = 0
        number_of_core = 1
        hardware = Hardware(env, self.hardware_id, number_of_core)
        # make Microservice instance
        _, services = Util.load_config("config/test.yml")
        s = services[0]
        _, microservices, _, jobs_of_service, _, jobs = Util.parse_service(s)
        self.microservice_id = list(microservices.keys())[0]
        job_list = jobs_of_service[self.microservice_id]
        job_dict = jobs
        self.microservice = Microservice(
            hardware, self.microservice_id, job_list, job_dict)
        self.parent_info = dict()
        self.parent_info["parent_hardware"] = "parent_hardware_name"
        self.parent_info["parent_microservice"] = "parent_microservice_name"
        self.parent_info["parent_job_id"] = "parent_id"
        self.job_dict = job_dict[list(job_dict.keys())[0]]
        self.job_id = 1

    def test_run(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        self.assertEqual(job.remain_time, 10)
        self.assertEqual(job.run(5), 0)
        self.assertEqual(job.remain_time, 5)
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        self.assertEqual(job.run(20), 10)
        self.assertEqual(job.remain_time, 0)

    def test_hardware_id(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        self.assertEqual(job.get_hardware_id(), self.hardware_id)

    def test_get_microservice_id(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        self.assertEqual(job.get_microservice_id(), self.microservice_id)

    def test_generate_message(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        message = job.generate_message(2)
        self.assertEqual(message.to_hardware,
                         self.parent_info["parent_hardware"])
        self.assertEqual(message.to_microservice,
                         self.parent_info["parent_microservice"])
        self.assertEqual(message.to_job_id, self.parent_info["parent_job_id"])
        message_list = job.generate_message(1)
        message = message_list[0]
        self.assertEqual(message.to_microservice,
                         self.job_dict["next_jobs"][0]["servicename"])
        self.assertEqual(message.to_job_type,
                         self.job_dict["next_jobs"][0]["jobname"])

    def test_send_message(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        message = job.generate_message(2)
        job.send_message(message)
        env = job.microservice.get_hardware().get_env()
        orchestrator = env.get_orchestrator()
        self.assertEqual(orchestrator.number_of_message(), 1)
        job.send_message(message)
        self.assertEqual(orchestrator.number_of_message(), 2)

    def test_count_up(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        self.assertEqual(job.count, 0)
        job.count_up()
        self.assertEqual(job.count, 1)
        job.count_up()
        self.assertEqual(job.count, 2)

    def test_isend(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        for i in range(job.number_of_next_jobs):
            self.assertFalse(job.isend())
            job.count_up()
        self.assertTrue(job.isend())

    def test_end(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        job.end()
        env = job.microservice.get_hardware().get_env()
        orchestrator = env.get_orchestrator()
        self.assertEqual(orchestrator.number_of_message(), 1)

    def test_wait(self):
        job = Job(self.microservice, self.parent_info,
                  self.job_dict, self.job_id)
        job.wait()
        env = job.microservice.get_hardware().get_env()
        orchestrator = env.get_orchestrator()
        self.assertEqual(orchestrator.number_of_message(),
                         job.number_of_next_jobs)


if __name__ == "__main__":
    unittest.main()
