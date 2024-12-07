import math
import numpy as np
import csv
class AircraftController3D:
    def __init__(self, current_location, destination_location, velocity=1, danger_zone=1, warning_zone=2):
        self.current_location = current_location
        self.destination_location = destination_location
        self.velocity = velocity
        self.danger_zone = danger_zone
        self.warning_zone = warning_zone
        self.direction = ("y", 1)
        self.warning_signal = False
        self.collision_alert = False
        self.adjust_signal = False
        self.warning_aircraft_log = {}
    # def update_direction(self):
    #     x_dist = abs(self.destination_location[0] - self.current_location[0])
    #     y_dist = abs(self.destination_location[1] - self.current_location[1])
    #     z_dist = abs(self.destination_location[2] - self.current_location[2])
    #
    #     # Prioritize movement along the largest distance axis
    #     if x_dist >= y_dist and x_dist >= z_dist:
    #         self.direction = "x"
    #     elif y_dist >= x_dist and y_dist >= z_dist:
    #         self.direction = "y"
    #     else:
    #         self.direction = "z"
    def update_direction(self):
        x_dist = self.destination_location[0] - self.current_location[0]
        y_dist = self.destination_location[1] - self.current_location[1]
        z_dist = self.destination_location[2] - self.current_location[2]

        # Prioritize movement along the axis with the largest absolute distance
        if abs(x_dist) >= abs(y_dist) and abs(x_dist) >= abs(z_dist):
            self.direction = ("x", 1 if x_dist > 0 else -1)
        elif abs(y_dist) >= abs(x_dist) and abs(y_dist) >= abs(z_dist):
            self.direction = ("y", 1 if y_dist > 0 else -1)
        else:
            self.direction = ("z", 1 if z_dist > 0 else -1)

    def check_warning_zone(self, nearby_aircrafts):
        for i, aircraft_pos in enumerate(nearby_aircrafts):
            dist_in_warning_zone = all(
                abs(self.current_location[j] - aircraft_pos[j]) <= self.warning_zone
                for j in range(3)
            )

            if dist_in_warning_zone:
                self.warning_signal = True
                if i not in self.warning_aircraft_log:
                    self.warning_aircraft_log[i] = []  # 初始化记录
                self.warning_aircraft_log[i].append(aircraft_pos)

            elif i in self.warning_aircraft_log:
                del self.warning_aircraft_log[i]

            if dist_in_warning_zone and i in self.warning_aircraft_log:
                #self.collision_alert = True
                self.adjust_direction_from_log(i)
                return  # 只需要调整一次方向

        if not self.warning_aircraft_log:
            self.warning_signal = False
    def check_collision_zone(self, nearby_aircrafts):
        for i, aircraft_pos in enumerate(nearby_aircrafts):
            dist_in_collision_zone = all(
                abs(self.current_location[j] - aircraft_pos[j]) < self.danger_zone
                for j in range(3)
            )
        if dist_in_collision_zone:
            self.collision_alert = True
            # 如果飞机进入危险区，根据记录调整方向
            # if dist_in_collision_zone and i in self.warning_aircraft_log:
            #     self.collision_alert = True
            #     self.adjust_direction_from_log(i)
            #     return  # 只需要调整一次方向
        #self.collision_alert = False
