# Nota técnica: matriz proxy municipal de intensidad inmobiliaria formal

## 1. Objeto

Esta nota documenta la construcción de la matriz proxy municipal utilizada para aproximar la posible territorialización del `IVA inmobiliario` en ausencia de una base observada de recaudación municipal de ese impuesto.

La matriz fue diseñada inicialmente para recalibrar el módulo `JH-F2` de la propuesta de Julio Héctor, pero su utilidad va más allá de ese caso. También puede servir para:

- aproximar la geografía del mercado inmobiliario formal;
- identificar municipios con mayor probabilidad de captar impuestos ligados a transacciones y construcción formal;
- diferenciar mejor municipios grandes, intermedios y pequeños desde una lógica inmobiliaria y no solo demográfica;
- apoyar simulaciones futuras sobre compensación municipal, mercado de vivienda, crédito y formalización.

## 2. Problema que busca resolver

La propuesta de Julio Héctor introduce una lógica de compensación municipal basada en `IVA inmobiliario`. El problema empírico es que no contamos con una base municipal observada, cerrada y pública que permita responder directamente:

- cuánto `IVA inmobiliario` recauda cada municipio;
- qué parte de ese flujo proviene de vivienda nueva, compraventa formal u operaciones inmobiliarias urbanas;
- cómo se distribuye territorialmente ese flujo.

Sin esa base, la compensación no puede estimarse como observación directa. Por eso se construyó una **matriz proxy**, es decir, una aproximación empírica basada en variables observables que, en conjunto, captan la **intensidad inmobiliaria formal** de cada municipio.

## 3. Lógica conceptual

La hipótesis central es que el `IVA inmobiliario` no se repartiría territorialmente como el `IUSI` actual de manera mecánica. Su captación dependería más de municipios con:

- mayor urbanización y centralidad;
- más construcción formal;
- más empresas y actividad económica visible;
- mayor presencia de crédito, banca y formalidad laboral;
- mejor capacidad institucional y catastral.

Por tanto, la matriz no intenta replicar solamente la geografía del `IUSI percibido`, sino combinarla con señales del **mercado inmobiliario formal** y de la **capacidad institucional local**.

## 4. Fuentes utilizadas

Se integraron tres familias de fuentes:

### 4.1. Base municipal de IUSI 2025

Archivo:
- [iusi_minfin_municipal_2025.csv](C:/IUSI/Datos%20Kevin/data/raw/sat/iusi_minfin_municipal_2025.csv)

Variables principales usadas:
- `iusi_vigente_Q`
- `iusi_devengado_Q`
- `iusi_percibido_Q`
- `municipalidad`
- `departamento`
- `region`
- `cod_entidad`

Uso dentro de la matriz:
- aporta la señal observada de recaudación municipal actual;
- permite construir un ranking empírico de visibilidad fiscal inmobiliaria;
- ayuda a que la matriz no se vuelva un índice puramente abstracto.

### 4.2. Ranking ADIG / RIIM 2024

Archivo:
- [Ranking_ADIG_INDICADORES_240214 FINAL 22-02-2024 v trabajo.xlsx](C:/IUSI/Ranking_ADIG_INDICADORES_240214%20FINAL%2022-02-2024%20v%20trabajo.xlsx)

Hoja usada:
- `INDICADORES`

Esta fuente aporta variables directamente ligadas a condiciones urbanas, mercado inmobiliario, construcción y herramientas territoriales municipales.

### 4.3. FUNDESA / ICL 2025

Archivo:
- [FUNDESA_-_ICL_2025_Database.xlsx](C:/IUSI/FUNDESA_-_ICL_2025_Database.xlsx)

Hojas usadas:
- `ICL 2025 (12 pilares)`
- `ICL 2025 (datos serie original)`

Esta fuente aporta variables de formalidad, sistema financiero, tamaño de mercado, institucionalidad e infraestructura, muy útiles para aproximar la probabilidad de que exista actividad inmobiliaria formal gravable.

## 5. Unidad de análisis y cobertura

La unidad de análisis es el **municipio**.

