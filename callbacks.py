#callbacks

import pandas as pd
from dash import Input, Output, State, callback, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from feriados import get_busdaycalendar_with_holidays
from dash.exceptions import PreventUpdate   
import io
import base64
import warnings
import numpy as np
import datetime
import time
import math

warnings.simplefilter("ignore", UserWarning)

date_columns = ["DT. INICIO ETAPA", "Data Abertura", "DT. FINALIZAÇÃO"]

# Status 
STATUS_CHAMADO_EM_ATRASO = 'Chamado em atraso'
STATUS_CHAMADO_DENTRO_DO_PRAZO = 'Chamado dentro do prazo'
STATUS_CHAMADO_FINALIZADO_FORA_DO_SLA = 'Chamado finalizado com atraso'
STATUS_CHAMADO_FINALIZADO_DENTRO_DO_SLA = 'Chamado finalizado dentro do SLA'
STATUS_CHAMADO_AINDA_NAO_ATENDIDO = 'Chamado ainda não atendido'

# --------------------------------
# Callbacks de Upload
# --------------------------------

@callback(
    Output('stored-upload-1', 'data'),
    Output('upload-1-status', 'children'),
    Input('upload-1', 'contents'),
    State('upload-1', 'filename')
)
def store_upload1(contents, filename):
    try:
        if contents is not None:
            return contents, html.Div(
                f"Upload realizado: {filename}",
                style={"textAlign": "center", "color": "green", "fontSize": "0.85rem", "marginTop": "5px"}
            )
        else:
            return None, ""
    except Exception as e:
        return None, html.Div(
            f"Erro no Upload: {str(e)}",
            style={"textAlign": "center", "color": "red", "fontSize": "0.85rem", "marginTop": "5px"}
        )

@callback(
    Output('stored-upload-2', 'data'),
    Output('upload-2-status', 'children'),
    Input('upload-2', 'contents'),
    State('upload-2', 'filename')
)
def store_upload2(contents, filename):
    try:
        if contents is not None:
            return contents, html.Div(
                f"Upload realizado: {filename}",
                style={"textAlign": "center", "color": "green", "fontSize": "0.85rem", "marginTop": "5px"}
            )
        else:
            return None, ""
    except Exception as e:
        return None, html.Div(
            f"Erro no Upload: {str(e)}",
            style={"textAlign": "center", "color": "red", "fontSize": "0.85rem", "marginTop": "5px"}
        )

# --------------------------------
# Callback: Confirmar Uploads -> gera o DataFrame unificado e atualiza o Dropdown
# --------------------------------

