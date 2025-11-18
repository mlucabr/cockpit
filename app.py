import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import locale

# Configurar locale brasileiro (tentar múltiplas opções)
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass  # Se não conseguir, usar formato manual

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Investimentos",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funções auxiliares para formatação
def formatar_moeda(valor):
    """Formata valor como moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

def formatar_percentual(valor):
    """Formata valor como percentual"""
    return f"{valor*100:.2f}%".replace(".", ",")

# Cache para carregar dados
@st.cache_data
def carregar_dados():
    """Carrega todas as abas da planilha Excel"""
    file_path = 'datainvest.xlsx'
    
    # Carregar cada aba
    data_mes = pd.read_excel(file_path, sheet_name='data_mes')
    data_ano = pd.read_excel(file_path, sheet_name='data_ano')
    data_port_historico = pd.read_excel(file_path, sheet_name='data_port_historico')
    data_port_mes = pd.read_excel(file_path, sheet_name='data_port_mes')
    
    # Garantir que as datas estejam no formato correto
    data_mes['date'] = pd.to_datetime(data_mes['date'])
    
    return data_mes, data_ano, data_port_historico, data_port_mes

# Função para transformar data_port_historico de wide para long
@st.cache_data
def transformar_historico(df):
    """Transforma dados de formato wide para long"""
    from datetime import datetime
    
    # Identificar colunas de datas (todas exceto as 3 primeiras)
    date_columns = [col for col in df.columns if isinstance(col, datetime)]
    
    # Melt o dataframe
    df_long = df.melt(
        id_vars=['Tipo', 'Categoria', 'Alocação'],
        value_vars=date_columns,
        var_name='Data',
        value_name='Valor'
    )
    
    # Remover linhas com valores NaN ou zero
    df_long = df_long[df_long['Valor'].notna()]
    df_long = df_long[df_long['Valor'] > 0]
    
    # Converter Data para datetime se necessário
    df_long['Data'] = pd.to_datetime(df_long['Data'])
    
    return df_long

# Carregar dados
data_mes, data_ano, data_port_historico, data_port_mes = carregar_dados()

# Sidebar - Navegação
st.sidebar.title("💰 Dashboard de Investimentos")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação",
    ["📊 Performance Mensal", "📈 Performance Anual", "🔄 Evolução do Portfólio", "💼 Posição Atual"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Sobre")
st.sidebar.info("Dashboard interativo para análise de investimentos com dados em tempo real.")

# ========== PÁGINA 1 - PERFORMANCE MENSAL ==========
if pagina == "📊 Performance Mensal":
    st.title("📊 Análise Mensal de Investimentos")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    ultimo_mes = data_mes.iloc[-1]
    patrimonio_atual = ultimo_mes['vlr_mercado']
    rentabilidade_total = ultimo_mes['twr_acc']
    lucro_total = ultimo_mes['vlr_mercado'] - ultimo_mes['vlr_investido']
    
    with col1:
        st.metric(
            "💰 Patrimônio Atual",
            formatar_moeda(patrimonio_atual),
            delta=formatar_moeda(lucro_total)
        )
    
    with col2:
        st.metric(
            "📈 Rentabilidade Total",
            formatar_percentual(rentabilidade_total)
        )
    
    with col3:
        st.metric(
            "💵 Lucro Total",
            formatar_moeda(lucro_total),
            delta=formatar_percentual(lucro_total / ultimo_mes['vlr_investido'])
        )
    
    st.markdown("---")
    
    # Gráfico 1: Performance Histórica vs Benchmarks
    st.subheader("📊 Performance Histórica vs Benchmarks")
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=data_mes['date'],
        y=data_mes['twr_acc'] * 100,
        mode='lines',
        name='Carteira',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig1.add_trace(go.Scatter(
        x=data_mes['date'],
        y=data_mes['ibov_acc'] * 100,
        mode='lines',
        name='Ibovespa',
        line=dict(color='#ff7f0e', width=2)
    ))
    
    fig1.add_trace(go.Scatter(
        x=data_mes['date'],
        y=data_mes['selic_acc'] * 100,
        mode='lines',
        name='Selic',
        line=dict(color='#2ca02c', width=2)
    ))
    
    fig1.update_layout(
        xaxis_title="Data",
        yaxis_title="Rentabilidade Acumulada (%)",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Evolução Patrimonial
    st.subheader("💰 Evolução Patrimonial")
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=data_mes['date'],
        y=data_mes['fluxo_acc'],
        mode='lines',
        name='Aportes Acumulados',
        line=dict(color='#9467bd', width=2),
        fill='tozeroy'
    ))
    
    fig2.add_trace(go.Scatter(
        x=data_mes['date'],
        y=data_mes['vlr_investido'],
        mode='lines',
        name='Capital Investido',
        line=dict(color='#8c564b', width=2)
    ))
    
    fig2.add_trace(go.Scatter(
        x=data_mes['date'],
        y=data_mes['vlr_mercado'],
        mode='lines',
        name='Patrimônio Atual',
        line=dict(color='#e377c2', width=3)
    ))
    
    fig2.update_layout(
        xaxis_title="Data",
        yaxis_title="Valor (R$)",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# ========== PÁGINA 2 - PERFORMANCE ANUAL ==========
elif pagina == "📈 Performance Anual":
    st.title("📈 Análise Anual de Investimentos")
    
    # Métricas principais do último ano
    ultimo_ano = data_ano.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Patrimônio",
            formatar_moeda(ultimo_ano['vlr_mercado'])
        )
    
    with col2:
        st.metric(
            "📊 TWR Acumulado",
            formatar_percentual(ultimo_ano['twr_acc'])
        )
    
    with col3:
        st.metric(
            "📈 TWR Ano",
            formatar_percentual(ultimo_ano['twr_ano'])
        )
    
    with col4:
        st.metric(
            "💵 Lucro",
            formatar_moeda(ultimo_ano['lucro'])
        )
    
    st.markdown("---")
    
    # Gráfico 1: Performance Histórica Anual
    st.subheader("📊 Performance Acumulada por Ano")
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=data_ano['date'],
        y=data_ano['twr_acc'] * 100,
        mode='lines+markers',
        name='Carteira',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig1.add_trace(go.Scatter(
        x=data_ano['date'],
        y=data_ano['ibov_acc'] * 100,
        mode='lines+markers',
        name='Ibovespa',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=6)
    ))
    
    fig1.add_trace(go.Scatter(
        x=data_ano['date'],
        y=data_ano['selic_acc'] * 100,
        mode='lines+markers',
        name='Selic',
        line=dict(color='#2ca02c', width=2),
        marker=dict(size=6)
    ))
    
    fig1.update_layout(
        xaxis_title="Ano",
        yaxis_title="Rentabilidade Acumulada (%)",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Evolução Patrimonial Anual
    st.subheader("💰 Evolução Patrimonial Anual")
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=data_ano['date'],
        y=data_ano['fluxo_acc'],
        mode='lines+markers',
        name='Aportes Acumulados',
        line=dict(color='#9467bd', width=2),
        marker=dict(size=6)
    ))
    
    fig2.add_trace(go.Scatter(
        x=data_ano['date'],
        y=data_ano['vlr_investido'],
        mode='lines+markers',
        name='Capital Investido',
        line=dict(color='#8c564b', width=2),
        marker=dict(size=6)
    ))
    
    fig2.add_trace(go.Scatter(
        x=data_ano['date'],
        y=data_ano['vlr_mercado'],
        mode='lines+markers',
        name='Patrimônio Atual',
        line=dict(color='#e377c2', width=3),
        marker=dict(size=8)
    ))
    
    fig2.update_layout(
        xaxis_title="Ano",
        yaxis_title="Valor (R$)",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico 3: Performance por Ano
    st.subheader("📊 Performance Anual (Comparativo)")
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        x=data_ano['date'],
        y=data_ano['twr_ano'] * 100,
        name='Carteira',
        marker_color='#1f77b4'
    ))
    
    fig3.add_trace(go.Bar(
        x=data_ano['date'],
        y=data_ano['ibov_ano'] * 100,
        name='Ibovespa',
        marker_color='#ff7f0e'
    ))
    
    fig3.add_trace(go.Bar(
        x=data_ano['date'],
        y=data_ano['selic_ano'] * 100,
        name='Selic',
        marker_color='#2ca02c'
    ))
    
    # Adicionar linha zero
    fig3.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero")
    
    fig3.update_layout(
        xaxis_title="Ano",
        yaxis_title="Rentabilidade Anual (%)",
        barmode='group',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# ========== PÁGINA 3 - EVOLUÇÃO DO PORTFÓLIO ==========
elif pagina == "🔄 Evolução do Portfólio":
    st.title("🔄 Evolução Histórica por Alocação")
    
    # Transformar dados
    df_historico_long = transformar_historico(data_port_historico)
    
    # Filtros na sidebar
    st.sidebar.markdown("### Filtros")
    
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo",
        options=df_historico_long['Tipo'].unique(),
        default=df_historico_long['Tipo'].unique()
    )
    
    categorias_selecionadas = st.sidebar.multiselect(
        "Categoria",
        options=df_historico_long['Categoria'].unique(),
        default=df_historico_long['Categoria'].unique()
    )
    
    alocacoes_selecionadas = st.sidebar.multiselect(
        "Alocação",
        options=df_historico_long['Alocação'].unique(),
        default=df_historico_long['Alocação'].unique()[:5]  # Primeiras 5 por padrão
    )
    
    # Aplicar filtros
    df_filtrado = df_historico_long[
        (df_historico_long['Tipo'].isin(tipos_selecionados)) &
        (df_historico_long['Categoria'].isin(categorias_selecionadas)) &
        (df_historico_long['Alocação'].isin(alocacoes_selecionadas))
    ]
    
    if len(df_filtrado) == 0:
        st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Selecione ao menos um item em cada filtro.")
    else:
        # Calcular totalizadores
        df_ultimo_mes = df_filtrado[df_filtrado['Data'] == df_filtrado['Data'].max()]
        
        total_por_tipo = df_ultimo_mes.groupby('Tipo')['Valor'].sum().reset_index()
        total_por_categoria = df_ultimo_mes.groupby('Categoria')['Valor'].sum().reset_index()
        total_por_alocacao = df_ultimo_mes.groupby('Alocação')['Valor'].sum().reset_index()
        
        # Cards de totalizadores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💼 Total Portfólio", formatar_moeda(df_ultimo_mes['Valor'].sum()))
        
        with col2:
            st.metric("📊 Tipos", len(total_por_tipo))
        
        with col3:
            st.metric("🏷️ Alocações", len(total_por_alocacao))
        
        st.markdown("---")
        
        # Gráfico 1: Evolução por Alocação
        st.subheader("📈 Evolução por Alocação")
        
        fig1 = px.line(
            df_filtrado,
            x='Data',
            y='Valor',
            color='Alocação',
            title="Evolução do Valor por Alocação ao Longo do Tempo"
        )
        
        fig1.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor (R$)",
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Composição ao Longo do Tempo
        st.subheader("📊 Composição do Portfólio ao Longo do Tempo")
        
        # Calcular percentuais
        df_percentual = df_filtrado.copy()
        df_percentual['Total_Data'] = df_percentual.groupby('Data')['Valor'].transform('sum')
        df_percentual['Percentual'] = (df_percentual['Valor'] / df_percentual['Total_Data']) * 100
        
        fig2 = px.area(
            df_percentual,
            x='Data',
            y='Percentual',
            color='Alocação',
            title="Composição Percentual do Portfólio"
        )
        
        fig2.update_layout(
            xaxis_title="Data",
            yaxis_title="Percentual (%)",
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Gráfico 3: Distribuição Atual
        st.subheader("🥧 Distribuição Atual por Tipo")
        
        fig3 = px.treemap(
            df_ultimo_mes,
            path=['Tipo', 'Categoria', 'Alocação'],
            values='Valor',
            title="Hierarquia do Portfólio (Tipo > Categoria > Alocação)"
        )
        
        fig3.update_layout(height=600)
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # Tabelas de totalizadores
        st.markdown("---")
        st.subheader("📋 Totalizadores")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Por Tipo**")
            total_por_tipo['Percentual'] = (total_por_tipo['Valor'] / total_por_tipo['Valor'].sum()) * 100
            total_por_tipo['Valor'] = total_por_tipo['Valor'].apply(formatar_moeda)
            total_por_tipo['Percentual'] = total_por_tipo['Percentual'].apply(lambda x: f"{x:.2f}%".replace(".", ","))
            st.dataframe(total_por_tipo, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Por Categoria**")
            total_por_categoria['Percentual'] = (total_por_categoria['Valor'] / total_por_categoria['Valor'].sum()) * 100
            total_por_categoria['Valor'] = total_por_categoria['Valor'].apply(formatar_moeda)
            total_por_categoria['Percentual'] = total_por_categoria['Percentual'].apply(lambda x: f"{x:.2f}%".replace(".", ","))
            st.dataframe(total_por_categoria, use_container_width=True, hide_index=True)
        
        with col3:
            st.markdown("**Por Alocação**")
            total_por_alocacao['Percentual'] = (total_por_alocacao['Valor'] / total_por_alocacao['Valor'].sum()) * 100
            total_por_alocacao['Valor'] = total_por_alocacao['Valor'].apply(formatar_moeda)
            total_por_alocacao['Percentual'] = total_por_alocacao['Percentual'].apply(lambda x: f"{x:.2f}%".replace(".", ","))
            st.dataframe(total_por_alocacao, use_container_width=True, hide_index=True)

# ========== PÁGINA 4 - POSIÇÃO ATUAL ==========
elif pagina == "💼 Posição Atual":
    st.title("💼 Portfolio Atual - Detalhamento por Ativo")
    
    # Filtros na sidebar
    st.sidebar.markdown("### Filtros")
    
    tipos_disponiveis = data_port_mes['Tipo'].unique()
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo",
        options=tipos_disponiveis,
        default=tipos_disponiveis
    )
    
    classes_disponiveis = data_port_mes['classe'].unique()
    classes_selecionadas = st.sidebar.multiselect(
        "Classe",
        options=classes_disponiveis,
        default=classes_disponiveis
    )
    
    setores_disponiveis = data_port_mes['setor'].unique()
    setores_selecionados = st.sidebar.multiselect(
        "Setor",
        options=setores_disponiveis,
        default=setores_disponiveis
    )
    
    busca_ativo = st.sidebar.text_input("🔍 Buscar Ativo", "")
    
    # Aplicar filtros
    df_filtrado = data_port_mes[
        (data_port_mes['Tipo'].isin(tipos_selecionados)) &
        (data_port_mes['classe'].isin(classes_selecionadas)) &
        (data_port_mes['setor'].isin(setores_selecionados))
    ]
    
    if busca_ativo:
        df_filtrado = df_filtrado[
            df_filtrado['ativo'].str.contains(busca_ativo, case=False, na=False) |
            df_filtrado['Nome'].str.contains(busca_ativo, case=False, na=False)
        ]
    
    if len(df_filtrado) == 0:
        st.warning("⚠️ Nenhum ativo encontrado com os filtros aplicados.")
    else:
        # Calcular métricas gerais
        total_investido = df_filtrado['vlr_investido'].sum()
        total_mercado = df_filtrado['vlr_mercado'].sum()
        lucro_total = df_filtrado['lucro_total'].sum()
        lucro_pct = (lucro_total / total_investido) * 100 if total_investido > 0 else 0
        
        # XIRR médio ponderado
        df_filtrado_xirr = df_filtrado[df_filtrado['xirr'].notna()]
        if len(df_filtrado_xirr) > 0:
            xirr_carteira = (df_filtrado_xirr['xirr'] * df_filtrado_xirr['vlr_investido']).sum() / df_filtrado_xirr['vlr_investido'].sum()
        else:
            xirr_carteira = 0
        
        # Cards de métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Total Investido", formatar_moeda(total_investido))
        
        with col2:
            st.metric("📈 Patrimônio Atual", formatar_moeda(total_mercado))
        
        with col3:
            st.metric(
                "💵 Lucro Total",
                formatar_moeda(lucro_total),
                delta=f"{lucro_pct:.2f}%".replace(".", ",")
            )
        
        with col4:
            st.metric("📊 XIRR Médio", f"{xirr_carteira:.2f}%".replace(".", ","))
        
        st.markdown("---")
        
        # Tabela Interativa de Ativos
        st.subheader("📋 Tabela de Ativos")
        
        # Preparar dados para exibição
        df_exibicao = df_filtrado[['ativo', 'Nome', 'Tipo', 'vlr_investido', 'vlr_mercado', 'lucro_total', 'lucro_total_pct', 'xirr']].copy()
        
        # Calcular % do portfólio
        df_exibicao['% Carteira'] = (df_exibicao['vlr_mercado'] / total_mercado) * 100
        
        # Formatar colunas
        df_exibicao['vlr_investido_fmt'] = df_exibicao['vlr_investido'].apply(formatar_moeda)
        df_exibicao['vlr_mercado_fmt'] = df_exibicao['vlr_mercado'].apply(formatar_moeda)
        df_exibicao['lucro_total_fmt'] = df_exibicao['lucro_total'].apply(formatar_moeda)
        df_exibicao['lucro_total_pct_fmt'] = df_exibicao['lucro_total_pct'].apply(lambda x: f"{x:.2f}%".replace(".", ","))
        df_exibicao['xirr_fmt'] = df_exibicao['xirr'].apply(lambda x: f"{x:.2f}%".replace(".", ",") if pd.notna(x) else "N/A")
        df_exibicao['% Carteira_fmt'] = df_exibicao['% Carteira'].apply(lambda x: f"{x:.2f}%".replace(".", ","))
        
        # Selecionar colunas finais
        df_exibicao_final = df_exibicao[['ativo', 'Nome', 'Tipo', 'vlr_investido_fmt', 'vlr_mercado_fmt', 
                                          'lucro_total_fmt', 'lucro_total_pct_fmt', 'xirr_fmt', '% Carteira_fmt']]
        
        df_exibicao_final.columns = ['Ativo', 'Nome', 'Tipo', 'Investido', 'Valor Mercado', 'Lucro', 'Lucro %', 'XIRR', '% Carteira']
        
        st.dataframe(
            df_exibicao_final,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Linha de totais
        st.markdown("**Totais:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Total Investido:** {formatar_moeda(total_investido)}")
        with col2:
            st.write(f"**Total Mercado:** {formatar_moeda(total_mercado)}")
        with col3:
            st.write(f"**Lucro Total:** {formatar_moeda(lucro_total)} ({lucro_pct:.2f}%)".replace(".", ","))
        
        st.markdown("---")
        
        # Gráfico 1: Treemap
        st.subheader("🗺️ Distribuição do Portfólio")
        
        fig1 = px.treemap(
            df_filtrado,
            path=['Tipo', 'classe', 'ativo'],
            values='vlr_mercado',
            color='lucro_total_pct',
            color_continuous_scale=['red', 'yellow', 'green'],
            color_continuous_midpoint=0,
            title="Hierarquia: Tipo > Classe > Ativo (Tamanho: Valor Mercado | Cor: Rentabilidade %)"
        )
        
        fig1.update_layout(height=600)
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Top 10 Ativos
        st.subheader("🏆 Top 10 Ativos por Participação")
        
        df_top10 = df_filtrado.nlargest(10, 'vlr_mercado').copy()
        df_top10['% Carteira'] = (df_top10['vlr_mercado'] / total_mercado) * 100
        df_top10 = df_top10.sort_values('% Carteira')
        
        fig2 = px.bar(
            df_top10,
            x='% Carteira',
            y='ativo',
            orientation='h',
            title="Top 10 Maiores Posições (% do Portfólio)",
            text='% Carteira'
        )
        
        fig2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig2.update_layout(height=500, xaxis_title="% da Carteira", yaxis_title="Ativo")
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Gráfico 3: Rentabilidade vs Alocação
        st.subheader("📊 Rentabilidade vs Alocação")
        
        df_scatter = df_filtrado[df_filtrado['xirr'].notna()].copy()
        df_scatter['% Carteira'] = (df_scatter['vlr_mercado'] / total_mercado) * 100
        
        fig3 = px.scatter(
            df_scatter,
            x='% Carteira',
            y='xirr',
            size='vlr_mercado',
            color='Tipo',
            hover_data=['ativo', 'Nome'],
            title="Rentabilidade (XIRR) vs Alocação (% da Carteira)",
            labels={'xirr': 'XIRR (%)', '% Carteira': '% da Carteira'}
        )
        
        fig3.update_layout(height=500)
        
        st.plotly_chart(fig3, use_container_width=True)
