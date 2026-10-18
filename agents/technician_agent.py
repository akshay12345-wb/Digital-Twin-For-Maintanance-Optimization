"""
Technician Agent
Assigns maintenance action
"""


class TechnicianAgent:

    @staticmethod
    def assign(machine):

        print("=" * 50)
        print("Technician Agent Report")
        print("=" * 50)

        if machine.health >= 80:

            technician = "No Technician Required"

            action = "Continue Operation"

        elif machine.health >= 50:

            technician = "Maintenance Technician"

            action = "Inspect Machine"

        else:

            technician = "Senior Maintenance Engineer"

            action = "Immediate Repair"

        print(f"Machine ID : {machine.machine_id}")
        print(f"Assigned To : {technician}")
        print(f"Action : {action}")

        return technician, action