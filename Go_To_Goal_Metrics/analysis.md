# Análisis de Métricas - Lab 3

![Conceptual Dashboard](/home/RicardoCRosas/.gemini/antigravity/brain/2e4b5626-2558-4d4a-bbbb-144419d6d4ba/lab_dashboard_premium_1778489353523.png)

Este archivo contiene el análisis detallado de los resultados obtenidos en las simulaciones de control del robot Turtlesim en ROS 2.

## Resumen de Resultados

A continuación se presentan las métricas obtenidas para los tres casos de prueba:

| Case | Initial Error | Final Error | Arrival Time (s) | Distance Traveled | Max Error | Avg Error | Max Velocity |
|---|---|---|---|---|---|---|---|
| Case A (k_l=0.8, k_a=3.0) | 3.4727 | 0.0981 | 5.3507 | 3.4810 | 3.4727 | 1.0027 | 2.3562 |
| Case B (k_l=1.0, k_a=4.0) | 3.4727 | 0.0956 | 3.8991 | 3.4500 | 3.4727 | 1.1138 | 3.1416 |
| Case C (k_l=1.5, k_a=6.0) | 3.4727 | 0.0980 | 2.7505 | 3.4134 | 3.4727 | 1.2620 | 4.7124 |

## Evidencias Gráficas

### Caso A: k_linear=0.8, k_angular=3.0
- **Trayectoria**: ![Trayectoria Case A](metrics_results/case_A_trajectory.png)
- **Error vs Tiempo**: ![Error Case A](metrics_results/case_A_error_vs_time.png)
- **Velocidad Lineal**: ![Linear Vel Case A](metrics_results/case_A_linear_velocity.png)
- **Velocidad Angular**: ![Angular Vel Case A](metrics_results/case_A_angular_velocity.png)

### Caso B: k_linear=1.0, k_angular=4.0
- **Trayectoria**: ![Trayectoria Case B](metrics_results/case_B_trajectory.png)
- **Error vs Tiempo**: ![Error Case B](metrics_results/case_B_error_vs_time.png)
- **Velocidad Lineal**: ![Linear Vel Case B](metrics_results/case_B_linear_velocity.png)
- **Velocidad Angular**: ![Angular Vel Case B](metrics_results/case_B_angular_velocity.png)

### Caso C: k_linear=1.5, k_angular=6.0
- **Trayectoria**: ![Trayectoria Case C](metrics_results/case_C_trajectory.png)
- **Error vs Tiempo**: ![Error Case C](metrics_results/case_C_error_vs_time.png)
- **Velocidad Lineal**: ![Linear Vel Case C](metrics_results/case_C_linear_velocity.png)
- **Velocidad Angular**: ![Angular Vel Case C](metrics_results/case_C_angular_velocity.png)

## Conclusiones

1. **Trayectoria**: En las gráficas de trayectoria se observa claramente el punto de inicio (círculo verde) y el punto de meta (X roja). El robot sigue un camino suave hacia el objetivo, ajustando su orientación antes de avanzar linealmente de forma agresiva.
2. **Efecto de las Ganancias**: Se observa que al aumentar las ganancias $k_{linear}$ y $k_{angular}$, el tiempo de llegada disminuye significativamente (de 5.35s en el Caso A a 2.75s en el Caso C).
3. **Precisión**: Todos los casos alcanzaron la meta con un error final dentro de la tolerancia de 0.1m.
4. **Comportamiento**: El Caso C, aunque es el más rápido, presenta mayores velocidades máximas y una curva de error más pronunciada, lo que indica un control más agresivo. No se detectaron oscilaciones que comprometieran la estabilidad.
