from typing import List, Tuple


def generate_coverage_trajectory(
    wall_width: float,
    wall_height: float,
    obstacle_list: List[Tuple[float, float, float, float]],
    step: float = 0.5,
) -> List[Tuple[float, float]]:
    """
    Generate a list of (x, y) waypoints that cover the wall with given rectangular obstacles.
    Args:
        wall_width: width of the wall (m)
        wall_height: height of the wall (m)
        obstacle_list: list of (x, y, w, h) for each rectangular obstacle, where
                       (x, y) is bottom-left corner relative to the wall origin, and w, h are dimensions.
        step: spacing between adjacent path lines (m)
    Returns:
        List of (x, y) waypoints forming a continuous coverage path.
    """
    
    x_steps = int(wall_width / step) + 1
    y_steps = int(wall_height / step) + 1

   
    def is_in_obstacle(px: float, py: float) -> bool:
        for ox, oy, ow, oh in obstacle_list:
            if ox <= px <= ox + ow and oy <= py <= oy + oh:
                return True
        return False

    trajectory: List[Tuple[float, float]] = []
    direction = 1 

    y = 0.0
    while y <= wall_height:
        if direction == 1:
            x = 0.0
            while x <= wall_width:
                if not is_in_obstacle(x, y):
                    trajectory.append((x, y))
                x += step
        else:
            x = wall_width
            while x >= 0.0:
                if not is_in_obstacle(x, y):
                    trajectory.append((x, y))
                x -= step
        direction *= -1
        y += step

    return trajectory