La matriz final cubre:
- `280` municipios con información usable;
- `280` municipios con valor en `IUSI percibido 2025`;
- `280` municipios con score compuesto;
- `280` municipios con información en los cuatro bloques del índice.

La llave de integración se construyó a partir del código municipal:
- en `IUSI`, a partir de los últimos cuatro dígitos de `cod_entidad`;
- en ADIG y FUNDESA, a partir de los códigos municipales reportados en sus propias bases.

## 6. Variables incorporadas

La matriz se construyó sobre cuatro bloques.

### 6.1. Urbanidad y centralidad

Busca captar municipios donde hay mayor densidad urbana, concentración de equipamientos y actividad espacialmente visible.

Indicadores incluidos:
- `VIIRS`
- `Equipamientos urbanos importantes`
- `Densidad habxkm2`
- `Poblacion 2018`
- `INFRAESTRUCTURA`
- `PIB local (US$ al año por Km2)`

Interpretación:
- municipios más densos, iluminados, equipados y con mayor intensidad económica por superficie tienden a tener mercados inmobiliarios más activos y formalizados.

### 6.2. Mercado inmobiliario formal

Busca captar señales más directas de actividad inmobiliaria y capacidad de demanda solvente.

Indicadores incluidos:
- `Cantidad de actividades relacionadas a la construcción`
- `Cantidad de Empresas`
- `Segmento abc alquila`
- `Ingreso mensual medio por hogar`
- `Porcentaje del segmento ABC`
- `Tamaño del mercado`
- `Dinamismo de los negocios`

Interpretación:
- donde hay más construcción, más empresas, hogares con mayor ingreso y segmentos medios-altos, es más plausible observar operaciones formales de vivienda, compraventa, alquiler formal y desarrollo inmobiliario.

### 6.3. Finanzas, crédito y formalidad

Busca captar condiciones financieras y laborales que facilitan vivienda formal, financiamiento hipotecario y operaciones bancarizadas.

Indicadores incluidos:
- `Cartera de Créditos en relación al PIB`
- `% de la PEA afiliada al IGSS`
- `Agentes Bancarios por 100,000 hab.`
- `Depósitos en relación al PIB per cápita`
- `SISTEMA FINANCIERO`

Interpretación:
- municipios con mayor bancarización, crédito y formalidad laboral tienden a sostener mejor mercados inmobiliarios formales y gravables.

### 6.4. Capacidad institucional y catastral

Busca captar qué tan preparado está el municipio para soportar formalización territorial, ordenamiento y administración del impuesto.

Indicadores incluidos:
- `Uso del Catastro como instrumento de OT`
- `Reglamento de construción como aplicación del plan de uso de suelo y reglamento de ordenamiento territorial`
- `Autonomía financiera`
- `Volumen de la tributación`
- `Ranking Gestión Municipal`
- `INSTITUCIONES`
- `ICL 2025`

Interpretación:
- municipios con mejor capacidad de gestión, uso catastral y marco regulatorio son mejores candidatos para capturar y administrar flujos ligados a mercado inmobiliario formal.

## 7. Método de construcción

### 7.1. Limpieza y homologación

Se hizo una limpieza básica de texto para:
- corregir problemas de codificación;
- unificar nombres municipales;
- normalizar espacios y caracteres.

Además, se armonizaron nombres de variables para que la salida quedara legible y reutilizable.

### 7.2. Conversión a escala comparable

Como los indicadores vienen en unidades distintas:
- conteos;
- porcentajes;
- índices;
- montos;
- densidades;

se transformó cada variable a **rango percentilar** dentro del universo municipal mediante `rank(pct=True) * 100`.

Esto implica que:
- un municipio con valor `90` en una variable está por encima de aproximadamente el `90%` de los municipios en ese indicador;
- la matriz compara posiciones relativas, no magnitudes absolutas.

### 7.3. Construcción de bloques

Dentro de cada bloque, el score municipal se calculó como el **promedio simple** de los percentiles disponibles de sus indicadores.

Así se obtuvieron:
- `urbanidad_centralidad_score`
- `mercado_inmobiliario_formal_score`
- `finanzas_credito_formalidad_score`
- `capacidad_institucional_catastral_score`

