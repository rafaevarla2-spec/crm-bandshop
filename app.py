import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="CRM Prospecção Band", layout="wide")

st.title("📊 CRM de Prospecção & Vendas")
st.markdown("---")

# Função para carregar os dados (Simulação baseada no seu arquivo real)
def load_data():
    # Aqui criamos uma amostra baseada no seu "CRM - HUNTING"
    data = {
        'Analista': ['Adriana', 'Varela', 'Adriana', 'Varela', 'Adriana', 'Adriana'],
        'Seller': ['Tok & stok', 'Chico Rei', 'Via varejo', 'Electrolux', 'Malwee', 'Mondial'],
        'Categoria': ['Móveis', 'Moda', 'Magazine', 'Eletrodoméstico', 'Moda', 'Eletro'],
        'Fúnil': ['Standby', 'Proposta Enviada', 'Negociação', 'Contrato', 'Em Prospecção', 'Perdida'],
        'Potencial de venda': ['AA', 'AA', 'AA', 'AAA', 'AA', 'A'],
        'Valor_Est': [150000, 45000, 300000, 500000, 80000, 25000]
    }
    return pd.DataFrame(data)

df = load_data()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/pt/d/d3/Band_Logo.png", width=100)
st.sidebar.header("Filtros do Dashboard")

analista_f = st.sidebar.multiselect("Filtrar por Analista", df['Analista'].unique(), default=df['Analista'].unique())
funil_f = st.sidebar.multiselect("Status do Funil", df['Fúnil'].unique(), default=df['Fúnil'].unique())

# Aplicar filtros
df_filtered = df[(df['Analista'].isin(analista_f)) & (df['Fúnil'].isin(funil_f))]

# --- DASHBOARD (KPIs) ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total de Leads", len(df_filtered))
kpi2.metric("Oportunidades em Aberto", len(df_filtered[df_filtered['Fúnil'] != 'Perdida']))
kpi3.metric("Ticket Médio (Est.)", f"R$ {df_filtered['Valor_Est'].mean():,.2f}")

st.markdown("---")

# --- GRÁFICOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Funil de Vendas")
    fig_funil = px.funnel(df_filtered.groupby("Fúnil").size().reset_index(name='Qtd'), x='Qtd', y='Fúnil', color='Fúnil')
    st.plotly_chart(fig_funil, use_container_width=True)

with col2:
    st.subheader("Volume por Categoria")
    fig_pie = px.pie(df_filtered, values='Valor_Est', names='Categoria', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- TABELA INTERATIVA ---
st.subheader("📋 Lista de Sellers (Filtro Dinâmico)")
st.dataframe(df_filtered, use_container_width=True)

st.success("CRM pronto para uso. Para atualizar com dados reais, basta subir seu Excel no repositório!")
