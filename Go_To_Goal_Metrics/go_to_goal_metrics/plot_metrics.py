import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_metrics(csv_path, output_dir, case_name):
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    data = pd.read_csv(csv_path)
    os.makedirs(output_dir, exist_ok=True)

    t = data['time_s']
    err = data['distance_error']
    v = data['linear_velocity']
    w = data['angular_velocity']

    plt.figure()
    plt.plot(t, err)
    plt.xlabel('Time [s]')
    plt.ylabel('Distance error [m]')
    plt.title(f'Distance Error vs Time - {case_name}')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f'{case_name}_error.png'))
    plt.close()

    plt.figure()
    plt.plot(t, v)
    plt.xlabel('Time [s]')
    plt.ylabel('Linear velocity [m/s]')
    plt.title(f'Linear Velocity vs Time - {case_name}')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f'{case_name}_linear.png'))
    plt.close()

    plt.figure()
    plt.plot(t, w)
    plt.xlabel('Time [s]')
    plt.ylabel('Angular velocity [rad/s]')
    plt.title(f'Angular Velocity vs Time - {case_name}')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f'{case_name}_angular.png'))
    plt.close()


if __name__ == "__main__":
    # Example usage
    plot_metrics('metrics_results/case_A_metrics.csv', 'metrics_results', 'case_A')
