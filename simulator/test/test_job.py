#import sys
#sys.path.append("../")
from source.job import Job
from source.service import Microservice
from source.hardware import Hardware
import unittest


class TestJob(unittest.TestCase):

    def __init__(self):
        super().__init__(*args, **kwargs)
        #make Hardware instance
        hardware = Hardware()
        parent_intfo =
        #make Microservice instance
        microservice_id = 1
        job_list =
        job_dict =
        micorservice = Microservice(hardware, microservice_id, job_list)
        job_dict =
        job_id = 1
        job_instance = Job(microservice)

    def test_run(self):


if __name__ == "__main__":
    unittest.main()
