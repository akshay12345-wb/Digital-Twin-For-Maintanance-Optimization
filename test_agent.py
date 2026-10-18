from digital_twin.machine import MachineTwin

from agents.machine_agent import MachineAgent
from agents.technician_agent import TechnicianAgent
from agents.scheduler_agent import SchedulerAgent
from agents.cost_agent import CostAgent

machine = MachineTwin(
    machine_id="M-001",
    temperature=85,
    vibration=6.5,
    pressure=7.0,
    rpm=1450
)

MachineAgent.monitor(machine)

TechnicianAgent.assign(machine)

SchedulerAgent.schedule(machine)

CostAgent.estimate(machine)