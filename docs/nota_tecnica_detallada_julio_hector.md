# Nota técnica detallada: evaluación integral y opciones de recalibración de la propuesta de Julio Héctor

## Proposito

Esta nota integra dos planos de análisis sobre la propuesta de Julio Héctor:

1. sus **efectos probables** sobre finanzas municipales, distribución social y mercado inmobiliario;
2. los **elementos que conviene conservar** y los que conviene **recalibrar** a la luz de nuestras simulaciones.

El objetivo no es evaluar la propuesta solo en términos binarios de aprobación o rechazo. El objetivo es identificar:

- qué instrumentos son técnicamente valiosos;
- qué riesgos aparecen cuando esos instrumentos se modelan;
- y cómo podría rediseñarse la propuesta para acercarla a un mejor equilibrio entre objetivo social, objetivo fiscal y objetivo de mercado.

La nota se apoya principalmente en:

- [lectura_tecnico_legal_julio_hector_vs_modelos.md](C:/IUSI/docs/lectura_tecnico_legal_julio_hector_vs_modelos.md)
- [tabla_comparativa_6586_6709_julio_hector.md](C:/IUSI/docs/tabla_comparativa_6586_6709_julio_hector.md)
- [nota_efectos_propuesta_julio_hector.md](C:/IUSI/docs/nota_efectos_propuesta_julio_hector.md)
- [nota_elementos_rescatables_julio_hector.md](C:/IUSI/docs/nota_elementos_rescatables_julio_hector.md)
- [jh_f1_bloque_iusi.md](C:/IUSI/docs/jh_f1_bloque_iusi.md)
- [jh_f2b_compensacion_iva_matriz_proxy.md](C:/IUSI/docs/jh_f2b_compensacion_iva_matriz_proxy.md)
- [jh_s1_impacto_social_perfiles.md](C:/IUSI/docs/jh_s1_impacto_social_perfiles.md)
- [jh_m1_mercado_inmobiliario.md](C:/IUSI/docs/jh_m1_mercado_inmobiliario.md)
- [nota_tecnica_matriz_proxy_iva_inmobiliario.md](C:/IUSI/docs/nota_tecnica_matriz_proxy_iva_inmobiliario.md)

## 1. Cómo debe leerse la propuesta

La propuesta de Julio Héctor no debe leerse como una simple reforma del `IUSI`. Es una propuesta más amplia, que combina cuatro bloques:

- `IUSI`: tasa cero, régimen preferencial, actualización al alza del valor fiscal, control del uso del inmueble;
- `IVA inmobiliario`: destino municipal de la recaudación efectivamente percibida en primera venta y transferencias;
- `ISR`: exoneración de ganancia de capital en ciertas ventas ocasionales;
- `implementación`: interoperabilidad, registro nacional de beneficios, trazabilidad y autoavalúo simplificado.

Ese carácter ampliado es su principal fortaleza y también su principal fuente de complejidad. Frente a `6586` y `6709`, la propuesta intenta responder no solo a la carga del IUSI, sino también a:

- la sostenibilidad municipal;
- la debilidad de registros;
- la necesidad de actualizar valores;
- y la tributación de ciertas ventas inmobiliarias.

## 2. Qué muestran las simulaciones sobre sus efectos

## 2.1 Efecto fiscal directo del bloque IUSI

La primera conclusión fuerte es que, si se aísla solo el bloque `IUSI`, la propuesta sigue siendo contractiva.

`JH-F1` mostró que, en su escenario `central`, la caída del `IUSI per capita` sería de:

- `Grandes`: `Q221.24 -> Q158.63` (`-28.3%`)
- `Medianas`: `Q44.37 -> Q28.08` (`-36.7%`)
- `Pequenas`: `Q7.26 -> Q4.15` (`-42.8%`)

Esto significa que la propuesta no puede defenderse diciendo que el incentivo de actualización compensa por sí solo el alivio tributario. El bloque directo de IUSI sigue reduciendo ingreso propio municipal de forma importante.

## 2.2 Efecto de compensación por IVA inmobiliario

La segunda pregunta es si el bloque de `IVA inmobiliario` corrige esa pérdida.

La primera versión `JH-F2` sugería compensaciones por grupo municipal con supuestos analíticos relativamente gruesos. Por eso se construyó `JH-F2b`, que distribuye la compensación según una matriz proxy municipal de intensidad inmobiliaria formal basada en:

