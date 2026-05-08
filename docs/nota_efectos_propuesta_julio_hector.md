# Nota de trabajo: efectos probables de la propuesta de Julio Héctor sobre IUSI, IVA inmobiliario e ISR

## Proposito

Esta nota sintetiza los efectos probables de la **propuesta de Julio Héctor** a partir de su texto legal y de las simulaciones construidas en `C:\IUSI`.

Su objetivo es separar con claridad cinco cosas:

- qué propone exactamente la iniciativa;
- qué pasa con el `IUSI` directo;
- qué cambia cuando se agrega la compensación municipal vía `IVA inmobiliario`;
- qué efectos distributivos y sociales aparecen;
- y qué efectos de mercado sugiere la combinación `IUSI + IVA + ISR`.

La nota se apoya principalmente en:

- [lectura_tecnico_legal_julio_hector_vs_modelos.md](C:/IUSI/docs/lectura_tecnico_legal_julio_hector_vs_modelos.md)
- [tabla_comparativa_6586_6709_julio_hector.md](C:/IUSI/docs/tabla_comparativa_6586_6709_julio_hector.md)
- [jh_f1_bloque_iusi.md](C:/IUSI/docs/jh_f1_bloque_iusi.md)
- [jh_f2_compensacion_iva.md](C:/IUSI/docs/jh_f2_compensacion_iva.md)
- [jh_f2b_compensacion_iva_matriz_proxy.md](C:/IUSI/docs/jh_f2b_compensacion_iva_matriz_proxy.md)
- [jh_s1_impacto_social_perfiles.md](C:/IUSI/docs/jh_s1_impacto_social_perfiles.md)
- [jh_m1_mercado_inmobiliario.md](C:/IUSI/docs/jh_m1_mercado_inmobiliario.md)

## 1. Que propone realmente la propuesta de Julio Hector

La propuesta de Julio Héctor no debe leerse como una tercera iniciativa “de tasa del IUSI” comparable sin más a `6586` o `6709`. Su arquitectura es más amplia y combina cuatro bloques.

### 1.1 Bloque IUSI

Introduce:

- un `11 Bis` con definiciones de inmueble residencial, no residencial, mixto, residencia habitual y vivienda habitual;
- un `12 Bis` con **tasa cero** para:
  - mayores de `60 anos` con al menos `5 anos` de control del inmueble;
  - primera vivienda por hasta `7 anos`;
- un `12 Ter` con **regimen preferencial** para vivienda habitual y para inmuebles que actualicen al alza su valor fiscal.

### 1.2 Bloque de administracion y control del IUSI

Agrega reglas para:

- impedir que la mora del IUSI suspenda servicios publicos;
- mantener facultades de catastro, inspeccion y verificacion;
- exigir declaracion de uso y actualizacion de informacion;
- y habilitar un mecanismo transitorio de autoavaluo voluntario simplificado.

### 1.3 Bloque IVA inmobiliario

La propuesta no baja la tasa privada del `IVA` en operaciones inmobiliarias. Lo que hace es **destinar a municipalidades** los `7 puntos porcentuales` del `IVA efectivamente percibido` en primera venta y demas transferencias de inmuebles, con reglas de:

- registro geografico;
- avisos notariales electronicos;
- conciliacion territorial;
- y publicacion mensual de datos abiertos por municipio.

### 1.4 Bloque ISR sobre ganancia de capital

Exonera la ganancia de capital en la venta de inmuebles cuando concurren estas condiciones:

- que el vendedor sea `persona individual`;
- que no tenga `giro inmobiliario` ni `habitualidad`;
- y que haya sido propietario por al menos `3 anos` continuos.

Por tanto, la propuesta debe leerse como una **reforma tributaria inmobiliaria ampliada**: reduce o reorganiza la carga recurrente del IUSI, intenta compensar municipalidades vía IVA y altera también el costo tributario de ciertas ventas inmobiliarias.

## 2. Efecto fiscal directo del bloque IUSI

La primera conclusión fuerte es que, si se aísla solo el bloque `IUSI`, la propuesta sigue siendo contractiva para las finanzas municipales.

La simulacion `JH-F1` combina:

- tasa cero para vivienda habitual protegida;
- régimen preferencial;
- y actualización al alza del valor fiscal como incentivo.

En su escenario `central`, la caída estimada del `IUSI per capita` es:

- `Grandes`: `Q221.24 -> Q158.63` (`-28.3%`)
- `Medianas`: `Q44.37 -> Q28.08` (`-36.7%`)
- `Pequenas`: `Q7.26 -> Q4.15` (`-42.8%`)

Esta lectura es importante por dos razones.

Primero, muestra que la propuesta no es fiscalmente neutra en su componente directo de IUSI. Aun con el incentivo de actualización de valor, la combinación de tasa cero y régimen preferencial reduce con fuerza el ingreso propio municipal.

Segundo, muestra que el golpe relativo parece mayor en `Medianas` y `Pequenas` que en `Grandes`, porque las primeras pierden más base directa y tienen menos capacidad de absorber el alivio en vivienda habitual.

