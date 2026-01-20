# Sistema de Trading Algorítmico – Estrategia SMA (SP500)

Este proyecto implementa un **sistema de trading algorítmico en Python** basado en una estrategia de medias móviles simples (SMA), inspirada en principios de _price action_, gestión de riesgo profesional y ejecución realista.

El sistema realiza un **backtest histórico sobre el índice S&P 500** utilizando datos diarios desde 1990, calculando métricas clave y generando la curva de capital.

---

## Descripción General

El proyecto está dividido en **tres archivos principales**, cada uno con una responsabilidad clara:

- `data_loader.py` → Descarga y prepara los datos históricos
- `strategy.py` → Contiene la lógica completa de la estrategia
- `main.py` → Ejecuta el backtest, calcula métricas y grafica resultados

Esta separación sigue buenas prácticas de diseño y facilita el mantenimiento, la extensión y la reutilización del código.

---

## Estructura del Proyecto

```
Estrategia Iván Scherman/
│
├── main.py           # Script principal: ejecución del backtest y resultados
├── data_loader.py    # Descarga y limpieza de datos del SP500
├── strategy.py       # Lógica de la estrategia y gestión del capital
├── requirements.txt  # Bibliotecas del proyecto
└── README.md         # Documentación del proyecto
```

---

## Estrategia de Trading

### Filtro de Tendencia

- Solo se buscan **operaciones largas (long)**.
- El precio debe estar **por encima de la SMA 200**, lo que filtra mercados bajistas.

### Condición de Entrada

Se entra en largo cuando se cumplen **todas** las siguientes condiciones:

1. Precio por encima de la SMA 200
2. Tres velas consecutivas bajistas
3. Cada cierre es menor que el anterior
4. No existen gaps relevantes entre velas
5. La volatilidad histórica es válida

La entrada se ejecuta **al precio de apertura del día siguiente**, evitando _look-ahead bias_.

### Stop Loss

- Stop dinámico basado en volatilidad histórica (desvío estándar de retornos).
- Ajustable mediante el parámetro `vol_multiplier`.

### Salida

La posición se cierra cuando ocurre **alguna** de las siguientes condiciones:

- El precio alcanza el **stop loss**
- El precio cierra por encima de la **SMA 5**, indicando fin del pullback

---

## Gestión de Riesgo

- Riesgo fijo por operación (por defecto: **1% del capital**)
- Tamaño de posición calculado dinámicamente según el stop
- Capital marcado a mercado en cada barra

Este enfoque evita el sobreapalancamiento y replica prácticas profesionales de trading.

---

## Métricas Calculadas

Al finalizar el backtest, el sistema muestra:

- Capital inicial
- Capital final
- Rentabilidad total (%)
- Cantidad de trades
- Winrate (%)
- Máximo Drawdown (%)

Además, se genera una **curva de capital en escala logarítmica**.

---

## Dependencias

El proyecto utiliza las siguientes bibliotecas:

- **pandas** → Manipulación de datos financieros
- **numpy** → Cálculos numéricos y manejo de NaN
- **matplotlib** → Visualización de resultados
- **yfinance** → Descarga de datos históricos desde Yahoo Finance

Instalación recomendada:

```
pip install pandas numpy matplotlib yfinance
```

---

## Ejecución

Para ejecutar el backtest:

```
python main.py
```

El script descargará los datos, ejecutará la estrategia y mostrará los resultados en consola junto con el gráfico de la curva de capital.

---

## Advertencia

Este proyecto tiene **fines educativos y de investigación**.

- Los datos provienen de Yahoo Finance (no aptos para trading en vivo).
- No se consideran comisiones ni slippage.

---

## Posibles Mejoras

- Incorporar comisiones y slippage
- Calcular métricas avanzadas (Sharpe, Sortino, Calmar)
- Optimización de parámetros
- Walk-forward analysis
- Soporte multi-activo
- Conexión a datos en tiempo real

---

## Conclusión

Este sistema representa una **base sólida y profesional** para el desarrollo de estrategias cuantitativas:

- Arquitectura clara
- Gestión de riesgo realista
- Ejecución sin sesgos
- Fácil de extender y optimizar

Ideal como punto de partida para investigación cuantitativa avanzada o evolución hacia trading algorítmico en vivo.
