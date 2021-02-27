import yaml


class Util:

    def __init__(self):
        pass

    def load_config(filename: str):
        f = open(filename)
        data = yaml.load(f)
        return data["Number_of_hardware"], data["Service"]

    # parse data["Service"]
    def parse_service(data: dict):
        return data["service_id"], data["microservices"], data["hardware_map"], data["jobs_of_service"], data["query"], data["jobs"]