- `IUSI municipal 2025`;
- `ADIG / RIIM`;
- `FUNDESA / ICL`.

En el escenario `central` de `JH-F2b`, el saldo neto queda así:

- `Grandes`: `-25.2%`
- `Medianas`: `-9.8%`
- `Pequenas`: `-25.1%`

Esto es importante por tres razones:

1. la compensación sí cambia la lectura fiscal de la propuesta;
2. pero no la vuelve fiscalmente neutra;
3. y su reparto es territorialmente desigual, porque depende de la geografía del mercado inmobiliario formal.

## 2.3 Efecto social y distributivo

`JH-S1` muestra que la propuesta sí protege con mucha fuerza la vivienda habitual, pero con focalización amplia.

Resultados ilustrativos:

- `Adulto mayor de bajos ingresos con vivienda unica`: `Q450 -> Q0`
- `Adulto mayor con vivienda principal de alto valor`: `Q3,240 -> Q0`
- `Adulto mayor con vivienda principal y otras propiedades`: `Q1,620 -> Q0`
- `Persona joven con primera vivienda`: `Q756 -> Q0`
- `Hogar formal de clase media con vivienda habitual`: `Q1,170 -> Q330`
- `Hogar informal con vivienda principal reconocida fiscalmente`: `Q576 -> Q132`
- `Arrendador formal que actualiza valor de inmueble no habitual`: `Q2,520 -> Q990`

La propuesta sí protege mejor que las otras dos:

- vivienda habitual;
- primera vivienda;
- adultos mayores;
- y contribuyentes reconocidos fiscalmente aunque no siempre registralmente.

Pero también abre beneficios a perfiles no vulnerables:

- vivienda principal de alto valor;
- vivienda principal aun cuando existan otras propiedades;
- e inmuebles no habituales que entran por la puerta de actualización.

## 2.4 Efecto de mercado

`JH-M1` sugiere que el efecto de mercado de la propuesta no debe leerse como una simple baja de costo de compra.

El `IVA inmobiliario` no se modeló como rebaja directa para comprador o vendedor, porque el texto legal no cambia la tasa privada, sino su destino municipal. En cambio, el módulo de mercado distingue dos canales privados:

- `tenencia`: alivio anual en IUSI;
- `venta`: alivio en ISR sobre ganancia de capital.

Resultados ilustrativos:

- `Adulto mayor con vivienda principal de alto valor`: ahorro anual de `Q3,240` y ahorro potencial en venta de `Q75,000`
- `Rentista con vivienda principal y alquileres`: ahorro anual de `Q1,500` y ahorro potencial en venta de `Q40,000`
- `Arrendador formal` con inmueble no habitual: ahorro anual de `Q1,530` y ahorro potencial en venta de `Q35,000`

La propuesta puede facilitar:

- movilidad residencial;
- formalización de ventas;
- y rotación patrimonial.

Pero también puede abrir beneficios de liquidez patrimonial a propietarios no vulnerables, porque la exoneración de ISR no queda encerrada en vivienda principal.

## 3. Qué instrumentos de la propuesta conviene conservar

## 3.1 Definiciones de uso y vivienda habitual

Conviene conservar plenamente el bloque que distingue entre:

- inmueble residencial;
- no residencial;
- mixto;
- residencia habitual;
- vivienda habitual.

Esto mejora la calidad del impuesto y también la legitimidad pública de la reforma, porque evita tratar igual:

- primera vivienda;
- renta corta turística;
- arrendamiento habitacional;
- uso comercial;
- y activos patrimoniales no principales.

## 3.2 Protección visible a la vivienda habitual

También conviene conservar el principio de que la vivienda habitual merece protección especial. Tanto las simulaciones como la lectura sociológica apuntan a que la vivienda principal es el centro de sensibilidad política del debate.

## 3.3 Régimen preferencial ligado a actualización del valor fiscal

Este es uno de los componentes más valiosos de la propuesta. Ayuda a alinear:

- alivio tributario;
- actualización voluntaria de base;
- mejora catastral;
- y mayor aceptación política del reavalúo.

## 3.4 Compensación municipal vía IVA inmobiliario