#################################################################################
#################################################################################
    def get_relative_axes(self, current_location, destination_location):

        direction_vector = [
            destination_location[i] - current_location[i] for i in range(2)  # 仅考虑 x, y 平面
        ]


        if direction_vector[1] > 0:
            unit_y = [0, 1]
        else:
            unit_y = [0, -1]


        unit_x = [unit_y[1], -unit_y[0]]

        return unit_x, unit_y

    def convert_motion_to_relative(self, previous_position, current_position, unit_x, unit_y):


        motion_vector = [
            current_position[i] - previous_position[i] for i in range(2)
        ]

        relative_dx = motion_vector[0] * unit_x[0] + motion_vector[1] * unit_x[1]
        relative_dy = motion_vector[0] * unit_y[0] + motion_vector[1] * unit_y[1]
        return [relative_dx, relative_dy]

    def convert_to_relative(self, position, current_location, unit_x, unit_y):

        relative_vector = [
            position[0] - current_location[0],
            position[1] - current_location[1],
        ]
        relative_x = relative_vector[0] * unit_x[0] + relative_vector[1] * unit_x[1]
        relative_y = relative_vector[0] * unit_y[0] + relative_vector[1] * unit_y[1]
        return [relative_x, relative_y]

    def determine_avoidance_direction(self, relative_position, relative_motion):

        # 初始化规避方向
        avoidance_direction = None

        # 冲突飞机接近当前飞机的判断
        # if relative_position[1] > 0 and relative_motion[1] < 0:  # 冲突飞机在 +Y 且接近
        #     # 优先规避到左右两侧
        #     if relative_motion[0] > 0:  # 冲突飞机向 +X
        #         avoidance_direction = [-1, 0]  # 向 -X 规避
        #     elif relative_motion[0] < 0:  # 冲突飞机向 -X
        #         avoidance_direction = [1, 0]  # 向 +X 规避
        #     else:  # 冲突飞机仅在 Y 方向运动
        #         avoidance_direction = [1, 0]  # 向 +X 规避
        #
        # elif relative_position[1] <= 0:  # 冲突飞机不在 +Y 区域
        #     # 根据冲突飞机位置，选择远离其位置的方向
        #     if relative_position[0] > 0:  # 冲突飞机在 +X
        #         avoidance_direction = [-1, 0]  # 向 -X 规避
        #     elif relative_position[0] < 0:  # 冲突飞机在 -X
        #         avoidance_direction = [1, 0]  # 向 +X 规避
        #     else:  # 冲突飞机在 -Y
        #         avoidance_direction = [0, 1]  # 向 +Y 规避
        avoidance_direction = [1, 0]

        return avoidance_direction

    def naive_determine_avoidance_direction_x(self, relative_position):

        if relative_position[0] > 0:  # 冲突飞机在 X > 0
            avoidance_direction = [-1, 0]  # 向 X 负方向规避
        elif relative_position[0] < 0:  # 冲突飞机在 X < 0
            avoidance_direction = [1, 0]  # 向 X 正方向规避
        else:  # 冲突飞机在 X = 0
            avoidance_direction = [1, 0]  # 默认向 X 正方向规避

        return avoidance_direction

    def convert_to_real(self, relative_direction, unit_x, unit_y):

        real_x = relative_direction[0] * unit_x[0] + relative_direction[1] * unit_y[0]
        real_y = relative_direction[0] * unit_x[1] + relative_direction[1] * unit_y[1]
        return [real_x, real_y]
    def adjust_direction_from_log(self, aircraft_index):

        positions = self.warning_aircraft_log.get(aircraft_index, [])
        if len(positions) < 2:
            return


        last_position = positions[-1]
        previous_position = positions[-2]
        movement_vector = [
            last_position[i] - previous_position[i] for i in range(3)
        ]


        relative_position = [
            last_position[i] - self.current_location[i] for i in range(3)
        ]

        direction_vector = [
            self.destination_location[1] - self.current_location[1]
        ]

        unit_x, unit_y = self.get_relative_axes(self.current_location[:2], self.destination_location[:2])
        relative_position = self.convert_to_relative(last_position[:2], self.current_location[:2], unit_x, unit_y)

        relative_motion = self.convert_motion_to_relative(
            previous_position[:2],
            last_position[:2],
            unit_x,
            unit_y
        )
        avoidance_direction = self.naive_determine_avoidance_direction_x(relative_position)
        real_avoidance_direction = self.convert_to_real(avoidance_direction, unit_x, unit_y)
        # if(real_avoidance_direction == [1,0]):
        #     self.direction = ("x", 1)
        # if (real_avoidance_direction == [-1, 0]):
        #     self.direction = ("x", -1)

        self.direction = ("x", real_avoidance_direction[0])
###################################################################################
###################################################################################
    def get_relative_axes_3d(current_location, destination_location):

        # 目标方向向量
        target_vector = np.array(destination_location) - np.array(current_location)
        target_magnitude = np.linalg.norm(target_vector)

        # 单位向量 Y：目标方向归一化
        unit_y = target_vector / target_magnitude

        # 单位向量 X：Y 在 X 平面顺时针旋转 90 度
        unit_x = np.array([unit_y[1], -unit_y[0], 0])
        unit_x /= np.linalg.norm(unit_x)

        # 单位向量 Z：Y 在 Z 平面逆时针旋转 90 度
        unit_z = np.array([0, -unit_y[2], unit_y[1]])
        unit_z /= np.linalg.norm(unit_z)

        return unit_x, unit_y, unit_z

    def convert_to_relative_3d(position, current_location, unit_x, unit_y, unit_z):

        relative_vector = np.array(position) - np.array(current_location)
        relative_x = np.dot(relative_vector, unit_x)
        relative_y = np.dot(relative_vector, unit_y)
        relative_z = np.dot(relative_vector, unit_z)
        return [relative_x, relative_y, relative_z]

    def convert_to_real_3d(relative_direction, current_location, unit_x, unit_y, unit_z):

        real_vector = (
                relative_direction[0] * unit_x +
                relative_direction[1] * unit_y +
                relative_direction[2] * unit_z
        )
        return current_location + real_vector
####################################################################################
    def navigate(self):
        axis, sign = self.direction
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        self.current_location[axis_index] += self.velocity * sign
    def execute_time_step(self, nearby_aircrafts):
        if self.reached_destination():
            print("Aircraft has reached the destination.")
            return

        self.check_warning_zone(nearby_aircrafts)
        self.check_collision_zone(nearby_aircrafts)

        if self.warning_signal:
            print("Warning! Adjusting course.")
            #self.adjust_direction(nearby_aircrafts)
        else:
            self.update_direction()

        self.navigate()
        print(
            f"Location: {self.current_location}, Direction: {self.direction}, Neighbor: {nearby_aircrafts}, "
            f"Warning: {self.warning_signal}, Collision Alert: {self.collision_alert}"
        )

    def reached_destination(self):
        return self.current_location == self.destination_location


