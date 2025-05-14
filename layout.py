#layout.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def create_layout(app):
    return dbc.Container(
        fluid=True,
        id="layout-container",      
        children=[
            # Cabeçalho com título e logo
            dbc.Container(
                fluid=True,
                className="header-container",
                style={
                    "position": "relative",
                    "background": "linear-gradient(135deg, #283E51 0%, #4B79A1 100%)",
                    "padding": "50px 15px",
                    "borderBottom": "3px solid #FFA80B",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                    "borderBottomLeftRadius": "12px",
                    "borderBottomRightRadius": "12px"
            },
            children=[
                dbc.Row(
                    align="center",
                    justify="between",
                    children=[
                        # Título à esquerda
                        dbc.Col(
                            html.H1(
                                "CRM Junix",
                                className="h2 text-white mb-0",
                                style={
                                    "fontWeight": "700",
                                    "fontSize": "45px",
                                    "margin": "0"
                                }
                            ),
                            width="auto"
                        ),
                        # Logo à direita
                        dbc.Col(
                            html.Img(
                                src=app.get_asset_url("logoOR.png"),
                                height="70px"
                            ),
                            width="auto"
                        )
                    ]
                )
            ]
        ),

            # Container para o primeiro card (Upload de Planilhas)
            dbc.Container(
                fluid=True,
                style={"marginTop": "10px","backgroundColor": "#FFFFFF"},
                children=[
                    dbc.Row(
                        justify="center",
                        children=[
                            dbc.Col(
                                xs=15, sm=15, md=15, lg=12, xl=12,
                                children=dbc.Card(
                                    className="mt-5 shadow-lg",
                                    style={"height": "auto", "backgroundColor": "#F2F2F2"},
                                    children=dbc.CardBody(
                                        [
                                            html.H4(
                                                "Upload e Filtro de Planilhas",
                                                className="card-title",
                                                style={"textAlign": "center", "color": "#345F6C"}
                                            ),
                                            html.P(
                                                "Carregue as planilhas e confirme para gerar o relatório consolidado.",
                                                className="card-text",
                                                style={"textAlign": "center", "color": "#7F7F7F"}
                                            ),
                                            html.Hr(
                                                style={
                                                    "borderColor": "#FFA80B",
                                                    "borderWidth": "1px",
                                                    "borderStyle": "solid"
                                                }
                                            ),

                                            # Linha de itens (Uploads, Botão Confirmar, Dropdown, Gerar Relatório)
                                            dbc.Row(
                                                className="mb-3 justify-content-center",
                                                children=[
                                                    # Coluna para Upload 1
                                                    dbc.Col(
                                                        xs=12, sm=6, md=2,
                                                        style={"textAlign": "center"},  
                                                        children=[
                                                            dbc.Label(
                                                                "Relatório Tickets",
                                                                style={
                                                                    "textAlign": "center",
                                                                    "display": "block",
                                                                    "marginTop": "10px",
                                                                    "color": "#345F6C",
                                                                    "fontSize": "0.85rem"  
                                                                }
                                                            ),
                                                            dcc.Upload(
                                                                id="upload-1",
                                                                children=dbc.Button(
                                                                    "Upload 1",
                                                                    color="primary",
                                                                    size="sm",
                                                                    style={
                                                                        "width": "80%",           
                                                                        "marginLeft": "auto",     
                                                                        "marginRight": "auto",
                                                                        "height": "40px",
                                                                        "display": "block",
                                                                        "marginTop": "5px",
                                                                        "color": "white",
                                                                        "fontSize": "0.8rem"
                                                                    }
                                                                ),
                                                                accept=".xlsx",
                                                                className="mb-3"
                                                            ),
                                                            html.Div(
                                                                id="upload-1-status",
                                                                style={"textAlign": "center", "color": "#345F6C"}
                                                            ),
                                                        ],
                                                    ),

                                                    # Coluna para Upload 2
                                                    dbc.Col(
                                                        xs=12, sm=6, md=2,
                                                        children=[
                                                            dbc.Label(
                                                                "Dados Gerais",
                                                                style={
                                                                    "textAlign": "center",
                                                                    "display": "block",
                                                                    "marginTop": "10px",
                                                                    "color": "#345F6C",
                                                                    "fontSize": "0.85rem"  
                                                                }
                                                            ),
                                                            dcc.Upload(
                                                                id="upload-2",
                                                                children=dbc.Button(
                                                                    "Upload 2",
                                                                    color="primary",
                                                                    size="sm",
                                                                    style={
                                                                        "width": "80%",           
                                                                        "marginLeft": "auto",     
                                                                        "marginRight": "auto",
                                                                        "height": "40px",
                                                                        "display": "block",
                                                                        "marginTop": "5px",
                                                                        "color": "white",
                                                                        "fontSize": "0.8rem"
                                                                    }
                                                                ),
                                                                accept=".xlsx",
                                                                className="mb-3"
                                                            ),
                                                            html.Div(
                                                                id="upload-2-status",
                                                                style={"textAlign": "center", "color": "#345F6C"}
                                                            ),
                                                        ],
                                                    ),

                                                    # Coluna do Botão Confirmar Uploads
                                                    dbc.Col(
                                                        xs=12, sm=6, md=2,
                                                        style={"textAlign": "center"},  
                                                        children=[
                                                            dbc.Button(
                                                                "Confirmar Uploads",
                                                                id="confirm-upload",
                                                                n_clicks=0,
                                                                size="sm",
                                                                color="success",
                                                                style={
                                                                    "width": "80%",
                                                                    "height": "40px",
                                                                    "display": "block",
                                                                    "marginTop": "38px",
                                                                    "marginLeft": "auto",
                                                                    "marginRight": "auto",
                                                                    "fontSize": "0.85rem"
                                                                },
                                                            ),

                                                            # 2) O Loading (com o texto de status) vem abaixo do botão
                                                            dcc.Loading(
                                                                id="loading-confirm-upload",
                                                                type="circle",
                                                                style={"marginTop": "15px", "display": "block"},  
                                                                children=html.Div(
                                                                    id="confirm-upload-status",
                                                                    style={
                                                                        "textAlign": "center",
                                                                        "color": "#345F6C",
                                                                        "marginTop": "20px"
                                                                    }
                                                                )
                                                            ),
                                                        ],
                                                    ),

                                                    # Coluna do Dropdown
                                                    dbc.Col(
                                                        xs=12, sm=6, md=3,
                                                        style={"textAlign": "center"},
                                                        children=[
                                                            dbc.Label(
                                                                "Empreendimento",
                                                                className="text-center",
                                                                style={
                                                                    "marginTop": "10px",
                                                                    "color": "#345F6C",
                                                                    "fontSize": "0.85rem"
                                                                }
                                                            ),
                                                            dcc.Dropdown(
                                                                id="empreendimento-dropdown",
                                                                options=[],
                                                                value=[],
                                                                placeholder="🔍 Selecione empreendimentos",
                                                                multi=True,
                                                                clearable=True,
                                                                className="p-2 rounded-pill modern-dropdown",
                                                                style={
                                                                    "width":    "100%",
                                                                    "fontSize": "0.85rem",
                                                                    "marginTop": "-2px"
                                                                }
                                                            ),
                                                        ],
                                                    ),

                                                    # Coluna do Botão Gerar Relatório
                                                    dbc.Col(
                                                        xs=12, sm=12, md=3,
                                                        style={"textAlign": "center"},
                                                        children=[
                                                            dcc.Loading(
                                                                type="circle",
                                                                children=dbc.Button(
                                                                    "Gerar Relatório",
                                                                    id="generate-report",
                                                                    n_clicks=0,
                                                                    color="secondary",
                                                                    size="sm",
                                                                    style={
                                                                        "backgroundColor": "#FFA80B",
                                                                        "borderColor": "#FFA80B",
                                                                        "width": "80%",         
                                                                        "height": "40px",
                                                                        "display": "block",
                                                                        "marginTop": "38px",    
                                                                        "marginLeft": "auto",   
                                                                        "marginRight": "auto",
                                                                        "fontSize": "0.85rem"
                                                                    }
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                ],
                                            ),

                                            # Mensagem de saída com loading
                                            dcc.Loading(
                                                type="circle",
                                                children=dbc.Row(
                                                    className="justify-content-center",
                                                    children=[
                                                        dbc.Col(
                                                            width=12,
                                                            children=html.Div(
                                                                id="output-message",
                                                                className="text-center mt-4",
                                                                style={"textAlign": "center", "color": "#345F6C"}
                                                            )
                                                        )
                                                    ],
                                                ),
                                            )
                                        ],
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
            ),


            # Container para o card de Informações Gerais
            dbc.Container(
                fluid=True,
                style={"marginTop": "10px"},
                children=[
                    dbc.Row(
                        justify="center",
                        children=[
                            dbc.Col(
                                xs=12, sm=12, md=12, lg=12, xl=12,
                                children=dbc.Card(
                                    className="mt-5 shadow-lg",
                                    style={"height": "auto", "backgroundColor": "#F2F2F2"},
                                    children=dbc.CardBody(
                                        [
                                            html.H4(
                                                "Informações Gerais",
                                                className="card-title",
                                                style={"textAlign": "center", "color": "#345F6C"}
                                            ),
                                            html.P(
                                                "Cards com as principais informações da tabela.",
                                                className="card-text",
                                                style={"textAlign": "center", "color": "#7F7F7F"}
                                            ),
                                            html.Hr(style={"borderColor": "#FFA80B", "borderWidth": "1px", "borderStyle": "solid"}),

                                            # Div com margem para espaçamento
                                            html.Div(style={"marginBottom": "30px"}),

                                            # Novo card "Total Chamados" acima das 4 colunas
                                            dbc.Row(
                                                justify="center",
                                                children=[
                                                    dbc.Col(
                                                        xs=12, sm=6, md=4, lg=3, xl=3,
                                                        children=[
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#6A5ACD", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Total Chamados",
                                                                            className="card-title",
                                                                            style={
                                                                                "fontSize": "14px",
                                                                                "color": "#FFFFFF",
                                                                                "fontWeight": "bold",
                                                                                "textAlign": "center"
                                                                            }
                                                                        ),
                                                                        html.P(
                                                                            id="total-chamados",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={
                                                                                "fontSize": "16px",
                                                                                "color": "white",
                                                                                "fontWeight": "bold",
                                                                                "textAlign": "center"
                                                                            }
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor": "#6A5ACD", "borderRadius": "10px"},
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),

                                            html.Div(style={"marginBottom": "20px"}),

                                            # Quatro colunas de cards
                                            dbc.Row(
                                                className="justify-content-center align-items-start",
                                                children=[

                                                    # Primeira Coluna de Cards (1º Atendimento)
                                                    dbc.Col(
                                                        xs=12, sm=12, md=6, lg=3, xl=3,
                                                        children=[
                                                            html.H5(
                                                                "1º Atendimento",
                                                                style={
                                                                    "textAlign": "center",
                                                                    "marginBottom": "10px",
                                                                    "fontSize": "18px",
                                                                    "fontWeight": "bold",
                                                                    "color": "#345F6C"
                                                                }
                                                            ),
                                                            # 1º Atendimento dentro do SLA
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#2E8B57", "border": "none", "boxShadow": "none", "borderRadius": "10px"},                                                  
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "1º Atendimento dentro do SLA",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-5",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#2E8B57","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                            # 1º Atendimento fora do SLA
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#556B2F", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "1º Atendimento fora do SLA",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-6",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#556B2F","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                            # Não atendido pelo portal
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#228B22", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Não atendido pelo portal",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-8",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#228B22","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                        ],
                                                    ),

                                                    # Segunda Coluna de Cards (Chamados Pendentes)
                                                    dbc.Col(
                                                        xs=12, sm=12, md=6, lg=3, xl=3,
                                                        children=[
                                                            html.H5(
                                                                "Chamados Pendentes",
                                                                style={
                                                                    "textAlign": "center",
                                                                    "marginBottom": "10px",
                                                                    "fontSize": "18px",
                                                                    "fontWeight": "bold",
                                                                    "color": "#345F6C"
                                                                }
                                                            ),
                                                            # Chamado em atraso
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#FF6347", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Chamado em atraso",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-1",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#FF6347","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                            # Chamado ainda não atendido
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#DAA520", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Chamado ainda não atendido",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-7",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#DAA520","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                            # Chamado dentro do prazo
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#CD853F", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Chamado dentro do prazo",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-2",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#CD853F","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                        ],
                                                    ),

                                                    # Terceira Coluna de Cards (Chamados Finalizados)
                                                    dbc.Col(
                                                        xs=12, sm=12, md=6, lg=3, xl=3,
                                                        children=[
                                                            html.H5(
                                                                "Chamados Finalizados",
                                                                style={
                                                                    "textAlign": "center",
                                                                    "marginBottom": "10px",
                                                                    "fontSize":"18px",
                                                                    "fontWeight":"bold",
                                                                    "color": "#345F6C"
                                                                }
                                                            ),
                                                            # Chamado finalizado dentro do SLA
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#4682B4", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Chamado finalizado dentro do SLA",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-4",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#4682B4","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                            # Chamado finalizado fora do SLA
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#1E90FF", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Chamado finalizado fora do SLA",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-3",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#1E90FF","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                        ],
                                                    ),

                                                    # Quarta Coluna de Cards (Ação Ticket)
                                                    dbc.Col(
                                                        xs=12, sm=12, md=6, lg=3, xl=3,
                                                        children=[
                                                            html.H5(
                                                                "Ação Ticket",
                                                                style={
                                                                    "textAlign": "center",
                                                                    "marginBottom": "10px",
                                                                    "fontSize": "18px",
                                                                    "fontWeight": "bold",
                                                                    "color": "#345F6C"
                                                                }
                                                            ),
                                                            # Ativa
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#8B0000", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Ativa",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-ativa",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#8B0000","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                            # Receptiva
                                                            dbc.Card(
                                                                className="mb-3 shadow-lg",
                                                                style={"width": "270px", "margin": "0 auto", "backgroundColor": "#4E3B31", "border": "none", "boxShadow": "none", "borderRadius": "10px"},
                                                                children=dbc.CardBody(
                                                                    [
                                                                        html.H6(
                                                                            "Receptiva",
                                                                            className="card-title",
                                                                            style={"fontSize":"14px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                        html.P(
                                                                            id="valor-receptiva",
                                                                            children="0",
                                                                            className="card-text",
                                                                            style={"fontSize":"16px","color":"white","fontWeight":"bold"}
                                                                        ),
                                                                    ],
                                                                    style={"backgroundColor":"#4E3B31","borderRadius":"10px"},
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
            ),
            
           html.Div(style={"marginTop": "40px"}),
 
           # Exemplo para o container do "Top 5 – Assuntos mais demandados no período"
            dbc.Container(
                id='top5-table-container',
                style={
                    "display": "none",
                    "width": "100%",
                    "margin": "0 auto",
                    "backgroundColor": "#F8F8F8",
                    "marginTop": "30px",  
                    "padding": "0"        
                },
                children=[
                    dbc.Card(
                        style={
                            "width": "100%",
                            "backgroundColor": "#F8F8F8",
                            "border": "none",     
                            "boxShadow": "none",  
                            "borderRadius": "0",  
                            "padding": "0"
                        },
                        children=dbc.CardBody(
                            style={
                                "width": "100%",
                                "backgroundColor": "#F8F8F8",
                                "border": "none",
                                "boxShadow": "none",
                                "borderRadius": "0",
                                "padding": "0"
                            },
                            children=[
                                html.H4(
                                    "Top 5 – Assuntos mais demandados no período",
                                    className="card-title",
                                    style={
                                        "textAlign": "center",
                                        "color": "#345F6C",
                                        "margin": "20px 0"  
                                    }
                                ),
                                html.Hr(style={"borderColor": "#FFA80B", "borderWidth": "1px", "borderStyle": "solid", "width": "85%", "margin": "0 auto 20px auto"}),  # Linha laranja
                                dash_table.DataTable(
                                    id='top5-table',
                                    columns=[
                                        {"name": "Titulo", "id": "Titulo"},
                                        {"name": "Quantidade", "id": "Quantidade"},
                                        {"name": "Percentual", "id": "Percentual"},
                                    ],
                                    data=[],
                                    page_size=10,
                                    style_table={
                                        'overflowX': 'auto',
                                        'width': '100%',
                                        'border': 'none',
                                        'backgroundColor': '#F8F8F8'
                                    },
                                    style_cell={
                                        'textAlign': 'left',
                                        'padding': '10px',
                                        'backgroundColor': '#F2F2F2',
                                        'color': '#345F6C',
                                        'border': '1px solid #E0E0E0',
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                    },
                                    style_header={
                                        'backgroundColor': '#345F6C',
                                        'fontWeight': 'bold',
                                        'color': '#FFFFFF',
                                        'textAlign': 'center',
                                        'borderBottom': '2px solid #2E4A5B',
                                    },
                                ),
                            ],
                        ),
                    ),
                ],
            ),

            html.Div(style={"marginTop": "40px"}),

            # Exemplo para o container da "Quantidade por Empreendimento"
            dbc.Container(
                id='aggregated-table-container',
                style={
                    "display": "none",
                    "width": "100%",
                    "margin": "0 auto",
                    "backgroundColor": "#F8F8F8",
                    "marginTop": "30px", 
                    "padding": "0"
                },
                children=[
                    dbc.Card(
                        style={
                            "width": "100%",
                            "backgroundColor": "#F8F8F8",
                            "border": "none",
                            "boxShadow": "none",
                            "borderRadius": "0",
                            "padding": "0"
                        },
                        children=dbc.CardBody(
                            style={
                                "width": "100%",
                                "backgroundColor": "#F8F8F8",
                                "border": "none",
                                "boxShadow": "none",
                                "borderRadius": "0",
                                "padding": "0"
                            },
                            children=[
                                html.H4(
                                    "Quantidade por Empreendimento",
                                    className="card-title",
                                    style={
                                        "textAlign": "center",
                                        "color": "#345F6C",
                                        "margin": "20px 0"
                                    }
                                ),
                                html.Hr(style={"borderColor": "#FFA80B", "borderWidth": "1px", "borderStyle": "solid", "width": "85%", "margin": "0 auto 20px auto"}),  # Linha laranja
                                dash_table.DataTable(
                                    id='aggregated-table',
                                    columns=[],
                                    data=[],
                                    page_size=10,
                                    style_table={
                                        'overflowX': 'auto',
                                        'width': '100%',
                                        'border': 'none',
                                        'backgroundColor': '#F8F8F8'
                                    },
                                    style_cell={
                                        'textAlign': 'left',
                                        'padding': '5px',
                                        'backgroundColor': '#F2F2F2',
                                        'color': '#345F6C',
                                        'border': '1px solid #E0E0E0',
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                    },
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'Empreendimento'}, 'width': '30%'},
                                        {'if': {'column_id': 'Quantidade'}, 'width': '15%'},
                                        {'if': {'column_id': 'Média Primeira Tratativa (horas)'}, 'width': '18%'},
                                        {'if': {'column_id': 'Média Última Tratativa (horas)'}, 'width': '18%'},
                                        {'if': {'column_id': 'Média Prazo Total do Chamado (Dias)'}, 'width': '19%'},
                                    ],
                                    style_header={
                                        'backgroundColor': '#345F6C',
                                        'fontWeight': 'bold',
                                        'color': '#F0F0F0',
                                        'borderBottom': '2px solid #2E4A5B',
                                    },
                                ),
                            ],
                        ),
                    ),
                ],
            ),

        # Tabela e botão de exportação
        dbc.Container(
            fluid=True,
            style={
                "backgroundColor": "#F8F8F8",  
                "width": "100%",
                "margin": "0 auto",
                "marginTop": "40px",  
                "border": "none",     
                "borderRadius": "0",  
                "padding": "15px",    
                "boxShadow": "none"   
            },
            children=[
                dbc.Card(
                    id="table-container",
                    className="mt-5",
                    style={
                        "display": "none",
                        "backgroundColor": "#D2D2D2",
                        "width": "100%",
                        "border": "none",       
                        "borderRadius": "0",    
                        "boxShadow": "none"     
                    },
                    children=dbc.CardBody(
                        style={
                            "width": "100%",
                            "backgroundColor": "#F8F8F8",
                            "border": "none",    
                            "boxShadow": "none", 
                            "borderRadius": "0",
                            "padding": "0"
                        },
                        children=[
                            # Título e Linha Laranja
                            html.H4(
                                "Tabela Final",
                                className="card-title",
                                style={
                                    "textAlign": "center",
                                    "color": "#345F6C",
                                    "margin": "20px 0"
                                }
                            ),
                            html.Hr(
                                style={
                                    "borderColor": "#FFA80B",
                                    "borderWidth": "1px",
                                    "borderStyle": "solid",
                                    "width": "80%",
                                    "margin": "0 auto 20px auto"  
                                }
                            ),
                            
                            # Botões: Exportar para Excel e Abrir Dashboard
                            dbc.Row(
                                className="mb-3 justify-content-center",
                                children=[
                                    dbc.Col(
                                        width="auto",
                                        children=dbc.Button(
                                            "Exportar para Excel",
                                            id="export-button",
                                            n_clicks=0,
                                            color="success",
                                            style={
                                                "backgroundColor": "#28a745",       
                                                "color": "#FFFFFF",
                                                "border": "none",
                                                "borderRadius": "50px",            
                                                "padding": "8px 20px",
                                                "fontSize": "0.9rem",
                                                "fontWeight": "bold",
                                                "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
                                                "transition": "0.3s",
                                                "width": "170px",
                                                "marginRight": "10px",
                                            },
                                            className="shadow-sm",
                                        )
                                    ),
                                    dbc.Col(
                                        width="auto",
                                        children=dcc.Link(
                                            dbc.Button(
                                                "Abrir Dashboard",
                                                id="open-dashboard",
                                                color="primary",
                                                style={
                                                    "backgroundColor": "#007bff",   
                                                    "color": "#FFFFFF",
                                                    "border": "none",
                                                    "borderRadius": "50px",
                                                    "padding": "8px 20px",
                                                    "fontSize": "0.9rem",
                                                    "fontWeight": "bold",
                                                    "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
                                                    "transition": "0.3s",
                                                    "width": "170px",
                                                },
                                                className="shadow-sm",
                                            ),
                                            href="/dashboards",
                                            refresh=False,
                                        )
                                    ),
                                ]
                            ),

                            # Tabela
                            dash_table.DataTable(
                                id="merged-table",
                                columns=[],  
                                data=[],     
                                page_size=15,
                                style_table={
                                    "overflowX": "auto",
                                    "width": "100%",
                                    "border": "none",
                                    "backgroundColor": "#D2D2D2"
                                },
                                style_cell={
                                    "textAlign": "left",
                                    "padding": "10px",
                                    "backgroundColor": "#F2F2F2",
                                    "color": "#345F6C",
                                    "border": "1px solid #E0E0E0",
                                    "whiteSpace": "normal",
                                    "height": "auto"
                                },
                                style_header={
                                    "backgroundColor": "#345F6C",
                                    "fontWeight": "bold",
                                    "color": "#F0F0F0",
                                    "textAlign": "center",
                                    "borderBottom": "1px solid #FFFFFF",
                                    "borderRight": "1px solid #FFFFFF",
                                    "border": "none"
                                },
                            ),
                        ],
                    ),
                ),

                # Toast de confirmação
                dbc.Toast(
                    id="toast-confirmacao",
                    header="Sucesso!",
                    icon="success",
                    dismissable=True,
                    is_open=False,
                    duration=4000,
                    children="Uploads confirmados com sucesso.",
                    style={
                        "position": "fixed",
                        "top": 70,
                        "right": 30,
                        "width": 350,
                        "zIndex": 1050,
                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
                    }
                ),

                # Armazenamento dos conteúdos e dados
                dcc.Store(id="stored-upload-1"),
                dcc.Store(id="stored-upload-2"),
                dcc.Store(id="merged-data"),
                dcc.Store(id="report-date"),
                dcc.Download(id="download-report"),
            ],
        )
    ],
)