Conviene conservarla como idea, porque introduce una responsabilidad institucional ausente en `6586` y `6709`: si se reorganiza o reduce el IUSI, hay que discutir cómo se sostiene el ingreso municipal.

## 3.5 Interoperabilidad, registro nacional de beneficios y trazabilidad

Esto conviene mantenerlo. Sin registro, interoperabilidad y trazabilidad, cualquier beneficio bien diseñado queda expuesto a duplicidades, arbitraje y opacidad.

## 3.6 Autoavalúo simplificado transitorio

También conviene conservarlo como herramienta de transición y actualización de base, especialmente para municipios con menor capacidad técnica.

## 4. Qué instrumentos conviene recalibrar

## 4.1 Tasa cero para mayores de 60 años

El problema de esta pieza no es el espíritu, sino su amplitud.

`JH-S1` mostró que puede llevar a `Q0`:

- vivienda principal de alto valor;
- y adultos mayores con otras propiedades.

Sería mejor rediseñarla con alguno de estos criterios:

- vivienda principal única;
- umbral de valor;
- o capacidad de pago.

## 4.2 Tasa cero para primera vivienda por 7 años

La idea es razonable, pero el plazo parece largo. Un rediseño más sostenible podría ser:

- `3 a 5 anos`;
- o un alivio decreciente en el tiempo;
- o un beneficio focalizado por valor de vivienda.

## 4.3 Régimen preferencial por actualización

Conviene mantenerlo, pero con mejores candados.

Hoy puede abrir alivio a:

- inmuebles no habituales;
- activos de renta;
- y perfiles que actualizan valor con lógica patrimonial.

Sería mejor introducir:

- umbral mínimo claro de actualización;
- exclusión más explícita de renta corta turística;
- y diferenciación más fina entre vivienda habitual y activos lucrativos.

## 4.4 Exoneración de ISR sobre ganancia de capital

Este es el punto más delicado de mercado.

La idea de reducir fricción tributaria en ciertas ventas puede ser útil, pero `JH-M1` muestra que su alcance es demasiado amplio si no se calibra mejor. Sería razonable considerar:

- limitarla a vivienda principal;
- permitirla solo una vez cada cierto número de años;
- establecer un techo de ganancia exenta;
- o diferenciar entre movilidad residencial y rotación patrimonial.

## 4.5 Narrativa de compensación plena por IVA

El `IVA inmobiliario` conviene mantenerlo como pieza de compensación, pero no como promesa de neutralidad fiscal automática. `JH-F2b` muestra que su efecto es:

- parcial;
- territorialmente desigual;
- y dependiente de implementación.

## 5. Qué rediseño sugieren nuestros modelos

Tomando `JH-F1`, `JH-F2b`, `JH-S1` y `JH-M1` en conjunto, la versión mejor calibrada de esta propuesta tendría cinco rasgos:

1. protección fuerte a vivienda principal, pero no universal;
2. mayor peso del régimen preferencial y menor peso de la tasa cero amplia;
3. conservación del incentivo a actualizar valor;
4. compensación municipal vía IVA como mecanismo complementario y no como sustituto pleno;
5. restricción mejor definida del bloque ISR para evitar alivios patrimoniales demasiado amplios.

En términos simples: conviene moverse desde una propuesta de beneficios muy abiertos hacia una propuesta de **beneficios condicionados, trazables y mejor focalizados**.

## 6. Lectura final

La propuesta de Julio Héctor contiene mejores instrumentos que `6586` y `6709`, pero hoy mezcla:

- una arquitectura inteligente;
- beneficios socialmente defendibles;
- y algunos alivios demasiado amplios.

Su gran virtud es que reconoce al mismo tiempo:

- la necesidad de proteger vivienda habitual;
- la necesidad de sostener finanzas municipales;
- y la necesidad de actualizar base, registros y trazabilidad.

Su principal debilidad es que, una vez modelada, algunos de sus beneficios parecen demasiado generosos o demasiado abiertos frente al objetivo declarado.

Por eso, la mejor conclusión técnica no es desecharla, sino **rescatar sus mejores instrumentos y recalibrar sus componentes más expansivos**. Esa ruta probablemente produciría una propuesta más sólida que las otras dos y más cercana a un verdadero equilibrio entre política social, sostenibilidad fiscal y ordenamiento del mercado.
