"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designated waypoint.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own
        self.reached_waypoint = False  # Track if the waypoint has been reached

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Calculate distance to waypoint
        distance_to_waypoint = self.waypoint.distance_to(report.position)

        # Check drone status
        if report.status == "Landed":
            # Drone has already landed
            return commands.Command.create_null_command()

        if self.reached_waypoint:
            # Drone has reached the waypoint, issue land command
            if report.status == "Halted":
                return commands.Command.create_land_command()

        if distance_to_waypoint <= self.acceptance_radius:
            # Drone is within the acceptance radius
            self.reached_waypoint = True
            if report.status == "Halted":
                return commands.Command.create_land_command()
            else:
                return commands.Command.create_halt_command()

        # If the drone is not at the waypoint
        if report.status == "Halted":
            relative_x = self.waypoint.x - report.position.x
            relative_y = self.waypoint.y - report.position.y
            return commands.Command.create_set_relative_destination_command(relative_x, relative_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
