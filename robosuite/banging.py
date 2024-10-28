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

for i in range(1000):
    # Move downwards or upwards based on current state
    action[2] = downward_step if is_moving_down else upward_step
    
    # Take action
    obs, reward, done, info = env.step(action)
    env.render()

    # Check for contact with the table
    if 'robot0_contact' in obs and np.any(obs['robot0_contact']):
        # Collision detected; switch direction
        is_moving_down = not is_moving_down

    # Reset action to avoid accumulation
    action.fill(0)
