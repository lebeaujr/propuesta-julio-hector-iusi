from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_F1 = ROOT / "outputs" / "jh_f1_iusi_direct_scenarios.csv"
INPUT_F2B = ROOT / "outputs" / "jh_f2b_iva_compensation_proxy_scenarios.csv"
INPUT_F2B_AGG = ROOT / "outputs" / "jh_f2b_iva_compensation_proxy_group_aggregation.csv"
INPUT_S1 = ROOT / "outputs" / "jh_s1_social_profiles.csv"
INPUT_M1 = ROOT / "outputs" / "jh_m1_market_incentives.csv"
OUTPUT_HTML = ROOT / "dashboard" / "julio_hector_dashboard.html"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def to_float(value: str) -> float:
    return float(value.strip())


def fmt_q(value: float) -> str:
    return f"Q{value:,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%"


def build_payload() -> dict[str, object]:
    f1_rows = read_csv(INPUT_F1)
    f2b_rows = read_csv(INPUT_F2B)
    agg_rows = read_csv(INPUT_F2B_AGG)
    s1_rows = read_csv(INPUT_S1)
    m1_rows = read_csv(INPUT_M1)

    f1_central = [row for row in f1_rows if row["scenario_code"] == "jh_f1_central"]
    f2b_central = [row for row in f2b_rows if row["scenario_code"] == "jh_f2b_central"]
    agg_central = [row for row in agg_rows if row["scenario_code"] == "central"]

    social_zero = [row for row in s1_rows if abs(to_float(row["jh_final_q_anual"])) < 1e-9]
    social_preferential = [
        row for row in s1_rows
        if row["best_route"] != "Actual" and abs(to_float(row["jh_final_q_anual"])) > 1e-9
    ]

    market_isr = [row for row in m1_rows if row["qualifies_isr_exemption"].strip().upper() == "TRUE"]
    market_top_sale = max(m1_rows, key=lambda row: to_float(row["sale_tax_savings_q"]))

    summary = {
        "direct_groups": [
            {
                "group": row["grupo_municipal"],
                "base": to_float(row["iusi_per_capita_base_q"]),
                "simulated": to_float(row["iusi_per_capita_simulado_q"]),
                "delta_pct": to_float(row["delta_per_capita_pct"]),
            }
            for row in f1_central
        ],
        "comp_groups": [
            {
                "group": row["grupo_municipal"],
                "direct": to_float(row["iusi_per_capita_direct_q"]),
                "net": to_float(row["iusi_per_capita_compensado_q"]),
                "net_pct": to_float(row["saldo_neto_pct"]),
                "proxy_share": to_float(row["proxy_weight_share_pct"]),
                "loss_covered": to_float(row["share_compensacion_sobre_perdida_pct"]),
            }
            for row in f2b_central
        ],
        "agg_groups": [
            {
                "group": row["grupo_municipal"],
                "municipios": int(float(row["municipios"])),
                "iusi": to_float(row["iusi_percibido_q"]),
                "loss": to_float(row["direct_loss_q"]),
                "comp": to_float(row["compensation_q"]),
                "proxy_share": to_float(row["proxy_weight_share_pct"]),
            }
            for row in agg_central
        ],
        "social_zero_count": len(social_zero),
        "social_pref_count": len(social_preferential),
        "social_rows": [
            {
                "perfil": row["perfil"],
                "actual": to_float(row["iusi_actual_q_anual"]),
                "final": to_float(row["jh_final_q_anual"]),
                "route": row["best_route"],
                "delta_pct": to_float(row["delta_final_vs_actual_pct"]),
            }
            for row in s1_rows
        ],
        "market_isr_count": len(market_isr),
        "market_rows": [
            {
                "perfil": row["perfil"],
                "holding": to_float(row["holding_savings_q_anual"]),
                "sale": to_float(row["sale_tax_savings_q"]),
                "signal": row["market_signal"],
            }
            for row in m1_rows
        ],
        "market_top_sale": {
            "perfil": market_top_sale["perfil"],
            "sale": to_float(market_top_sale["sale_tax_savings_q"]),
        },
    }
    return summary


