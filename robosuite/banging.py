import numpy as np
import robosuite as suite
from robosuite import load_controller_config

controller_name='OSC_POSITION' # control hand
# controller_name='IK' # control hand
# controller_name='JOINT_POSITION' # control joints

num_actions = 4 # (x,y,z, gripper open/close), maybe 7
# num_actions = env.robots[0].dof # joints

config = load_controller_config(default_controller=controller_name)

# create environment instance
env = suite.make(
    env_name="Lift", # try with other tasks like "Stack" and "Door"
    robots="Panda",  # try with other robots like "Sawyer" and "Jaco"
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    controller_configs=config
)

# reset the environment
env.reset()

# Initial position settings
downward_step = -1.5  # Step size for downward motion
upward_step = 1.5  # Step size for upward motion
is_moving_down = True  # State variable
action = np.zeros(num_actions)  # Initialize action array
steps_moved = 0  # Counter for steps

for i in range(1000):
    if is_moving_down:
        action[2] = downward_step  # Move downwards
    else:
        action[2] = upward_step  # Move upwards

    # Take action in the environment
    obs, reward, done, info = env.step(action)  
    env.render()  # Render on display

    steps_moved += 1  # Increment the step counter

    # Switch states after a fixed number of steps
    if is_moving_down and steps_moved >= 35:  # Adjust 50 as needed
        is_moving_down = False
        steps_moved = 0  # Reset the counter
    elif not is_moving_down and steps_moved >= 35:  # Adjust 50 as needed
        is_moving_down = True
        steps_moved = 0  # Reset the counter


    # Initial settings to access collision data 
    table_id = env.sim.model.body_name2id("table")
    robot_id = env.sim.model.body_name2id("gripper0_right_gripper")

    for contact in env.sim.data.contact:
        if (contact.geom1 == table_id and contact.geom2 == robot_id) or (contact.geom2 == table_id and contact.geom1 == robot_id):
            print("Collision detected between robot and table")

    print(table_id)


    # Reset action to avoid accumulation
    action.fill(0)  # Clear the action except for the z component