En otras palabras: **si se mira solo el IUSI**, la propuesta reduce ingresos municipales de forma relevante.

## 3. Efecto de compensacion via IVA inmobiliario

La segunda pregunta es si el bloque de `IVA inmobiliario` compensa esa pérdida. Aquí conviene separar dos niveles.

### 3.1 Primera aproximacion: JH-F2

`JH-F2` trabajó con shares de compensación por grupo municipal definidos como supuestos analíticos. Esa versión sugirió que la compensación podía mejorar mucho la lectura fiscal, sobre todo en `Grandes`, pero todavía descansaba en una territorialización bastante gruesa.

### 3.2 Version recalibrada: JH-F2b

`JH-F2b` mejora esa lectura usando la [nota_tecnica_matriz_proxy_iva_inmobiliario.md](C:/IUSI/docs/nota_tecnica_matriz_proxy_iva_inmobiliario.md), que reparte la compensación según un **proxy municipal de intensidad inmobiliaria formal** construido con:

- `IUSI municipal 2025`;
- `ADIG / RIIM`;
- `FUNDESA / ICL`.

En vez de fijar shares ex ante por grupo, `JH-F2b`:

1. toma la pérdida directa del `JH-F1 central`;
2. arma un `pool nacional compensatorio` prudente;
3. lo distribuye según `proxy_iva_weight_share_pct`.

En el escenario `central` de `JH-F2b`, el saldo neto queda así:

- `Grandes`: `Q158.63 -> Q165.54`, saldo `-25.2%`
- `Medianas`: `Q28.08 -> Q40.04`, saldo `-9.8%`
- `Pequenas`: `Q4.15 -> Q5.44`, saldo `-25.1%`

La lectura es muy importante:

- la compensación **sí** cambia bastante la evaluación fiscal;
- pero **no** compensa homogéneamente a todos;
- y su reparto parece territorialmente desigual.

`Grandes` captan la mayor parte del flujo compensatorio en montos absolutos (`68.2%` del peso proxy), pero también concentran la mayor pérdida agregada, así que su recuperación relativa es limitada. `Medianas` sale mejor parada en esta calibración. `Pequenas` mejora frente a `JH-F1`, pero sigue con una brecha fuerte.

Entonces, la propuesta de Julio Héctor es la única que intenta construir una **compensación municipal explícita**, pero esa compensación:

- depende de implementación institucional compleja;
- descansa en una geografía inmobiliaria formal muy desigual;
- y no garantiza reemplazo pleno del IUSI.

## 4. Efecto distributivo y social probable

La tercera conclusión es social. La propuesta sí protege con fuerza la vivienda habitual, pero lo hace con una focalización amplia.

`JH-S1` modela perfiles sintéticos bajo cuatro rutas:

- `IUSI actual`
- `JH tasa cero`
- `JH preferencial`
- `JH mejor opcion legal disponible`

Los resultados más visibles son estos:

- `Adulto mayor de bajos ingresos con vivienda unica`: `Q450 -> Q0`
- `Adulto mayor con vivienda principal de alto valor`: `Q3,240 -> Q0`
- `Adulto mayor con vivienda principal y otras propiedades`: `Q1,620 -> Q0`
- `Persona joven con primera vivienda`: `Q756 -> Q0`
- `Hogar formal de clase media con vivienda habitual`: `Q1,170 -> Q330`
- `Hogar informal con vivienda principal reconocida fiscalmente`: `Q576 -> Q132`
- `Arrendador formal que actualiza valor de inmueble no habitual`: `Q2,520 -> Q990`
- `Renta corta turistica registrada como residencial`: `Q1,440 -> Q516`

La lectura distributiva es doble.

Por un lado, la propuesta **sí** protege mejor que `6586` y `6709` a:

- vivienda habitual;
- primera vivienda;
- adultos mayores;
- y hogares reconocidos fiscalmente aunque no siempre tengan formalidad registral plena.

Pero, por otro lado, la focalización es bastante amplia:

- la tasa cero por edad puede llevar a `Q0` viviendas principales de alto valor;
- la vivienda principal puede quedar protegida incluso si el contribuyente tiene otras propiedades;
- y la puerta de `actualización al alza` no es solo social, porque también beneficia perfiles no habituales o patrimoniales.

Por eso la propuesta parece **más sofisticada socialmente** que `6586` y `6709`, pero no está exenta de beneficios amplios para perfiles no vulnerables.

## 5. Efecto de mercado probable

La cuarta conclusión es de mercado, y aquí la propuesta de Julio Héctor es bastante distinta a las otras.

`JH-M1` no modela el `IVA` como baja directa del costo privado de compra, porque el articulado no promete eso. En cambio, distingue dos canales privados reales:

- `tenencia`: alivio anual de IUSI;
- `venta`: exoneración de ISR sobre ganancia de capital.

### 5.1 Tenencia

