# Metodología general

Este paquete junta dos líneas de trabajo relacionadas:

1. un análisis integrado de la propuesta de Julio Héctor sobre IUSI, IVA inmobiliario e ISR;
2. una matriz proxy municipal para aproximar la distribución territorial potencial de un componente municipal de IVA inmobiliario.

## 1. Dashboard general de la propuesta

El dashboard `julio_hector_dashboard.html` se apoya en cuatro bloques:

- efecto fiscal directo del bloque IUSI;
- compensación municipal aproximada vía IVA inmobiliario;
- impacto social por perfiles de propietarios y hogares;
- efecto de mercado por alivio de tenencia y exoneración de ISR en ventas ocasionales.

Los archivos base más importantes son:

- `data/jh_f1_iusi_direct_scenarios.csv`
- `data/jh_f2b_iva_compensation_proxy_scenarios.csv`
- `data/jh_s1_social_profiles.csv`
- `data/jh_m1_market_incentives.csv`

## 2. Radar proxy municipal

El radar municipal no estima un monto observado de IVA por municipio. Construye un **índice compuesto de intensidad inmobiliaria formal** a partir de cuatro bloques:

- urbanidad y centralidad;
- mercado inmobiliario formal;
- finanzas, crédito y formalidad;
- capacidad institucional y catastral.

La base principal es:

- `data/jh_f2_proxy_matrix_municipal.csv`

Los scripts de generación son:

- `scripts/build_jh_dashboard.py`
- `scripts/build_jh_proxy_radar_dashboard.py`

## 3. Importante sobre el “resumen fiscal proxy”

El resumen fiscal del radar municipal parte del IUSI percibido actualmente en cada municipio y aplica factores centrales por grupo proxy para aproximar:

- un efecto directo de reforma sobre el IUSI;
- y un efecto neto, entendido como saldo final aproximado después de una compensación parcial ligada al IVA inmobiliario.

Esto debe leerse como una **aproximación comparativa**, no como proyección oficial municipio por municipio.
