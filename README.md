# Lab 3: Metrics

Este repositorio contiene la entrega individual para el Lab 3 de ROS 2.

## Requisitos
- ROS 2 Humble
- Turtlesim
- Matplotlib y Pandas (para generación de métricas y gráficas)

## Instalación
1. Clona este repositorio en tu espacio de trabajo (colcon_ws/src).
2. Construye el paquete:
   ```bash
   colcon build --packages-select go_to_goal_metrics
   ```
3. Carga el entorno:
   ```bash
   source install/setup.bash
   ```

## Uso
Para ejecutar el controlador con los parámetros por defecto:
```bash
ros2 run go_to_goal_metrics turtle_go_to_goal_metrics
```

Puedes pasar parámetros personalizados:
```bash
ros2 run go_to_goal_metrics turtle_go_to_goal_metrics --ros-args -p x_goal:=9.0 -p y_goal:=2.0 -p k_linear:=1.5
```
