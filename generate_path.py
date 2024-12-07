import random


def generate_aircraft_definitions(num_aircrafts, space_size, mandatory_point_ratio):
    """
    Generates aircraft definitions with starting and ending points on the edges of a 3D space.
    Ensures the y-axis dimension of the start and end points are different.

    :param num_aircrafts: Number of aircraft to generate
    :param space_size: Size of the 3D space as [x_max, y_max, z_max]
    :param mandatory_point_ratio: Mandatory point as a ratio of space size (e.g., (0.5, 0.5, 0.5))
    :return: List of aircraft definitions with shortest paths
    """
    x_max, y_max, z_max = space_size
    mandatory_point = [int(x_max * mandatory_point_ratio[0]),
                       int(y_max * mandatory_point_ratio[1]),
                       int(z_max * mandatory_point_ratio[2])]

    def random_edge_point():
        """Generate a random integer point on the edge of the 3D space."""
        axis = random.choice([0, 1, 2])  # Choose which axis to fix (x, y, or z)
        point = [0, 0, 0]
        for i in range(3):
            if i == axis:
                point[i] = random.choice([0, space_size[i]])  # Fix to min or max
            else:
                point[i] = random.randint(0, space_size[i])  # Random integer along the axis
        return point

    aircraft_definitions = []
    for _ in range(num_aircrafts):
        start = random_edge_point()
        end = random_edge_point()

        # Ensure start and end are not identical and y-axis values differ
        while start == end or start[1] == end[1]:
            end = random_edge_point()

        # Append valid path
        path = {"current_location": start, "destination_location": end}
        aircraft_definitions.append(path)

    return aircraft_definitions, mandatory_point


# Example usage
if __name__ == "__main__":
    num_aircrafts = 5
    space_size = [10, 10, 10]
    mandatory_point_ratio = (0.5, 0.5, 0.5)

    aircraft_definitions, mandatory_point = generate_aircraft_definitions(
        num_aircrafts, space_size, mandatory_point_ratio
    )

    print("Mandatory Point:", mandatory_point)
    print("Aircraft Definitions:")
    for aircraft in aircraft_definitions:
        print(aircraft)