### 7.4. Construcción del índice compuesto

El índice final:
- `intensidad_inmobiliaria_formal_score`

se calculó con la siguiente ponderación:

- `30%` urbanidad y centralidad
- `30%` mercado inmobiliario formal
- `25%` finanzas, crédito y formalidad
- `15%` capacidad institucional y catastral

La lógica de esta ponderación es:
- dar más peso a condiciones urbanas y de mercado, porque son el corazón de la actividad inmobiliaria gravable;
- dar peso importante a crédito y formalidad, porque el IVA inmobiliario depende fuertemente de operaciones visibles y bancarizadas;
- mantener la institucionalidad como factor relevante, pero no dominante.

### 7.5. Del índice al peso proxy de IVA

Después del índice compuesto se generaron dos elementos adicionales:

1. `proxy_iva_potential_index_100`
   - ranking percentilar del índice compuesto;
   - mide potencial relativo de captación de IVA inmobiliario.

2. `proxy_iva_weight_share_pct`
   - se construyó combinando:
     - el ranking del potencial inmobiliario formal; y
     - el ranking del `IUSI percibido 2025`.

La fórmula operativa fue:

`peso bruto = (ranking potencial / 100) * (ranking IUSI percibido / 100)`

Luego esos pesos brutos se normalizaron para obtener un porcentaje de participación municipal sobre el total.

Interpretación:
- el `proxy_iva_potential_index_100` dice quién tiene más potencial relativo;
- el `proxy_iva_weight_share_pct` dice cómo repartir una compensación agregada si queremos combinar potencial inmobiliario con presencia fiscal municipal ya observada.

## 8. Resultados principales

### 8.1. Concentración territorial

La matriz muestra una fuerte concentración en:
- municipios metropolitanos de Guatemala;
- municipios urbanos consolidados de Sacatepéquez;
- cabeceras y nodos regionales con mercado formal activo.

Los primeros lugares por `peso proxy final` son:
- `Mixco`
- `Guatemala`
- `San Miguel Petapa`
- `Villa Nueva`
- `Santa Catarina Pinula`
- `Fraijanes`
- `San Jose Pinula`
- `Villa Canales`
- `Amatitlan`
- `Antigua Guatemala`

También aparecen con fuerza:
- `Quetzaltenango`
- `Escuintla`
- `Huehuetenango`
- `Chimaltenango`

### 8.2. Lectura sustantiva

La señal principal es que una compensación municipal basada en `IVA inmobiliario` sería probablemente:
- mucho más potente en municipios grandes, metropolitanos y formalizados;
- intermedia en cabeceras urbanas regionales;
- más débil en municipios pequeños o de baja formalidad.

Esto refuerza una intuición importante de `JH-F2`: la compensación por IVA no neutraliza de manera homogénea la caída del IUSI. Puede cerrar mucho mejor en mercados urbanos grandes que en municipios más periféricos o rurales.

## 9. Fortalezas de la matriz

- No depende exclusivamente de juicio experto.
- Usa información municipal ya disponible.
- Integra dimensión urbana, económica, financiera e institucional.
- Es flexible y se puede recalibrar.
- Sirve tanto para simulaciones fiscales como para lectura territorial del mercado formal.

## 10. Limitaciones

La matriz tiene límites importantes y debe leerse con prudencia.

### 10.1. No observa IVA real

No es una base observada de `IVA inmobiliario`. Es una aproximación indirecta.

### 10.2. Trabaja con posiciones relativas

Los percentiles ordenan municipios entre sí, pero no permiten inferir directamente montos absolutos de IVA.

### 10.3. Mezcla señales de oferta, demanda y capacidad institucional

Eso es útil para una aproximación general, pero no equivale a medir operaciones inmobiliarias concretas.

### 10.4. Puede sobrerrepresentar centralidad metropolitana

Como varias variables están correlacionadas con urbanización y tamaño, la matriz naturalmente eleva municipios metropolitanos. Eso no es necesariamente un error, pero sí una característica que conviene explicitar.

### 10.5. No incorpora transacciones observadas

