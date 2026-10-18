import random
import time

from database.db import Machine
from database.db import session


machines = [
    "M-001",
    "M-002",
    "M-003",
    "M-004",
    "M-005"
]


def calculate_health(temp, vib):

    health = 100

    health -= (temp - 50) * 0.6

    health -= vib * 5

    if health < 0:
        health = 0

    return round(health, 2)


def machine_status(health):

    if health >= 75:
        return "Healthy"

    elif health >= 50:
        return "Warning"

    else:
        return "Critical"


print("Starting Sensor Simulator...\n")


while True:

    for machine in machines:

        temperature = round(random.uniform(55, 95), 2)

        vibration = round(random.uniform(2, 8), 2)

        pressure = round(random.uniform(4, 8), 2)

        rpm = random.randint(1200, 1600)

        health = calculate_health(
            temperature,
            vibration
        )

        status = machine_status(
            health
        )

        data = Machine(

            machine_id=machine,

            temperature=temperature,

            vibration=vibration,

            pressure=pressure,

            rpm=rpm,

            health=health,

            status=status

        )

        session.add(data)

        session.commit()

        print(
            machine,
            temperature,
            vibration,
            pressure,
            rpm,
            health,
            status
        )

    print("-----------------------------")

    time.sleep(2)