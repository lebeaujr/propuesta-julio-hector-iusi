from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "data" / "jh_f2_proxy_matrix_municipal.csv"
INPUT_JH_F1 = ROOT / "outputs" / "jh_f1_iusi_direct_scenarios.csv"
INPUT_JH_F2B = ROOT / "outputs" / "jh_f2b_iva_compensation_proxy_scenarios.csv"
OUTPUT_HTML = ROOT / "dashboard" / "jh_proxy_municipal_radar.html"


BLOCKS = {
    "urbanidad": {
        "label": "6.1 Urbanidad y centralidad",
        "score": "urbanidad_centralidad_score",
        "indicators": [
            ("viirs", "VIIRS"),
            ("equipamientos_urbanos_importantes", "Equipamientos urbanos"),
            ("densidad_hab_km2", "Densidad hab/km2"),
            ("poblacion_2018", "Poblacion 2018"),
            ("infraestructura", "Infraestructura"),
            ("pib_local_km2", "PIB local por km2"),
        ],
    },
    "mercado": {
        "label": "6.2 Mercado inmobiliario formal",
        "score": "mercado_inmobiliario_formal_score",
        "indicators": [
            ("actividades_construccion", "Actividades de construccion"),
            ("cantidad_empresas", "Cantidad de empresas"),
            ("segmento_abc_alquila", "Segmento ABC alquila"),
            ("ingreso_mensual_hogar", "Ingreso mensual hogar"),
            ("porcentaje_segmento_abc", "% segmento ABC"),
            ("tamano_mercado", "Tamano del mercado"),
            ("dinamismo_negocios", "Dinamismo de negocios"),
        ],
    },
    "finanzas": {
        "label": "6.3 Finanzas, credito y formalidad",
        "score": "finanzas_credito_formalidad_score",
        "indicators": [
            ("cartera_creditos_pib_fund", "Cartera creditos / PIB"),
            ("pea_igss_fund", "% PEA afiliada IGSS"),
            ("agentes_bancarios_100k", "Agentes bancarios 100k"),
            ("depositos_pib_percapita", "Depositos / PIB per capita"),
            ("sistema_financiero", "Sistema financiero"),
        ],
    },
    "institucional": {
        "label": "6.4 Capacidad institucional y catastral",
        "score": "capacidad_institucional_catastral_score",
        "indicators": [
            ("uso_catastro_ot", "Uso del catastro"),
            ("reglamento_construccion_ot", "Reglamento construccion"),
            ("autonomia_financiera", "Autonomia financiera"),
            ("volumen_tributacion", "Volumen tributacion"),
            ("ranking_gestion_municipal", "Ranking gestion municipal"),
            ("instituciones", "Instituciones"),
            ("icl_2025", "ICL 2025"),
        ],
    },
}


def repair_text(value):
    if not isinstance(value, str):
        return value
    if any(token in value for token in ("Ã", "â", "Â")):
        try:
            value = value.encode("latin1").decode("utf-8")
        except Exception:
            pass
    return " ".join(value.split())


