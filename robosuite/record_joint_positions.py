from pathlib import Path
import numpy as np  # Import numpy for array operations

def record_joint_positions(env, steps=100, filename="joint_positions.csv"):
    joint_positions = []
    for step in range(steps):
        obs = env.step(np.zeros(env.action_spec[0].shape))
        joint_positions.append(env.sim.data.qpos.copy())
        env.render()
        print(f"Step {step}: Joint positions recorded.")  # Debug info

    joint_positions = np.array(joint_positions)

    # Ensure directory exists
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save to a file
    try:
        np.savetxt(output_path, joint_positions, delimiter=",")
        print(f"Joint positions saved successfully to {output_path}")
    except Exception as e:
        print(f"Error saving joint positions: {e}")
