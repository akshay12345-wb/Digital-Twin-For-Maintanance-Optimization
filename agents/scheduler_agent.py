"""
Scheduler Agent
Schedules machine maintenance
"""


class SchedulerAgent:

    @staticmethod
    def schedule(machine):

        print("=" * 50)
        print("Scheduler Agent Report")
        print("=" * 50)

        if machine.health >= 80:
            schedule = "Next 30 Days"

        elif machine.health >= 50:
            schedule = "Within 7 Days"

        else:
            schedule = "Immediately"

        print(f"Machine ID : {machine.machine_id}")
        print(f"Maintenance Schedule : {schedule}")

        return schedule