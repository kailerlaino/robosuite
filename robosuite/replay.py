import numpy as np
import time

def replay_joint_positions(env, filename="my_joint_data.csv", delay=0.05):
    """
    Replays joint positions from a CSV file in the robosuite environment.

    Args:
        env: The robosuite environment instance.
        filename: Path to the CSV file containing joint position data.
        delay: Time delay (in seconds) between each frame for smooth replay.
    """
    try:
        # Load joint positions from file
        joint_positions = np.loadtxt(filename, delimiter=",")
        print(f"Loaded {len(joint_positions)} steps from {filename}.")
    except Exception as e:
        print(f"Error loading joint positions: {e}")
        return

    # Replay each joint configuration
    for step, positions in enumerate(joint_positions):
        # Set joint positions directly in the simulator
        env.sim.data.qpos[:len(positions)] = positions  # Update all joints
        env.sim.forward()  # Apply the changes to the simulation

        # Render the environment to visualize changes
        env.render()

        # Wait for the specified delay for smooth playback
        time.sleep(delay)

        print(f"Replayed step {step + 1}/{len(joint_positions)}.")

    print("Replay finished.")


replay_joint_positions()