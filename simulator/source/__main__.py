from source.orchestrator import Orchestrator
from source.environment import Environment
e = Environment()
o = Orchestrator(e)
print(o.hardware_score("hello"))
print(o.environment.queries.qsize())