No incluye aún:
- compraventas efectivas;
- licencias de construcción municipales comparables;
- inscripciones registrales observadas;
- cartera hipotecaria municipal directa;
- datos tributarios territoriales de IVA.

Si esas bases aparecen, la matriz debería actualizarse.

## 11. Uso recomendado en adelante

Esta matriz puede servir para:

- recalibrar `JH-F2` en lugar de repartir compensación solo por grupos grandes/medianos/pequeños;
- construir escenarios de compensación `bajo / central / alto` más empíricos;
- identificar municipios “ganadores” y “perdedores” probables bajo una municipalización del IVA inmobiliario;
- apoyar análisis futuros sobre vivienda formal, crédito, construcción y mercado metropolitano;
- servir como insumo para dashboards o mapas territoriales.

## 12. Traducción de la matriz a dashboard

Además de la matriz y sus notas de apoyo, se construyó un dashboard específico para explorar los `280` municipios de manera visual.

Archivo principal:
- [jh_proxy_municipal_radar.html](C:/IUSI/dashboard/jh_proxy_municipal_radar.html)

Script generador:
- [build_jh_proxy_radar_dashboard.py](C:/IUSI/scripts/build_jh_proxy_radar_dashboard.py)

La lógica del dashboard es traducir la matriz técnica a un formato más cercano a los tableros de `ranking` o `ICL`, donde el usuario pueda:

- seleccionar un municipio;
- comparar dos municipios lado a lado;
- observar la forma relativa de sus perfiles;
- y leer los bloques y subindicadores sin tener que entrar directamente al `.csv`.

El dashboard no agrega nueva información al índice. Su función es hacer visible, navegable y comparable la estructura ya calculada en la matriz.

## 13. Estructura del dashboard

El dashboard fue diseñado como archivo `HTML` autocontenido, de modo que pueda:

- abrirse localmente sin servidor;
- compartirse como archivo único;
- y, si se desea, publicarse más adelante vía `GitHub Pages`.

Sus componentes principales son:

### 13.1. Filtros y selección

Incluye:
- filtro por `región`;
- filtro por `departamento`;
- búsqueda rápida por nombre;
- selección de `Municipio A`;
- selección de `Municipio B`;
- selección del bloque de detalle.

Esto permite pasar de una lectura general del universo municipal a comparaciones concretas entre territorios específicos.

### 13.2. Tarjetas de resumen

Para cada comparación, el tablero muestra:
- `IUSI percibido 2025`;
- `IUSI vigente 2025`;
- `índice compuesto`;
- `potencial IVA`;
- `peso proxy IVA`.

Estas tarjetas ayudan a conectar tres planos:
- la observación fiscal actual (`IUSI`);
- la posición relativa dentro del índice;
- y la posible participación en una compensación vía `IVA inmobiliario`.

### 13.3. Telaraña principal

La gráfica principal de radar muestra simultáneamente los cuatro bloques:
- `6.1 Urbanidad y centralidad`
- `6.2 Mercado inmobiliario formal`
- `6.3 Finanzas, crédito y formalidad`
- `6.4 Capacidad institucional y catastral`

Cada municipio aparece con un color distinto. Esto permite ver no solo quién tiene mayor score agregado, sino también **cómo está compuesto ese score**.

Por ejemplo:
- dos municipios pueden tener índice compuesto parecido;
- pero uno puede ser fuerte en mercado y débil en institucionalidad;
- mientras otro puede tener perfil más equilibrado.

### 13.4. Telaraña de subindicadores

El dashboard incluye una segunda gráfica de radar que se actualiza según el bloque elegido. Ahí se muestran los subindicadores percentilares del bloque para los dos municipios comparados.

Esto es importante porque evita que el análisis se quede en promedios agregados y permite ver:
- qué indicador empuja hacia arriba un bloque;
- qué indicador lo frena;
- y si la diferencia entre municipios proviene de un patrón amplio o de uno o dos ejes particulares.

### 13.5. Tabla comparativa

Debajo de la telaraña de subindicadores se presenta una tabla con:
- nombre del indicador;
- percentil del Municipio A;
- valor original del Municipio A;
- percentil del Municipio B;
- valor original del Municipio B.

