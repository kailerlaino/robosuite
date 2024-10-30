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

# Initial position settings
downward_step = -0.5  # Step size for downward motion
upward_step = 0.5  # Step size for upward motion
is_moving_down = True  # State variable
action = np.zeros(num_actions)  # Initialize action array
steps_moved = 0  # Counter for steps

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


    # Initial settings to access collision data 
    table_id = env.sim.model.geom_name2id("table_collision")
    robot_id = env.sim.model.geom_name2id("gripper0_finger1_collision")

    for contact in env.sim.data.contact:
        if (contact.geom1 == table_id and contact.geom2 == robot_id) or (contact.geom2 == table_id and contact.geom1 == robot_id):
            print("Collision detected between robot and table")
        print(contact)

    print(table_id)


    # Reset action to avoid accumulation
    action.fill(0)

# Close the environment when done
env.close()
