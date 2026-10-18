"""
Cost Agent
Estimates maintenance cost
"""


class CostAgent:

    @staticmethod
    def estimate(machine):

        print("=" * 50)
        print("Cost Agent Report")
        print("=" * 50)

        if machine.health >= 80:
            cost = 500
            level = "Low"

        elif machine.health >= 50:
            cost = 3000
            level = "Medium"

        else:
            cost = 10000
            level = "High"

        print(f"Machine ID : {machine.machine_id}")
        print(f"Estimated Cost : ₹{cost}")
        print(f"Cost Level : {level}")

        return cost, level