def pct_rank(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.rank(pct=True, method="average") * 100


def fmt_raw(value):
    if pd.isna(value):
        return None
    if abs(float(value)) >= 1000:
        return round(float(value), 2)
    return round(float(value), 4)


def build_dataset() -> dict:
    df = pd.read_csv(INPUT_CSV)
    jh_f1 = pd.read_csv(INPUT_JH_F1)
    jh_f2b = pd.read_csv(INPUT_JH_F2B)

    for col in ["municipio_nombre", "departamento_nombre", "region"]:
        df[col] = df[col].map(repair_text)

    df["grupo_proxy_jh"] = pd.qcut(
        df["intensidad_inmobiliaria_formal_score"],
        3,
        labels=["Pequenas", "Medianas", "Grandes"],
    )

    direct_factors = (
        jh_f1.loc[jh_f1["scenario_code"] == "jh_f1_central", ["grupo_municipal", "factor_recaudacion"]]
        .set_index("grupo_municipal")["factor_recaudacion"]
        .to_dict()
    )
    net_factors = (
        jh_f2b.loc[jh_f2b["scenario_code"] == "jh_f2b_central", ["grupo_municipal", "iusi_per_capita_compensado_q", "iusi_per_capita_base_q"]]
        .assign(factor_neto=lambda d: d["iusi_per_capita_compensado_q"] / d["iusi_per_capita_base_q"])
        .set_index("grupo_municipal")["factor_neto"]
        .to_dict()
    )

    for block in BLOCKS.values():
        for code, _label in block["indicators"]:
            df[f"{code}_pct"] = pct_rank(df[code])

    municipalities = []
    for _, row in df.sort_values(["departamento_nombre", "municipio_nombre"]).iterrows():
        blocks_payload = {}
        for block_key, block in BLOCKS.items():
            blocks_payload[block_key] = {
                "label": block["label"],
                "score": round(float(row[block["score"]]), 2),
                "indicators": [
                    {
                        "code": code,
                        "label": label,
                        "percentile": round(float(row[f"{code}_pct"]), 2),
                        "raw": fmt_raw(row[code]),
                    }
                    for code, label in block["indicators"]
                ],
                }

        grupo_proxy = str(row["grupo_proxy_jh"])
        iusi_actual = float(row["iusi_percibido_2025"])
        factor_directo = float(direct_factors[grupo_proxy])
        factor_neto = float(net_factors[grupo_proxy])

        municipalities.append(
            {
                "codigo": int(row["municipio_codigo"]),
                "municipio": row["municipio_nombre"],
                "departamento": row["departamento_nombre"],
                "region": row["region"],
                "iusi_percibido": round(float(row["iusi_percibido_2025"]), 2),
                "iusi_vigente": round(float(row["iusi_vigente_2025"]), 2),
                "proxy_iva_potential_index_100": round(float(row["proxy_iva_potential_index_100"]), 2),
                "proxy_iva_weight_share_pct": round(float(row["proxy_iva_weight_share_pct"]), 4),
                "intensidad_inmobiliaria_formal_score": round(float(row["intensidad_inmobiliaria_formal_score"]), 2),
                "grupo_proxy_jh": grupo_proxy,
                "jh_current_iusi_q": round(iusi_actual, 2),
                "jh_direct_factor": round(factor_directo, 4),
                "jh_net_factor": round(factor_neto, 4),
                "jh_direct_estimated_q": round(iusi_actual * factor_directo, 2),
                "jh_net_estimated_q": round(iusi_actual * factor_neto, 2),
                "blocks": blocks_payload,
            }
        )

    summary = {
        "municipalities": len(municipalities),
        "top_weight": municipalities and max(m["proxy_iva_weight_share_pct"] for m in municipalities),
        "top_index": municipalities and max(m["proxy_iva_potential_index_100"] for m in municipalities),
    }

    return {"blocks": BLOCKS, "municipalities": municipalities, "summary": summary}


def build_html(data: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Radar municipal de intensidad inmobiliaria formal</title>
  <style>
    :root {{
      --bg: #f7f1e7;
      --panel: rgba(255,255,255,0.86);
      --line: #dbc8ac;
      --ink: #25333a;
      --muted: #667680;
      --teal: #1d6a67;
      --gold: #b8782a;
      --blue: #2f5f88;
      --green: #45855e;
      --shadow: 0 16px 34px rgba(71, 51, 16, 0.12);
      --radius: 24px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(20,121,121,0.14), transparent 32%),
        radial-gradient(circle at top right, rgba(184,120,42,0.16), transparent 28%),
        var(--bg);
    }}
    .wrap {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 28px;
    }}
    .hero {{
      background: linear-gradient(135deg, #184f57, #7d5322);
      color: #fff;
      border-radius: 32px;
      padding: 32px 34px;
      box-shadow: var(--shadow);
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: clamp(2rem, 4.2vw, 3.4rem);
      line-height: 1.02;
    }}
    .hero p {{
      max-width: 1040px;
      margin: 0;
      font-size: 1.04rem;
      line-height: 1.55;
      color: rgba(255,255,255,0.92);
    }}
    .layout {{
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 22px;
      margin-top: 22px;
      align-items: start;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid rgba(219, 200, 172, 0.95);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }}
    .sidebar {{
      padding: 20px;
      position: sticky;
      top: 16px;
    }}
    .content {{
      display: grid;
      gap: 22px;
    }}
    h2 {{
      margin: 0 0 14px;
      font-size: 1.25rem;
    }}
    h3 {{
      margin: 0 0 10px;
      font-size: 1.05rem;
    }}
    .filters {{
      display: grid;
      gap: 12px;
    }}
    label {{
      display: block;
      font-size: 0.92rem;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    select, input {{
      width: 100%;
      border: 1.5px solid #cbb899;
      border-radius: 14px;
      padding: 12px 14px;
      background: rgba(255,255,255,0.95);
      font: inherit;
      color: var(--ink);
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }}
    .kpi {{
      padding: 18px;
      min-height: 120px;
    }}
    .kpi .label {{
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 12px;
    }}
    .kpi .value {{
      font-size: 1.9rem;
      font-weight: 800;
      line-height: 1;
      margin-bottom: 8px;
    }}
    .kpi .sub {{
      font-size: 0.92rem;
      color: var(--muted);
      line-height: 1.45;
    }}
    .grid2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 22px;
    }}
    .chart-card {{
      padding: 18px 18px 12px;
    }}
    canvas {{
      width: 100%;
      height: 420px;
      display: block;
    }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px 16px;
      margin-top: 8px;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .dot {{
      display: inline-block;
      width: 11px;
      height: 11px;
      border-radius: 999px;
      margin-right: 8px;
      vertical-align: middle;
    }}
    .table-card {{
      padding: 18px;
      overflow: hidden;
    }}
    .table-wrap {{
      overflow: auto;
      border: 1px solid rgba(219, 200, 172, 0.95);
      border-radius: 18px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 760px;
      background: rgba(255,255,255,0.76);
    }}
    th, td {{
      padding: 12px 14px;
      border-bottom: 1px solid rgba(219, 200, 172, 0.75);
      text-align: left;
      font-size: 0.94rem;
    }}
    th {{
      background: rgba(37, 51, 58, 0.05);
      font-size: 0.84rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
    }}
    .small {{
      font-size: 0.9rem;
      color: var(--muted);
      line-height: 1.55;
    }}
    .notes {{
      padding: 18px;
      display: grid;
      gap: 12px;
    }}
    .note-box {{
      border: 1px solid rgba(219, 200, 172, 0.95);
      border-radius: 18px;
      padding: 14px 16px;
      background: rgba(255,255,255,0.58);
    }}
    .municipio-title {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 14px;
    }}
    .municipio-title h2 {{
      margin-bottom: 6px;
    }}
    .badge {{
      border-radius: 999px;
      padding: 8px 12px;
      background: rgba(29,106,103,0.12);
      color: var(--teal);
      font-weight: 700;
      white-space: nowrap;
      font-size: 0.86rem;
    }}
    @media (max-width: 1160px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; }}
      .kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .grid2 {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 720px) {{
      .wrap {{ padding: 18px; }}
      .hero {{ padding: 24px; }}
      .kpis {{ grid-template-columns: 1fr; }}
      canvas {{ height: 360px; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>Radar municipal de intensidad inmobiliaria formal</h1>
      <p>
        Tablero exploratorio para los 280 municipios de la matriz proxy de IVA inmobiliario.
        Permite ver, estilo ranking/ICL, los cuatro grandes bloques del índice y sus subindicadores
        en gráfica de telaraña, con lectura comparativa sobre el potencial territorial de mercado inmobiliario formal.
      </p>
    </section>

    <div class="layout">
      <aside class="panel sidebar">
        <h2>Seleccion</h2>
        <div class="filters">
          <div>
            <label for="regionSelect">Region</label>
            <select id="regionSelect"></select>
          </div>
          <div>
            <label for="deptoSelect">Departamento</label>
            <select id="deptoSelect"></select>
          </div>
          <div>
            <label for="muniSearch">Busqueda rapida</label>
            <input id="muniSearch" type="text" placeholder="Ej. Mixco, Antigua, Quetzaltenango">
          </div>
          <div>
            <label for="muniSelect">Municipio</label>
            <select id="muniSelect"></select>
          </div>
          <div>
            <label for="compareSearch">Busqueda rapida municipio B</label>
            <input id="compareSearch" type="text" placeholder="Ej. Coban, Zacapa, Mixco">
          </div>
          <div>
            <label for="compareSelect">Comparar con</label>
            <select id="compareSelect"></select>
          </div>
          <div>
            <label for="blockSelect">Bloque de detalle</label>
            <select id="blockSelect"></select>
          </div>
        </div>
        <div class="notes" style="padding-left:0;padding-right:0;padding-bottom:0;margin-top:16px;">
          <div class="note-box">
            <strong>Como leer este tablero</strong>
            <div class="small" style="margin-top:8px;">
              Las telarañas permiten comparar de forma visual la posicion relativa de dos municipios.
              Mientras mas se expande la figura hacia afuera, mayor es su desempeno relativo en ese bloque
              o subindicador frente al resto del pais. No muestran montos exactos de IVA, sino condiciones
              territoriales que hacen mas probable la existencia de actividad inmobiliaria formal.
            </div>
          </div>
          <div class="note-box">
            <strong>Como leer la telaraña</strong>
            <div class="small" style="margin-top:8px;">
              Cada eje se expresa en escala relativa 0-100. No muestra montos absolutos de IVA,
              sino posicion comparativa del municipio frente al resto del pais.
            </div>
          </div>
          <div class="note-box">
            <strong>Fuentes integradas</strong>
            <div class="small" style="margin-top:8px;">
              Matriz construida a partir de IUSI municipal 2025, ADIG-Innovaterra/RIIM 2024 y FUNDESA/ICL 2025.
            </div>
          </div>
        </div>
      </aside>

      <main class="content">
        <section class="municipio-title">
          <div>
            <h2 id="municipioHeading">Municipio</h2>
            <div class="small" id="municipioMeta"></div>
          </div>
          <div class="badge" id="municipioBadge">Indice compuesto</div>
        </section>

        <section class="kpis">
          <div class="panel kpi">
            <div class="label">IUSI percibido 2025</div>
            <div class="value" id="kpiIusi">Q0</div>
            <div class="sub" id="kpiIusiSub"></div>
          </div>
          <div class="panel kpi">
            <div class="label">Indice compuesto</div>
            <div class="value" id="kpiIndice">0</div>
            <div class="sub">Intensidad inmobiliaria formal</div>
          </div>
          <div class="panel kpi">
            <div class="label">Potencial IVA</div>
            <div class="value" id="kpiPotencial">0</div>
            <div class="sub">Ranking percentilar municipal</div>
          </div>
          <div class="panel kpi">
            <div class="label">Peso proxy IVA</div>
            <div class="value" id="kpiPeso">0%</div>
            <div class="sub">Participacion estimada sobre el total proxy</div>
          </div>
        </section>

        <section class="panel notes">
          <div class="note-box">
            <strong>Como leer las tarjetas resumen</strong>
            <div class="small" style="margin-top:8px;">
              Las cuatro tarjetas superiores condensan la comparacion entre los dos municipios seleccionados.
              <strong>IUSI percibido 2025</strong> muestra lo observado hoy. <strong>Indice compuesto</strong>
              resume la intensidad inmobiliaria formal. <strong>Potencial IVA</strong> expresa la posicion
              relativa del municipio en la matriz proxy. <strong>Peso proxy IVA</strong> estima su participacion
              relativa dentro del total nacional proxy, no una cuota observada de recaudacion real.
            </div>
          </div>
        </section>

        <section class="grid2">
          <article class="panel chart-card">
            <h3>Telaraña de los cuatro bloques</h3>
            <div class="small">Comparacion sintetica de 6.1 a 6.4 para dos municipios seleccionados.</div>
            <canvas id="mainRadar" width="620" height="440"></canvas>
            <div class="legend">
              <span><span class="dot" style="background: var(--teal)"></span>Municipio A</span>
              <span><span class="dot" style="background: var(--gold)"></span>Municipio B</span>
            </div>
          </article>

          <article class="panel chart-card">
            <h3 id="detailTitle">Telaraña de subindicadores</h3>
            <div class="small" id="detailSubtitle">Detalle del bloque seleccionado en escala percentilar.</div>
            <canvas id="detailRadar" width="620" height="440"></canvas>
            <div class="legend">
              <span><span class="dot" style="background: var(--teal)"></span>Municipio A</span>
              <span><span class="dot" style="background: var(--gold)"></span>Municipio B</span>
            </div>
          </article>
        </section>

        <section class="panel table-card">
          <h3 id="tableTitle">Indicadores del bloque</h3>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Indicador</th>
                  <th id="thPctA">Percentil A</th>
                  <th id="thRawA">Valor A</th>
                  <th id="thPctB">Percentil B</th>
                  <th id="thRawB">Valor B</th>
                </tr>
              </thead>
              <tbody id="detailTableBody"></tbody>
            </table>
          </div>
        </section>

        <section class="panel table-card">
          <h3>Resumen fiscal proxy: IUSI actual y con reforma</h3>
          <div class="small" style="margin-bottom:12px;">
            Esta tabla no muestra una proyeccion oficial municipio por municipio. Presenta una aproximacion
            construida a partir del IUSI observado hoy y de dos pasos simplificados: primero, una estimacion
            del efecto directo de la reforma sobre el IUSI; segundo, una estimacion del resultado
            <strong>neto</strong>, es decir, del IUSI despues de considerar una compensacion parcial asociada
            al componente municipal del IVA inmobiliario segun el perfil territorial del municipio.
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Concepto</th>
                  <th id="thFiscalA">Municipio A</th>
                  <th id="thFiscalB">Municipio B</th>
                </tr>
              </thead>
              <tbody id="fiscalProxyBody"></tbody>
            </table>
          </div>
        </section>

        <section class="panel notes">
          <div class="note-box">
            <strong>Lectura metodologica</strong>
            <div class="small" style="margin-top:8px;">
              El indice final pondera: 30% urbanidad y centralidad, 30% mercado inmobiliario formal,
              25% finanzas, credito y formalidad, y 15% capacidad institucional y catastral.
            </div>
          </div>
          <div class="note-box">
            <strong>Interpretacion recomendada</strong>
            <div class="small" style="margin-top:8px;">
              Un municipio con score alto no necesariamente recauda mas IVA hoy; mas bien presenta
              una combinacion de condiciones urbanas, de mercado, financieras e institucionales
              que lo hacen mas probable candidato a captar operaciones inmobiliarias formales.
            </div>
          </div>
          <div class="note-box">
            <strong>Como leer el resumen fiscal proxy</strong>
            <div class="small" style="margin-top:8px;">
              <strong>IUSI percibido actual</strong> es lo observado hoy. <strong>IUSI directo estimado con reforma</strong>
              es una aproximacion de lo que quedaria si solo operara el cambio principal en el IUSI.
              <strong>IUSI neto estimado con compensacion</strong> agrega una compensacion parcial esperada
              por la via municipal del IVA inmobiliario. Por eso “neto” significa aqui el saldo final
              aproximado despues de esa compensacion, no una cifra ejecutada u observada.
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>

  <script id="dataset" type="application/json">{data_json}</script>
  <script>
    const dataset = JSON.parse(document.getElementById('dataset').textContent);
    const municipalities = dataset.municipalities;
    const blocksMeta = dataset.blocks;

    const regionSelect = document.getElementById('regionSelect');
    const deptoSelect = document.getElementById('deptoSelect');
    const muniSearch = document.getElementById('muniSearch');
    const muniSelect = document.getElementById('muniSelect');
    const compareSearch = document.getElementById('compareSearch');
    const compareSelect = document.getElementById('compareSelect');
    const blockSelect = document.getElementById('blockSelect');

    const municipioHeading = document.getElementById('municipioHeading');
    const municipioMeta = document.getElementById('municipioMeta');
    const municipioBadge = document.getElementById('municipioBadge');

    const kpiIusi = document.getElementById('kpiIusi');
    const kpiIusiSub = document.getElementById('kpiIusiSub');
    const kpiIndice = document.getElementById('kpiIndice');
    const kpiPotencial = document.getElementById('kpiPotencial');
    const kpiPeso = document.getElementById('kpiPeso');

    const detailTitle = document.getElementById('detailTitle');
    const detailSubtitle = document.getElementById('detailSubtitle');
    const tableTitle = document.getElementById('tableTitle');
    const detailTableBody = document.getElementById('detailTableBody');
    const thPctA = document.getElementById('thPctA');
    const thRawA = document.getElementById('thRawA');
    const thPctB = document.getElementById('thPctB');
    const thRawB = document.getElementById('thRawB');
    const thFiscalA = document.getElementById('thFiscalA');
    const thFiscalB = document.getElementById('thFiscalB');
    const fiscalProxyBody = document.getElementById('fiscalProxyBody');

    const mainRadar = document.getElementById('mainRadar');
    const detailRadar = document.getElementById('detailRadar');

    function uniqueSorted(values) {{
      return ['Todos'].concat([...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, 'es')));
    }}

    function money(v) {{
      return new Intl.NumberFormat('es-GT', {{ style: 'currency', currency: 'GTQ', maximumFractionDigits: 0 }}).format(v || 0);
    }}

    function num(v, digits = 1) {{
      return new Intl.NumberFormat('es-GT', {{ minimumFractionDigits: digits, maximumFractionDigits: digits }}).format(v || 0);
    }}

    function fillSelect(select, values, selected = 'Todos') {{
      select.innerHTML = values.map(v => `<option value="${{v}}">${{v}}</option>`).join('');
      select.value = values.includes(selected) ? selected : values[0];
    }}

    function getFilteredMunicipalities() {{
      const region = regionSelect.value;
      const depto = deptoSelect.value;
      const search = muniSearch.value.trim().toLowerCase();
      return municipalities.filter(m => {{
        if (region && region !== 'Todos' && m.region !== region) return false;
        if (depto && depto !== 'Todos' && m.departamento !== depto) return false;
        if (search && !(`${{m.municipio}} ${{m.departamento}}`.toLowerCase().includes(search))) return false;
        return true;
      }});
    }}

    function getCompareFilteredMunicipalities() {{
      const search = compareSearch.value.trim().toLowerCase();
      return municipalities.filter(m => {{
        if (search && !(`${{m.municipio}} ${{m.departamento}}`.toLowerCase().includes(search))) return false;
        return true;
      }});
    }}

    function refreshDeptos() {{
      const region = regionSelect.value;
      const deptos = uniqueSorted(
        municipalities
          .filter(m => region === 'Todos' || m.region === region)
          .map(m => m.departamento)
      );
      const keep = deptoSelect.value;
      fillSelect(deptoSelect, deptos, keep);
    }}

    function refreshMunicipios() {{
      const current = muniSelect.value;
      const currentCompare = compareSelect.value;
      const filtered = getFilteredMunicipalities();
      const compareFiltered = getCompareFilteredMunicipalities();
      const optionsHtml = filtered
        .map(m => `<option value="${{m.codigo}}">${{m.municipio}} (${{m.departamento}})</option>`)
        .join('');
      const compareOptionsHtml = compareFiltered
        .map(m => `<option value="${{m.codigo}}">${{m.municipio}} (${{m.departamento}})</option>`)
        .join('');
      muniSelect.innerHTML = optionsHtml;
      compareSelect.innerHTML = compareOptionsHtml;
      if (!filtered.length) {{
        muniSelect.innerHTML = '<option value="">Sin coincidencias</option>';
      }}
      if (!compareFiltered.length) {{
        compareSelect.innerHTML = '<option value="">Sin coincidencias</option>';
      }}
      if (!filtered.length) {{
        return;
      }}
      const currentExists = filtered.some(m => String(m.codigo) === current);
      muniSelect.value = currentExists ? current : String(filtered[0].codigo);
      if (!compareFiltered.length) {{
        return;
      }}
      const compareExists = compareFiltered.some(m => String(m.codigo) === currentCompare);
      compareSelect.value = compareExists ? currentCompare : String(compareFiltered[Math.min(1, compareFiltered.length - 1)].codigo);
      if (compareSelect.value === muniSelect.value && compareFiltered.length > 1) {{
        const alternative = compareFiltered.find(m => String(m.codigo) !== muniSelect.value);
        if (alternative) compareSelect.value = String(alternative.codigo);
      }}
    }}

    function getCurrentMunicipality() {{
      return municipalities.find(m => String(m.codigo) === muniSelect.value) || municipalities[0];
    }}

    function getCompareMunicipality() {{
      return municipalities.find(m => String(m.codigo) === compareSelect.value) || getCurrentMunicipality();
    }}

    function drawRadar(canvas, labels, datasets) {{
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const width = canvas.clientWidth || canvas.width;
      const height = canvas.clientHeight || canvas.height;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, width, height);

      const centerX = width / 2;
      const centerY = height / 2 + 8;
      const radius = Math.min(width, height) * 0.30;
      const levels = 5;
      const angleStep = (Math.PI * 2) / labels.length;

      ctx.strokeStyle = 'rgba(84, 93, 101, 0.18)';
      ctx.fillStyle = 'rgba(84, 93, 101, 0.16)';
      ctx.lineWidth = 1;

      for (let level = 1; level <= levels; level++) {{
        const r = radius * (level / levels);
        ctx.beginPath();
        labels.forEach((_, i) => {{
          const angle = -Math.PI / 2 + i * angleStep;
          const x = centerX + Math.cos(angle) * r;
          const y = centerY + Math.sin(angle) * r;
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }});
        ctx.closePath();
        ctx.stroke();
      }}

      labels.forEach((label, i) => {{
        const angle = -Math.PI / 2 + i * angleStep;
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.stroke();

        const lx = centerX + Math.cos(angle) * (radius + 28);
        const ly = centerY + Math.sin(angle) * (radius + 28);
        ctx.fillStyle = '#43525b';
        ctx.font = '12px Segoe UI, sans-serif';
        ctx.textAlign = lx < centerX - 10 ? 'right' : (lx > centerX + 10 ? 'left' : 'center');
        ctx.textBaseline = ly < centerY - 10 ? 'bottom' : (ly > centerY + 10 ? 'top' : 'middle');
        wrapText(ctx, label, lx, ly, 100, 14);
      }});

      datasets.forEach((dataset, idx) => {{
        const fill = dataset.fill || (idx === 0 ? 'rgba(29,106,103,0.18)' : 'rgba(184,120,42,0.18)');
        const stroke = dataset.stroke || (idx === 0 ? '#1d6a67' : '#b8782a');
        const point = dataset.point || stroke;
        const values = dataset.values || [];

        ctx.beginPath();
        values.forEach((value, i) => {{
          const angle = -Math.PI / 2 + i * angleStep;
          const r = radius * ((value || 0) / 100);
          const x = centerX + Math.cos(angle) * r;
          const y = centerY + Math.sin(angle) * r;
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }});
        ctx.closePath();
        ctx.fillStyle = fill;
        ctx.strokeStyle = stroke;
        ctx.lineWidth = 2.4;
        ctx.fill();
        ctx.stroke();

        values.forEach((value, i) => {{
          const angle = -Math.PI / 2 + i * angleStep;
          const r = radius * ((value || 0) / 100);
          const x = centerX + Math.cos(angle) * r;
          const y = centerY + Math.sin(angle) * r;
          ctx.beginPath();
          ctx.arc(x, y, 4.2, 0, Math.PI * 2);
          ctx.fillStyle = point;
          ctx.fill();
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = 1.5;
          ctx.stroke();
        }});
      }});
    }}

    function wrapText(ctx, text, x, y, maxWidth, lineHeight) {{
      const words = text.split(' ');
      let line = '';
      const lines = [];
      for (const word of words) {{
        const test = line ? `${{line}} ${{word}}` : word;
        if (ctx.measureText(test).width > maxWidth && line) {{
          lines.push(line);
          line = word;
        }} else {{
          line = test;
        }}
      }}
      lines.push(line);
      lines.forEach((part, idx) => {{
        const dy = (idx - (lines.length - 1) / 2) * lineHeight;
        ctx.fillText(part, x, y + dy);
      }});
    }}

    function render() {{
      const muni = getCurrentMunicipality();
      const compare = getCompareMunicipality();
      if (!muni || !compare) return;

      const blockKey = blockSelect.value || 'urbanidad';
      const block = muni.blocks[blockKey];
      const compareBlock = compare.blocks[blockKey];

      municipioHeading.textContent = `${{muni.municipio}} vs ${{compare.municipio}}`;
      municipioMeta.textContent = `${{muni.departamento}} | ${{muni.region}}  comparado con  ${{compare.departamento}} | ${{compare.region}}`;
      municipioBadge.textContent = `Indice compuesto: ${{num(muni.intensidad_inmobiliaria_formal_score, 1)}} vs ${{num(compare.intensidad_inmobiliaria_formal_score, 1)}}`;

      kpiIusi.textContent = `${{money(muni.iusi_percibido)}} / ${{money(compare.iusi_percibido)}}`;
      kpiIusiSub.textContent = `Vigente 2025: ${{money(muni.iusi_vigente)}} / ${{money(compare.iusi_vigente)}}`;
      kpiIndice.textContent = `${{num(muni.intensidad_inmobiliaria_formal_score, 1)}} / ${{num(compare.intensidad_inmobiliaria_formal_score, 1)}}`;
      kpiPotencial.textContent = `${{num(muni.proxy_iva_potential_index_100, 1)}} / ${{num(compare.proxy_iva_potential_index_100, 1)}}`;
      kpiPeso.textContent = `${{num(muni.proxy_iva_weight_share_pct, 2)}}% / ${{num(compare.proxy_iva_weight_share_pct, 2)}}%`;

      const mainLabels = Object.keys(blocksMeta).map(key => blocksMeta[key].label.replace(/^6\\.[0-9]\\s+/, ''));
      drawRadar(mainRadar, mainLabels, [
        {{
          values: [
            muni.blocks.urbanidad.score,
            muni.blocks.mercado.score,
            muni.blocks.finanzas.score,
            muni.blocks.institucional.score,
          ],
          fill: 'rgba(29,106,103,0.20)',
          stroke: '#1d6a67',
          point: '#1d6a67',
        }},
        {{
          values: [
            compare.blocks.urbanidad.score,
            compare.blocks.mercado.score,
            compare.blocks.finanzas.score,
            compare.blocks.institucional.score,
          ],
          fill: 'rgba(184,120,42,0.20)',
          stroke: '#b8782a',
          point: '#b8782a',
        }}
      ]);

      detailTitle.textContent = block.label;
      detailSubtitle.textContent = `Subindicadores expresados en percentiles relativos 0-100 para ${{muni.municipio}} y ${{compare.municipio}}.`;
      tableTitle.textContent = `Indicadores de ${{block.label}}`;
      thPctA.textContent = `Percentil ${{muni.municipio}}`;
      thRawA.textContent = `Valor ${{muni.municipio}}`;
      thPctB.textContent = `Percentil ${{compare.municipio}}`;
      thRawB.textContent = `Valor ${{compare.municipio}}`;
      thFiscalA.textContent = muni.municipio;
      thFiscalB.textContent = compare.municipio;

      drawRadar(
        detailRadar,
        block.indicators.map(i => i.label),
        [
          {{
            values: block.indicators.map(i => i.percentile),
            fill: 'rgba(29,106,103,0.20)',
            stroke: '#1d6a67',
            point: '#1d6a67',
          }},
          {{
            values: compareBlock.indicators.map(i => i.percentile),
            fill: 'rgba(184,120,42,0.20)',
            stroke: '#b8782a',
            point: '#b8782a',
          }}
        ]
      );

      detailTableBody.innerHTML = block.indicators.map((ind, idx) => `
        <tr>
          <td>${{ind.label}}</td>
          <td>${{num(ind.percentile, 1)}}</td>
          <td>${{ind.raw === null ? 's/d' : num(ind.raw, Math.abs(ind.raw) >= 100 ? 2 : 4)}}</td>
          <td>${{num(compareBlock.indicators[idx].percentile, 1)}}</td>
          <td>${{compareBlock.indicators[idx].raw === null ? 's/d' : num(compareBlock.indicators[idx].raw, Math.abs(compareBlock.indicators[idx].raw) >= 100 ? 2 : 4)}}</td>
        </tr>
      `).join('');

      fiscalProxyBody.innerHTML = [
        ['Grupo proxy JH', muni.grupo_proxy_jh, compare.grupo_proxy_jh],
        ['IUSI percibido actual', money(muni.jh_current_iusi_q), money(compare.jh_current_iusi_q)],
        ['IUSI directo estimado con reforma', money(muni.jh_direct_estimated_q), money(compare.jh_direct_estimated_q)],
        ['IUSI neto estimado con compensacion', money(muni.jh_net_estimated_q), money(compare.jh_net_estimated_q)],
        ['Factor directo aplicado', num(muni.jh_direct_factor * 100, 1) + '%', num(compare.jh_direct_factor * 100, 1) + '%'],
        ['Factor neto aplicado', num(muni.jh_net_factor * 100, 1) + '%', num(compare.jh_net_factor * 100, 1) + '%'],
      ].map(row => `
        <tr>
          <td>${{row[0]}}</td>
          <td>${{row[1]}}</td>
          <td>${{row[2]}}</td>
        </tr>
      `).join('');
    }}

    function init() {{
      fillSelect(regionSelect, uniqueSorted(municipalities.map(m => m.region)));
      refreshDeptos();
      refreshMunicipios();
      blockSelect.innerHTML = Object.entries(blocksMeta)
        .map(([key, meta]) => `<option value="${{key}}">${{meta.label}}</option>`)
        .join('');
      blockSelect.value = 'urbanidad';

      regionSelect.addEventListener('change', () => {{
        refreshDeptos();
        refreshMunicipios();
        render();
      }});
      deptoSelect.addEventListener('change', () => {{
        refreshMunicipios();
        render();
      }});
      muniSearch.addEventListener('input', () => {{
        refreshMunicipios();
        render();
      }});
      compareSearch.addEventListener('input', () => {{
        refreshMunicipios();
        render();
      }});
      muniSelect.addEventListener('change', render);
      compareSelect.addEventListener('change', render);
      blockSelect.addEventListener('change', render);
      window.addEventListener('resize', render);

      render();
    }}

    init();
  </script>
</body>
</html>
"""


def main() -> None:
    data = build_dataset()
    OUTPUT_HTML.write_text(build_html(data), encoding="utf-8")


if __name__ == "__main__":
    main()
