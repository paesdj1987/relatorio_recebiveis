
# 🧠 Dash Ticket

Aplicação web interativa construída com [Dash](https://plotly.com/dash/) para upload, processamento e análise de dados de chamados, com filtros por empreendimento, status, datas e geração de gráficos e relatórios.

---

## 🚀 Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

2. Crie um ambiente virtual

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

3. Instale as dependências

pip install -r requirements.txt

4. Execute a aplicação

python app.py
Acesse http://127.0.0.1:8053 no navegador.

📁 Estrutura de diretórios
.
├── app.py                   # Arquivo principal
├── layout.py                # Layout geral
├── callbacks.py             # Callbacks principais (upload e relatório)
├── dashboard.py             # Layout do dashboard
├── dashboard_callbacks.py   # Callbacks dos gráficos
├── feriados.py              # Utilitários de feriado (SLA)
├── assets/
│   └── custom.css           # Estilo visual da aplicação
├── requirements.txt         # Dependências principais
├── devops.txt               # Alterações recentes e notas técnicas
├── CHANGELOG.md             # Histórico de versões e melhorias
└── README.md                # Instruções de uso e descrição do projeto

✨ Funcionalidades
Upload de arquivos Excel
Confirmação de uploads
Filtros por empreendimento, status, origem e data
Indicadores e gráficos interativos
Geração de relatório e exportação para Excel
Interface responsiva com Bootstrap


🛠️ Tecnologias
Dash
Plotly
Pandas
Bootstrap (via dash-bootstrap-components)