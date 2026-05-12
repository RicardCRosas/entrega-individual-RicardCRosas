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

---

# Análisis de Ingeniería

## Identify

1. **¿Cuáles son los objetivos principales del controlador?**
   El objetivo principal es lograr que el robot móvil (Turtlesim) se desplace hacia una meta fija `(x_goal, y_goal)` partiendo desde cualquier posición inicial, minimizando el error posicional de manera autónoma. Además, el movimiento debe ser estable, eficiente y capaz de detenerse automáticamente al alcanzar una precisión aceptable (error < tolerancia).

2. **¿Qué restricciones de diseño identificaste?**
   - El robot es no holonómico (sólo avanza hacia adelante y rota), lo que implica que debe alinear su ángulo (`theta`) antes de avanzar efectivamente hacia la meta.
   - Las velocidades máximas del sistema están limitadas para evitar comportamientos erráticos.
   - Existe un compromiso entre la rapidez para llegar (altas velocidades) y la estabilidad (evitar oscilaciones y "overshoot").
   - Es necesario mantener un movimiento suave y seguro sin oscilaciones excesivas que desgastarían los actuadores.

---

## Analyze

3. **¿Cómo afectan las ganancias del controlador al desempeño?**
   - El aumento de la ganancia proporcional lineal (`k_linear`) hace que el robot reaccione más rápido para reducir la distancia (acelera más), reduciendo el tiempo total pero pudiendo causar inestabilidad (overshoot) si no está balanceado.
   - El aumento de la ganancia proporcional angular (`k_angular`) acelera la corrección de orientación del robot hacia el punto deseado. Un valor alto ayuda a alinear rápido y evitar "arcos" largos, pero si es demasiado alto, el robot puede oscilar en torno a la orientación deseada.

4. **¿Qué métricas fueron más importantes para evaluar el sistema?**
   Las métricas más relevantes fueron:
   - **Tiempo de llegada**: para medir la agilidad del sistema.
   - **Error final**: para validar la precisión al detenerse.
   - **Oscilaciones**: porque indican directamente la estabilidad y el consumo eficiente del controlador.

---

## Develop Solutions

5. **¿Qué estrategia utilizaste para mejorar el controlador?**
   Aumentar las ganancias de control de forma empírica y analizar los resultados visualmente (gráficas de velocidad y error) y métricamente (tiempos y distancia recorrida). Se ajustaron $k_l$ y $k_a$ manteniendo una proporción en la cual la alineación sea rápida para optimizar el trayecto final rectilíneo.

6. **¿Qué combinación de ganancias produjo el mejor resultado?**
   La combinación del **Caso C ($k_l=1.5, k_a=6.0$)** produjo el mejor resultado. Proporcionó el tiempo más corto de llegada (2.75s) manteniendo cero oscilaciones notables y un error de distancia que converge limpiamente sin salirse de la ruta.

---

## Evaluate Solutions

7. **¿Qué controlador tuvo mejor desempeño y por qué?**
   El controlador del **Caso C** obtuvo el mejor desempeño general porque redujo el tiempo de llegada a casi la mitad comparado con el caso base, no incrementó la distancia recorrida significativamente, mantuvo un error final de 0.098 m y demostró ser el más ágil para alinear la dirección del robot con la meta.

8. **¿Qué trade-offs observaste entre rapidez y estabilidad?**
   En el controlador del Caso C, las velocidades angulares alcanzan picos más altos inicialmente (movimiento agresivo). Aunque esto resulta en una convergencia más rápida, en un entorno físico implicaría mayor torque instantáneo, lo que puede provocar deslizamiento en las ruedas de un robot real.

---

## Sustainability

9. **¿Por qué minimizar oscilaciones y trayectorias innecesarias puede ser importante en robots reales?**
   En la vida real, cada oscilación se traduce en movimientos repetitivos de los motores, lo que provoca desgaste excesivo de los engranes, mayor fricción, calentamiento y un comportamiento impredecible que es peligroso cerca de humanos o de equipos valiosos.

10. **¿Cómo impacta la eficiencia de movimiento en:**
   - **consumo energético:** Movimientos suaves y directos conservan la carga de las baterías, alargando la autonomía del robot.
   - **desgaste mecánico:** Trayectorias sin cambios bruscos de dirección extienden la vida útil de motores y transmisiones.
   - **seguridad:** Un movimiento directo y predecible reduce enormemente el riesgo de colisión.
   - **sostenibilidad:** Alargar la vida útil de los componentes y optimizar el uso de energía se alinea con la meta de producir tecnología duradera, reduciendo la generación de residuos electrónicos y consumo general.
