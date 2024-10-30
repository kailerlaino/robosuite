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

for i in range(1000):
    # Move downwards or upwards based on current state
    action[2] = downward_step if is_moving_down else upward_step
    
    # Take action
    obs, reward, done, info = env.step(action)
    env.render()
    
    # Get the end effector position
    eef_pos = obs['robot0_eef_pos']
    print(obs['robot0_eef_pos'])
    
    # Check for contact with the table
    if 'robot0_contact' in obs and np.any(obs['robot0_contact']):
        is_moving_down = not is_moving_down
        print('Collision detected: robot0_contact')
    
    # Check if the end effector is below the lower threshold
    if eef_pos[2] < lower_threshold and is_moving_down:
        is_moving_down = False  # Switch to moving up
        print('Switching to upward movement due to position')
        print(obs['robot0_eef_pos'])

    # Check if the end effector is above the upper threshold
    if eef_pos[2] > upper_threshold and not is_moving_down:
        is_moving_down = True  # Switch to moving down
        print('Switching to downward movement due to position')
        print(obs['robot0_eef_pos'])

    # Reset action to avoid accumulation
    action.fill(0)

# Close the environment when done
env.close()
