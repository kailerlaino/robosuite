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


def move_to_position(env, target_x, target_y, target_z, tolerance=0.2, max_steps=1000, is_moving_down=True, back_to_start=False):

    action = np.zeros(num_actions)
    

    for i in range(max_steps):
        obs, reward, done, info = env.step(action)
        action[2] = downward_step if is_moving_down else upward_step
        
        # Get the current end effector position
        eef_pos = obs['robot0_eef_pos']
        # Calculate the movement needed to reach the target x and y
        action[0] = target_x - eef_pos[0]  # Adjust x
        action[1] = target_y - eef_pos[1]  # Adjust y
        
        # Control z position based on whether we are above or below the target
        if eef_pos[2] < lower_threshold and is_moving_down:
            is_moving_down = False  # Switch to moving up
            # print('Switching to upward movement due to position')
            # print(obs['robot0_eef_pos'])

        # Check if the end effector is above the upper threshold
        if eef_pos[2] > upper_threshold and not is_moving_down:
            is_moving_down = True  # Switch to moving down
            # print('Switching to downward movement due to position')
            # print(obs['robot0_eef_pos'])


        # Take action
        env.step(action)
        env.render()

        # Check if the end effector is close enough to the target position
        if (abs(eef_pos[0] - target_x) < tolerance and
            abs(eef_pos[1] - target_y) < tolerance and
            abs(eef_pos[2]) < lower_threshold):
            print("Reached target position:", eef_pos)
            if (back_to_start):
                print("going back to start")
                break
            else:
                move_to_position(env, -0.10034241, -0.01272051, 1.0, tolerance=0.3, max_steps=1000, is_moving_down=is_moving_down, back_to_start=True)

        # Reset action to avoid accumulation
        action.fill(0)

# Example usage of the function
initial_position = None

# Define target position for movement
target_position_1 = (0.2, 0.2, 0.82)  # Example coordinates
move_to_position(env, *target_position_1, is_moving_down=is_moving_down)

# After moving to the target, store the current position as the initial position
initial_position = env.sim.data.get_site_xpos("gripper0_grip_site")

# Move back to the initial position
print("Moving back to the initial position...")
# Close the environment when done
env.close()

