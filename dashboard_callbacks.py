# dashboard_callbacks.py

from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from io import StringIO
from dateutil.relativedelta import relativedelta
import time
import numpy as np


# Mapeamento Empreendimento → Região, baseado na sua lista
REGION_MAPPING = {
    "RESERVA SAUIPE - FASE 1": "Bahia",
    "TERRA DOURADA - FASE 2": "Bahia",
    "TERRA DOURADA - FASE 1": "Bahia",
    "LEGACY": "Bahia",
    "QUINTAS DE SAUIPE GRANDE LAGUNA": "Bahia",
    "EVOKE - FASE 2": "Pernambuco",
    "EVOKE - FASE 1": "Pernambuco",
    "RESERVA SAUIPE - FASE 2": "Bahia",
    "HANGAR EMPRESARIAL - FASE 2": "Bahia",
    "VERANO": "Pernambuco",
    "Baume": "Sudeste",
    "VITRIUM - FASE 1": "Sudeste",
    "CONSORCIO PORTO ATLANTICO LESTE - FASE 2": "Sudeste",
    "Inspira Itaim": "Sudeste",
    "RYT - PAULISTA": "Sudeste",
    "LED": "Sudeste",
    "THE BLUE": "Sudeste",
    "DIMENSION OFFICE & PARK": "Sudeste",
    "ROYAL CAMPINAS SUL": "Sudeste",
    "VENT RESIDENCIAL - FASE 1": "Sudeste",
    "PARQUE TROPICAL": "Bahia",
    "JARDIM DO MAR": "Pernambuco",
    "HANGAR EMPRESARIAL - FASE 1": "Bahia",
    "MUNDO PLAZA": "Bahia",
    "VERDE MORUMBI - FASE 1": "Sudeste",
    "LED BARRA FUNDA RESIDENCIAL": "Sudeste",
    "D AZUR": "Bahia",
    "MONVERT": "Bahia",
    "VILA DOS CORAIS": "Pernambuco",
    "NOVO MUNDO EMPRESARIAL": "Pernambuco",
    "J. MANGUEIRAL - QUADRA 9 - JATOBAS": "Sudeste",
    "CONDOMINIO VALONGO BRASIL": "Sudeste",
    "PARQUE AVENIDA": "Sudeste",
    "VENT RESIDENCIAL - FASE 2": "Sudeste"
}

# Abreviação para extrair colunas de usuário
def _user_col(df):
    return "USUÁRIO" if "USUÁRIO" in df.columns else "USUARIOS"


