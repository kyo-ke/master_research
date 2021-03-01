from source.util import Util
from source.service import Microservice
from source.hardware import Hardware
from source.environment import Environment
from source.job import Job, Message
import unittest
import sys
sys.path.append("./")


class TestHardware(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestHardware, self).__init__(*args, **kwargs)
        # make Environment instance
        self.env = Environment()
        self.hardware_id = 0
        self.number_of_core = 1

    def test_get_env(self):
        hardware = Hardware(self.env, self.hardware_id, self.number_of_core)
        self.assertEqual(hardware.get_env(), self.env)

    def test_get_id(self):
        hardware = Hardware(self.env, self.hardware_id, self.number_of_core)
        self.assertEqual(hardware.get_id(), self.hardware_id)

    def test_deploy(self):
        hardware = Hardware(self.env, self.hardware_id, self.number_of_core)
        _, services = Util.load_config("config/test.yml")
        s = services[0]
        _, microservices, _, jobs_of_service, _, jobs = Util.parse_service(s)
        microservice_id = list(microservices.keys())[0]
        job_list = jobs_of_service[microservice_id]
        job_dict = jobs
        microservice = Microservice(
            hardware, microservice_id, job_list, job_dict)
        hardware.deploy(microservice, microservice_id)
        self.assertEqual(
            hardware.microservice_dict[microservice_id], microservice)

    def test_recieved_message(self):
        hardware = Hardware(self.env, self.hardware_id, self.number_of_core)
        message_type = 1
        to_microservice = "service1"
        message = Message(message_type, to_microservice)
        hardware.recieve_message(message)
        self.assertEqual(hardware.message_recieved.qsize(), 1)
        hardware.recieve_message(message)
        self.assertEqual(hardware.message_recieved.qsize(), 2)

    def test_execute_message(self):
        hardware = Hardware(self.env, self.hardware_id, self.number_of_core)
        _, services = Util.load_config("config/test.yml")
        s = services[0]
        _, microservices, _, jobs_of_service, _, jobs = Util.parse_service(s)
        microservice_id = list(microservices.keys())[0]
        job_list = jobs_of_service[microservice_id]
        job_dict = jobs
        microservice = Microservice(
            hardware, microservice_id, job_list, job_dict)
        hardware.deploy(microservice, microservice_id)



