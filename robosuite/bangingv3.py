import numpy as np
import robosuite as suite
from robosuite import load_controller_config

# Load the controller configuration
controller_name = 'OSC_POSITION'
num_actions = 4
config = load_controller_config(default_controller=controller_name)

# Create the environment instance
env = suite.make(
    env_name="Lift", 
    robots="Panda",  
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    use_object_obs=True,  # Enable contact info
    controller_configs=config
)

# Reset the environment
env.reset()

# Rotation function for y-axis
def rotate(theta, x, y, z):
    # Create a rotation matrix for y-axis rotation
    rotation_matrix = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])
    
    # Original position vector
    original_position = np.array([x, y, z])
    
    # Apply the rotation matrix to the position vector
    rotated_position = rotation_matrix @ original_position
    return rotated_position[0], rotated_position[1], rotated_position[2]

# Function to move the robot to the target position with arcing
def move_to_position(env, target_x, target_y, target_z, tolerance=0.1, max_steps=500, back_to_start=False, arc_steps=100):
    action = np.zeros(num_actions)

    # Perform an initial step to get observations
    obs, _, _, _ = env.step(action)
    eef_pos = obs['robot0_eef_pos']
    
    # Calculate the angle step for the arc based on the number of arc_steps
    theta_increment = np.pi / arc_steps  # Adjust the range and step size for the arc

    for i in range(max_steps):
        # Compute a theta angle that arcs from the start to the target position
        theta = i * theta_increment if i <= arc_steps else np.pi

        # Rotate the current eef position to create an arc towards the target
        arc_x, arc_y, arc_z = rotate(theta, eef_pos[0], eef_pos[1], eef_pos[2])

        # Update action to move the robot along the arcing path
        action[0] = (arc_x - eef_pos[0]) * 2
        action[1] = (arc_y - eef_pos[1]) * 2
        action[2] = (arc_z - eef_pos[2]) * 0.5  # Slower adjustment for z-axis to maintain control

        # Step the environment forward
        obs, reward, done, info = env.step(action)
        eef_pos = obs['robot0_eef_pos']
        env.render()

        # Check if the end effector is close enough to the target position
        if (abs(eef_pos[0] - target_x) < tolerance and
            abs(eef_pos[1] - target_y) < tolerance and
            abs(eef_pos[2] - target_z) < 0.01):
            if back_to_start:
                break
            else:
                move_to_position(env, -0.10034241, -0.01272051, 1.0, tolerance=0.3, max_steps=500, back_to_start=True)

        # Reset action to avoid accumulation
        action.fill(0)

# Example usage of the function
initial_position = None

# Define target position for movement
target_position_1 = (0.2, 0.2, 0.82)  # Example coordinates
move_to_position(env, *target_position_1)

# Store the current position as the initial position after moving
initial_position = env.sim.data.get_site_xpos("gripper0_grip_site")

# Print a message indicating the robot is returning to its starting position
print("Moving back to the initial position...")

# Close the environment when done
env.close()
