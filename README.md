# Dashboard de Investimentos 💰

Dashboard interativo para análise de investimentos pessoais, desenvolvido com Streamlit e Python.

## 📋 Descrição

Este dashboard fornece análises detalhadas de performance de investimentos com base em dados históricos de uma planilha Excel. O sistema permite visualizar:

- Performance mensal e anual vs benchmarks (Ibovespa, Selic, etc.)
- Evolução patrimonial ao longo do tempo
- Análise histórica do portfólio por alocação
- Posição atual detalhada por ativo

## 🚀 Funcionalidades

### 📊 Performance Mensal
- Gráficos de rentabilidade acumulada comparando carteira com Ibovespa e Selic
- Evolução do patrimônio e aportes ao longo dos meses
- Cards com métricas principais (patrimônio atual, rentabilidade total, lucro)

### 📈 Performance Anual
- Análise consolidada ano a ano
- Comparativo de performance anual (gráfico de barras)
- Evolução patrimonial consolidada

### 🔄 Evolução do Portfólio
- Filtros interativos por Tipo, Categoria e Alocação
- Gráfico de evolução temporal das alocações
- Composição percentual do portfólio ao longo do tempo
- Visualização hierárquica (Treemap) da distribuição atual
- Totalizadores por Tipo, Categoria e Alocação

### 💼 Posição Atual
- Tabela interativa com todos os ativos
- Filtros por Tipo, Classe, Setor e busca por nome
- Treemap com hierarquia Tipo > Classe > Ativo
- Top 10 maiores posições
- Análise de rentabilidade vs alocação (gráfico de dispersão)
- Cards com métricas consolidadas (XIRR médio ponderado, lucro total, etc.)

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Passos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/dashboard-investimentos.git
   cd dashboard-investimentos
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Adicione sua planilha:**
   - Coloque o arquivo `datainvest.xlsx` na raiz do projeto
   - Certifique-se de que a planilha possui as abas: `data_mes`, `data_ano`, `data_port_historico`, `data_port_mes`

## 🎯 Como Usar

### Executar Localmente

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente no seu navegador em `http://localhost:8501`

### Deploy no Streamlit Cloud

1. **Faça upload do projeto para o GitHub**
2. **Acesse [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Conecte sua conta do GitHub**
4. **Crie um novo app:**
   - Selecione o repositório
   - Defina o branch (geralmente `main`)
   - Especifique o arquivo principal: `app.py`
5. **Clique em "Deploy"**

## 📊 Estrutura da Planilha Excel

O arquivo `datainvest.xlsx` deve conter as seguintes abas:

### 1. data_mes
Histórico mensal de investimentos
- **Colunas principais:** date, vlr_investido, vlr_mercado, twr_acc, ibov_acc, selic_acc, fluxo_acc

### 2. data_ano
Histórico anual de investimentos
- **Colunas principais:** date, vlr_investido, vlr_mercado, twr_ano, twr_acc, ibov_ano, selic_ano

### 3. data_port_historico
Evolução histórica do portfólio
- **Colunas:** Tipo, Categoria, Alocação, + colunas de datas com valores de mercado

### 4. data_port_mes
Snapshot atual do portfólio
- **Colunas principais:** ativo, Nome, Tipo, classe, setor, vlr_investido, vlr_mercado, lucro_total, lucro_total_pct, xirr

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework para criação de aplicações web
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados
- **[Plotly](https://plotly.com/python/)** - Visualizações interativas
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** - Leitura de arquivos Excel

## 📝 Formatação

O dashboard utiliza formatação brasileira:
- **Moeda:** R$ 1.234,56
- **Percentual:** 12,34%
- **Data:** DD/MM/YYYY

## 📄 Licença

Este projeto é de código aberto e está disponível sob a Licença MIT.