def register_dashboard_callbacks(app):
    # ------------------------------------------------------------------
    # 0) Regionais
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-region-checklist", "options"),
        Input("filtered-data", "data"),
        Input("refresh-button", 		 "n_clicks"),
    )
    def update_region_options(json_data, refresh_clicks):
        if not json_data:
            return []
        regions = sorted(set(REGION_MAPPING.values()))
        return [{"label": r, "value": r} for r in regions]

    # ------------------------------------------------------------------
    # A) Empreendimentos ← Regionais
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-empreendimento-checklist", "options"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("refresh-button", 		 "n_clicks"),
    )
    def update_empreendimento_options(json_data, regions, refresh_clicks):
        if not json_data:
            return []
        df = pd.read_json(StringIO(json_data), orient="split")
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        opts = sorted(df["Empreendimento"].dropna().unique())
        return [{"label": e, "value": e} for e in opts]

    # ------------------------------------------------------------------
    # B) Macro Assunto ← Regionais + Empreendimentos
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-macro-checklist", "options"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("dash-empreendimento-checklist", "value"),
        Input("refresh-button", 		 "n_clicks"),
    )
    def update_macro_options(json_data, regions, empre, refresh_clicks):
        if not json_data:
            return []
        df = pd.read_json(StringIO(json_data), orient="split")
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        opts = sorted(df["TITULO1"].dropna().unique())
        return [{"label": m, "value": m} for m in opts]

    # ------------------------------------------------------------------
    # C) Tipo Ticket
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-ticket-checklist", "options"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("dash-empreendimento-checklist", "value"),
        Input("dash-macro-checklist", "value"),
        Input("refresh-button", 		 "n_clicks"),
    )
    def update_ticket_options(json_data, regions, empre, macros, refresh_clicks):
        if not json_data:
            return []
        df = pd.read_json(StringIO(json_data), orient="split")
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        opts = sorted(df["TIPO TICKET"].dropna().unique())
        return [{"label": t, "value": t} for t in opts]

    # ------------------------------------------------------------------
    # D) Tipo Ação
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-action-checklist", "options"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("dash-empreendimento-checklist", "value"),
        Input("dash-macro-checklist", "value"),
        Input("dash-ticket-checklist", "value"),
        Input("refresh-button", 		 "n_clicks"),
    )
    def update_action_options(json_data, regions, empre, macros, tickets, refresh_clicks):
        if not json_data:
            return []
        df = pd.read_json(StringIO(json_data), orient="split")
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        opts = sorted(df["TIPO AÇÃO"].dropna().unique())
        return [{"label": a, "value": a} for a in opts]

    # ------------------------------------------------------------------
    # E) TIPO ORIGEM  (dash‑tipo‑origem‑checklist)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-tipo-origem-checklist", "options"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("dash-empreendimento-checklist", "value"),
        Input("dash-macro-checklist", "value"),
        Input("dash-ticket-checklist", "value"),
        Input("dash-action-checklist", "value"),
        Input("refresh-button", 		 "n_clicks"),
    )
    def update_tipo_origem_options(json_data, regions, empre, macros, tickets, actions, refresh_clicks):
        if not json_data:
            return []
        df = pd.read_json(StringIO(json_data), orient="split")
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        opts = sorted(df["TIPO ORIGEM"].dropna().unique())
        return [{"label": o, "value": o} for o in opts]

    # ------------------------------------------------------------------
    # F) ORIGEM  (dash‑origem‑checklist)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-origem-checklist", "options"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("dash-empreendimento-checklist", "value"),
        Input("dash-macro-checklist", "value"),
        Input("dash-ticket-checklist", "value"),
        Input("dash-action-checklist", "value"),
        Input("dash-tipo-origem-checklist", "value"),
        Input("refresh-button", 		 "n_clicks"),
    )
    def update_origem_options(json_data, regions, empre, macros, tickets, actions, tipo_origs, refresh_clicks):
        if not json_data:
            return []
        df = pd.read_json(StringIO(json_data), orient="split")
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origs:
            df = df[df["TIPO ORIGEM"].isin(tipo_origs)]
        opts = sorted(df["ORIGEM"].dropna().unique())
        return [{"label": o, "value": o} for o in opts]

    # ------------------------------------------------------------------
    # G) Usuário ← todos os filtros (inclui TIPO ORIGEM e ORIGEM)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-user-checklist", "options"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("dash-empreendimento-checklist", "value"),
        Input("dash-macro-checklist", "value"),
        Input("dash-ticket-checklist", "value"),
        Input("dash-action-checklist", "value"),
        Input("dash-tipo-origem-checklist", "value"),   
        Input("dash-origem-checklist", "value"),
        Input("refresh-button", 		 "n_clicks"),        
    )
    def update_user_options(json_data,
                            regions,
                            empre,
                            macros,
                            tickets,
                            actions,
                            tipo_origs,
                            origs,
                            refresh_clicks):
        if not json_data:
            return []

        df = pd.read_json(StringIO(json_data), orient="split")
        col = _user_col(df)

        # aplica filtros em sequência
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origs:
            df = df[df["TIPO ORIGEM"].isin(tipo_origs)]
        if origs:
            df = df[df["ORIGEM"].isin(origs)]

        opts = sorted(df[col].dropna().unique())
        return [{"label": u, "value": u} for u in opts]


    # ------------------------------------------------------------------
    # H) Gráfico ← todos os filtros
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-1", "figure"),
        Input("filtered-data", "data"),
        Input("dash-region-checklist", "value"),
        Input("dash-empreendimento-checklist", "value"),
        Input("dash-macro-checklist", "value"),
        Input("dash-ticket-checklist", "value"),
        Input("dash-action-checklist", "value"),
        Input("dash-tipo-origem-checklist", "value"),   
        Input("dash-origem-checklist", "value"),        
        Input("dash-user-checklist", "value"),
        Input("refresh-button", "n_clicks"),
    )
    def update_dashboard(json_data,
                        regions,
                        empre,
                        macros,
                        tickets,
                        actions,
                        tipo_origs,
                        origs,
                        users,
                        refresh_clicks):
        if not json_data:
            return {}

        df = pd.read_json(StringIO(json_data), orient="split")
        col = _user_col(df)

        # aplica filtros na mesma ordem
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origs:
            df = df[df["TIPO ORIGEM"].isin(tipo_origs)]
        if origs:
            df = df[df["ORIGEM"].isin(origs)]
        if users:
            df = df[df[col].isin(users)]

        resumo = df[col].value_counts().reset_index()
        resumo.columns = [col, "Quantidade"]

        # Gráfico de barras (Chamados por Usuário)
        fig = px.bar(
            resumo,
            x=col,
            y="Quantidade",
            text="Quantidade", 
            orientation="v",
            labels={col: "Usuário", "Quantidade": "Chamados"},
            title="Chamados por Usuário",
            color_discrete_sequence=["#FFA726"]
        )
        fig.update_layout(
            template=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            autosize=True,
            margin=dict(l=40, r=20, t=50, b=80),
            xaxis_title="",    
            yaxis_title=""     
        )
        fig.update_xaxes(
            tickfont=dict(size=10, color="#FFFFFF"),
            color="#FFFFFF",
            gridcolor="rgba(255,255,255,0.1)"
        )
        fig.update_yaxes(
            color="#FFFFFF",
            gridcolor="rgba(255,255,255,0.1)"
        )
        fig.update_traces(
            textposition="outside",
            textfont_size=11,
            cliponaxis=False
        )
        # devolve o gráfico sem rótulos nos eixos
        return fig


    # ------------------------------------------------------------------
    # H) Histograma DT. ABERTURA ← reage só aos mesmos filtros
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-2", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_timeline(json_data,
                        selected_regions,
                        selected_empreendimentos,
                        selected_macros,
                        selected_tickets,
                        selected_actions,
                        selected_tipo_origem,
                        selected_origem,
                        selected_users,
                        refresh_clicks):
        if not json_data:
            return {}

        # 1) Carrega e aplica filtros
        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)
        if selected_regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(selected_regions)]
        if selected_empreendimentos:
            df = df[df["Empreendimento"].isin(selected_empreendimentos)]
        if selected_macros:
            df = df[df["TITULO1"].isin(selected_macros)]
        if selected_tickets:
            df = df[df["TIPO TICKET"].isin(selected_tickets)]
        if selected_actions:
            df = df[df["TIPO AÇÃO"].isin(selected_actions)]
        if selected_tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(selected_tipo_origem)]
        if selected_origem:
            df = df[df["ORIGEM"].isin(selected_origem)]
        if selected_users:
            df = df[df[col_user].isin(selected_users)]

        # 2) Prepara Data Abertura
        df["Data Abertura"] = pd.to_datetime(df["Data Abertura"], dayfirst=True, errors="coerce")
        df = df.dropna(subset=["Data Abertura"])

        # 3) Cria histograma mensal
        fig2 = px.histogram(
            df,
            x="Data Abertura",
            nbins=max(df["Data Abertura"].dt.to_period("M").nunique(), 1),
            title="Data Abertura",
            labels={"Data Abertura": "Data Abertura", "count": "Quantidade"},
            color_discrete_sequence=["#FFA726"],
            template=None,
            text_auto=True
        )
        fig2.update_layout(
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            autosize=True,
            bargap=0.2,                      
            margin=dict(l=40, r=20, t=50, b=50),  
            yaxis_title="Quantidade",
            xaxis_title="",                                
            xaxis=dict(rangeslider=dict(visible=True), type="date")
        )
        fig2.update_xaxes(
            tickfont=dict(size=10, color="#FFFFFF"),
            color="#FFFFFF",
            gridcolor="rgba(255,255,255,0.1)"
        )
        fig2.update_yaxes(
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)"
        )
        fig2.update_traces(
            textposition="outside",
            texttemplate="%{y}",            
            textfont=dict(color="#FFFFFF", size=10),
            cliponaxis=False
        )

        return fig2
    

    # ------------------------------------------------------------------
    # I) Qtd por Mês  (dashboard‑graph‑3)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-3", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_qtd_mes(json_data,
                       regions, empre, macros, tickets,
                       actions, tipo_origem, origem, users, refresh_clicks):
        if not json_data:
            return {}

        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)

        # aplica mesmos filtros
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(tipo_origem)]
        if origem:
            df = df[df["ORIGEM"].isin(origem)]
        if users:
            df = df[df[col_user].isin(users)]

        # → Agrupa por mês/ano
        df["Data Abertura"] = pd.to_datetime(df["Data Abertura"], dayfirst=True, errors="coerce")
        df = df.dropna(subset=["Data Abertura"])
        df["Mes"] = df["Data Abertura"].dt.to_period("M")
        mensal = (df.groupby("Mes").size().reset_index(name="Quantidade"))
        mensal["Mes"] = mensal["Mes"].dt.strftime("%b/%y")
        media = mensal["Quantidade"].mean()

        # gráfico
        fig3 = px.bar(
            mensal,
            x="Mes",
            y="Quantidade",
            title="Qtd por Mês",
            text="Quantidade",
            color_discrete_sequence=["#FF8C25"],   
            template=None,
        )
        # linha de média
        fig3.add_hline(
            y=media,
            line_dash="dot",
            line_color="#CCCCCC",
            annotation_text="",           
            annotation_position="top right",
            annotation_font_color="#FFA726",
            annotation_bgcolor="rgba(0,0,0,0)",
        )
        # → Ajustes de barra e texto
        fig3.update_traces(
            width=0.6,              
            textposition="outside", 
            cliponaxis=False        
        )
        fig3.update_layout(
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            autosize=True,
            margin=dict(l=40, r=20, t=50, b=100), 
            xaxis_title="",
        )
        # ── Insere texto “Média Mensal: XX.X” no canto superior direito ──
        fig3.add_annotation(
            xref="paper", yref="paper",
            x=1,    
            y=1.15, 
            text=f"Média Mensal: {media:.1f}",
            showarrow=False,
            font=dict(size=12, color="#FFA726")
        )
        fig3.update_xaxes(
            tickangle=-45,
            automargin=True,
            tickfont=dict(size=11, color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )
        fig3.update_yaxes(
            automargin=True,
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )
        return fig3

    # ------------------------------------------------------------------
    # J) Qtd por Empreendimento  –  barras grossas + wrapper com scroll
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-4", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_qtd_empreendimento(json_data,
                                regions, empre, macros, tickets,
                                actions, tipo_origem, origem, users, refresh_clicks):
        # 1) Carrega e aplica filtros
        if not json_data:
            return {}
        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(tipo_origem)]
        if origem:
            df = df[df["ORIGEM"].isin(origem)]
        if users:
            df = df[df[col_user].isin(users)]

        # 2) Contagem por Empreendimento, ordenada
        cont = (
            df["Empreendimento"]
            .value_counts()
            .rename_axis("Empreendimento")
            .reset_index(name="Quantidade")
            .sort_values("Quantidade", ascending=True)
        )

        # 3) Cria o bar horizontal
        fig4 = px.bar(
            cont,
            x="Quantidade",
            y="Empreendimento",
            orientation="h",
            text="Quantidade",
            title="Qtd por Empreendimento",
            color_discrete_sequence=["#FFA726"],
            template=None,
        )

        # 4) Ajusta grossura das barras e posiciona texto fora
        fig4.update_traces(
            width=0.5,          
            textposition="outside",
            cliponaxis=False
        )

        # 5) Layout “dark” com altura dinâmica:
        total_barras = len(cont)
        altura_svg = max(345, total_barras * 40 + 80)  

        fig4.update_layout(
            height=altura_svg,
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            bargap=0.05,           
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="",   
            yaxis_title="",   
        )

        # 6) Ajuste fino de eixos
        fig4.update_yaxes(
            automargin=True,
            tickfont=dict(size=11, color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )
        fig4.update_xaxes(
            automargin=True,
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )

        return fig4


    # ------------------------------------------------------------------
    # L) Qtd por Origem  (dashboard‑graph‑5)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-5", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_qtd_origem(json_data,
                        regions, empre, macros, tickets,
                        actions, tipo_origem, origem, users, refresh_clicks):
        if not json_data:
            return {}

        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)

        # filtros
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(tipo_origem)]
        if origem:
            df = df[df["ORIGEM"].isin(origem)]
        if users:
            df = df[df[col_user].isin(users)]

        cont = df["ORIGEM"].value_counts().reset_index()
        cont.columns = ["Origem", "Quantidade"]

        fig5 = px.bar(
            cont.sort_values("Quantidade", ascending=True),
            x="Quantidade",
            y="Origem",
            orientation="h",
            text="Quantidade",
            title="Qtd por Origem",
            color_discrete_sequence=["#FFA726"],
            template=None,
        )

        fig5.update_traces(
            width=0.6,
            textposition="outside",
            cliponaxis=False
        )

        fig5.update_layout(
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            autosize=True,
            margin=dict(l=120, r=20, t=50, b=60),
            xaxis_title="",
        )

        fig5.update_yaxes(
            automargin=True,
            tickfont=dict(size=10, color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )
        fig5.update_xaxes(
            automargin=True,
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )

        return fig5

    # ------------------------------------------------------------------
    # M) Qtd por Status (dashboard-graph-6)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-6", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_qtd_status(json_data,
                        regions, empre, macros, tickets,
                        actions, tipo_origem, origem, users, refresh_clicks):
        if not json_data:
            return {}
        df = pd.read_json(StringIO(json_data), orient="split")
        # reaplica filtros como nos outros gráficos
        col_user = _user_col(df)
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(tipo_origem)]
        if origem:
            df = df[df["ORIGEM"].isin(origem)]
        if users:
            df = df[df[col_user].isin(users)]

        # 1) Contagem por status
        cont = df["STATUS"].value_counts().reset_index()
        cont.columns = ["Status", "Quantidade"]
        total = int(cont["Quantidade"].sum())

        # 2) Pie com furo, com pull e borda branca
        fig6 = px.pie(
            cont,
            names="Status",
            values="Quantidade",
            hole=0.5,
            color_discrete_sequence=["#FFA726","#1F77B4","#2CA02C","#D62728"],
            title="Qtd por Status",
            template=None,
            hover_data=["Quantidade"],
        )
        fig6.update_traces(
            textinfo="none", 
            pull=[0.05]*len(cont),
            marker=dict(line=dict(color="#FFFFFF", width=2)),
            hovertemplate="<b>%{label}</b><br>%{customdata[0]} chamados<extra></extra>"
        )

        # 3) Anotação central com total
        fig6.add_annotation(
            text=f"<b>Total<br>{total}</b>",
            showarrow=False,
            font=dict(size=14, color="#FFFFFF"),
            x=0.5, y=0.5,
            xref="paper", yref="paper"
        )

        # 4) Layout moderno: fundo transparente, legenda embaixo
        fig6.update_layout(
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            legend=dict(
                orientation="h",
                y=-0.15,
                x=0.5,
                xanchor="center",
                font=dict(size=12, color="#FFFFFF")
            ),
            margin=dict(l=20, r=20, t=50, b=80)
        )

        return fig6

    # ------------------------------------------------------------------
    # N) Qtd por Status  (dashboard-graph-7)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-7", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_qtd_status(json_data,
                        selected_regions,
                        selected_empreendimentos,
                        selected_macros,
                        selected_tickets,
                        selected_actions,
                        selected_tipo_origem,
                        selected_origem,
                        selected_users,
                        refresh_clicks):
        if not json_data:
            return {}

        # 1) DataFrame e filtros
        df = pd.read_json(StringIO(json_data), orient="split")
        col = _user_col(df)
        if selected_regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(selected_regions)]
        if selected_empreendimentos:
            df = df[df["Empreendimento"].isin(selected_empreendimentos)]
        if selected_macros:
            df = df[df["TITULO1"].isin(selected_macros)]
        if selected_tickets:
            df = df[df["TIPO TICKET"].isin(selected_tickets)]
        if selected_actions:
            df = df[df["TIPO AÇÃO"].isin(selected_actions)]
        if selected_tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(selected_tipo_origem)]
        if selected_origem:
            df = df[df["ORIGEM"].isin(selected_origem)]
        if selected_users:
            df = df[df[col].isin(selected_users)]

        # 2) Contagem por status
        cont = df["Chamados atendidos dentro do SLA"].value_counts().reset_index()
        cont.columns = ["Status", "Quantidade"]

        # 3) Monta o bar
        fig7 = px.bar(
            cont,
            x="Status",
            y="Quantidade",
            orientation="v",
            text="Quantidade",
            title="SLA 1º Atendimento (48h)",
            color_discrete_sequence=["#FFA726"],  
            template=None,
        )
        fig7.update_traces(
            width=0.6,
            textposition="outside",
            cliponaxis=False
        )

        # 4) Layout Dark
        fig7.update_layout(
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            autosize=True,
            margin=dict(l=40, r=20, t=50, b=80),
            xaxis_title="",
            yaxis_title=""
        )
        fig7.update_xaxes(
            tickfont=dict(size=12, color="#FFFFFF"),
            tickangle=-45,
            gridcolor="rgba(255,255,255,0.1)"
        )
        fig7.update_yaxes(
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)"
        )

        return fig7

    # ------------------------------------------------------------------
    # O) SLA Finalização do Atendimento (72h) ← gráfico-8
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-8", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_sla_finalizacao(json_data,
                            selected_regions,
                            selected_empreendimentos,
                            selected_macros,
                            selected_tickets,
                            selected_actions,
                            selected_tipo_origem,
                            selected_origem,
                            selected_users,
                            refresh_clicks):
        if not json_data:
            return {}
        # 1) Carrega e aplica filtros
        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)
        if selected_regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(selected_regions)]
        if selected_empreendimentos:
            df = df[df["Empreendimento"].isin(selected_empreendimentos)]
        if selected_macros:
            df = df[df["TITULO1"].isin(selected_macros)]
        if selected_tickets:
            df = df[df["TIPO TICKET"].isin(selected_tickets)]
        if selected_actions:
            df = df[df["TIPO AÇÃO"].isin(selected_actions)]
        if selected_tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(selected_tipo_origem)]
        if selected_origem:
            df = df[df["ORIGEM"].isin(selected_origem)]
        if selected_users:
            df = df[df[col_user].isin(selected_users)]

        # 2) Contagem por SLA de finalização
        cont = df["Chamados sem interação há 72h"].value_counts().reset_index()
        cont.columns = ["Status", "Quantidade"]

        # 3) Monta o gráfico de barras
        fig8 = px.bar(
            cont,
            x="Status",
            y="Quantidade",
            orientation="v",
            text="Quantidade",
            title="SLA Finalização do Atendimento (72h)",
            color_discrete_sequence=["#FFA726"],
            template=None,
        )
        fig8.update_traces(
            width=0.6,
            textposition="outside",
            cliponaxis=False
        )

        # 4) Layout Dark, mesmo look dos anteriores
        fig8.update_layout(
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            autosize=True,
            margin=dict(l=40, r=20, t=50, b=80),
            xaxis_title="",  
            yaxis_title=""   
        )
        fig8.update_xaxes(
            tickfont=dict(size=12, color="#FFFFFF"),
            tickangle=-45,
            gridcolor="rgba(255,255,255,0.1)"
        )
        fig8.update_yaxes(
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)"
        )

        return fig8


    # ------------------------------------------------------------------
    # P) Top 5 – Assuntos Mais Demandados (dashboard-graph-9)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-9", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_top5_assuntos(json_data,
                            selected_regions,
                            selected_empreendimentos,
                            selected_macros,
                            selected_tickets,
                            selected_actions,
                            selected_tipo_origem,
                            selected_origem,
                            selected_users,
                            refresh_clicks):
        if not json_data:
            return {}

        # 1) DataFrame + filtros
        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)
        if selected_regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(selected_regions)]
        if selected_empreendimentos:
            df = df[df["Empreendimento"].isin(selected_empreendimentos)]
        if selected_macros:
            df = df[df["TITULO1"].isin(selected_macros)]
        if selected_tickets:
            df = df[df["TIPO TICKET"].isin(selected_tickets)]
        if selected_actions:
            df = df[df["TIPO AÇÃO"].isin(selected_actions)]
        if selected_tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(selected_tipo_origem)]
        if selected_origem:
            df = df[df["ORIGEM"].isin(selected_origem)]
        if selected_users:
            df = df[df[col_user].isin(selected_users)]

        # 2) Top 5 TITULO3
        top5 = (
            df["TITULO3"]
            .value_counts()
            .head(5)
            .reset_index()
        )
        top5.columns = ["Titulo", "Quantidade"]

        # 3) Gráfico de barras
        fig9 = px.bar(
            top5,
            x="Titulo",
            y="Quantidade",
            orientation="v",
            text="Quantidade",
            title="Top 5: assuntos mais demandados",
            color_discrete_sequence=["#FFA726"],
            template=None,
        )
        fig9.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        # 4) Layout dark e estilo uniforme
        fig9.update_layout(
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            autosize=True,
            margin=dict(l=40, r=20, t=50, b=80),
            xaxis_title="", yaxis_title=""
        )
        fig9.update_xaxes(
            tickangle=-45,
            tickfont=dict(size=10, color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)"
        )
        fig9.update_yaxes(
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)"
        )

        return fig9
    
    # ------------------------------------------------------------------
    # Q) Ação × Tipo Origem   (dashboard‑graph‑10)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-10", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",        "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",         "value"),
        Input("dash-ticket-checklist",        "value"),
        Input("dash-action-checklist",        "value"),
        Input("dash-tipo-origem-checklist",   "value"),
        Input("dash-origem-checklist",        "value"),
        Input("dash-user-checklist",          "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_acao_tipo_origem(json_data,
                                selected_regions,
                                selected_empreendimentos,
                                selected_macros,
                                selected_tickets,
                                selected_actions,
                                selected_tipo_origem,
                                selected_origem,
                                selected_users,
                                refresh_clicks):
        if not json_data:
            return {}

        # 1) DataFrame + filtros
        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)

        if selected_regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(selected_regions)]
        if selected_empreendimentos:
            df = df[df["Empreendimento"].isin(selected_empreendimentos)]
        if selected_macros:
            df = df[df["TITULO1"].isin(selected_macros)]
        if selected_tickets:
            df = df[df["TIPO TICKET"].isin(selected_tickets)]
        if selected_actions:
            df = df[df["TIPO AÇÃO"].isin(selected_actions)]
        if selected_tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(selected_tipo_origem)]
        if selected_origem:
            df = df[df["ORIGEM"].isin(selected_origem)]
        if selected_users:
            df = df[df[col_user].isin(selected_users)]

        # 2) Contagem por TIPO AÇÃO × TIPO ORIGEM
        pivot = (
            df.pivot_table(index="TIPO AÇÃO",
                        columns="TIPO ORIGEM",
                        values="Nº Ticket",
                        aggfunc="count",
                        fill_value=0)
            .reset_index()
        )
        melted = pivot.melt(id_vars="TIPO AÇÃO",
                            var_name="Tipo Origem",
                            value_name="Quantidade")

        # 3) Barra empilhada
        fig10 = px.bar(
            melted,
            x="TIPO AÇÃO",
            y="Quantidade",
            color="Tipo Origem",
            text="Quantidade",
            title="Ação × Origem",
            color_discrete_map={
                "Interna": "#FFD54F",
                "Externa": "#8B4513",
            },
        )
        fig10.update_traces(
            width=0.4,
            textposition="outside",
            cliponaxis=False,
        )

        # 4) Layout dark padronizado
        fig10.update_layout(
            title_x=0.5,
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF", size=10),
            autosize=True,
            margin=dict(l=40, r=20, t=50, b=80),
            xaxis_title="", yaxis_title="",
        )
        fig10.update_xaxes(
            tickfont=dict(size=9, color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )
        fig10.update_yaxes(
            tickfont=dict(size=9, color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )

        return fig10


    # ------------------------------------------------------------------
    # R) Métricas dos mini-cards do Gráfico 10
    # ------------------------------------------------------------------
    @app.callback(
        Output("avg-primeira-tratativa", "children"),
        Output("avg-prazo-total",        "children"),
        Input("filtered-data", "data"),
    )
    def update_mini_cards(json_data):
        if not json_data:
            return "", ""

        df = pd.read_json(StringIO(json_data), orient="split")

        media_inicio = df["Primeira Tratativa (dias)"].mean()
        media_total  = df["Prazo Total do Chamado (dias)"].mean()

        m1 = f"{media_inicio:.1f}" if pd.notnull(media_inicio) else ""
        m2 = f"{media_total:.1f}"  if pd.notnull(media_total)  else ""

        return m1, m2


    # ------------------------------------------------------------------
    # P) Micro Assunto  (dashboard‑graph‑11)
    # ------------------------------------------------------------------
    @app.callback(
        Output("dashboard-graph-11", "figure"),
        Input("filtered-data",                "data"),
        Input("dash-region-checklist",       "value"),
        Input("dash-empreendimento-checklist","value"),
        Input("dash-macro-checklist",        "value"),
        Input("dash-ticket-checklist",       "value"),
        Input("dash-action-checklist",       "value"),
        Input("dash-tipo-origem-checklist",  "value"),
        Input("dash-origem-checklist",       "value"),
        Input("dash-user-checklist",         "value"),
        Input("refresh-button",              "n_clicks"),
    )
    def update_micro_assunto(json_data,
                            regions, empre, macros, tickets,
                            actions, tipo_origem, origem, users, refresh_clicks):
        if not json_data:
            return {}

        # 1) DataFrame + filtros
        df = pd.read_json(StringIO(json_data), orient="split")
        col_user = _user_col(df)
        if regions:
            df = df[df["Empreendimento"].map(REGION_MAPPING).isin(regions)]
        if empre:
            df = df[df["Empreendimento"].isin(empre)]
        if macros:
            df = df[df["TITULO1"].isin(macros)]
        if tickets:
            df = df[df["TIPO TICKET"].isin(tickets)]
        if actions:
            df = df[df["TIPO AÇÃO"].isin(actions)]
        if tipo_origem:
            df = df[df["TIPO ORIGEM"].isin(tipo_origem)]
        if origem:
            df = df[df["ORIGEM"].isin(origem)]
        if users:
            df = df[df[col_user].isin(users)]

        # 2) Contagem de micro‑assunto (TITULO3)
        cont = (df["TITULO3"]
                .value_counts()
                .rename_axis("Micro Assunto")
                .reset_index(name="Quantidade")
                .sort_values("Quantidade", ascending=False))

        # 3) Barra vertical com rótulos
        fig11 = px.bar(
            cont,
            x="Micro Assunto", y="Quantidade",
            text="Quantidade",
            title="Micro Assunto",
            color_discrete_sequence=["#FFA726"],
            template=None,
        )
        fig11.update_traces(
            textposition="outside",
            width=0.9,
            cliponaxis=False
        )

        # 4) Layout – rótulos inclinados, fundo dark
        fig11.update_layout(
            autosize=True,               
            height=None,                
            bargap=0.02,                 
            margin=dict(l=40, r=20, t=20, b=90),  
            title_x=0.5,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            xaxis_title="", yaxis_title="",
            yaxis_type="log",      
        )
        fig11.update_xaxes(
            tickangle=-65,
            tickfont=dict(
                family="Montserrat, sans-serif",
                size=11,               
                color="#FFFFFF"
            ),
            gridcolor="rgba(255,255,255,0.1)",
        )

        fig11.update_yaxes(
            tickfont=dict(color="#FFFFFF"),
            gridcolor="rgba(255,255,255,0.1)",
        )

        return fig11

    # ------------------------------------------------------------------
    # Z) Limpar todos os checklists
    # ------------------------------------------------------------------
    @app.callback(
        Output("dash-region-checklist",        "value"),
        Output("dash-empreendimento-checklist","value"),
        Output("dash-macro-checklist",         "value"),
        Output("dash-ticket-checklist",        "value"),
        Output("dash-action-checklist",        "value"),
        Output("dash-tipo-origem-checklist",   "value"),
        Output("dash-origem-checklist",        "value"),
        Output("dash-user-checklist",          "value"),
        Input("clear-filters", "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_all_filters(_):
        return [], [], [], [], [], [], [], []
 


    # Callback que abre/fecha filtro 
    @app.callback(
        Output("filter-body", "is_open"),         
        Input("filter-toggle", "n_clicks"),
        State("filter-body", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_filter_body(n_clicks, is_open):
        return not is_open





