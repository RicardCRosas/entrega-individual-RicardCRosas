#!/usr/bin/env python3

import csv
import math
import os
import time
from dataclasses import dataclass

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty


@dataclass
class Sample:
    t: float
    x: float
    y: float
    theta: float
    distance_error: float
    angle_error: float
    linear_velocity: float
    angular_velocity: float


class TurtleGoToGoalMetrics(Node):
    def __init__(self):
        super().__init__('turtle_go_to_goal_metrics')

        # Parameters. They can be changed from terminal with --ros-args -p name:=value
        self.declare_parameter('x_goal', 8.0)
        self.declare_parameter('y_goal', 8.0)
        self.declare_parameter('k_linear', 1.0)
        self.declare_parameter('k_angular', 4.0)
        self.declare_parameter('tolerance', 0.10)
        self.declare_parameter('max_linear_speed', 2.0)
        self.declare_parameter('max_angular_speed', 6.0)
        self.declare_parameter('sample_time', 0.05)
        self.declare_parameter('case_name', 'case_A')
        self.declare_parameter('output_dir', 'metrics_results')
        self.declare_parameter('create_plots', True)
        self.declare_parameter('reset_turtlesim', True)

        self.x_goal = float(self.get_parameter('x_goal').value)
        self.y_goal = float(self.get_parameter('y_goal').value)
        self.k_linear = float(self.get_parameter('k_linear').value)
        self.k_angular = float(self.get_parameter('k_angular').value)
        self.tolerance = float(self.get_parameter('tolerance').value)
        self.max_linear_speed = float(self.get_parameter('max_linear_speed').value)
        self.max_angular_speed = float(self.get_parameter('max_angular_speed').value)
        self.sample_time = float(self.get_parameter('sample_time').value)
        self.case_name = str(self.get_parameter('case_name').value)
        self.output_dir = str(self.get_parameter('output_dir').value)
        self.create_plots = bool(self.get_parameter('create_plots').value)
        self.reset_turtlesim = bool(self.get_parameter('reset_turtlesim').value)

        os.makedirs(self.output_dir, exist_ok=True)

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        self.timer = self.create_timer(self.sample_time, self.control_loop)

        self.current_pose = None
        self.previous_pose_for_distance = None
        self.distance_traveled = 0.0

        self.start_time = None
        self.initial_error = None
        self.final_error = None
        self.max_error = 0.0
        self.max_velocity = 0.0
        self.oscillations = 0
        self.previous_angular_sign = 0
        self.finished = False
        self.samples = []

        self.get_logger().info(
            f'Controller started | goal=({self.x_goal:.2f}, {self.y_goal:.2f}) | '
            f'k_linear={self.k_linear:.2f} | k_angular={self.k_angular:.2f}'
        )

        if self.reset_turtlesim:
            self.get_logger().info('Reset requested via parameter, but it should be handled externally for better sync.')

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

        # Approximate traveled distance by adding the distance between consecutive poses.
        if not self.finished:
            if self.previous_pose_for_distance is not None:
                dx = msg.x - self.previous_pose_for_distance.x
                dy = msg.y - self.previous_pose_for_distance.y
                self.distance_traveled += math.sqrt(dx * dx + dy * dy)
            self.previous_pose_for_distance = msg

    @staticmethod
    def normalize_angle(angle: float) -> float:
        """Normalize an angle to the interval [-pi, pi]."""
        return math.atan2(math.sin(angle), math.cos(angle))

    @staticmethod
    def limit(value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(value, max_value))

    def stop_turtle(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def control_loop(self):
        if self.current_pose is None or self.finished:
            return

        if self.start_time is None:
            self.start_time = time.time()

        now = time.time() - self.start_time

        # Current pose
        x = self.current_pose.x
        y = self.current_pose.y
        theta = self.current_pose.theta

        # Distance To Goal (DTG)
        error_x = self.x_goal - x
        error_y = self.y_goal - y
        distance_error = math.sqrt(error_x ** 2 + error_y ** 2)

        # Angle To Goal (ATG) and angular error
        desired_angle = math.atan2(error_y, error_x)
        angle_error = self.normalize_angle(desired_angle - theta)

        if self.initial_error is None:
            self.initial_error = distance_error

        self.max_error = max(self.max_error, distance_error)

        # Proportional control law.
        # Linear velocity is proportional to distance.
        # Angular velocity is proportional to heading error.
        linear_velocity = self.k_linear * distance_error
        angular_velocity = self.k_angular * angle_error

        # Smooth behavior: if the turtle is looking far away from the goal,
        # reduce forward speed so it rotates first and avoids a very curved path.
        if abs(angle_error) > math.pi / 2:
            linear_velocity = 0.0
        else:
            linear_velocity *= max(0.0, math.cos(angle_error))

        # Speed limits for safety and smoother motion.
        linear_velocity = self.limit(linear_velocity, 0.0, self.max_linear_speed)
        angular_velocity = self.limit(angular_velocity, -self.max_angular_speed, self.max_angular_speed)

        self.max_velocity = max(self.max_velocity, abs(linear_velocity), abs(angular_velocity))

        # Oscillation detection: count relevant sign changes in the angular command.
        current_angular_sign = 0
        if abs(angular_velocity) > 0.15:
            current_angular_sign = 1 if angular_velocity > 0 else -1

        if (
            self.previous_angular_sign != 0 and
            current_angular_sign != 0 and
            current_angular_sign != self.previous_angular_sign
        ):
            self.oscillations += 1

        if current_angular_sign != 0:
            self.previous_angular_sign = current_angular_sign

        self.samples.append(Sample(
            t=now,
            x=x,
            y=y,
            theta=theta,
            distance_error=distance_error,
            angle_error=angle_error,
            linear_velocity=linear_velocity,
            angular_velocity=angular_velocity
        ))

        # Stop condition
        if distance_error <= self.tolerance:
            self.finished = True
            self.final_error = distance_error
            self.stop_turtle()
            self.print_metrics()
            self.save_csv()
            if self.create_plots:
                self.save_plots()
            
            # Shutdown the node after finishing the task
            raise SystemExit
            return

        msg = Twist()
        msg.linear.x = linear_velocity
        msg.angular.z = angular_velocity
        self.publisher_.publish(msg)

        self.get_logger().info(
            f'DTG={distance_error:.3f} | angle_error={math.degrees(angle_error):.2f} deg | '
            f'v={linear_velocity:.3f} | w={angular_velocity:.3f}'
        )

    def compute_average_error(self) -> float:
        if not self.samples:
            return 0.0
        return sum(s.distance_error for s in self.samples) / len(self.samples)

    def print_metrics(self):
        arrival_time = self.samples[-1].t if self.samples else 0.0
        avg_error = self.compute_average_error()

        self.get_logger().info('\nMeta alcanzada.\n')
        self.get_logger().info('Métricas de desempeño:')
        self.get_logger().info(f'Error inicial: {self.initial_error:.4f}')
        self.get_logger().info(f'Error final: {self.final_error:.4f}')
        self.get_logger().info(f'Tiempo de llegada: {arrival_time:.4f} s')
        self.get_logger().info(f'Distancia recorrida: {self.distance_traveled:.4f}')
        self.get_logger().info(f'Error máximo: {self.max_error:.4f}')
        self.get_logger().info(f'Error promedio: {avg_error:.4f}')
        self.get_logger().info(f'Oscilaciones detectadas: {self.oscillations}')
        self.get_logger().info(f'Velocidad máxima: {self.max_velocity:.4f}')

    def save_csv(self):
        csv_path = os.path.join(self.output_dir, f'{self.case_name}_metrics.csv')
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'time_s', 'x', 'y', 'theta_rad', 'distance_error',
                'angle_error_rad', 'linear_velocity', 'angular_velocity'
            ])
            for s in self.samples:
                writer.writerow([
                    f'{s.t:.6f}', f'{s.x:.6f}', f'{s.y:.6f}', f'{s.theta:.6f}',
                    f'{s.distance_error:.6f}', f'{s.angle_error:.6f}',
                    f'{s.linear_velocity:.6f}', f'{s.angular_velocity:.6f}'
                ])

        self.get_logger().info(f'CSV saved: {csv_path}')

    def save_plots(self):
        try:
            import matplotlib.pyplot as plt
        except Exception as exc:
            self.get_logger().warn(f'Matplotlib is not available. Plots were not created. Error: {exc}')
            return

        if not self.samples:
            return

        t = [s.t for s in self.samples]
        err = [s.distance_error for s in self.samples]
        v = [s.linear_velocity for s in self.samples]
        w = [s.angular_velocity for s in self.samples]

        # Error vs time
        plt.figure()
        plt.plot(t, err)
        plt.xlabel('Time [s]')
        plt.ylabel('Distance error [m]')
        plt.title(f'Distance Error vs Time - {self.case_name}')
        plt.grid(True)
        path_error = os.path.join(self.output_dir, f'{self.case_name}_error_vs_time.png')
        plt.savefig(path_error, dpi=150, bbox_inches='tight')
        plt.close()

        # Linear velocity vs time
        plt.figure()
        plt.plot(t, v)
        plt.xlabel('Time [s]')
        plt.ylabel('Linear velocity [m/s]')
        plt.title(f'Linear Velocity vs Time - {self.case_name}')
        plt.grid(True)
        path_linear = os.path.join(self.output_dir, f'{self.case_name}_linear_velocity.png')
        plt.savefig(path_linear, dpi=150, bbox_inches='tight')
        plt.close()

        # Angular velocity vs time
        plt.figure()
        plt.plot(t, w)
        plt.xlabel('Time [s]')
        plt.ylabel('Angular velocity [rad/s]')
        plt.title(f'Angular Velocity vs Time - {self.case_name}')
        plt.grid(True)
        path_angular = os.path.join(self.output_dir, f'{self.case_name}_angular_velocity.png')
        plt.savefig(path_angular, dpi=150, bbox_inches='tight')
        plt.close()

        # Trajectory plot (X vs Y)
        plt.figure()
        x_pos = [s.x for s in self.samples]
        y_pos = [s.y for s in self.samples]
        plt.plot(x_pos, y_pos, 'b-', label='Trayectoria')
        plt.plot(x_pos[0], y_pos[0], 'go', label='Inicio')
        plt.plot(self.x_goal, self.y_goal, 'rx', label='Meta')
        plt.xlabel('X [m]')
        plt.ylabel('Y [m]')
        plt.title(f'Trayectoria del Robot - {self.case_name}')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        path_trajectory = os.path.join(self.output_dir, f'{self.case_name}_trajectory.png')
        plt.savefig(path_trajectory, dpi=150, bbox_inches='tight')
        plt.close()

        self.get_logger().info(f'Plots saved in: {self.output_dir}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleGoToGoalMetrics()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop_turtle()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