def build_html(data: dict[str, object]) -> str:
    data_json = json.dumps(data, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dashboard Julio Héctor - IUSI, IVA e ISR</title>
  <style>
    :root {{
      --bg: #f4f0e8;
      --paper: #fffdfa;
      --ink: #1d2628;
      --muted: #5f686d;
      --accent: #6d3d8f;
      --accent-2: #2f7a78;
      --accent-3: #c67b33;
      --alert: #a83b38;
      --soft-violet: #ebe1f4;
      --soft-teal: #dff1ed;
      --soft-amber: #f6e6d0;
      --soft-rose: #f3ddd7;
      --line: #d6cec2;
      --shadow: 0 18px 44px rgba(72, 66, 56, 0.09);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Palatino Linotype", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(109, 61, 143, 0.12), transparent 28%),
        radial-gradient(circle at top right, rgba(47, 122, 120, 0.10), transparent 26%),
        linear-gradient(180deg, #faf7f1 0%, var(--bg) 100%);
    }}
    .wrap {{ max-width: 1280px; margin: 0 auto; padding: 28px; }}
    .hero {{
      background: linear-gradient(135deg, rgba(73, 43, 97, 0.97), rgba(109, 61, 143, 0.95));
      color: #fffaf6;
      border-radius: 28px;
      padding: 34px 36px;
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      right: -34px;
      top: -34px;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: rgba(255,255,255,0.08);
    }}
    .eyebrow {{
      font-family: "Trebuchet MS", sans-serif;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 12px;
      opacity: 0.84;
      margin-bottom: 12px;
    }}
    h1,h2,h3 {{ margin: 0; }}
    h1 {{
      font-size: clamp(30px, 5vw, 50px);
      line-height: 1.02;
      max-width: 940px;
    }}
    .hero p {{
      max-width: 980px;
      margin: 18px 0 0;
      line-height: 1.58;
      font-size: 18px;
      color: rgba(248, 245, 251, 0.93);
    }}
    .grid {{ display: grid; gap: 20px; margin-top: 22px; }}
    .cards-4 {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
    .cards-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .cards-2 {{ grid-template-columns: 1.2fr 0.8fr; }}
    .panel {{
      background: var(--paper);
      border: 1px solid rgba(91, 83, 69, 0.12);
      border-radius: 22px;
      padding: 24px;
      box-shadow: var(--shadow);
    }}
    .metric {{
      background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(248,245,239,0.98));
    }}
    .metric-label {{
      color: var(--muted);
      font-size: 13px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      font-family: "Trebuchet MS", sans-serif;
    }}
    .metric-value {{
      margin-top: 10px;
      font-size: 38px;
      line-height: 1;
      color: var(--accent);
    }}
    .metric-note {{
      margin-top: 10px;
      font-size: 15px;
      line-height: 1.45;
      color: var(--muted);
    }}
    .section-title {{ font-size: 28px; margin-bottom: 8px; }}
    .section-lead {{
      color: var(--muted);
      font-size: 16px;
      line-height: 1.55;
      margin-bottom: 20px;
    }}
    .pill-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 16px; }}
    .pill {{
      padding: 10px 14px;
      border-radius: 999px;
      font-family: "Trebuchet MS", sans-serif;
      font-size: 13px;
      background: #efe7f6;
      color: #5a3377;
      border: 1px solid rgba(109, 61, 143, 0.18);
    }}
    .bars {{ display: grid; gap: 16px; }}
    .bar-row {{
      display: grid;
      grid-template-columns: 145px 1fr 110px;
      gap: 14px;
      align-items: center;
    }}
    .bar-label {{
      font-family: "Trebuchet MS", sans-serif;
      font-size: 15px;
    }}
    .bar-track {{
      width: 100%;
      height: 18px;
      border-radius: 999px;
      background: #ebe5d9;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent-2), var(--accent));
    }}
    .bar-fill.alt {{ background: linear-gradient(90deg, #efb66b, var(--accent-3)); }}
    .bar-fill.alert {{ background: linear-gradient(90deg, #d98973, var(--alert)); }}
    .bar-value {{
      text-align: right;
      font-family: "Trebuchet MS", sans-serif;
      font-weight: 700;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
      line-height: 1.45;
    }}
    th, td {{
      padding: 12px 10px;
      border-bottom: 1px solid rgba(99, 87, 74, 0.12);
      vertical-align: top;
    }}
    th {{
      text-align: left;
      color: var(--muted);
      font-family: "Trebuchet MS", sans-serif;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .note-box {{
      background: linear-gradient(180deg, #fffaf0, #fff);
      border: 1px solid rgba(205, 152, 68, 0.20);
      border-radius: 18px;
      padding: 18px;
      color: #5d4731;
      line-height: 1.55;
    }}
    .warning-box {{
      background: linear-gradient(180deg, #fbefec, #fff);
      border: 1px solid rgba(168, 59, 56, 0.18);
      border-radius: 18px;
      padding: 18px;
      color: #5b3938;
      line-height: 1.55;
    }}
    .soft-grid {{
      display: grid;
      gap: 14px;
    }}
    .soft-card {{
      border-radius: 18px;
      padding: 18px;
      border: 1px solid rgba(90, 80, 66, 0.10);
    }}
    .violet {{ background: var(--soft-violet); }}
    .teal {{ background: var(--soft-teal); }}
    .amber {{ background: var(--soft-amber); }}
    .rose {{ background: var(--soft-rose); }}
    .soft-card h3 {{ margin-bottom: 8px; font-size: 20px; }}
    .soft-card p {{ margin: 0; line-height: 1.55; }}
    @media (max-width: 1040px) {{
      .cards-4, .cards-3, .cards-2 {{ grid-template-columns: 1fr; }}
      .bar-row {{ grid-template-columns: 1fr; }}
      .bar-value {{ text-align: left; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <div class="eyebrow">Dashboard exclusivo</div>
      <h1>Propuesta de Julio Héctor: IUSI, IVA inmobiliario e ISR</h1>
      <p>
        Este tablero resume la lectura técnico-legal y los resultados de simulación de una propuesta más amplia que <strong>6586</strong> y <strong>6709</strong>.
        No solo reorganiza el IUSI: también intenta compensar a municipalidades vía IVA inmobiliario y abaratar ciertas ventas vía ISR.
      </p>
      <div class="pill-row">
        <div class="pill">Bloque IUSI</div>
        <div class="pill">Compensación por IVA</div>
        <div class="pill">Protección a vivienda habitual</div>
        <div class="pill">Exoneración de ISR en ventas ocasionales</div>
      </div>
    </section>

    <section class="grid cards-4">
      <article class="panel metric">
        <div class="metric-label">IUSI directo</div>
        <div class="metric-value">-28.3%</div>
        <div class="metric-note">Caída central en municipios <strong>Grandes</strong> antes de compensación por IVA.</div>
      </article>
      <article class="panel metric">
        <div class="metric-label">Mejor saldo neto</div>
        <div class="metric-value">-9.8%</div>
        <div class="metric-note">Resultado central de <strong>Medianas</strong> después de <strong>JH-F2b</strong>.</div>
      </article>
      <article class="panel metric">
        <div class="metric-label">Perfiles en Q0</div>
        <div class="metric-value">4 / 10</div>
        <div class="metric-note">Perfiles sociales que llegan a <strong>tasa cero</strong> bajo la mejor ruta legal.</div>
      </article>
      <article class="panel metric">
        <div class="metric-label">ISR en venta</div>
        <div class="metric-value">6 / 8</div>
        <div class="metric-note">Perfiles de mercado que capturan exoneración en ventas ocasionales.</div>
      </article>
    </section>

    <section class="grid cards-2">
      <article class="panel">
        <h2 class="section-title">Qué propone realmente</h2>
        <p class="section-lead">
          La propuesta de Julio Héctor es una reforma inmobiliario-tributaria ampliada. Combina protección a vivienda habitual con actualización de valor,
          compensación municipal por IVA y alivio de ISR en ciertas ventas.
        </p>
        <div class="soft-grid">
          <div class="soft-card violet">
            <h3>IUSI</h3>
            <p>Tasa cero para <strong>60+</strong> y <strong>primera vivienda</strong>, más régimen preferencial para vivienda habitual y actualización al alza del valor fiscal.</p>
          </div>
          <div class="soft-card teal">
            <h3>IVA inmobiliario</h3>
            <p>Los <strong>7 puntos porcentuales</strong> del IVA efectivamente percibido en operaciones inmobiliarias se destinan a la municipalidad donde se ubica el bien.</p>
          </div>
          <div class="soft-card amber">
            <h3>ISR</h3>
            <p>Exoneración de ganancia de capital en ventas ocasionales de personas individuales no habituales con al menos <strong>3 años</strong> de tenencia.</p>
          </div>
          <div class="soft-card rose">
            <h3>Implementación</h3>
            <p>Interoperabilidad, registro nacional de beneficios, avisos notariales, trazabilidad territorial y autoavalúo simplificado transitorio.</p>
          </div>
        </div>
      </article>

      <article class="panel">
        <h2 class="section-title">Lectura rápida</h2>
        <p class="section-lead">
          El corazón de la propuesta es más sofisticado que el de 6586 y 6709, pero también más complejo y más dependiente de buena implementación.
        </p>
        <div class="note-box">
          <strong>Lo más valioso:</strong> distingue vivienda habitual, premia actualización de valor y reconoce la necesidad de compensar a municipalidades.
        </div>
        <div style="height:12px"></div>
        <div class="warning-box">
          <strong>La principal alerta:</strong> varios beneficios se vuelven demasiado amplios en la simulación, especialmente la tasa cero por edad y la exoneración de ISR en ventas ocasionales.
        </div>
      </article>
    </section>

    <section class="grid cards-2">
      <article class="panel">
        <h2 class="section-title">Efecto fiscal directo del IUSI</h2>
        <p class="section-lead">
          <strong>JH-F1</strong> aísla solo el bloque IUSI. Incluso con el incentivo de actualización de valor, el resultado directo sigue siendo contractivo.
        </p>
        <div id="f1-bars" class="bars"></div>
      </article>

      <article class="panel">
        <h2 class="section-title">Compensación por IVA inmobiliario</h2>
        <p class="section-lead">
          <strong>JH-F2b</strong> reparte un pool nacional prudente según la geografía del mercado inmobiliario formal. La compensación ayuda, pero no igual para todos.
        </p>
        <div id="f2b-bars" class="bars"></div>
      </article>
    </section>

    <section class="grid cards-2">
      <article class="panel">
        <h2 class="section-title">Agregación territorial del IVA proxy</h2>
        <p class="section-lead">
          La matriz proxy no observa IVA municipal real; aproxima intensidad inmobiliaria formal territorial usando <strong>IUSI 2025</strong>, <strong>ADIG / RIIM</strong> y <strong>FUNDESA / ICL</strong>.
        </p>
        <table id="agg-table">
          <thead>
            <tr>
              <th>Grupo</th>
              <th>Municipios</th>
              <th>IUSI percibido</th>
              <th>Pérdida directa</th>
              <th>Compensación central</th>
              <th>Peso proxy IVA</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </article>

      <article class="panel">
        <h2 class="section-title">Qué significa fiscalmente</h2>
        <p class="section-lead">
          La compensación por IVA no debe leerse como reemplazo automático del IUSI.
        </p>
        <div class="note-box">
          <strong>Grandes</strong> concentran la mayor parte del flujo compensatorio en montos absolutos, pero también concentran la mayor pérdida directa.
        </div>
        <div style="height:12px"></div>
        <div class="note-box">
          <strong>Medianas</strong> salen relativamente mejor paradas en la calibración central porque combinan pérdida menor con peso proxy todavía relevante.
        </div>
        <div style="height:12px"></div>
        <div class="warning-box">
          <strong>Pequeñas</strong> mejoran respecto al bloque IUSI puro, pero siguen con brecha fuerte. La propuesta no corrige por sí sola la desigualdad territorial de la base inmobiliaria formal.
        </div>
      </article>
    </section>

    <section class="grid cards-2">
      <article class="panel">
        <h2 class="section-title">Impacto social por perfiles</h2>
        <p class="section-lead">
          <strong>JH-S1</strong> muestra que la propuesta sí protege mejor la vivienda habitual que 6586 y 6709, pero la focalización es amplia.
        </p>
        <table id="social-table">
          <thead>
            <tr>
              <th>Perfil</th>
              <th>Actual</th>
              <th>Final JH</th>
              <th>Ruta final</th>
              <th>Delta</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </article>

      <article class="panel">
        <h2 class="section-title">Lectura social</h2>
        <p class="section-lead">
          La propuesta es claramente más protectora con vivienda habitual, pero no focaliza solo en vulnerabilidad.
        </p>
        <div class="soft-grid">
          <div class="soft-card teal">
            <h3>Lo mejor</h3>
            <p>Protege vivienda habitual, primera vivienda y contribuyentes reconocidos fiscalmente aunque no siempre tengan formalidad registral plena.</p>
          </div>
          <div class="soft-card amber">
            <h3>La zona gris</h3>
            <p>La tasa cero por edad puede llevar a <strong>Q0</strong> viviendas principales de alto valor y también viviendas principales de personas con otras propiedades.</p>
          </div>
          <div class="soft-card rose">
            <h3>La puerta patrimonial</h3>
            <p>El régimen preferencial por actualización permite alivio también en inmuebles no habituales o de inversión si el valor se actualiza al alza.</p>
          </div>
        </div>
      </article>
    </section>

    <section class="grid cards-2">
      <article class="panel">
        <h2 class="section-title">Mercado inmobiliario</h2>
        <p class="section-lead">
          <strong>JH-M1</strong> no modela el IVA como rebaja privada de compra. Los dos canales privados reales son <strong>tenencia</strong> y <strong>venta</strong>.
        </p>
        <table id="market-table">
          <thead>
            <tr>
              <th>Perfil</th>
              <th>Ahorro anual IUSI</th>
              <th>Ahorro potencial ISR</th>
              <th>Lectura</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </article>

      <article class="panel">
        <h2 class="section-title">Lectura de mercado</h2>
        <p class="section-lead">
          La propuesta no parece abaratar directamente la compra. Su efecto más novedoso está en la <strong>movilidad de salida</strong> vía ISR.
        </p>
        <div class="note-box">
          <strong>Mayor alivio en venta:</strong> <span id="top-sale"></span>
        </div>
        <div style="height:12px"></div>
        <div class="warning-box">
          <strong>Alerta:</strong> la exoneración de ISR no queda encerrada en vivienda principal; también beneficia ventas ocasionales de activos no principales o de inversión si no cae en habitualidad.
        </div>
      </article>
    </section>

    <section class="grid cards-2">
      <article class="panel">
        <h2 class="section-title">Qué rescatar</h2>
        <p class="section-lead">
          A diferencia de las otras dos iniciativas, aquí sí hay instrumentos técnicos valiosos que conviene conservar.
        </p>
        <div class="soft-grid">
          <div class="soft-card violet"><h3>Definiciones de uso</h3><p>Ayudan a separar vivienda principal, renta corta, alquiler habitacional, uso comercial y uso mixto.</p></div>
          <div class="soft-card teal"><h3>Régimen preferencial</h3><p>Es la pieza más equilibrada: reduce la carga, mantiene algo de contribución y premia actualización de valor.</p></div>
          <div class="soft-card amber"><h3>Compensación por IVA</h3><p>Es la única propuesta que reconoce explícitamente el problema de sostenibilidad municipal.</p></div>
          <div class="soft-card rose"><h3>Registro e interoperabilidad</h3><p>Responde bien al problema de duplicidades, captura y opacidad en los beneficios.</p></div>
        </div>
      </article>

      <article class="panel">
        <h2 class="section-title">Qué recalibrar</h2>
        <p class="section-lead">
          Nuestros modelos sugieren que varias piezas son defendibles solo si se acotan mejor.
        </p>
        <div class="warning-box">
          <strong>Tasa cero por edad:</strong> hoy es demasiado amplia y debería ligarse mejor a vivienda principal única, valor o capacidad de pago.
        </div>
        <div style="height:12px"></div>
        <div class="warning-box">
          <strong>Primera vivienda por 7 años:</strong> convendría acortarla o volverla decreciente.
        </div>
        <div style="height:12px"></div>
        <div class="warning-box">
          <strong>Exoneración de ISR:</strong> convendría restringirla mejor a movilidad residencial o a techos claros de ganancia exenta.
        </div>
      </article>
    </section>

    <section class="grid">
      <article class="panel">
        <h2 class="section-title">Cuadro metodológico</h2>
        <p class="section-lead">
          Este dashboard es autocontenido, pero sus resultados mezclan datos observados, matriz proxy y perfiles sintéticos. Conviene leerlo como una herramienta de discusión técnica, no como liquidación oficial municipio por municipio.
        </p>
        <table>
          <thead>
            <tr>
              <th>Bloque</th>
              <th>Fuente principal</th>
              <th>Tipo de cálculo</th>
              <th>Alcance</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>IUSI directo</td>
              <td><code>jh_f1_iusi_direct_scenarios.csv</code></td>
              <td>Simulación por grupos municipales</td>
              <td>Mide el efecto del bloque IUSI antes de compensación.</td>
            </tr>
            <tr>
              <td>Compensación por IVA</td>
              <td><code>jh_f2b_iva_compensation_proxy_scenarios.csv</code></td>
              <td>Pool nacional prudente distribuido por matriz proxy</td>
              <td>No observa IVA territorial real; aproxima intensidad inmobiliaria formal municipal.</td>
            </tr>
            <tr>
              <td>Impacto social</td>
              <td><code>jh_s1_social_profiles.csv</code></td>
              <td>Perfiles sintéticos</td>
              <td>Traduce el articulado a tipos de contribuyente y rutas legales de beneficio.</td>
            </tr>
            <tr>
              <td>Mercado</td>
              <td><code>jh_m1_market_incentives.csv</code></td>
              <td>Perfiles patrimoniales y ventas ocasionales</td>
              <td>Distingue alivio de tenencia y alivio de venta vía ISR.</td>
            </tr>
          </tbody>
        </table>
        <div style="height:16px"></div>
        <div class="note-box">
          <strong>Cómo leerlo bien:</strong> el tablero no dice “qué va a pasar exactamente” en cada municipio o contribuyente. Dice <strong>qué direcciones y tensiones aparecen</strong> si se toma el texto legal en serio y se lo pasa por datos observados, una matriz territorial proxy y perfiles razonables.
        </div>
      </article>
    </section>
  </div>
  <script>
    const DATA = {data_json};

    function q(value) {{
      return new Intl.NumberFormat('es-GT', {{ style: 'currency', currency: 'GTQ', maximumFractionDigits: 0 }}).format(value);
    }}
    function pct(value) {{
      return `${{value.toFixed(1)}}%`;
    }}

    function renderBars() {{
      const f1Host = document.getElementById('f1-bars');
      DATA.direct_groups.forEach((row) => {{
        const width = Math.min(Math.abs(row.delta_pct), 100);
        f1Host.insertAdjacentHTML('beforeend', `
          <div class="bar-row">
            <div class="bar-label">${{row.group}}</div>
            <div class="bar-track"><div class="bar-fill alert" style="width:${{width}}%"></div></div>
            <div class="bar-value">${{pct(row.delta_pct)}}</div>
          </div>
        `);
      }});

      const f2Host = document.getElementById('f2b-bars');
      DATA.comp_groups.forEach((row) => {{
        const width = Math.min(Math.abs(row.net_pct), 100);
        f2Host.insertAdjacentHTML('beforeend', `
          <div class="bar-row">
            <div class="bar-label">${{row.group}}</div>
            <div class="bar-track"><div class="bar-fill alt" style="width:${{width}}%"></div></div>
            <div class="bar-value">${{pct(row.net_pct)}}</div>
          </div>
        `);
      }});
    }}

    function renderTables() {{
      const aggBody = document.querySelector('#agg-table tbody');
      DATA.agg_groups.forEach((row) => {{
        aggBody.insertAdjacentHTML('beforeend', `
          <tr>
            <td><strong>${{row.group}}</strong></td>
            <td>${{row.municipios}}</td>
            <td>${{q(row.iusi)}}</td>
            <td>${{q(row.loss)}}</td>
            <td>${{q(row.comp)}}</td>
            <td>${{pct(row.proxy_share)}}</td>
          </tr>
        `);
      }});

      const socialBody = document.querySelector('#social-table tbody');
      DATA.social_rows.forEach((row) => {{
        socialBody.insertAdjacentHTML('beforeend', `
          <tr>
            <td>${{row.perfil}}</td>
            <td>${{q(row.actual)}}</td>
            <td>${{q(row.final)}}</td>
            <td>${{row.route}}</td>
            <td>${{pct(row.delta_pct)}}</td>
          </tr>
        `);
      }});

      const marketBody = document.querySelector('#market-table tbody');
      DATA.market_rows.forEach((row) => {{
        marketBody.insertAdjacentHTML('beforeend', `
          <tr>
            <td>${{row.perfil}}</td>
            <td>${{q(row.holding)}}</td>
            <td>${{q(row.sale)}}</td>
            <td>${{row.signal}}</td>
          </tr>
        `);
      }});

      document.getElementById('top-sale').textContent =
        `${{DATA.market_top_sale.perfil}} (${{q(DATA.market_top_sale.sale)}})`;
    }}

    renderBars();
    renderTables();
  </script>
</body>
</html>
"""


def main() -> None:
    payload = build_payload()
    html = build_html(payload)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"Saved {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
