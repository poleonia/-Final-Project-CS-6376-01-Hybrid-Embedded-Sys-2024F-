import csv
import random
from final_acas_3d_v3 import *
from generate_path import *
def run_multiple_tests(num_tests, num_aircrafts, space_size, mandatory_point_ratio, output_csv="test_results.csv"):
    """
    Runs multiple tests for aircraft collision avoidance simulation and saves the results to a CSV file.

    :param num_tests: Number of test iterations
    :param num_aircrafts: Number of aircraft in each test
    :param space_size: Size of the 3D space
    :param mandatory_point_ratio: Ratio for mandatory point in the space
    :param output_csv: Path for the output CSV file
    """
    total_deviation_time = 0
    collision_alert_count = 0
    all_deviation_times = []

    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write header
        header = [
            "Test Number", "Aircraft Number", "Collision Alert", "Max Deviation Time"
        ]
        writer.writerow(header)

        for test_number in range(1, num_tests + 1):
            # Generate random aircraft definitions
            aircraft_definitions, mandatory_point = generate_aircraft_definitions(
                num_aircrafts, space_size, mandatory_point_ratio
            )

            print("Mandatory Point:", mandatory_point)
            print("Aircraft Definitions:")
            for aircraft in aircraft_definitions:
                print(aircraft)

            # aircraft_definitions = [
            #     {"current_location": [0, 0, 0], "destination_location": [10, 10, 10]},
            #     {"current_location": [0, 0, 10], "destination_location": [10, 10, 0]},
            #     {"current_location": [5, 0, 0], "destination_location": [5, 10, 10]},
            # ]

            # Initialize aircraft
            aircrafts = [
                AircraftController3D(
                    current_location=aircraft["current_location"],
                    destination_location=aircraft["destination_location"]
                ) for aircraft in aircraft_definitions
            ]

            print(aircrafts)
            # Run simulation
            collision_count, max_percentage, min_percentage = simulate_aircraft_movement(aircrafts, output_csv="aircraft_simulation.csv")

            #deviation_times, collision_count = simulate_aircraft_movement_with_metrics(aircrafts)

            # Collect statistics
            collision_alert_count += collision_count
            total_deviation_time += max_percentage
            #all_deviation_times.extend(deviation_times)

            # Write results to CSV

            writer.writerow([
                test_number, num_aircrafts, "Yes" if collision_count > 0 else "No",
                max_percentage
            ])

    # Calculate final statistics
    average_deviation_time = total_deviation_time / (num_tests)
    #highest_deviation_time = max(all_deviation_times)
    #lowest_deviation_time = min(all_deviation_times)

    print("Collision Alerts:", collision_alert_count)
    print("Average Deviation Time:", average_deviation_time)
    #print("Highest Deviation Time:", highest_deviation_time)
    #print("Lowest Deviation Time:", lowest_deviation_time)


def simulate_aircraft_movement_with_metrics(aircrafts):
    """
    Simulates aircraft movement and collects deviation time and collision alert metrics.

    :param aircrafts: List of AircraftController3D objects
    :return: (List of deviation times, collision alert count)
    """
    normal_times = [calculate_normal_time(aircraft) for aircraft in aircrafts]
    actual_times = [0] * len(aircrafts)
    collision_alert_count = 0

    for timestep in range(50):  # Assuming 50 max timesteps
        all_current_locations = [aircraft.current_location for aircraft in aircrafts]

        for i, aircraft in enumerate(aircrafts):
            nearby_aircrafts = all_current_locations[:i] + all_current_locations[i + 1:]
            aircraft.execute_time_step(nearby_aircrafts)

            if aircraft.collision_alert:
                collision_alert_count += 1

            if not aircraft.reached_destination():
                actual_times[i] += 1

        if all(aircraft.reached_destination() for aircraft in aircrafts):
            break

    deviation_times = [actual - normal for actual, normal in zip(actual_times, normal_times)]
    return deviation_times, collision_alert_count


# Example usage
if __name__ == "__main__":
    num_tests = 10
    num_aircrafts = 3
    space_size = [15,15, 15]
    mandatory_point_ratio = (0.5, 0.5, 0.5)

    run_multiple_tests(
        num_tests=num_tests,
        num_aircrafts=num_aircrafts,
        space_size=space_size,
        mandatory_point_ratio=mandatory_point_ratio,
        output_csv="test_results.csv"
    )