La propuesta sí baja de forma fuerte el costo de retener vivienda habitual:

- un `adulto mayor con vivienda principal de alto valor` pasa de `Q3,240` a `Q0`;
- un `hogar formal de clase media con vivienda habitual` ahorra `Q840` al año;
- un `rentista con vivienda principal y alquileres` ahorra `Q1,500` al año en su vivienda principal;
- un `arrendador formal` con inmueble no habitual actualizado ahorra `Q1,530`.

### 5.2 Venta y movilidad

El efecto más novedoso no está en la compra, sino en la **salida**. Bajo el supuesto visible de una tasa actual de `10%` sobre ganancia de capital, la exoneración de `ISR` genera ahorros importantes en ventas ocasionales:

- `Adulto mayor con vivienda principal de alto valor`: ahorro potencial de `Q75,000`
- `Rentista con vivienda principal y alquileres`: `Q40,000`
- `Arrendador formal que actualiza valor de inmueble no habitual`: `Q35,000`
- `Renta corta turistica registrada como residencial`: `Q25,000`
- `Hogar formal de clase media con vivienda habitual`: `Q16,000`

Eso sugiere que la propuesta puede:

- facilitar movilidad residencial;
- abaratar la formalización de ventas;
- y aumentar la rotación patrimonial.

Pero también muestra una alerta fuerte: la exoneración de ISR **no queda encerrada en vivienda principal**. En la corrida de `JH-M1`, `6` de `8` perfiles capturan ese beneficio, incluidos activos no principales o de inversión ocasional.

Por tanto, el componente de mercado de la propuesta no es solo “pro vivienda”. También puede ser “pro liquidez patrimonial” para propietarios con activos valorizados.

## 6. Lectura conjunta

Tomadas juntas, las simulaciones `JH-F1`, `JH-F2`, `JH-F2b`, `JH-S1` y `JH-M1` permiten una lectura bastante más rica que en `6586` y `6709`.

La propuesta de Julio Héctor:

- **sí** protege con fuerza la vivienda habitual;
- **sí** ofrece alivio visible a primera vivienda y a mayores de `60 anos`;
- **sí** intenta compensar municipios por la vía del `IVA inmobiliario`;
- **sí** reduce el costo de ciertas ventas inmobiliarias vía `ISR`;

pero al mismo tiempo:

- **reduce** de forma relevante el `IUSI` directo;
- **no garantiza** una compensación territorial homogénea;
- **abre beneficios amplios** a algunos propietarios no vulnerables;
- y **combina alivio social con alivio patrimonial y de movilidad**, no solo con política habitacional estricta.

En ese sentido, esta propuesta parece más completa que `6586` y `6709`, pero también más compleja y más dependiente de buena implementación institucional.

## 7. Lo que esta nota permite afirmar

Con la evidencia disponible, esta nota permite sostener razonablemente que:

1. la propuesta de Julio Héctor es una reforma **más amplia** que las otras dos, porque combina `IUSI`, `IVA inmobiliario`, `ISR` e implementación institucional;
2. su bloque directo de `IUSI` es fiscalmente contractivo;
3. la compensación por `IVA inmobiliario` puede amortiguar parte de esa pérdida, pero de forma territorialmente desigual;
4. socialmente protege mejor la vivienda habitual que `6586` y `6709`, aunque con beneficios amplios por edad, habitualidad o actualización;
5. su efecto de mercado más novedoso no está en la compra, sino en la `venta`, porque abarata ciertas ganancias de capital y puede facilitar movilidad y rotación patrimonial.

## 8. Lo que todavia no demuestra

Esta nota no demuestra todavía:

- el monto municipal observado del `IVA inmobiliario`, porque no existe una base territorial cerrada y la compensación sigue siendo proxy;
- la cantidad real de contribuyentes que calificaría a cada beneficio;
- la respuesta administrativa efectiva de SAT, MINFIN, DICABI y municipalidades;
- ni el efecto observado ex post sobre ventas, movilidad, construcción o formalización.

Por eso conviene leer estos resultados como una base sólida para discusión técnico-política, no como una predicción cerrada.

## 9. Cierre

La lectura más robusta de la propuesta de Julio Héctor es que intenta construir una **reforma inmobiliario-tributaria de equilibrio**:

- baja carga sobre vivienda habitual;
- no elimina del todo la progresividad del IUSI;
- intenta compensar municipios vía IVA;
- y reduce el costo tributario de ciertas ventas ocasionales.

Eso la vuelve más sofisticada que `6586` y `6709`, pero también más ambigua. Puede leerse al mismo tiempo como:

- una propuesta de alivio social;
- una propuesta de reorganización fiscal municipal;
- y una propuesta de mayor liquidez y movilidad patrimonial.

Su gran fortaleza es que intenta articular esos tres planos a la vez. Su gran riesgo es que, si la implementación falla o si la compensación vía IVA no se territorializa bien, el resultado puede terminar siendo una caída del IUSI directo con beneficios amplios y compensación incompleta.
