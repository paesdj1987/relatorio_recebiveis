# dashboard.py
from dash import html, dcc
import dash_bootstrap_components as dbc

# -----------------------------
# Constantes e opções fixas
# -----------------------------
REGION_OPTIONS = [
    {"label": "Bahia",      "value": "Bahia"},
    {"label": "Pernambuco", "value": "Pernambuco"},
    {"label": "Sudeste",    "value": "Sudeste"},
]

DROPDOWN_STYLE = {
    "width":      "100%",
    "maxWidth":   "240px",
    "fontSize":   "0.9rem",
    "color":      "#DDDDDD",
    "backgroundColor": "#2b2b2b",
    "border":     "1px solid #444",
    "borderRadius":"6px",
}

# -----------------------------
# Layout do Dashboard
# -----------------------------

def create_dashboard_layout():
    """Layout com filtros recolhíveis e dois gráficos responsivos."""

    # ── 1) Cabeçalho fixo do card de filtros ───────────────────────
    filter_header = html.Div(
        [
            html.Span(
                "☰",               
                id="filter-toggle", 
                style={
                    "cursor": "pointer",
                    "fontSize": "1.2rem",
                    "marginRight": "6px",
                    "display": "inline-block",
                },
            ),
            html.Span("Filtros - Dashboard CRM"),
        ],
        style={"color": "#FFA726", "fontWeight": "bold", "fontSize": "1.1rem"},
    )

    # ── 2) Corpo do card (dropdowns) – será recolhido ─────────────
    filter_body = dbc.Row(
        className="gx-3 gy-2",
        children=[
            # Regionais
            dbc.Col(
                dbc.DropdownMenu(
                    label="Regionais",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-region-checklist",
                            options=REGION_OPTIONS,
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
            # Empreendimentos
            dbc.Col(
                dbc.DropdownMenu(
                    label="Empreendimentos",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-empreendimento-checklist",
                            options=[],
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
            # Usuários
            dbc.Col(
                dbc.DropdownMenu(
                    label="Usuários",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-user-checklist",
                            options=[],
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
            # Macro Assuntos
            dbc.Col(
                dbc.DropdownMenu(
                    label="Macro Assuntos",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-macro-checklist",
                            options=[],
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
            # Origem
            dbc.Col(
                dbc.DropdownMenu(
                    label="Origem",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-origem-checklist",
                            options=[],
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
            # Tipo Tickets
            dbc.Col(
                dbc.DropdownMenu(
                    label="Tipo Tickets",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-ticket-checklist",
                            options=[],
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
            # Tipo Ação
            dbc.Col(
                dbc.DropdownMenu(
                    label="Tipo Ação",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-action-checklist",
                            options=[],
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
            # Tipo Origem
            dbc.Col(
                dbc.DropdownMenu(
                    label="Tipo Origem",
                    color="secondary",
                    className="text-start",
                    toggle_style=DROPDOWN_STYLE,
                    children=[
                        dbc.Checklist(
                            id="dash-tipo-origem-checklist",
                            options=[],
                            value=[],
                            inline=False,
                            switch=False,
                            input_checked_style={"backgroundColor": "#FFA726"},
                            label_checked_style={"color": "#FFA726"},
                            label_style={"fontSize": "13px"},
                        )
                    ],
                    direction="down",
                ),
                xs=12, sm=6, md=4, lg=3,
            ),
        ],
    )

    # ── 3) Collapse envolvendo o corpo dos filtros ────────────
    filter_collapse = dbc.Collapse(
        filter_body,
        id="filter-body",
        is_open=True,
        style={"marginTop": "10px"}
    )

    # ── 3‑b) Linha de botões abaixo dos dropdowns (centralizada) ─────
    filter_buttons = dbc.Row(
        className="gy-2 justify-content-center",     
        style={"marginTop": "20px"},
        children=[
            # Voltar para Página Inicial
            dbc.Col(
                dcc.Link(
                    dbc.Button(
                        "Voltar para Página Inicial",
                        color="primary",             
                        outline=True,
                        size="md",
                        style={"width": "100%", "fontSize": "0.8rem"},
                    ),
                    href="/",
                    refresh=False,
                ),
                xs=10, sm=5, md=3, lg=2,             
                className="d-grid",                  
            ),
            # Atualizar gráficos
            dbc.Col(
                dbc.Button(
                    "Atualizar Gráficos",
                    id="refresh-button",
                    n_clicks=0,
                    color="success",  
                    outline=True,
                    size="md",
                    style={"width": "100%", "fontSize": "0.8rem"},
                ),
                xs=10, sm=5, md=3, lg=2,
                className="d-grid",
            ),
            # Limpar filtros
            dbc.Col(
                dbc.Button(
                    "Limpar Filtros",
                    id="clear-filters",
                    n_clicks=0,
                    color="warning",                  
                    outline=True,
                    size="md",
                    style={"width": "100%", "fontSize": "0.8rem"},
                ),
                xs=10, sm=5, md=3, lg=2,
                className="d-grid",
            ),            
        ],
    )


    # ── 4) Card completo ──────────────────────────────────────
    filter_card = dbc.Card(
        className="shadow-lg",
        style={
            "background": "linear-gradient(145deg, #232E3C 0%, #232E3C 100%)",
            "padding": "20px",
            "borderRadius": "12px",
            "marginTop": "10px",
            "marginBottom": "20px",
        },
        children=[
            filter_header,
            filter_collapse,
            filter_buttons,    
        ],
    )

    #---------------------
    # Parte dos Gráficos
    #---------------------

    # ---------- Card Gráfico 1 ----------
    graph1_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor": "rgba(255,255,255,0.08)",
            "border":          "1px solid rgba(255,255,255,0.15)",
            "borderRadius":    "12px",
        },
        children=[
            dcc.Loading(
                dcc.Graph(
                    id="dashboard-graph-1",
                    figure={}, 
                    style={"width": "100%", "height": "100%"},
                    config={
                        "displayModeBar": "hover",         
                        "modeBarButtons": [["toImage"]],   
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": "grafico_1",
                            "height": 600,    
                            "width": 800,     
                            "scale": 1
                        },
                        "responsive": True
                    },
                    className="graph",
                ),
                type="circle",
                color="#FFA726",
            ),
            dbc.Tooltip("Passe o mouse para ampliar.", target="dashboard-graph-1"),
        ],
    )

    # ---------- Card Gráfico 2 ----------
    graph2_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor":"rgba(255,255,255,0.08)",
            "border":         "1px solid rgba(255,255,255,0.15)",
            "borderRadius":   "12px",
        },
        children=[
            dcc.Loading(
                dcc.Graph(
                    id="dashboard-graph-2",
                    figure={},  
                    style={"width": "100%", "height": "100%"},
                    config={
                        "displayModeBar": "hover",         
                        "modeBarButtons": [["toImage"]],   
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": "grafico_2",
                            "height": 600,    
                            "width": 800,     
                            "scale": 1
                        },
                        "responsive": True
                    },
                    className="graph",
                ),
                type="circle",
                color="#FFA726",
            ),
            dbc.Tooltip(
                "Use o slider para navegar pelas datas.",
                target="dashboard-graph-2"
            ),
        ],
    )

    # ---------- Card Gráfico 3: Chamados por Mês ----------
    graph3_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor": "rgba(255,255,255,0.08)",
            "border":          "1px solid rgba(255,255,255,0.15)",
            "borderRadius":    "12px",
        },
        children=[
            dcc.Loading(
                dcc.Graph(
                    id="dashboard-graph-3",
                    figure={},  
                    style={"width": "100%", "height": "100%"},
                    config={
                        "displayModeBar": "hover",         
                        "modeBarButtons": [["toImage"]],   
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": "chamados_por_mes",
                            "height": 600,    
                            "width": 800,     
                            "scale": 1
                        },
                        "responsive": True
                    },
                    className="graph",
                ),
                type="circle",
                color="#FFA726"
            ),
            dbc.Tooltip(
                "Quantidade de chamados por mês.",
                target="dashboard-graph-3"
            ),
        ],
    )

    # ---------- Card Gráfico 4: Qtd por Empreendimento ----------
    graph4_card = dbc.Card(
        className="shadow-lg graph-container graph-4-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor": "rgba(255,255,255,0.08)",
            "border":          "1px solid rgba(255,255,255,0.15)",
            "borderRadius":    "12px",
        },
        children=[
            html.Div(
                style={
                    "height": "360px",      
                    "overflowY": "auto",    
                    "paddingRight": "8px"
                },
                children=[
                    dcc.Loading(
                        dcc.Graph(
                            id="dashboard-graph-4",
                            figure={},            
                            style={"width": "100%"},  
                            config={
                                "displayModeBar": "hover",        
                                "modeBarButtons": [["toImage"]],  
                                "toImageButtonOptions": {
                                    "format": "png",
                                    "filename": "qtd_por_empreendimento",
                                    "height": 360,   
                                    "width": 600,   
                                    "scale": 1
                                },
                                "responsive": True
                            },
                        ),
                        type="circle",
                        color="#FFA726",
                    )
                ]
            ),
            dbc.Tooltip("Qtd por Empreendimento", target="dashboard-graph-4"),
        ],
    )

    # ---------- Card Gráfico 5: Qtd por Origem ----------
    graph5_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor": "rgba(255,255,255,0.08)",
            "border":          "1px solid rgba(255,255,255,0.15)",
            "borderRadius":    "12px",
        },
        children=[
            dcc.Loading(
                dcc.Graph(
                    id="dashboard-graph-5",
                    figure={},  
                    style={"width": "100%", "height": "100%"},
                    config={
                        "displayModeBar": "hover",         
                        "modeBarButtons": [["toImage"]],   
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": "qtd_por_origem",
                            "height": 600,   
                            "width": 800,     
                            "scale": 1
                        },
                        "responsive": True
                    },
                    className="graph",
                ),
                type="circle",
                color="#FFA726",
            ),
            dbc.Tooltip("Quantidades por Origem", target="dashboard-graph-5"),
        ],
    )

    # ---------- Card Gráfico 6: Qtd por Status ----------
    graph6_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor": "rgba(255,255,255,0.08)",
            "border":          "1px solid rgba(255,255,255,0.15)",
            "borderRadius":    "12px",
        },
        children=[
            dcc.Loading(
                dcc.Graph(
                    id="dashboard-graph-6",
                    figure={},  
                    style={"width": "100%", "height": "100%"},
                    config={
                        "displayModeBar": "hover",          
                        "modeBarButtons": [["toImage"]],    
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": "qtd_por_status_6",
                            "height": 600,    
                            "width": 800,     
                            "scale": 1
                        },
                        "responsive": True
                    },
                    className="graph",
                ),
                type="circle",
                color="#FFA726"
            ),
            dbc.Tooltip("Qtd por Status", target="dashboard-graph-6"),
        ],
    )

    # ---------- Card Gráfico 7: Qtd por Status ----------
    graph7_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor": "rgba(255,255,255,0.08)",
            "border":          "1px solid rgba(255,255,255,0.15)",
            "borderRadius":    "12px",
        },
        children=[
            html.Div(
                dcc.Loading(
                    dcc.Graph(
                        id="dashboard-graph-7",
                        figure={},  
                        style={"width": "100%", "height": "100%"},
                        config={
                            "displayModeBar": "hover",         
                            "modeBarButtons": [["toImage"]],   
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "qtd_por_status",
                                "height": 360,    
                                "width": 600,     
                                "scale": 1
                            },
                            "responsive": True
                        },
                        className="graph"
                    ),
                    type="circle",
                    color="#FFA726"
                ),
                style={"height": "360px"}
            ),
            dbc.Tooltip("Qtd por Status", target="dashboard-graph-7"),
        ],
    )


    # ---------- Card Gráfico 8: SLA Finalização do Atendimento (72h) ----------
    graph8_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor":"rgba(255,255,255,0.08)",
            "border":         "1px solid rgba(255,255,255,0.15)",
            "borderRadius":   "12px",
        },
        children=[
            html.Div(
                dcc.Loading(
                    dcc.Graph(
                        id="dashboard-graph-8",
                        figure={},  
                        style={"width": "100%", "height": "100%"},
                        config={
                            "displayModeBar": "hover",        
                            "modeBarButtons": [["toImage"]],  
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "sla_finalizacao_72h",
                                "height": 360,   
                                "width": 600,    
                                "scale": 1
                            },
                            "responsive": True
                        },
                        className="graph"
                    ),
                    type="circle",
                    color="#FFA726"
                ),
                style={"height": "360px"}
            ),
            dbc.Tooltip(
                "SLA Finalização do Atendimento (72h)",
                target="dashboard-graph-8"
            ),
        ],
    )


    # ---------- Card Gráfico 9: Top 5 – Assuntos Mais Demandados ----------
    graph9_card = dbc.Card(
        className="shadow-lg graph-container",
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor": "rgba(255,255,255,0.08)",
            "border":          "1px solid rgba(255,255,255,0.15)",
            "borderRadius":    "12px",
        },
        children=[
            html.Div(
                dcc.Loading(
                    dcc.Graph(
                        id="dashboard-graph-9",
                        figure={},  
                        style={"width": "100%", "height": "100%"},
                        config={
                            "displayModeBar": "hover",        
                            "modeBarButtons": [["toImage"]],  
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "top5_assuntos",   
                                "height": 360,                 
                                "width": 600,                  
                                "scale": 1
                            },
                            "responsive": True
                        },
                        className="graph"
                    ),
                    type="circle", color="#FFA726"
                ),
                style={"height": "360px"}
            ),
            dbc.Tooltip("Top 5 – assuntos mais demandados", target="dashboard-graph-9"),
        ],
    )


    # ---------- Card Gráfico 10: Ação e Origem + Métricas ----------
    graph10_card = dbc.Card(
        id="graph10-card",
        className="shadow-lg graph-container",        
        style={
            "backdropFilter":  "blur(6px)",
            "backgroundColor":"rgba(255,255,255,0.08)",
            "border":         "1px solid rgba(255,255,255,0.15)",
            "borderRadius":   "12px",
            "padding":        "10px",
        },
        children=[
            dbc.Row(
                [
                    # ── Gráfico 10 ──
                    dbc.Col(
                        dcc.Loading(
                            dcc.Graph(
                                id="dashboard-graph-10",
                                figure={},  
                                style={"width": "100%", "height": "100%"},
                                config={
                                    "displayModeBar": "hover",        
                                    "modeBarButtons": [["toImage"]], 
                                    "toImageButtonOptions": {
                                        "format": "png",
                                        "filename": "acao_origem",
                                        "height": 600,
                                        "width": 800,
                                        "scale": 1
                                    },
                                    "responsive": True
                                },
                            ),
                            type="circle",
                            color="#FFA726",
                        ),
                        xs=12, sm=12, md=7, lg=8,
                        className="h-100",
                    ),

                    # ── Mini‑Cards das Métricas ──
                    dbc.Col(
                        [
                            # 1ª linha de mini‑cards
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                html.H6(
                                                    "Média Início do Atendimento",
                                                    className="mb-1",
                                                    style={"fontSize": "0.6rem"},
                                                ),
                                                html.H4(
                                                    id="avg-primeira-tratativa",
                                                    className="mt-1",
                                                    style={"fontSize": "0.9rem", "fontWeight": "bold"},
                                                ),
                                            ],
                                            body=True,
                                            color="secondary",
                                            inverse=True,
                                            className="p-1 mini-equal",   
                                            style={"height": "100%"},
                                        ),
                                        xs=6,
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                html.H6(
                                                    "Média Total do Atendimento",
                                                    className="mb-1",
                                                    style={"fontSize": "0.6rem"},
                                                ),
                                                html.H4(
                                                    id="avg-prazo-total",
                                                    className="mt-1",
                                                    style={"fontSize": "0.9rem", "fontWeight": "bold"},
                                                ),
                                            ],
                                            body=True,
                                            color="light",
                                            inverse=True,
                                            className="p-1 mini-equal",   
                                            style={"height": "100%"},
                                        ),
                                        xs=6,
                                    ),
                                ],
                                className="mb-2",
                            ),

                            # 2ª linha de mini‑cards (Metas)
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                html.H6(
                                                    "Meta (dias)",
                                                    className="mb-1",
                                                    style={"fontSize": "0.6rem"},
                                                ),
                                                html.H4(
                                                    "2",
                                                    className="mt-1",
                                                    style={"fontSize": "0.9rem", "fontWeight": "bold"},
                                                ),
                                            ],
                                            body=True,
                                            color="secondary",
                                            inverse=False,
                                            className="p-1 mini-equal",   
                                            style={"height": "100%"},
                                        ),
                                        xs=6,
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                html.H6(
                                                    "Meta (dias)",
                                                    className="mb-1",
                                                    style={"fontSize": "0.6rem"},
                                                ),
                                                html.H4(
                                                    "3",
                                                    className="mt-1",
                                                    style={"fontSize": "0.9rem", "fontWeight": "bold"},
                                                ),
                                            ],
                                            body=True,
                                            color="light",
                                            inverse=False,
                                            className="p-1 mini-equal",  
                                            style={"height": "100%"},
                                        ),
                                        xs=6,
                                    ),
                                ]
                            ),
                        ],
                        xs=12, md=5, lg=4,                                 
                        className="h-100",
                    ),
                ],
                className="gx-3 gy-3 align-items-stretch",                   
                style={"height": "100%"},
            ),
            dbc.Tooltip("Ação × Origem (empilhado)", target="dashboard-graph-10"),
        ],
    )

    # ---------- Card Gráfico 11: Micro Assunto ----------
    graph11_card = dbc.Card(
    id="graph11-card",
    className="shadow-lg graph-container graph11-responsive",
    style={
        "width":       "98%",
        "maxWidth":    "1400px",
        "margin":      "0 auto",
        "backdropFilter": "blur(6px)",
        "backgroundColor":"rgba(255,255,255,0.08)",
        "border":      "1px solid rgba(255,255,255,0.15)",
        "borderRadius":"12px",
        "padding":     "10px",
        "height":     "50vh",
        "minHeight":  "460px",
        "maxHeight":  "860px"
    },
    children=[
        dcc.Loading(
            id="loading-graph11",
            type="circle",
            color="#FFA726",
            style={"height": "100%"},       
            children=dcc.Graph(
                id="dashboard-graph-11",
                figure={},
                style={"width": "100%", "height": "100%"},  
                config={
                    "displayModeBar": "hover",
                    "modeBarButtons": [["toImage"]],
                    "toImageButtonOptions": {
                        "format": "png",
                        "filename": "micro_assunto",
                        "height": 600,
                        "width": 800,
                        "scale": 1
                    },
                    "responsive": True
                },
            ),
        ),
        dbc.Tooltip(
            "Contagem de micro‑assuntos (TITULO3)",
            target="dashboard-graph-11"
        ),
    ],
)

    
    # monta as duas colunas
    left_col = dbc.Col(
        [
            graph1_card,
            html.Div(style={"marginTop": "20px"}),
            graph3_card,
            html.Div(style={"marginTop": "20px"}),
            graph5_card,
            html.Div(style={"marginTop": "20px"}),
            graph7_card,
            html.Div(style={"marginTop": "20px"}),
            graph9_card,
        ],
        xs=12, md=6,
    )
    right_col = dbc.Col(
        [
            graph2_card,
            html.Div(style={"marginTop": "20px"}),
            graph4_card,
            html.Div(style={"marginTop": "20px"}),
            graph6_card,
            html.Div(style={"marginTop": "20px"}),
            graph8_card,
            html.Div(style={"marginTop": "20px"}),
            graph10_card,
        ],
        xs=12, md=6,
    )

    # Linha 1
    graph_row = dbc.Row(
        [left_col, right_col],
        className="gx-4 gy-4 justify-content-center"
    )

    # Linha 2
    graph11_row = dbc.Row(
        dbc.Col(graph11_card, xs=12),
        className="gx-4 gy-4 justify-content-center"
    )

    # ---------- Container principal ----------
    return dbc.Container(
        fluid=True,
        style={"padding": "20px"},
        children=[
            filter_card,
            graph_row,
            html.Div(style={"marginTop": "20px"}),  
            graph11_row,                            
        ],
    )


