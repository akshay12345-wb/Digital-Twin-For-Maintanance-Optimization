"""
Machine Agent
Monitors the machine condition
"""

class MachineAgent:

    @staticmethod
    def monitor(machine):

        print("=" * 50)
        print("Machine Agent Report")
        print("=" * 50)

        print(f"Machine ID : {machine.machine_id}")
        print(f"Health : {machine.health}%")
        print(f"Status : {machine.status}")
        print(f"AI Prediction : {machine.ai_prediction}")

        if machine.health >= 80:
            decision = "Machine is operating normally."

        elif machine.health >= 50:
            decision = "Machine requires scheduled maintenance."

        else:
            decision = "Machine requires immediate maintenance."

        print(f"Decision : {decision}")

        return decision