@callback(
    Output("empreendimento-dropdown", "options"),
    Output("confirm-upload-status", "children"),
    Output("merged-data", "data"),
    Input("confirm-upload", "n_clicks"),
    State("stored-upload-1", "data"),
    State("stored-upload-2", "data"),
    prevent_initial_call=True
)
def confirm_upload(n_clicks, content1, content2):
    if not content1 or not content2:
        return (
            [],
            html.Div("Faça o upload das duas planilhas antes de confirmar.", style={"color": "red"}),
            None
        )

    # simula processamento
    time.sleep(2)

    def parse_contents(contents, sheet_name=0):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        return pd.read_excel(io.BytesIO(decoded), sheet_name=sheet_name)

    try:
        # Leitura dos DataFrames
        df1 = parse_contents(content1, sheet_name="TicketsChamados")
        df2 = parse_contents(content2, sheet_name=0)

        # ------------------ Validação de colunas obrigatórias ------------------
        obrigatorias_df1 = {"Data Abertura","Nº Ticket"}
        obrigatorias_df2 = {"Nº", "ORIGEM", "EMPREEND.", "DT. FINALIZAÇÃO", "DT. INICIO ETAPA"}
        faltando_df1 = obrigatorias_df1 - set(df1.columns)
        faltando_df2 = obrigatorias_df2 - set(df2.columns)
        if faltando_df1 or faltando_df2:
            msgs = []
            if faltando_df1:
                msgs.append(f"A(s) coluna(s) {', '.join(sorted(faltando_df1))} não está(ão) presente(s) na planilha 'Relatório Geral - Tickets CRM'. Você exportou a planilha 'Relatório Geral - Tickets' faltando colunas.")
            if faltando_df2:
                msgs.append(f"A(s) coluna(s) {', '.join(sorted(faltando_df2))} não está(ão) presente(s) na planilha 'Dados'. Você exportou a planilha 'Dados' faltando colunas.")
            return (
                [],
                html.Div(" ".join(msgs),
                         style={"color": "red", "textAlign": "center", "fontSize": "0.85rem", "marginTop": "5px"}),
                None
            )

        # Excluir colunas indesejadas
        df1 = df1.drop(
            columns=['Tipo Ticket', 'Status Ticket', 'Data Finalizado', 'Assunto'],
            errors='ignore'
        )
        df2 = df2.drop(
            columns=['DT. ABERTURA', 'EMPREEND.', 'BLOCO', 'UNIDADE','TITULO', 'SINTESE', 'RESPONSÁVEL', 'TICKET AGRUPADO', 'PRAZO TICKET', 'PRAZO ETAPA',
                     'USUÁRIO CADASTRO', 'COD. UNIDADE CLIENTE', 'CLASSIFICACAO', 'TICKETS VINCULADOS'],
            errors='ignore'
        )

        # Renomeia as colunas originais 
        df1 = df1.rename(columns={'Nº Ticket': 'ticket_raw'})
        df2 = df2.rename(columns={'Nº': 'ticket_raw'})

        def normalizar_ticket(col):
            """
            Converte qualquer coisa em string, remove espaços, tira .0, 
            mantém só dígitos e devolve como Int64 (suporta nulos).
            """
            return (
                col.astype(str)
                   .str.strip()
                   .str.replace(r'\.0$', '', regex=True)
                   .str.extract(r'(\d+)', expand=False)
                   .astype('Int64')
            )

        df1['ticket_key'] = normalizar_ticket(df1['ticket_raw'])
        df2['ticket_key'] = normalizar_ticket(df2['ticket_raw'])

        # Merge pela coluna chave limpa
        merged_df = pd.merge(
            df1,
            df2,
            on='ticket_key',
            how='outer',
            suffixes=('_df1', '_df2')
        )

        # Remove colunas auxiliares usadas no merge
        merged_df.drop(columns=['ticket_raw_df1', 'ticket_raw_df2'], inplace=True, errors='ignore')

        # Renomeia a chave final se quiser manter a nomenclatura original
        merged_df.rename(columns={'ticket_key': 'Nº Ticket'}, inplace=True)

        # Verifica se "Data Abertura" está em timestamp numérico (milissegundos) e converte se necessário
        if 'Data Abertura' in merged_df.columns:
            if pd.api.types.is_numeric_dtype(merged_df["Data Abertura"]):
                merged_df["Data Abertura"] = pd.to_datetime(merged_df["Data Abertura"], unit="ms", errors="coerce")


        # Converter colunas de data
        for col in date_columns:
            if col in merged_df.columns:
                merged_df[col] = pd.to_datetime(merged_df[col], dayfirst=True, errors='coerce')

        # Filtro de data (apenas chamados a partir de 01/10/2024)
        filtro_data = pd.Timestamp("2024-10-01 00:00:00")
        if 'Data Abertura' in merged_df.columns:
            merged_df = merged_df[merged_df['Data Abertura'] >= filtro_data]

        # --------------------- Funções para calcular prazos (sem alterações) ---------------------

        SECONDS_IN_DAY = 24 * 60 * 60

        def calculate_first_treatment(row):
            start = row["Data Abertura"]
            end   = row["DT. INICIO ETAPA"]

            # 1) Nulos
            if pd.isnull(start) or pd.isnull(end):
                return None, None

            # 2) Ordem cronológica
            if start > end:
                start, end = end, start

            # 3) Mesma data → 0 dias e horas completas
            delta = end - start
            if start.date() == end.date():
                duration_days = 0
                duration_hours = int(delta.total_seconds() // 3600)
                return duration_days, duration_hours

            # 4) Calendário de dias úteis
            bus_cal    = get_busdaycalendar_with_holidays(start, end)
            start_date = np.datetime64(start.date())
            end_date   = np.datetime64(end.date())

            # 5) Dias úteis completos (exclui extremos, trunca negativo)
            full_days = np.busday_count(
                start_date + np.timedelta64(1, "D"),
                end_date,
                busdaycal=bus_cal
            )
            if full_days < 0:
                full_days = 0

            # 6) Segundos totais = dias completos + frações do primeiro/último dia
            total_secs = full_days * SECONDS_IN_DAY
            if np.is_busday(start_date, busdaycal=bus_cal):
                fim = datetime.datetime.combine(start.date(), datetime.time.max)
                total_secs += (fim - start).total_seconds()
            if np.is_busday(end_date, busdaycal=bus_cal):
                inicio = datetime.datetime.combine(end.date(), datetime.time.min)
                total_secs += (end - inicio).total_seconds()

            # 7) Converte para dias (ceil: resto vira 1 dia)
            duration_days = math.ceil(total_secs / SECONDS_IN_DAY)

            # 8) Horas completas brutas
            duration_hours = int(delta.total_seconds() // 3600)

            return duration_days, duration_hours


        def calculate_last_treatment(row):
            start = row["DT. INICIO ETAPA"]
            end   = row["DT. FINALIZAÇÃO"]

            # 1) Nulos
            if pd.isnull(start) or pd.isnull(end):
                return None, None

            # 2) Ordem cronológica
            if start > end:
                start, end = end, start

            # 3) Mesma data → 0 dias e horas completas
            delta = end - start
            if start.date() == end.date():
                duration_days = 0
                duration_hours = int(delta.total_seconds() // 3600)
                return duration_days, duration_hours

            # 4) Calendário de dias úteis
            bus_cal    = get_busdaycalendar_with_holidays(start, end)
            start_date = np.datetime64(start.date())
            end_date   = np.datetime64(end.date())

            # 5) Dias úteis completos (exclui extremos, trunca negativo)
            full_days = np.busday_count(
                start_date + np.timedelta64(1, "D"),
                end_date,
                busdaycal=bus_cal
            )
            if full_days < 0:
                full_days = 0

            # 6) Segundos totais = dias completos + frações do primeiro/último dia
            total_secs = full_days * SECONDS_IN_DAY
            if np.is_busday(start_date, busdaycal=bus_cal):
                fim = datetime.datetime.combine(start.date(), datetime.time.max)
                total_secs += (fim - start).total_seconds()
            if np.is_busday(end_date, busdaycal=bus_cal):
                inicio = datetime.datetime.combine(end.date(), datetime.time.min)
                total_secs += (end - inicio).total_seconds()

            # 7) Converte para dias (resto vira 1 dia)
            duration_days = math.ceil(total_secs / SECONDS_IN_DAY)
            # 8) Horas completas brutas
            duration_hours = int(delta.total_seconds() // 3600)

            return duration_days, duration_hours


        def calculate_total_duration(row):
            start = row["Data Abertura"]
            end   = row["DT. FINALIZAÇÃO"]

            # 1) Nulos
            if pd.isnull(start) or pd.isnull(end):
                return None, None

            # 2) Ordem cronológica
            if start > end:
                start, end = end, start

            # 3) Mesma data → 0 dias e horas completas
            delta = end - start
            if start.date() == end.date():
                duration_days = 0
                duration_hours = int(delta.total_seconds() // 3600)
                return duration_days, duration_hours

            # 4) Calendário de dias úteis
            bus_cal    = get_busdaycalendar_with_holidays(start, end)
            start_date = np.datetime64(start.date())
            end_date   = np.datetime64(end.date())

            # 5) Dias úteis completos (exclui extremos, trunca negativo)
            full_days = np.busday_count(
                start_date + np.timedelta64(1, "D"),
                end_date,
                busdaycal=bus_cal
            )
            if full_days < 0:
                full_days = 0

            # 6) Segundos totais = dias completos + frações do primeiro/último dia
            total_secs = full_days * SECONDS_IN_DAY
            if np.is_busday(start_date, busdaycal=bus_cal):
                fim = datetime.datetime.combine(start.date(), datetime.time.max)
                total_secs += (fim - start).total_seconds()
            if np.is_busday(end_date, busdaycal=bus_cal):
                inicio = datetime.datetime.combine(end.date(), datetime.time.min)
                total_secs += (end - inicio).total_seconds()

            # 7) Converte para dias (ceil: resto vira 1 dia)
            duration_days = math.ceil(total_secs / SECONDS_IN_DAY)
            # 8) Horas completas brutas
            duration_hours = int(delta.total_seconds() // 3600)

            return duration_days, duration_hours

        def sla_compliance(row):
            origem = row.get("ORIGEM")
            if origem == "E-mail OR":
                return "Não foi atendido pelo portal"
            duration_days = row["Primeira Tratativa (dias)"]
            if duration_days is None:
                return "Dados insuficientes"
            elif duration_days <= 2:
                return "1º atendimento dentro do SLA"
            else:
                return "1º atendimento fora do SLA"

        def determine_status(row):
            origem = str(row.get("ORIGEM", "")).strip().lower()
            if origem == "e-mail or":
                return "não foi atendido pelo portal"

            inicio_etapa = row["DT. INICIO ETAPA"]
            finalizacao = row["DT. FINALIZAÇÃO"]
            titulo3 = str(row.get("TITULO3", "")).strip().upper()

            titulos_especiais = {"ESCRITURA", "CESSÃO DE DIREITOS", "HIPOTECA/ESCRITURA"}

            if pd.isnull(inicio_etapa):
                return STATUS_CHAMADO_AINDA_NAO_ATENDIDO
            elif pd.isnull(finalizacao):
                start_date = np.datetime64(inicio_etapa.date())
                current_date = np.datetime64(datetime.datetime.now().date())
                duration_days = np.busday_count(start_date, current_date)
                if duration_days > 3:
                    return STATUS_CHAMADO_EM_ATRASO
                else:
                    return STATUS_CHAMADO_DENTRO_DO_PRAZO
            else:
                start_date = np.datetime64(inicio_etapa.date())
                end_date = np.datetime64(finalizacao.date())
                bus_cal = get_busdaycalendar_with_holidays(inicio_etapa, finalizacao)
                duration_days = np.busday_count(start_date, end_date, busdaycal=bus_cal)
                if np.is_busday(end_date, busdaycal=bus_cal):
                    duration_days += 1

                if titulo3 in titulos_especiais:
                    if duration_days <= 10:
                        return STATUS_CHAMADO_FINALIZADO_DENTRO_DO_SLA
                    else:
                        return STATUS_CHAMADO_FINALIZADO_FORA_DO_SLA
                else:
                    if duration_days <= 3:
                        return STATUS_CHAMADO_FINALIZADO_DENTRO_DO_SLA
                    else:
                        return STATUS_CHAMADO_FINALIZADO_FORA_DO_SLA

        # --------------------------------------------------------

        # Aplica funções de cálculo
        resultados = merged_df.apply(calculate_first_treatment, axis=1, result_type='expand')
        merged_df["Primeira Tratativa (dias)"] = resultados[0]
        merged_df["Primeira Tratativa (horas)"] = resultados[1]
        # aplica e desempacota em duas colunas
        res_last = merged_df.apply(calculate_last_treatment, axis=1)
        merged_df[["Última Tratativa (dias)", "Última Tratativa (horas)"]] = pd.DataFrame(
            res_last.tolist(), index=merged_df.index
        )
        # Aplica e desempacota em duas colunas
        res_total = merged_df.apply(calculate_total_duration, axis=1)
        merged_df[["Prazo Total do Chamado (dias)", "Prazo Total do Chamado (horas)"]] = pd.DataFrame(
            res_total.tolist(), index=merged_df.index
        )

        merged_df["Chamados atendidos dentro do SLA"] = merged_df.apply(sla_compliance, axis=1)
        merged_df["Chamados sem interação há 72h"] = merged_df.apply(determine_status, axis=1)

        merged_df['Chamados sem interação há 72h'] = (
            merged_df['Chamados sem interação há 72h'].str.strip().str.lower()
        )
        merged_df['Chamados atendidos dentro do SLA'] = (
            merged_df['Chamados atendidos dentro do SLA'].str.strip().str.lower()
        )

        for col in date_columns:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].dt.strftime('%d/%m/%Y %H:%M:%S').fillna('')

        numeric_columns = ['Primeira Tratativa (dias)', 'Última Tratativa (dias)', 'Prazo Total do Chamado (dias)']
        for col in numeric_columns:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')


        # REORGANIZAÇÃO DE COLUNAS
        ordem_preferida = [
            "Cliente/Síndico/Admin",
            "Empreendimento",
            "Torre",
            "Unidade",
            "Nº Contrato",
            "Tipo Contrato",           
            "Nº Ticket",
            "ORIGEM",
            "CLIENTE/SÍNDICO",
            "USUÁRIO",
            "STATUS",
            "PRIORIDADE",
            "CPF",
            "TITULO1",
            "TITULO2",
            "TITULO3",
            "TIPO STATUS TICKET",
            "TIPO TICKET",
            "TIPO AÇÃO",
            "TIPO ORIGEM",
            "ETAPA ATUAL",
            "MOTIVO",
            "Data Abertura",
            "DT. PREVISÃO TÉRMINO ETAPA",
            "DT. HISTORICO",
            "DT. PREVISÃO TÉRMINO TICKET",
            "DT. INICIO ETAPA",
            "DT. FINALIZAÇÃO",
            "DT. CANCELAMENTO",
            "Primeira Tratativa (dias)",           
            "Última Tratativa (dias)",            
            "Prazo Total do Chamado (dias)",           
            "Chamados atendidos dentro do SLA",
            "Chamados sem interação há 72h",
            "Primeira Tratativa (horas)",
            "Última Tratativa (horas)",
            "Prazo Total do Chamado (horas)"
        ]
        outras = [col for col in merged_df.columns if col not in ordem_preferida]
        merged_df = merged_df[ordem_preferida + outras]

        # Dropdown de empreendimentos
        if "Empreendimento" in merged_df.columns:
            empreendimentos_unicos = merged_df["Empreendimento"].dropna().unique()
            empreendimentos_unicos = sorted(empreendimentos_unicos)
            dropdown_options = [{"label": "Todos", "value": "Todos"}] + [
                {"label": emp, "value": emp} for emp in empreendimentos_unicos
            ]
        else:
            dropdown_options = []

        # Serializa para JSON
        merged_json = merged_df.to_json(orient="split")

        return (
            dropdown_options,
            html.Div("Uploads confirmados!", style={
                "textAlign": "center",
                "color": "green",
                "fontSize": "0.85rem",
                "marginTop": "5px"
            }),
            merged_json
        )

    except Exception as e:
        return (
            [],
            html.Div(f"Ocorreu um erro ao confirmar uploads: {e}", style={
                "color": "red",
                "textAlign": "center",
                "fontSize": "0.85rem",
                "marginTop": "5px"
            }),
            None
        )

# --------------------------------
# Callback: Gerar relatório (inclui filtro e contagens)
# --------------------------------
@callback(
    Output("output-message", "children"),
    Output("table-container", "style"),
    Output("merged-table", "data"),
    Output("merged-table", "columns"),
    Output("export-button", "style"),
    Output("valor-1", "children"),  # chamado em atraso
    Output("valor-2", "children"),  # chamado dentro do prazo
    Output("valor-3", "children"),  # chamado finalizado fora do sla
    Output("valor-4", "children"),  # chamado finalizado dentro do sla
    Output("valor-5", "children"),  # 1º atendimento dentro do sla
    Output("valor-6", "children"),  # 1º atendimento fora do sla
    Output("valor-7", "children"),  # chamado ainda não atendido
    Output("valor-8", "children"),  # não foi atendido pelo portal
    Output("total-chamados", "children"),
    Output("valor-ativa", "children"),
    Output("valor-receptiva", "children"),
    Output("top5-table-container", "style"),
    Output("top5-table", "data"),
    Output("aggregated-table-container", "style"),
    Output("aggregated-table", "data"),
    Output("aggregated-table", "columns"),
    Output("report-date", "data"),
    Output("filtered-data", "data"),  
    Input("generate-report", "n_clicks"),
    State("merged-data", "data"),
    State("empreendimento-dropdown", "value"),  
    prevent_initial_call=True
)
def generate_report(n_clicks, merged_data_json, selected_empreendimento):

    if not n_clicks:
        raise PreventUpdate

    if not merged_data_json:
        return (
            html.Div(
                "Por favor, confirme os uploads antes de gerar o relatório.",
                style={"color": "red"}
            ),
            {"display": "none"}, [], [], {"display": "none"}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, {"display": "none"}, [], {"display": "none"},     
            [],
            [],
            None,
            None
        )
    
    try:
        # Converte JSON para DataFrame
        merged_df = pd.read_json(io.StringIO(merged_data_json), orient='split')

        # Tratar a opção "Todos"
        if not selected_empreendimento or "Todos" in selected_empreendimento:
            df_filtrado = merged_df
        else:
            # Filtrar pelos empreendimentos selecionados
            df_filtrado = merged_df[merged_df["Empreendimento"].isin(selected_empreendimento)]

        # Nenhum dado após o filtro
        if df_filtrado.empty:
            return (
                html.Div("Nenhum chamado encontrado para a seleção.", style={"color": "red"}),
                {"display": "none"},
                [],
                [],
                {"display": "none"},
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                {"display": "none"}, [],
                {"display": "none"}, [], [],
                None,
                None
            )

        # Cálculos de status e SLA
        status_counts = df_filtrado['Chamados sem interação há 72h'].value_counts()
        sla_counts = df_filtrado['Chamados atendidos dentro do SLA'].value_counts()

        valor1 = status_counts.get('chamado em atraso', 0)
        valor2 = status_counts.get('chamado dentro do prazo', 0)
        valor3 = status_counts.get('chamado finalizado com atraso', 0)
        valor4 = status_counts.get('chamado finalizado dentro do sla', 0)
        valor7 = status_counts.get('chamado ainda não atendido', 0)

        valor5 = sla_counts.get('1º atendimento dentro do sla', 0)
        valor6 = sla_counts.get('1º atendimento fora do sla', 0)
        valor8 = sla_counts.get('não foi atendido pelo portal', 0)

        total_chamados = df_filtrado.shape[0]

        # TIPO AÇÃO
        if "TIPO AÇÃO" in df_filtrado.columns:
            valor_ativa = (df_filtrado["TIPO AÇÃO"] == "Ativa").sum()
            valor_receptiva = (df_filtrado["TIPO AÇÃO"] == "Receptiva").sum()
        else:
            valor_ativa = 0
            valor_receptiva = 0

        # Top 5 (TITULO3)
        if "TITULO3" in df_filtrado.columns and not df_filtrado["TITULO3"].dropna().empty:
            top5_counts = df_filtrado["TITULO3"].value_counts().head(5)
            top5_data = []
            for titulo, qtd in top5_counts.items():
                perc = (qtd / total_chamados) * 100
                top5_data.append({
                    "Titulo": titulo,
                    "Quantidade": qtd,
                    "Percentual": f"{perc:.2f}%"
                })
            top5_container_style = {"display": "block"}
        else:
            top5_data = []
            top5_container_style = {"display": "none"}

        # Agregado por Empreendimento
        if "Empreendimento" in df_filtrado.columns:
            aggregated_df = df_filtrado.groupby('Empreendimento').agg({
                'Nº Ticket': 'count',
                'Primeira Tratativa (dias)': 'mean',
                'Última Tratativa (dias)': 'mean',
                'Prazo Total do Chamado (dias)': 'mean'
            }).reset_index()

            aggregated_df.rename(columns={
                'Nº Ticket': 'Quantidade',
                'Primeira Tratativa (dias)': 'Média Primeira Tratativa (dias)',
                'Última Tratativa (dias)': 'Média Última Tratativa (dias)',
                'Prazo Total do Chamado (dias)': 'Média Prazo Total do Chamado (dias)'
            }, inplace=True)

            aggregated_df['Média Primeira Tratativa (dias)'] = aggregated_df['Média Primeira Tratativa (dias)'].round(2)
            aggregated_df['Média Última Tratativa (dias)'] = aggregated_df['Média Última Tratativa (dias)'].round(2)
            aggregated_df['Média Prazo Total do Chamado (dias)'] = aggregated_df['Média Prazo Total do Chamado (dias)'].round(2)

            aggregated_data = aggregated_df.to_dict('records')
            aggregated_columns = [{"name": i, "id": i} for i in aggregated_df.columns]
            aggregated_container_style = {"display": "block"}
        else:
            aggregated_data = []
            aggregated_columns = []
            aggregated_container_style = {"display": "none"}

        # Dados para exibir na tabela principal
        data = df_filtrado.to_dict('records')
        columns = [{"name": i, "id": i} for i in df_filtrado.columns]

        # Data/hora do relatório
        report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Salvar DF filtrado para export
        filtered_json = df_filtrado.to_json(orient='split')

        return (
            html.Div("Relatório gerado com sucesso!", style={"color": "green"}),
            {"display": "block"},
            data,
            columns,
            {"display": "inline-block", "marginBottom": "10px"},
            valor1, valor2, valor3, valor4,
            valor5, valor6, valor7, valor8,
            total_chamados,
            valor_ativa,
            valor_receptiva,
            top5_container_style,
            top5_data,
            aggregated_container_style,
            aggregated_data,
            aggregated_columns,
            report_date,
            filtered_json
        )
    except Exception as e:
        # Loga o erro (pode ser substituído por um logger apropriado)
        print(f"Erro ao gerar relatório: {e}")
        return (
            html.Div(f"Erro ao gerar relatório: {str(e)}", style={"color": "red"}),
            {"display": "none"},
            [],
            [],
            {"display": "none"},
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            {"display": "none"},
            [],
            {"display": "none"},
            [],
            [],
            None,
            None
        )

# --------------------------------
# Callback: Exportar relatório Excel
# --------------------------------
@callback(
    Output("download-report", "data"),
    Input("export-button", "n_clicks"),
    State("filtered-data", "data"),
    State("report-date", "data"),
    prevent_initial_call=True
)
def export_to_excel(n_clicks, filtered_data_json, report_date):
    try:
        if n_clicks > 0 and filtered_data_json is not None:
            df_filtered = pd.read_json(io.StringIO(filtered_data_json), orient='split')

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter', datetime_format='dd/mm/yyyy hh:mm:ss') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Relatório', startrow=1)
                workbook = writer.book
                worksheet = writer.sheets['Relatório']

                worksheet.write(0, 0, "Data")
                worksheet.write(0, 1, report_date)

                date_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss'})
                number_format = workbook.add_format({'num_format': '0'})

                for idx, col in enumerate(df_filtered.columns):
                    if col in date_columns:
                        worksheet.set_column(idx, idx, 20, date_format)
                    elif col in ['Nº Ticket', 'Nº']:
                        worksheet.set_column(idx, idx, 20, number_format)
                    else:
                        worksheet.set_column(idx, idx, 20)

            output.seek(0)
            return dcc.send_bytes(output.read(), filename="relatorio_final.xlsx")
        else:
            return None
    except Exception as e:
        print(f"Erro na exportação: {e}")
        return None
