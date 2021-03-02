import yaml


class Util:

    def __init__(self):
        pass

    def load_config(filename: str):
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        return data["Number_of_hardware"], data["Service"]

    # parse values in data["Service"]
    def parse_service(data: dict):
        return data["service_id"], data["microservices"], data["hardware_map"], data["jobs_of_service"], data["query"], data["jobs"]
