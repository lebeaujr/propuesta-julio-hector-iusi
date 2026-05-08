# Propuesta Julio Héctor: dashboards y base técnica

Este repositorio reúne dos visualizaciones y su base técnica mínima para explorar la propuesta de reforma tributaria inmobiliaria asociada al IUSI conocida aquí como “propuesta Julio Héctor”.

## Contenido principal

- `index.html`: portada del repositorio con enlaces a los dos dashboards.
- `dashboards/julio_hector_dashboard.html`: tablero general de impactos de la propuesta.
- `dashboards/jh_proxy_municipal_radar.html`: radar municipal de intensidad inmobiliaria formal y resumen fiscal proxy.
- `docs/`: notas técnicas, comunicacionales y de lectura de la propuesta.
- `data/`: tablas base y salidas resumidas utilizadas para alimentar los dashboards.
- `scripts/`: generadores de ambos dashboards.

## Qué muestra cada dashboard

### 1. Dashboard general de Julio Héctor

Resume en formato accesible:

- qué propone la reforma;
- cómo cambia el IUSI directo;
- cómo podría operar una compensación municipal asociada al IVA inmobiliario;
- qué perfiles sociales ganan más;
- y qué efectos de mercado podrían activarse.

### 2. Radar proxy municipal

Permite comparar dos municipios del país y ver:

- urbanidad y centralidad;
- mercado inmobiliario formal;
- finanzas, crédito y formalidad;
- capacidad institucional y catastral;
- y un resumen fiscal proxy del IUSI actual y con reforma.

## Alcance

Este repositorio no presenta cifras oficiales de IVA inmobiliario territorializado por municipio. En su lugar, usa una **matriz proxy** construida a partir de IUSI municipal 2025, ADIG-Innovaterra/RIIM 2024 y FUNDESA/ICL 2025 para aproximar el potencial relativo de actividad inmobiliaria formal.

## Publicación sugerida

El repositorio está preparado para publicarse con **GitHub Pages** usando:

- `index.html` en la raíz;
- `.nojekyll` para evitar conflictos con archivos estáticos.

Ver también:

- `metodologia.md`
- `publicar_en_github_pages.md`
