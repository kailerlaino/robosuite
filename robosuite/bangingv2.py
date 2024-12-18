import numpy as np
import robosuite as suite
from robosuite import load_controller_config



controller_name = 'OSC_POSITION'
num_actions = 4

config = load_controller_config(default_controller=controller_name)

# Create environment instance
env = suite.make(
    env_name="Lift", 
    robots="Panda",  
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    use_object_obs=True,  # Enable contact info
    controller_configs=config
)

# Reset environment
env.reset()

# Position settings
downward_step = -0.5
upward_step = 0.5
is_moving_down = True
action = np.zeros(num_actions)

# Thresholds for direction switching
lower_threshold = 0.82  # Adjust based on your environment
upper_threshold = 1.0   # Adjust based on your environment


def move_to_position(env, target_x, target_y, target_z, tolerance=0.1, max_steps=200, back_to_start=False):
    action = np.zeros(num_actions)
    eef_positions = []  # List to store joint positions


    for i in range(max_steps):
        # Get current observation and apply action
        obs, reward, done, info = env.step(action)
        
        # Get the current end effector position
        eef_pos = obs['robot0_eef_pos']
        eef_positions.append(eef_pos.copy())  # Store the end effector position

        # Calculate the movement needed to reach the target x and y with larger steps
        action[0] = (target_x - eef_pos[0]) * 2  # Larger step for x direction
        action[1] = (target_y - eef_pos[1]) * 2  # Larger step for y direction
        
        # If we're close to the x, y target, focus on moving downward faster
        if abs(eef_pos[0] - target_x) < tolerance and abs(eef_pos[1] - target_y) < tolerance:
            # Move downward quickly once near the x and y positions
            z_error = target_z - eef_pos[2]
            if abs(z_error) > 0.01:
                action[2] = np.sign(z_error) * 1  # Faster downward movement (e.g., 0.3)
        else:
            # Otherwise, move both horizontally and vertically in sync (slower z movement)
            z_error = target_z - eef_pos[2]
            action[2] = np.sign(z_error) * min(abs(z_error), 0.1)  # Slightly slower downward movement for approach

        # Step the environment forward
        env.step(action)
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
    eef_positions = np.array(eef_positions)
    filename = "eef_positions2-1.csv"
    try:
        np.savetxt(filename, eef_positions, delimiter=",")  # Save end effector positions to a file
        print(f"End effector positions saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving end effector positions: {e}")

# Example usage of the function
initial_position = None

# Define target position for movement
target_position_1 = (0.1, 0.1, 0.82)  # Example coordinates
move_to_position(env, *target_position_1)

# After moving to the target, store the current position as the initial position
initial_position = env.sim.data.get_site_xpos("gripper0_grip_site")

# Move back to the initial position
print("Moving back to the initial position...")
# Close the environment when done
env.close()