Esta tabla cumple una función de trazabilidad:
- el radar resume;
- la tabla permite verificar.

## 14. Método de construcción del dashboard

El dashboard se construyó a partir del archivo:
- [jh_f2_proxy_matrix_municipal.csv](C:/IUSI/data/jh_f2_proxy_matrix_municipal.csv)

El script:
- [build_jh_proxy_radar_dashboard.py](C:/IUSI/scripts/build_jh_proxy_radar_dashboard.py)

realiza las siguientes operaciones:

### 14.1. Lectura de la matriz base

Carga la matriz municipal ya calculada y toma como insumo:
- scores de bloque;
- valores originales de subindicadores;
- `IUSI percibido`;
- `IUSI vigente`;
- `proxy_iva_potential_index_100`;
- `proxy_iva_weight_share_pct`.

### 14.2. Recalculo de percentiles para subindicadores

Aunque la matriz ya contiene scores compuestos, el dashboard recalcula percentiles por subindicador para poder dibujar las telarañas internas de manera homogénea en escala `0-100`.

Esto asegura que:
- todos los ejes del radar tengan una métrica comparable;
- y que la visualización responda a posición relativa, no a unidades incompatibles.

### 14.3. Conversión a estructura JSON embebida

El script transforma la matriz en una estructura `JSON` embebida dentro del `HTML`, con:
- lista de municipios;
- metadatos;
- bloques;
- indicadores;
- valores percentilares;
- valores originales.

Esto hace que el tablero sea:
- autocontenido;
- reproducible;
- y fácil de compartir.

### 14.4. Renderizado en cliente

La visualización se dibuja con `JavaScript` y `canvas` nativo, sin depender de librerías externas. Se eligió esta ruta para:

- mantener el archivo liviano y portable;
- evitar dependencias web;
- asegurar que funcione localmente sin conexión.

## 15. Utilidad analítica del dashboard

El dashboard agrega valor analítico por varias razones.

### 15.1. Permite comparar perfiles, no solo rankings

Una tabla de ranking dice quién está arriba y quién abajo. El radar permite ver la **forma** del municipio:
- si su fortaleza está en centralidad urbana;
- en crédito y formalidad;
- en institucionalidad;
- o en una combinación de factores.

### 15.2. Hace visibles diferencias entre municipios similares

Municipios con parecido `IUSI percibido` pueden tener perfiles muy distintos de mercado formal y capacidad institucional. Eso es importante para pensar compensación, reforma o focalización territorial.

### 15.3. Facilita comunicación no técnica

Para discusión con actores no especializados, el dashboard traduce la matriz en un formato más intuitivo que un archivo tabular de 280 filas.

### 15.4. Sirve para hipótesis futuras

Más adelante puede servir para:
- explorar clusters municipales;
- construir tipologías de mercado;
- comparar cabeceras con periferias metropolitanas;
- o contrastar territorios “ganadores” y “perdedores” de distintos esquemas de reforma.

## 16. Archivos asociados

- [build_jh_f2_proxy_matrix.py](C:/IUSI/scripts/build_jh_f2_proxy_matrix.py)
- [jh_f2_proxy_matrix_municipal.csv](C:/IUSI/data/jh_f2_proxy_matrix_municipal.csv)
- [jh_f2_proxy_matrix_summary.md](C:/IUSI/outputs/jh_f2_proxy_matrix_summary.md)
- [jh_f2_proxy_matrix.md](C:/IUSI/docs/jh_f2_proxy_matrix.md)
- [nota_proxies_iva_inmobiliario_adig_fundesa.md](C:/IUSI/docs/nota_proxies_iva_inmobiliario_adig_fundesa.md)

## 17. Siguiente paso sugerido

El siguiente paso metodológico natural es utilizar `proxy_iva_weight_share_pct` para construir una versión revisada de `JH-F2`, donde la compensación municipal:

- ya no se asigne solo por tipología general de municipios;
- sino por intensidad inmobiliaria formal territorial observada indirectamente.

Eso permitiría pasar de una compensación “por grupos” a una compensación más cercana a una geografía plausible del `IVA inmobiliario`.
