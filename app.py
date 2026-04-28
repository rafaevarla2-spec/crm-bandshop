import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
# Configuração visual
st.set_page_config(page_title="CRM Moderno - Band", layout="wide")

st.title("📊 CRM de Prospecção & Vendas")

# Tenta carregar o arquivo real. Se não existir, usa dados de exemplo.
try:
    # Ajuste o nome do arquivo abaixo se você subir o Excel para o GitHub
    df = pd.read_excel("CRM - Prospecção - nova base (2).xlsx", sheet_name="CRM")
    st.sidebar.success("✅ Dados reais carregados!")
except:
    st.sidebar.warning("⚠️ Usando dados de demonstração. Suba seu CSV no GitHub para atualizar.")
    data = {
        'Analista': ['Adriana', 'Varela', 'Adriana', 'Varela', 'Adriana', 'Varela'],
        'Seller': ['Tok & Stok', 'Chico Rei', 'Via Varejo', 'Electrolux', 'Malwee', 'Mondial'],
        'Fúnil': ['Standby', 'Proposta Enviada', 'Negociação', 'Contrato', 'Em Prospecção', 'Negociação'],
        'Valor_Est': [150000, 45000, 300000, 500000, 80000, 120000],
        'Categoria': ['Móveis', 'Moda', 'Magazine', 'Eletrodoméstico', 'Moda', 'Eletro']
    }
    df = pd.DataFrame(data)

# --- FILTROS LATERAIS ---
st.sidebar.header("Filtros")
analista_f = st.sidebar.multiselect("Vendedor", df['Analista'].unique(), default=df['Analista'].unique())
status_f = st.sidebar.multiselect("Etapa do Funil", df['Fúnil'].unique(), default=df['Fúnil'].unique())

df_filtered = df[(df['Analista'].isin(analista_f)) & (df['Fúnil'].isin(status_f))]

# --- DASHBOARD ---
c1, c2, c3 = st.columns(3)
c1.metric("Total de Leads", len(df_filtered))
c2.metric("Contratos Fechados", len(df_filtered[df_filtered['Fúnil'] == 'Contrato']))
c3.metric("Ticket Médio", f"R$ {df_filtered['Valor_Est'].mean():,.2f}")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Funil de Vendas")
    fig = px.funnel(df_filtered.groupby("Fúnil").size().reset_index(name='Qtd'), x='Qtd', y='Fúnil')
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Performance por Analista")
    fig2 = px.bar(df_filtered, x="Analista", y="Valor_Est", color="Fúnil", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 Base de Dados Interativa")
st.dataframe(df_filtered, use_container_width=True)
