import numpy as np
import robosuite as suite
from robosuite import load_controller_config

# Load the controller configuration
controller_name = 'JOINT_POSITION'
num_actions = 4  # Adjust based on your robot's action space
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

# Replay actions from a CSV file
def replay_actions(env, filename="my_joint_data.csv", delay=0.05):
    """
    Replays actions stored in a CSV file.

    Args:
        env: The robosuite environment instance.
        filename: Path to the CSV file containing the actions.
        delay: Time delay (in seconds) between each action for smooth replay.
    """
    try:
        # Load actions from the file
        actions = np.loadtxt(filename, delimiter=",")
        print(f"Loaded {len(actions)} actions from {filename}.")
    except Exception as e:
        print(f"Error loading actions: {e}")
        return

    for step, action in enumerate(actions):
        # Step the environment with the loaded action
        obs, reward, done, info = env.step(action)

        # Render the environment to visualize the replay
        env.render()

        # Add a delay for smooth playback
        import time
        time.sleep(delay)

        print(f"Replayed action {step + 1}/{len(actions)}.")

        # Reset the environment if the episode ends
        if done:
            print("Episode terminated. Resetting the environment.")
            env.reset()

    print("Replay finished.")

# Record actions to a CSV file
def record_actions(env, max_steps=200, filename="recorded_actions.csv"):
    """
    Records actions applied to the environment and saves them to a CSV file.

    Args:
        env: The robosuite environment instance.
        max_steps: Number of steps to record.
        filename: Path to save the recorded actions.
    """
    actions = []
    for _ in range(max_steps):
        # Generate a random action (or replace with your custom action logic)
        action = np.random.uniform(-1, 1, size=num_actions)  # Example: random action
        env.step(action)
        env.render()

        # Record the action
        actions.append(action)

    # Save actions to file
    try:
        np.savetxt(filename, actions, delimiter=",")
        print(f"Actions saved to {filename}.")
    except Exception as e:
        print(f"Error saving actions: {e}")

# Example Usage

# Record actions
record_actions(env, max_steps=200, filename="my_joint_data.csv")

# Replay the recorded actions
replay_actions(env, filename="my_joint_data.csv", delay=0.05)

# Close the environment when done
env.close()