def simulate_aircraft_movement(aircrafts, output_csv="aircraft_simulation.csv", max_timesteps=50):

    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header
        header = ["Timestep"] + [
            f"Aircraft {i + 1} Location (x, y, z)"
            for i in range(len(aircrafts))
        ]
        writer.writerow(header)

        # Initialize tracking for deviation time
        normal_times = [
            calculate_normal_time(aircraft) for aircraft in aircrafts
        ]
        actual_times = [0] * len(aircrafts)

        for timestep in range(max_timesteps):
            print(f"Timestep {timestep + 1}:")

            # Collect all current locations for collision checking
            all_current_locations = [aircraft.current_location for aircraft in aircrafts]

            # Write the current timestep and locations to the CSV file
            row = [timestep + 1] + [tuple(loc) for loc in all_current_locations]
            writer.writerow(row)

            # Execute one timestep for each aircraft
            for i, aircraft in enumerate(aircrafts):
                # Remove the current aircraft's location from the list of nearby aircrafts
                nearby_aircrafts = all_current_locations[:i] + all_current_locations[i + 1:]

                print(f"Aircraft {i + 1}:")
                aircraft.execute_time_step(nearby_aircrafts)

                # Increment the actual time for this aircraft if it's not at the destination
                if not aircraft.reached_destination():
                    actual_times[i] += 1

                # Check if this aircraft has a collision alert
                if aircraft.collision_alert:
                    print(f"Collision alert triggered by Aircraft {i + 1} at location {aircraft.current_location}.")
                    print("Simulation stopped due to collision alert.")
                    return  # Stop the simulation immediately

            # Check if all aircraft have reached their destinations
            if all(aircraft.reached_destination() for aircraft in aircrafts):
                print("All aircraft have reached their destinations safely.")
                break
        else:
            print("Simulation ended without all aircraft reaching their destinations.")

        # Calculate and print deviation times and percentages
        deviation_times = [actual+1 - normal for actual, normal in zip(actual_times, normal_times)]
        deviation_percentages = [
            round((deviation / normal) * 100, 2) if normal > 0 else 0.0
            for deviation, normal in zip(deviation_times, normal_times)
        ]

        # Find the highest and lowest deviation percentages
        max_percentage = max(deviation_percentages)
        min_percentage = min(deviation_percentages)
        max_index = deviation_percentages.index(max_percentage) + 1
        min_index = deviation_percentages.index(min_percentage) + 1

        for i, (deviation, percentage) in enumerate(zip(deviation_times, deviation_percentages)):
            print(
                f"Aircraft {i + 1}: Normal Time = {normal_times[i]}, "
                f"Actual Time = {actual_times[i]}, Deviation = {deviation}, "
                f"Deviation Percentage = {percentage}%"
            )

        # Output the highest and lowest deviation percentages
        print(
            f"Highest Deviation Percentage: Aircraft {max_index} with {max_percentage}%\n"
            f"Lowest Deviation Percentage: Aircraft {min_index} with {min_percentage}%"
        )


    return aircraft.collision_alert,max_percentage,min_percentage


def calculate_normal_time(aircraft):
    """
    Calculates the time needed for an aircraft to reach its destination in a straight path without interference.

    :param aircraft: AircraftController3D object
    :return: Time (in timesteps) to reach the destination
    """
    distances = [
        abs(aircraft.destination_location[i] - aircraft.current_location[i])
        for i in range(3)
    ]
    return sum(distances)  # Since velocity = 1, each unit of distance = 1 timestep


# Example usage:
if __name__ == "__main__":
    # Define current and destination locations for each aircraft
    aircraft_definitions = [
        {"current_location": [0, 0, 0], "destination_location": [10, 10, 10]},
        {"current_location": [0, 0, 10], "destination_location": [10, 10, 0]},
        {"current_location": [5, 0, 0], "destination_location": [5, 10, 10]},
    ]

    aircraft_definitions = [
        {'current_location': [10, 8, 5], 'destination_location': [7, 10, 10]},
        {'current_location': [10, 10, 1], 'destination_location': [0, 1, 6]},
        {'current_location': [10, 8, 8], 'destination_location': [10, 0, 2]},
    ]
    # Initialize aircraft based on definitions
    aircrafts = [
        AircraftController3D(
            current_location=aircraft["current_location"],
            destination_location=aircraft["destination_location"]
        ) for aircraft in aircraft_definitions
    ]

    # Run the simulation and output results to a CSV file
    simulate_aircraft_movement(aircrafts, output_csv="aircraft_simulation.csv")



