import streamlit as st
import pandas as pd
import calendar as py_calendar
from datetime import date, timedelta
import os
import base64

# 1. Configuração da página
st.set_page_config(page_title="CRM Dottz", page_icon="logo.png", layout="wide")

# --- SISTEMA DE LOGIN DE UTILIZADORES ---
USERS = {
    "amcabral": "DBS2027",
    "alcastro": "DBS2027"
}

# --- CONFIGURAÇÃO DOS CAMINHOS DAS PASTAS (CORRIGIDO PARA A CLOUD) ---
DB_PATH = "leads_database.csv"
TODO_PATH = "todo_database.csv"
PAYMENTS_PATH = "payments_database.csv"
INSTALLMENTS_PATH = "installments_database.csv"
KPI_PATH = "kpis_database.csv"
ALCA_PATH = "alca_database.csv" # Alterado LIG para ALCA
TCT_PATH = "tct_database.csv"
FAMO_PATH = "famo_database.csv" # Novo caminho adicionado para a FAMO
BUILDERS_PATH = "builders_database.csv"
ARCHITECTS_PATH = "architects_database.csv"

ATTACHMENTS_DIR = "Anexos"
LOGO_PATH = "logo.png"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

if not st.session_state["logged_in"]:
    logo_b64 = get_base64_of_bin_file(LOGO_PATH)
    
    st.markdown(
        """
        <style>
        /* Fundo totalmente branco */
        .stApp { background-color: #FFFFFF !important; }
        header { visibility: hidden !important; }
        
        /* Limpar as caixas extra e formatações base do Streamlit */
        [data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
            max-width: 350px !important;
            margin: 0 auto !important;
        }
        
        /* Estilização minimalista dos inputs (com texto ao centro) */
        [data-testid="stForm"] input {
            background-color: #F8F9FA !important;
            border: 1px solid #E0E0E0 !important;
            color: #333333 !important;
            border-radius: 6px !important;
            padding: 14px !important;
            text-align: center !important;
            font-size: 16px !important;
            margin-bottom: 10px !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stForm"] input:focus {
            border-color: #7B2CBF !important;
            box-shadow: 0 0 0 1px #7B2CBF !important;
            background-color: #FFFFFF !important;
        }
        
        /* Estilização EXCLUSIVA do botão de submeter (evita estragar o botão do "olho" da password) */
        [data-testid="stFormSubmitButton"] button {
            background-color: #7B2CBF !important;
            color: #FFFFFF !important;
            font-weight: bold !important;
            border-radius: 6px !important;
            border: none !important;
            width: 100% !important;
            padding: 12px !important;
            margin-top: 15px !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            background-color: #5B2C83 !important;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    # Espaçamento para centrar verticalmente na página
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # Três colunas para trancar o login no centro do ecrã
    _, col_center, _ = st.columns([1, 1, 1])
    
    with col_center:
        # Logótipo da Dottz centrado
        if logo_b64:
            st.markdown(f"<div style='text-align: center; margin-bottom: 35px;'><img src='data:image/png;base64,{logo_b64}' style='max-width: 250px;'></div>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; color: #5B2C83; margin-bottom: 35px;'>DOTTZ CRM</h2>", unsafe_allow_html=True)
            
        # Formulário com Placeholders e Labels Invisíveis
        with st.form("login_form"):
            user_input = st.text_input("Utilizador", placeholder="Username", label_visibility="collapsed")
            pass_input = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            submit_login = st.form_submit_button("ENTRAR NO CRM", use_container_width=True)

            if submit_login:
                if user_input in USERS and USERS[user_input] == pass_input:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = user_input
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
                    
    st.stop()


# --- CSS E DESIGN (MODO LOGADO) ---
st.markdown(
    """
    <style>
    body, p, label, input, textarea, select, button, code { font-family: "Agency FB", "Bahnschrift", "Segoe UI Variable", sans-serif !important; }
    h1, h2, h3, h4, h5, h6 { font-family: "Agency FB", "Bahnschrift", sans-serif !important; font-weight: 700 !important; }
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText { color: #000000 !important; }
    input, textarea, div[data-baseweb="select"] > div { background-color: #F8F9FA !important; color: #000000 !important; border: 1px solid #CCCCCC !important; }
    button[data-baseweb="tab"] p { color: #666666 !important; }
    button[data-baseweb="tab"][aria-selected="true"] p { color: #000000 !important; font-weight: bold !important; }
    [data-testid="stDataFrame"] div, [data-testid="stDataFrame"] span { color: #000000 !important; }
    .stTabs [role="tablist"] { justify-content: center; flex-wrap: wrap; }
    .stTabs [data-testid="stTab"] p { font-size: 1.1em !important; }
    .stTabs [data-testid="stTab"] .react-aria-SelectionIndicator { background-color: #7B2CBF !important; }
    
    /* BOTÃO DE LOGOUT SUPERIOR ESQUERDO MINIMALISTA E INVISÍVEL */
    .st-key-btn_logout {
        position: absolute;
        top: -40px; 
        left: 10px;
        z-index: 999999;
    }
    .st-key-btn_logout button {
        background-color: transparent !important;
        border: none !important;
        color: #C0C0C0 !important; 
        font-size: 12px !important;
        font-weight: 300 !important;
        opacity: 0.4 !important;
        box-shadow: none !important;
        padding: 5px !important;
    }
    .st-key-btn_logout button:hover {
        color: #000000 !important;
        opacity: 1 !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True
)

if st.button("log out", key="btn_logout"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()

EMPRESAS_CONSTRUCAO = [f"Empresa de Construção {i}" for i in range(1, 6)]
DATAS_ORCAMENTO = [f"Data de Entrega do Orçamento {i}" for i in range(1, 6)]
VALORES_ORCAMENTO = [f"Valor do Orçamento {i}" for i in range(1, 6)]
FOLLOW_UPS_EMPRESA = [f"Follow up Empresa {i}" for i in range(1, 6)]
ANEXOS_EMPRESA = [f"Anexo Empresa {i}" for i in range(1, 6)]
COLUNA_ARQUITECTO = "Arquitecto"
COLUNA_ANEXO_PROJETO = "Anexo Projeto"

FASES_ATUAIS = ["⚪ Em Análise", "🟡 Em Concurso", "🟣 Em Negociação", "🟢 Adjudicado", "🔴 Não Adjudicado"]
ESTADOS_PAGAMENTO = ["⚪ Não facturado", "🟡 Fatura por pagar", "🟢 Recebido"]

# CRIAR PASTAS SE NÃO EXISTIREM
if not os.path.exists(ATTACHMENTS_DIR): os.makedirs(ATTACHMENTS_DIR)

def get_clean_list(df, col):
    if col not in df.columns: return ["Todos"]
    raw = df[col].dropna().astype(str).unique()
    clean = sorted([str(x).strip() for x in raw if str(x).strip() != "" and str(x).strip().lower() != "nan"])
    return ["Todos"] + clean

def parse_currency(val):
    try:
        if pd.isna(val) or val == "": return 0.0
        if isinstance(val, (int, float)): return float(val)
        s = str(val).replace("€", "").strip()
        if "apurar" in s.lower(): return 0.0
        s = s.replace("<", "").replace(">", "").strip()
        if "-" in s: s = s.split("-")[0]
        s = s.replace(" ", "")
        if "." in s and "," in s:
            if s.rfind(".") > s.rfind(","): s = s.replace(",", "")
            else: s = s.replace(".", "").replace(",", ".")
        elif "," in s: s = s.replace(",", ".")
        elif "." in s:
            parts = s.split(".")
            if len(parts) > 1 and len(parts[-1]) == 3: s = s.replace(".", "")
        return float(s)
    except: return 0.0

def save_uploaded_file(uploaded_file, prefix):
    if uploaded_file is not None:
        safe_name = "".join([c for c in uploaded_file.name if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '-')]).rstrip()
        file_path = os.path.join(ATTACHMENTS_DIR, f"{prefix}_{safe_name}")
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
        return file_path
    return None

def sync_financial_math(df):
    changed = False
    if df.empty: return df, changed
    
    # Correção Definitiva: Limpeza da coluna 'Inter' feita de uma vez só e fora do ciclo
    if "Inter" in df.columns:
        old_inter = df["Inter"].astype(str).copy()
        df["Inter"] = df["Inter"].fillna("").astype(str).replace(["nan", "None", "<NA>", "NaN"], "")
        if not df["Inter"].astype(str).equals(old_inter):
            changed = True
            
    for idx in df.index:
        if "Valor Estimado" not in df.columns: continue
        v_est = parse_currency(df.at[idx, "Valor Estimado"])
        p_dbs = pd.to_numeric(df.at[idx, "% DBS"], errors="coerce") if "% DBS" in df.columns else 0.0
        p_int = pd.to_numeric(df.at[idx, "% Inter"], errors="coerce") if "% Inter" in df.columns else 0.0
        if pd.isna(p_dbs): p_dbs = 0.0
        if pd.isna(p_int): p_int = 0.0
        
        calc_dbs = v_est * (p_dbs / 100.0)
        calc_int = v_est * (p_int / 100.0)
        
        if df.at[idx, "Valor Estimado"] != v_est: df.at[idx, "Valor Estimado"] = v_est; changed = True
        if "% DBS" in df.columns and df.at[idx, "% DBS"] != p_dbs: df.at[idx, "% DBS"] = p_dbs; changed = True
        if "% Inter" in df.columns and df.at[idx, "% Inter"] != p_int: df.at[idx, "% Inter"] = p_int; changed = True
            
        if "Valor da % DBS" in df.columns:
            atual_dbs = pd.to_numeric(df.at[idx, "Valor da % DBS"], errors="coerce")
            if pd.isna(atual_dbs): atual_dbs = 0.0
            if round(calc_dbs, 2) != round(atual_dbs, 2): df.at[idx, "Valor da % DBS"] = calc_dbs; changed = True
                
        if "Valor da % Inter" in df.columns:
            atual_int = pd.to_numeric(df.at[idx, "Valor da % Inter"], errors="coerce")
            if pd.isna(atual_int): atual_int = 0.0
            if round(calc_int, 2) != round(atual_int, 2): df.at[idx, "Valor da % Inter"] = calc_int; changed = True
            
    return df, changed

def load_data():
    if os.path.exists(DB_PATH):
        df = pd.read_csv(DB_PATH)
        if "Próximo Follow-up" in df.columns: df["Próximo Follow-up"] = pd.to_datetime(df["Próximo Follow-up"]).dt.date
        for col in FOLLOW_UPS_EMPRESA:
            if col in df.columns: df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
        return df
    return pd.DataFrame(columns=["ID", "Cliente", "Projeto", COLUNA_ARQUITECTO, "Fase", "Valor Estimado", "Próximo Follow-up", "Notas", COLUNA_ANEXO_PROJETO, *EMPRESAS_CONSTRUCAO, *DATAS_ORCAMENTO, *VALORES_ORCAMENTO, *FOLLOW_UPS_EMPRESA, *ANEXOS_EMPRESA, "% DBS", "Valor da % DBS", "Inter", "% Inter", "Valor da % Inter"])

def save_data(df): df.to_csv(DB_PATH, index=False)

def guardar_campo_projeto(project_id, column_name, widget_key, is_currency=False):
    indice = st.session_state.leads_db.index[st.session_state.leads_db["ID"] == project_id][0]
    valor = st.session_state[widget_key]
    if is_currency: valor = parse_currency(valor)
    st.session_state.leads_db.at[indice, column_name] = valor if valor is not None else ""
    st.session_state.leads_db, _ = sync_financial_math(st.session_state.leads_db)
    save_data(st.session_state.leads_db)

def normalize_builder_columns(df):
    if "Empresa" not in df.columns: return df, False
    df = df.copy()
    if "Nome" in df.columns:
        nome_atual = df["Nome"].astype("string").str.strip()
        sem_nome = nome_atual.isna() | nome_atual.eq("")
        df.loc[sem_nome, "Nome"] = df.loc[sem_nome, "Empresa"]
        df = df.drop(columns="Empresa")
    else: df = df.rename(columns={"Empresa": "Nome"})
    return df, True

def listar_nomes_arquitectos():
    if "architects_db" not in st.session_state: return []
    arquitectos = st.session_state.architects_db
    if "Nome" not in arquitectos.columns: return []
    nomes = arquitectos["Nome"].dropna().astype(str).str.strip()
    return sorted(nomes[nomes != ""].unique().tolist())

def load_contact_data(file_name):
    file_path = file_name
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        if file_name == "builders_database.csv":
            data, renamed = normalize_builder_columns(data)
            if renamed: save_contact_data(data, file_name)
        return data
    return pd.DataFrame()

def save_contact_data(df, file_name):
    file_path = file_name
    df.to_csv(file_path, index=False, encoding="utf-8-sig")

# --- FUNÇÃO ATUALIZADA: SEM IMPORTAÇÃO CSV ---
def render_contact_tab(tab, title, state_key, file_name, fields, submit_label, allow_manual_add=True, col_config=None, filter_distrito=False, filter_alvara=False):
    with tab:
        st.markdown(f"### {title}")
        st.caption("Usa os filtros para procurar e editar registos. Adiciona novos através do botão abaixo.")
        editor_version_key = f"{state_key}_editor_version"
        form_version_key = f"{state_key}_form_version"
        st.session_state.setdefault(editor_version_key, 0)
        st.session_state.setdefault(form_version_key, 0)

        if allow_manual_add:
            with st.expander("➕ Adicionar Individualmente"):
                with st.form(f"{state_key}_entry_form_{st.session_state[form_version_key]}"):
                    values = {field: st.text_input(field, key=f"{state_key}_{st.session_state[form_version_key]}_{field}") for field in fields}
                    submitted = st.form_submit_button(submit_label)

                if submitted:
                    if not values.get("Nome", "").strip():
                        st.warning("O campo Nome é obrigatório.")
                    else:
                        new_row = {f: values[f] for f in fields}
                        for c in st.session_state[state_key].columns:
                            if c not in new_row:
                                if c in ["Contactado", "Interessado", "Parceria", "Projectos"]: new_row[c] = "🔴 Não"
                                else: new_row[c] = ""
                        new_data = pd.concat([st.session_state[state_key], pd.DataFrame([new_row])], ignore_index=True, sort=False)
                        st.session_state[state_key] = new_data
                        save_contact_data(new_data, file_name)
                        st.session_state[editor_version_key] += 1
                        st.session_state[form_version_key] += 1
                        st.success("Registo adicionado e guardado.")

        contact_data = st.session_state[state_key]
        if len(contact_data.columns) > 0:
            df_display = contact_data.copy()

            if filter_distrito or filter_alvara:
                st.markdown("**Filtros de Pesquisa:**")
                fc1, fc2 = st.columns(2)
                if filter_distrito and "Distrito" in df_display.columns:
                    distritos = get_clean_list(df_display, "Distrito")
                    f_dist = fc1.selectbox("Filtrar por Distrito", distritos, key=f"filt_dist_{state_key}")
                    if f_dist != "Todos": df_display = df_display[df_display["Distrito"] == f_dist]
                if filter_alvara and "Alvará" in df_display.columns:
                    f_alv = fc2.text_input("Pesquisar por Alvará", key=f"filt_alv_{state_key}")
                    if f_alv.strip(): df_display = df_display[df_display["Alvará"].astype(str).str.contains(f_alv.strip(), case=False, na=False)]

            edited_data = st.data_editor(df_display, column_config=col_config, use_container_width=True, hide_index=True, num_rows="dynamic" if allow_manual_add else "fixed", key=f"{state_key}_editor_{st.session_state[editor_version_key]}")

            if not edited_data.equals(df_display):
                st.session_state[state_key].update(edited_data)
                new_rows = edited_data.loc[~edited_data.index.isin(st.session_state[state_key].index)]
                if not new_rows.empty: st.session_state[state_key] = pd.concat([st.session_state[state_key], new_rows])
                deleted_indices = df_display.index.difference(edited_data.index)
                if not deleted_indices.empty: st.session_state[state_key] = st.session_state[state_key].drop(deleted_indices)
                st.session_state[state_key] = st.session_state[state_key].reset_index(drop=True)
                save_contact_data(st.session_state[state_key], file_name)
                st.rerun()
        else:
            st.info("Ainda não existem registos. Adiciona um contacto para começar.")

# --- INICIALIZAR TODAS AS BASES DE DADOS E SINCRONIZAR FÓRMULAS ---
if "leads_db" not in st.session_state: st.session_state.leads_db = load_data()

colunas_construcao_novas = [COLUNA_ARQUITECTO, COLUNA_ANEXO_PROJETO, *EMPRESAS_CONSTRUCAO, *DATAS_ORCAMENTO, *VALORES_ORCAMENTO, *FOLLOW_UPS_EMPRESA, *ANEXOS_EMPRESA, "% DBS", "Valor da % DBS", "Inter", "% Inter", "Valor da % Inter"]
for coluna in [c for c in colunas_construcao_novas if c not in st.session_state.leads_db.columns]:
    st.session_state.leads_db[coluna] = ""
for coluna in DATAS_ORCAMENTO + FOLLOW_UPS_EMPRESA:
    st.session_state.leads_db[coluna] = pd.to_datetime(st.session_state.leads_db[coluna], errors="coerce").dt.date
for coluna in VALORES_ORCAMENTO:
    st.session_state.leads_db[coluna] = pd.to_numeric(st.session_state.leads_db[coluna], errors="coerce")

fases_migracao = {
    "Nova Consulta": "⚪ Em Análise", "Qualificação": "⚪ Em Análise", "Proposta Entregue": "🟡 Em Concurso",
    "Em Análise": "⚪ Em Análise", "Em Concurso": "🟡 Em Concurso", "Em Negociação": "🟣 Em Negociação",
    "Negociação": "🟣 Em Negociação", "Fechado - Ganho": "🟢 Adjudicado", "Adjudicado": "🟢 Adjudicado",
    "Fechado - Perdido": "🔴 Não Adjudicado", "Não Adjudicado": "🔴 Não Adjudicado"
}
if "Fase" in st.session_state.leads_db.columns:
    st.session_state.leads_db["Fase"] = st.session_state.leads_db["Fase"].replace(fases_migracao).apply(lambda x: x if x in FASES_ATUAIS else "⚪ Em Análise")

st.session_state.leads_db, leads_changed = sync_financial_math(st.session_state.leads_db)
if leads_changed: save_data(st.session_state.leads_db)

cols_tct_base = ["Cliente", "Projeto", "Fase", "Valor Estimado", "% DBS", "Valor da % DBS", "Inter", "% Inter", "Valor da % Inter"]

if "tct_db" not in st.session_state:
    df_tct = pd.read_csv(TCT_PATH) if os.path.exists(TCT_PATH) else pd.DataFrame(columns=cols_tct_base)
    for col in cols_tct_base:
        if col not in df_tct.columns: df_tct[col] = None
    df_tct, changed_tct = sync_financial_math(df_tct)
    if changed_tct: df_tct.to_csv(TCT_PATH, index=False, encoding="utf-8-sig")
    st.session_state.tct_db = df_tct

# --- LIG MUDOU PARA ALCA ---
if "alca_db" not in st.session_state:
    df_alca = pd.read_csv(ALCA_PATH) if os.path.exists(ALCA_PATH) else pd.DataFrame(columns=cols_tct_base)
    for col in cols_tct_base:
        if col not in df_alca.columns: df_alca[col] = None
    df_alca, changed_alca = sync_financial_math(df_alca)
    if changed_alca: df_alca.to_csv(ALCA_PATH, index=False, encoding="utf-8-sig")
    st.session_state.alca_db = df_alca

# Inicialização da base de dados FAMO
if "famo_db" not in st.session_state:
    df_famo = pd.read_csv(FAMO_PATH) if os.path.exists(FAMO_PATH) else pd.DataFrame(columns=cols_tct_base)
    for col in cols_tct_base:
        if col not in df_famo.columns: df_famo[col] = None
    df_famo, changed_famo = sync_financial_math(df_famo)
    if changed_famo: df_famo.to_csv(FAMO_PATH, index=False, encoding="utf-8-sig")
    st.session_state.famo_db = df_famo


config_parcerias = {
    "Contactado": st.column_config.SelectboxColumn("Contactado", options=["🟢 Sim", "🔴 Não"], required=True),
    "Interessado": st.column_config.SelectboxColumn("Interessado", options=["🟢 Sim", "🔴 Não"], required=True),
    "Parceria": st.column_config.SelectboxColumn("Parceria", options=["🟢 Sim", "🔴 Não"], required=True),
    "Projectos": st.column_config.SelectboxColumn("Projectos", options=["🟢 Sim", "🔴 Não"], required=True)
}
colunas_parcerias = ["Contactado", "Interessado", "Parceria", "Projectos"]

# Arquitectos
if "architects_db" not in st.session_state:
    st.session_state.architects_db = load_contact_data("architects_database.csv")
    col_remover = ["Tipo", "Especialidades", "Concelho", "Morada", "Código Postal", "URL"]
    cols_del = [c for c in col_remover if c in st.session_state.architects_db.columns]
    if cols_del: st.session_state.architects_db = st.session_state.architects_db.drop(columns=cols_del)

bd_arq_changed = False
for col in ["Responsável"] + colunas_parcerias:
    if col not in st.session_state.architects_db.columns:
        st.session_state.architects_db[col] = "🔴 Não" if col in colunas_parcerias else ""
        bd_arq_changed = True

for col in colunas_parcerias:
    if st.session_state.architects_db[col].isna().any() or (st.session_state.architects_db[col] == "").any():
        st.session_state.architects_db[col] = st.session_state.architects_db[col].replace("", "🔴 Não").fillna("🔴 Não")
        bd_arq_changed = True

text_cols_arq = ["Nome", "Distrito", "Responsável", "Telefone", "Email"]
for col in text_cols_arq:
    if col in st.session_state.architects_db.columns:
        st.session_state.architects_db[col] = st.session_state.architects_db[col].astype(str).replace("nan", "").replace("None", "")

ordem_arq = ["Nome", "Distrito", "Responsável", "Telefone", "Email", "Contactado", "Interessado", "Parceria", "Projectos"]
cols_exist_arq = st.session_state.architects_db.columns.tolist()
nova_ordem_arq = [c for c in ordem_arq if c in cols_exist_arq] + [c for c in cols_exist_arq if c not in ordem_arq]
if cols_exist_arq != nova_ordem_arq:
    st.session_state.architects_db = st.session_state.architects_db[nova_ordem_arq]
    bd_arq_changed = True

if bd_arq_changed: save_contact_data(st.session_state.architects_db, "architects_database.csv")
nomes_arquitectos = listar_nomes_arquitectos()

# Construtores
if "builders_db" not in st.session_state:
    st.session_state.builders_db = load_contact_data("builders_database.csv")
st.session_state.builders_db, builders_columns_renamed = normalize_builder_columns(st.session_state.builders_db)

bd_builders_changed = False
for col in ["Contacto", "Função"] + colunas_parcerias:
    if col not in st.session_state.builders_db.columns:
        st.session_state.builders_db[col] = "🔴 Não" if col in colunas_parcerias else ""
        bd_builders_changed = True

for col in colunas_parcerias:
    if st.session_state.builders_db[col].isna().any() or (st.session_state.builders_db[col] == "").any():
        st.session_state.builders_db[col] = st.session_state.builders_db[col].replace("", "🔴 Não").fillna("🔴 Não")
        bd_builders_changed = True

text_cols_builders = ["Nome", "Alvará", "Contacto", "Função", "Telefone", "Email", "Distrito"]
for col in text_cols_builders:
    if col in st.session_state.builders_db.columns:
        st.session_state.builders_db[col] = st.session_state.builders_db[col].astype(str).replace("nan", "").replace("None", "")

config_parcerias_const = config_parcerias.copy()
config_parcerias_const["Contacto"] = st.column_config.TextColumn("Contacto", disabled=False)
config_parcerias_const["Função"] = st.column_config.TextColumn("Função", disabled=False)

ordem_desejada_builders = ["Nome", "Alvará", "Contacto", "Função", "Telefone", "Email", "Distrito", "Contactado", "Interessado", "Parceria", "Projectos"]
cols_existentes_b = st.session_state.builders_db.columns.tolist()
nova_ordem_b = [c for c in ordem_desejada_builders if c in cols_existentes_b] + [c for c in cols_existentes_b if c not in ordem_desejada_builders]

if cols_existentes_b != nova_ordem_b:
    st.session_state.builders_db = st.session_state.builders_db[nova_ordem_b]
    bd_builders_changed = True

if builders_columns_renamed or bd_builders_changed:
    save_contact_data(st.session_state.builders_db, "builders_database.csv")

# To Do List 
if "todo_db" not in st.session_state:
    if os.path.exists(TODO_PATH):
        df_todo = pd.read_csv(TODO_PATH, dtype={"Próximos passos": str})
        if "Projeto" in df_todo.columns: df_todo = df_todo.rename(columns={"Projeto": "Tarefa"})
        if "Tarefa" not in df_todo.columns: df_todo["Tarefa"] = ""
        df_todo["Tarefa"] = df_todo["Tarefa"].fillna("").astype(str)
        df_todo["Próximos passos"] = df_todo["Próximos passos"].fillna("").astype(str)
        if "Follow up" in df_todo.columns: df_todo["Follow up"] = pd.to_datetime(df_todo["Follow up"], errors="coerce").dt.date
    else:
        df_todo = pd.DataFrame(columns=["Tarefa", "Próximos passos", "Follow up"])
    st.session_state.todo_db = df_todo

# Pagamentos - Overview 
col_base_pagamentos = ["Projeto", "Valor Global", "Data de Início", "Data Final", "Meses de duração", "Valor mensal"]
if "payments_db" not in st.session_state:
    if os.path.exists(PAYMENTS_PATH):
        df_pag = pd.read_csv(PAYMENTS_PATH)
        cols_to_keep = [c for c in col_base_pagamentos if c in df_pag.columns]
        df_pag = df_pag[cols_to_keep]
        for col in col_base_pagamentos:
            if col not in df_pag.columns: df_pag[col] = None
        df_pag["Projeto"] = df_pag["Projeto"].fillna("").astype(str)
        df_pag["Valor Global"] = pd.to_numeric(df_pag["Valor Global"], errors="coerce").fillna(0.0)
        df_pag["Meses de duração"] = pd.to_numeric(df_pag["Meses de duração"], errors="coerce").fillna(1).astype(int)
        df_pag["Valor mensal"] = pd.to_numeric(df_pag["Valor mensal"], errors="coerce").fillna(0.0)
        st.session_state.payments_db = df_pag
    else:
        st.session_state.payments_db = pd.DataFrame(columns=col_base_pagamentos)

# Installments - Pagamentos Mensais Discriminados
cols_inst = ["Projeto", "Mês", "Mensalidade (€)", "IVA (%)", "Valor com IVA (€)", "IVA IF", "Estado"]
if "installments_db" not in st.session_state:
    if os.path.exists(INSTALLMENTS_PATH):
        df_inst = pd.read_csv(INSTALLMENTS_PATH)
        if "Valor" in df_inst.columns: df_inst.rename(columns={"Valor": "Mensalidade (€)"}, inplace=True)
        for c in cols_inst:
            if c not in df_inst.columns: df_inst[c] = ""
        df_inst["Mensalidade (€)"] = pd.to_numeric(df_inst["Mensalidade (€)"], errors="coerce").fillna(0.0)
        df_inst["IVA (%)"] = pd.to_numeric(df_inst["IVA (%)"], errors="coerce").fillna(23.0)
        df_inst["Valor com IVA (€)"] = pd.to_numeric(df_inst["Valor com IVA (€)"], errors="coerce").fillna(0.0)
        df_inst["IVA IF"] = df_inst["IVA IF"].astype(str).replace("nan", "").replace("None", "")
        mask_z = df_inst["Valor com IVA (€)"] == 0.0
        df_inst.loc[mask_z, "Valor com IVA (€)"] = df_inst.loc[mask_z, "Mensalidade (€)"] * (1 + df_inst.loc[mask_z, "IVA (%)"]/100.0)
        df_inst["Estado"] = df_inst["Estado"].replace({"⚪ Não facturados": "⚪ Não facturado", "🟡 Facturados e não pagos": "🟡 Fatura por pagar", "🟢 Facturados e pagos": "🟢 Recebido"})
        st.session_state.installments_db = df_inst
    else:
        st.session_state.installments_db = pd.DataFrame(columns=cols_inst)

if "kpi_db" not in st.session_state:
    if os.path.exists(KPI_PATH):
        st.session_state.kpi_db = pd.read_csv(KPI_PATH)
    else:
        kpi_data = {
            "Métricas Globais": [
                "Total de Parcerias com Arquitectos", "Total de Parcerias com Construtores",
                "Total de Projectos", "Total de Projectos Adjudicados", "Total de Valor Adjudicado (€)",
                "Total de Valor da % DBS (€)", "% de Valor (Adjudicado / Estimado) (%)"
            ],
            "KPIS 2027": [
                "Total de Parcerias com Arquitectos", "Total de Parcerias com Construtores",
                "Total de Projectos", "Total de Projectos Adjudicados", "Total de Valor Adjudicado (€)",
                "Total de Valor da % DBS (€)", "% de Valor (Adjudicado / Estimado) (%)"
            ],
            "Objetivo": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }
        st.session_state.kpi_db = pd.DataFrame(kpi_data)
        st.session_state.kpi_db.to_csv(KPI_PATH, index=False, encoding="utf-8-sig")

# --- CABEÇALHO COM LOGOTIPO ---
if os.path.exists(LOGO_PATH):
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        st.image(LOGO_PATH, width=250)
else:
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        st.warning("Para veres o logotipo aqui, guarda a imagem da Dottz na pasta 'CRM DOTTZ' com o nome 'logo.png'.")
st.markdown("<br>", unsafe_allow_html=True)

st.session_state.setdefault("crm_tabs", "Capturar e Enriquecer")

# --- DEFINIÇÃO E ORDENAÇÃO DAS ABAS (Parcerias removidas, LIG passou a ALCA) ---
tab_captura, tab_pipeline, tab_comunicacao, tab_arquitectos, tab_construtores, tab_tct, tab_alca, tab_famo, tab_calendario, tab_financeiro, tab_pagamentos, tab_todo, tab_objectivos = st.tabs([
    "Capturar e Enriquecer",
    "Pipeline de Negócios",
    "Interações & Follow-Ups",
    "Arquitectos",
    "Construtores",
    "TCT",
    "ALCA", 
    "FAMO", 
    "Calendário",
    "Financeiro",
    "Pagamentos",
    "To do List",
    "Objectivos"
])

# --- 1. CAPTURAR E ENRIQUECER ---
with tab_captura:
    st.markdown("### Nova Consulta")
    with st.form("form_nova_lead", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            novo_cliente = st.text_input("Nome do Cliente / Entidade")
            novo_email = st.text_input("Email de Contacto")
        with col2:
            novo_projeto = st.text_input("Nome/Localização do Projeto")
            novo_valor = st.number_input("Valor Estimado (€)", min_value=0.0, step=1000.0)
        novo_arquitecto = st.selectbox("Arquitecto", [""] + nomes_arquitectos, key="novo_projeto_arquitecto")
        notas_iniciais = st.text_area("Notas Iniciais / Enriquecimento")
        
        submitted = st.form_submit_button("Criar Oportunidade")
        
        if submitted and novo_cliente and novo_projeto:
            novo_id = 1 if st.session_state.leads_db.empty else int(st.session_state.leads_db["ID"].max()) + 1
            nova_linha = {
                "ID": novo_id, "Cliente": novo_cliente, "Projeto": novo_projeto, COLUNA_ARQUITECTO: novo_arquitecto,
                "Fase": "⚪ Em Análise", "Valor Estimado": float(novo_valor), "Próximo Follow-up": date.today() + timedelta(days=1),
                "Notas": notas_iniciais
            }
            st.session_state.leads_db = pd.concat([st.session_state.leads_db, pd.DataFrame([nova_linha])], ignore_index=True)
            st.session_state.leads_db, _ = sync_financial_math(st.session_state.leads_db)
            save_data(st.session_state.leads_db)
            st.toast("Oportunidade guardada no pipeline.")
            st.rerun()

# --- 2. PIPELINE DE NEGÓCIOS ---
with tab_pipeline:
    st.markdown("### Oportunidades em Curso")
    st.markdown("Move os negócios pelas diferentes fases e anexa documentação relevante.")

    cores_fase = {
        "⚪ Em Análise": ("#FFFFFF", "#000000"),
        "🟡 Em Concurso": ("#FFD700", "#000000"),
        "🟣 Em Negociação": ("#7B2CBF", "#FFFFFF"),
        "🟢 Adjudicado": ("#A5D6A7", "#000000"),
        "🔴 Não Adjudicado": ("#FF6B6B", "#000000")
    }
    
    proporcoes_colunas = [1.8, 1.4, 1.3, 1.8, 1.1, 1.3, 1.4]
    cabecalhos = ["Cliente", "Projeto", "Arquitecto", "Fase do Negócio", "Valor", "Follow up", "Anexo Projeto"]

    if not st.session_state.leads_db.empty:
        st.markdown("<style>.st-key-pipeline_header {background:transparent;color:#5B2C83;padding:0 8px;border-radius:4px;min-height:48px;display:flex;align-items:center;font-size:0.9rem;} .st-key-pipeline_header > div {width:100%;} .st-key-pipeline_header [data-testid=\"stMarkdownContainer\"] {text-align:center;} .st-key-pipeline_header p {color:#5B2C83 !important;text-align:center !important;font-size:0.9rem !important;font-weight:700 !important;line-height:1.1 !important;}</style>", unsafe_allow_html=True)
        with st.container(key="pipeline_header"):
            for coluna, cabecalho in zip(st.columns(proporcoes_colunas), cabecalhos):
                coluna.markdown(f"**{cabecalho}**")

        for indice, registo in st.session_state.leads_db.iterrows():
            id_registo = int(registo["ID"])
            margem_linha = "-24px" if indice != st.session_state.leads_db.index[-1] else "0px"
            margem_superior_linha = "-24px" if indice == st.session_state.leads_db.index[0] else "0px"
            chave_linha = f"pipeline_row_{id_registo}"
            chave_follow_up = f"pipeline_follow_up_{id_registo}"
            chave_fase = f"pipeline_fase_{id_registo}"
            fase_atual = registo["Fase"] if registo["Fase"] in FASES_ATUAIS else "⚪ Em Análise"
            cor_fundo, cor_texto = cores_fase[fase_atual]
            
            st.markdown(
                f"""<style>
                [data-testid="stLayoutWrapper"]:has(.st-key-{chave_linha}) {{margin-top:{margem_superior_linha} !important;margin-bottom:{margem_linha} !important;}}
                .st-key-{chave_linha} {{background:transparent;color:#222;padding:0 8px;border-radius:4px;display:flex;align-items:center;font-size:0.9rem;line-height:1.1;}}
                .st-key-{chave_linha} > div {{width:100%;}}
                .st-key-{chave_linha} p, .st-key-{chave_linha} code {{color:#222 !important;text-align:center !important;font-size:0.9rem !important;line-height:1.1 !important;}}
                .st-key-{chave_linha} input {{background:#F8F9FA !important;color:#222 !important;text-align:center !important;border-color:#CCCCCC !important;font-size:0.9rem !important;}}
                .st-key-{chave_follow_up} {{background:#15803D;color:#fff;padding:4px;border-radius:4px;}}
                .st-key-{chave_follow_up} p, .st-key-{chave_follow_up} code {{background:#15803D;color:#fff !important;text-align:center !important;font-size:0.9rem !important;}}
                .st-key-{chave_follow_up} input {{background:#15803D !important;color:#fff !important;text-align:center !important;border-color:#15803D !important;font-size:0.9rem !important;}}
                .st-key-{chave_fase} [data-testid="stSelectbox"] .react-aria-ComboBox > div {{background:{cor_fundo} !important;color:{cor_texto} !important;}}
                .st-key-{chave_fase} [data-testid="stSelectbox"] .react-aria-ComboBox input,
                .st-key-{chave_fase} [data-testid="stSelectbox"] .react-aria-ComboBox button {{background:{cor_fundo} !important;color:{cor_texto} !important;text-align:center !important;font-size:0.9rem !important;}}
                .st-key-{chave_linha} [data-testid="stColumn"] {{display:flex;flex-direction:column;justify-content:center;}}
                </style>""",
                unsafe_allow_html=True
            )
            
            with st.container(key=chave_linha):
                colunas = st.columns(proporcoes_colunas)
                cliente_atual = registo.get("Cliente", "")
                cliente_atual = "" if pd.isna(cliente_atual) else str(cliente_atual)
                
                with colunas[0]:
                    st.text_input(
                        "Cliente", value=cliente_atual, key=f"pipeline_cliente_{id_registo}", 
                        label_visibility="collapsed", on_change=guardar_campo_projeto, 
                        args=(id_registo, "Cliente", f"pipeline_cliente_{id_registo}")
                    )
                    
                projeto_atual = registo.get("Projeto", "")
                projeto_atual = "" if pd.isna(projeto_atual) else str(projeto_atual)
                
                with colunas[1]:
                    st.text_input(
                        "Projeto", value=projeto_atual, key=f"pipeline_projeto_{id_registo}", 
                        label_visibility="collapsed", on_change=guardar_campo_projeto, 
                        args=(id_registo, "Projeto", f"pipeline_projeto_{id_registo}")
                    )
                
                arquitecto_atual = registo.get(COLUNA_ARQUITECTO, "")
                arquitecto_atual = "" if pd.isna(arquitecto_atual) else str(arquitecto_atual)
                opcoes_arquitecto = [""] + nomes_arquitectos
                if arquitecto_atual and arquitecto_atual not in opcoes_arquitecto:
                    opcoes_arquitecto.append(arquitecto_atual)
                    
                with colunas[2]:
                    st.selectbox(
                        "Arquitecto", opcoes_arquitecto, index=opcoes_arquitecto.index(arquitecto_atual), 
                        key=f"pipeline_arquitecto_{id_registo}", label_visibility="collapsed", 
                        on_change=guardar_campo_projeto, args=(id_registo, COLUNA_ARQUITECTO, f"pipeline_arquitecto_{id_registo}")
                    )
                    
                with colunas[3]:
                    nova_fase = st.selectbox(
                        "Fase do Negócio", FASES_ATUAIS, index=FASES_ATUAIS.index(fase_atual), 
                        key=chave_fase, label_visibility="collapsed"
                    )
                    
                valor_estimado_atual = registo.get("Valor Estimado", 0.0)
                val_fmt = f"{int(parse_currency(valor_estimado_atual)):,} €".replace(",", " ")
                
                with colunas[4]:
                    st.text_input(
                        "Valor", value=val_fmt, key=f"pipeline_valor_{id_registo}", 
                        label_visibility="collapsed", on_change=guardar_campo_projeto, 
                        args=(id_registo, "Valor Estimado", f"pipeline_valor_{id_registo}", True)
                    )
                
                follow_up = registo.get("Próximo Follow-up", None)
                follow_up = None if pd.isna(follow_up) or follow_up == "" else pd.to_datetime(follow_up).date()
                
                with colunas[5].container(key=chave_follow_up):
                    st.date_input(
                        "Próximo Follow-up", value=follow_up, key=f"pipeline_followup_{id_registo}", 
                        label_visibility="collapsed", on_change=guardar_campo_projeto, 
                        args=(id_registo, "Próximo Follow-up", f"pipeline_followup_{id_registo}")
                    )
                
                with colunas[6]:
                    anexo_proj = registo.get(COLUNA_ANEXO_PROJETO, "")
                    if pd.notna(anexo_proj) and anexo_proj != "" and os.path.exists(str(anexo_proj)):
                        ca1, ca2 = st.columns([1, 1])
                        with ca1:
                            with open(anexo_proj, "rb") as f:
                                st.download_button("⬇️", f, file_name=os.path.basename(anexo_proj), key=f"dl_proj_{id_registo}")
                        with ca2:
                            if st.button("❌", key=f"del_proj_{id_registo}"):
                                st.session_state.leads_db.at[indice, COLUNA_ANEXO_PROJETO] = ""
                                save_data(st.session_state.leads_db)
                                st.rerun()
                    else:
                        upl = st.file_uploader("Anexo", key=f"upl_proj_{id_registo}", label_visibility="collapsed")
                        if upl:
                            path = save_uploaded_file(upl, f"proj_{id_registo}")
                            st.session_state.leads_db.at[indice, COLUNA_ANEXO_PROJETO] = path
                            save_data(st.session_state.leads_db)
                            st.rerun()

            if nova_fase != registo["Fase"]:
                st.session_state.leads_db.at[indice, "Fase"] = nova_fase
                save_data(st.session_state.leads_db)
                st.rerun()

        with st.expander("Editar outros dados da oportunidade"):
            colunas_protegidas = ["ID", "Cliente", "Projeto", COLUNA_ARQUITECTO, "Fase", "Próximo Follow-up", COLUNA_ANEXO_PROJETO, *EMPRESAS_CONSTRUCAO, *DATAS_ORCAMENTO, *VALORES_ORCAMENTO, *FOLLOW_UPS_EMPRESA, *ANEXOS_EMPRESA, "% DBS", "Valor da % DBS", "Inter", "% Inter", "Valor da % Inter"]
            
            col_cfg_exp = {col: None for col in colunas_protegidas}
            col_cfg_exp["Valor Estimado"] = st.column_config.NumberColumn("Valor Estimado", format="%.0f €", step=1000.0)
            
            edited_df = st.data_editor(st.session_state.leads_db, column_config=col_cfg_exp, use_container_width=True, hide_index=True, num_rows="fixed")
            if not edited_df.equals(st.session_state.leads_db):
                st.session_state.leads_db = edited_df
                st.session_state.leads_db, _ = sync_financial_math(st.session_state.leads_db)
                save_data(st.session_state.leads_db)
                st.rerun()

        st.markdown("---")
        st.markdown("### Ações de Gestão")
        col1, col2 = st.columns(2)
        with col1:
            csv = st.session_state.leads_db.to_csv(index=False).encode("utf-8")
            st.download_button("Exportar Base de Dados (CSV)", data=csv, file_name="exportacao_leads_dottz.csv", mime="text/csv")
        with col2:
            projetos_apagar = [""] + [f"{row['ID']} | Projeto: {row['Projeto']} | Cliente: {row['Cliente']}" for _, row in st.session_state.leads_db.iterrows()]
            lead_apagar = st.selectbox("Eliminar Registo de Projeto", projetos_apagar)
            if st.button("Eliminar Lead") and lead_apagar != "":
                try:
                    id_to_delete = int(lead_apagar.split(" | ")[0])
                    st.session_state.leads_db = st.session_state.leads_db[st.session_state.leads_db["ID"] != id_to_delete]
                    st.session_state.leads_db, _ = sync_financial_math(st.session_state.leads_db)
                    save_data(st.session_state.leads_db)
                    st.success("Registo do projeto eliminado com sucesso.")
                    st.rerun()
                except Exception as e:
                    st.error("Erro ao eliminar projeto.")
    else:
        st.info("Ainda não existem leads. Vá ao separador 'Capturar e Enriquecer' para criar a primeira.")

# --- 3. INTERAÇÕES E FOLLOW-UPS ---
with tab_comunicacao:
    st.markdown("### Registar Interação e Orçamentos")
    
    if not st.session_state.leads_db.empty:
        projeto_ids = st.session_state.leads_db["ID"].astype(int).tolist()
        projeto_preselecionado = st.session_state.get("selected_project_id")
        indice_projeto = projeto_ids.index(projeto_preselecionado) if projeto_preselecionado in projeto_ids else 0
        nomes_projetos = {int(registo["ID"]): f"{registo['Projeto']} | {registo['Cliente']}" for _, registo in st.session_state.leads_db.iterrows()}
        
        projeto_id = st.selectbox("Selecionar Projeto", projeto_ids, index=indice_projeto, key="interaction_project_id", format_func=nomes_projetos.get)
        idx = st.session_state.leads_db.index[st.session_state.leads_db["ID"] == projeto_id][0]
        projeto_selecionado = st.session_state.leads_db.at[idx, "Projeto"]
        historico_atual = st.session_state.leads_db.at[idx, "Notas"]

        construtores = st.session_state.builders_db
        empresas_disponiveis = sorted(construtores["Nome"].dropna().astype(str).str.strip().loc[lambda nomes: nomes != ""].unique().tolist()) if "Nome" in construtores.columns else []

        st.markdown(f"### Projeto: {projeto_selecionado}")
        st.markdown("### Empresas de Construção")

        id_projeto = int(st.session_state.leads_db.at[idx, "ID"])
        for numero, (coluna_empresa, coluna_data, coluna_valor, coluna_follow, coluna_anexo) in enumerate(zip(EMPRESAS_CONSTRUCAO, DATAS_ORCAMENTO, VALORES_ORCAMENTO, FOLLOW_UPS_EMPRESA, ANEXOS_EMPRESA), start=1):
            coluna_empresa_ui, coluna_data_ui, coluna_valor_ui, coluna_follow_ui, coluna_anexo_ui = st.columns([1.6, 1, 1.2, 1, 0.7])
            
            empresa_atual = st.session_state.leads_db.at[idx, coluna_empresa]
            empresa_atual = "" if pd.isna(empresa_atual) else str(empresa_atual)
            opcoes_empresa = [""] + empresas_disponiveis
            indice_empresa = opcoes_empresa.index(empresa_atual) if empresa_atual in opcoes_empresa else 0
            chave_empresa = f"empresa_projeto_{id_projeto}_{numero}"
            
            with coluna_empresa_ui:
                st.selectbox(f"Empresa de Construção {numero}", opcoes_empresa, index=indice_empresa, key=chave_empresa, on_change=guardar_campo_projeto, args=(id_projeto, coluna_empresa, chave_empresa))
            
            data_atual = st.session_state.leads_db.at[idx, coluna_data]
            data_atual = None if pd.isna(data_atual) or data_atual == "" else pd.to_datetime(data_atual).date()
            chave_data = f"data_orcamento_{id_projeto}_{numero}"
            with coluna_data_ui:
                st.date_input(f"Entrega {numero}", value=data_atual, key=chave_data, on_change=guardar_campo_projeto, args=(id_projeto, coluna_data, chave_data))
            
            valor_atual = st.session_state.leads_db.at[idx, coluna_valor]
            valor_atual = None if pd.isna(valor_atual) else float(valor_atual)
            chave_valor = f"valor_orcamento_{id_projeto}_{numero}"
            with coluna_valor_ui:
                st.number_input(f"Valor {numero}", min_value=0.0, value=valor_atual, step=1000.0, format="%.0f", placeholder="€", key=chave_valor, on_change=guardar_campo_projeto, args=(id_projeto, coluna_valor, chave_valor, True))
            
            follow_atual = st.session_state.leads_db.at[idx, coluna_follow]
            follow_atual = None if pd.isna(follow_atual) or follow_atual == "" else pd.to_datetime(follow_atual).date()
            chave_follow = f"follow_orcamento_{id_projeto}_{numero}"
            with coluna_follow_ui:
                st.date_input(f"Follow up", value=follow_atual, key=chave_follow, on_change=guardar_campo_projeto, args=(id_projeto, coluna_follow, chave_follow))
            
            with coluna_anexo_ui:
                st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                anexo_atual = st.session_state.leads_db.at[idx, coluna_anexo]
                if pd.notna(anexo_atual) and anexo_atual != "" and os.path.exists(str(anexo_atual)):
                    ca1, ca2 = st.columns([1, 1])
                    with ca1:
                        with open(anexo_atual, "rb") as f:
                            st.download_button("📥", f, file_name=os.path.basename(anexo_atual), key=f"dl_emp_{id_projeto}_{numero}")
                    with ca2:
                        if st.button("❌", key=f"del_emp_{id_projeto}_{numero}"):
                            st.session_state.leads_db.at[idx, coluna_anexo] = ""
                            save_data(st.session_state.leads_db)
                            st.rerun()
                else:
                    upl = st.file_uploader(f"Anexar a Empresa {numero}", key=f"upl_emp_{id_projeto}_{numero}", label_visibility="collapsed")
                    if upl:
                        path = save_uploaded_file(upl, f"emp{numero}_{id_projeto}")
                        st.session_state.leads_db.at[idx, coluna_anexo] = path
                        save_data(st.session_state.leads_db)
                        st.rerun()
        
        if pd.isna(historico_atual) or str(historico_atual).strip() == "": 
            historico_atual = "Sem interações anteriores."
        
        with st.expander("Ver Histórico Atual deste Projeto", expanded=True):
            st.text(historico_atual)
        
        with st.form("form_interacao", clear_on_submit=True):
            data_interacao = st.date_input("Data da Interação", date.today())
            tipo = st.selectbox("Tipo de Comunicação", ["Email", "Chamada", "Reunião Presencial", "Teams/Zoom", "WhatsApp"])
            resumo = st.text_area("Resumo da Conversa")
            novo_follow_up = st.date_input("Agendar Próximo Follow-up Global", date.today() + timedelta(days=3))
            
            if st.form_submit_button("Registar Interação"):
                historico_limpo = historico_atual if historico_atual != 'Sem interações anteriores.' else ''
                nova_nota = f"[{data_interacao.strftime('%d/%m/%Y')} {tipo}]: {resumo}\n{historico_limpo}"
                st.session_state.leads_db.at[idx, "Notas"] = nova_nota
                st.session_state.leads_db.at[idx, "Próximo Follow-up"] = novo_follow_up
                save_data(st.session_state.leads_db)
                st.success("Interação registada com sucesso!")
                st.rerun() 
    else:
        st.info("Ainda não existem leads no sistema.")

# --- 4. ARQUITECTOS ---
render_contact_tab(
    tab_arquitectos, "Arquitectos", "architects_db", "architects_database.csv", 
    ["Nome", "Distrito", "Responsável", "Telefone", "Email"], "Adicionar arquitecto", 
    allow_manual_add=True, col_config=config_parcerias, filter_distrito=True
)

# --- 5. CONSTRUTORES ---
render_contact_tab(
    tab_construtores, "Construtores", "builders_db", "builders_database.csv", 
    ["Nome", "Alvará", "Contacto", "Função", "Telefone", "Email", "Distrito"], "Adicionar empresa", 
    allow_manual_add=True, col_config=config_parcerias_const, filter_distrito=True, filter_alvara=True
)


# --- 6. TCT ---
with tab_tct:
    st.markdown("### Gestão TCT")
    st.caption("Tabela independente para a TCT. Podes adicionar novos registos em baixo.")
    
    df_tct = st.session_state.tct_db.copy()
    styled_tct = df_tct.style.map(lambda v: {"⚪ Em Análise": "background-color:#FFF;color:#000", "🟡 Em Concurso": "background-color:#FFD700;color:#000", "🟣 Em Negociação": "background-color:#7B2CBF;color:#FFF", "🟢 Adjudicado": "background-color:#A5D6A7;color:#000", "🔴 Não Adjudicado": "background-color:#FF6B6B;color:#000"}.get(v, ""), subset=["Fase"])
    
    edited_tct = st.data_editor(
        styled_tct,
        column_config={
            "Fase": st.column_config.SelectboxColumn("Fase", options=FASES_ATUAIS),
            "Valor Estimado": st.column_config.NumberColumn("Valor Estimado", format="%.0f €", step=1000.0),
            "% DBS": st.column_config.NumberColumn("% DBS", format="%.2f %%"),
            "Valor da % DBS": st.column_config.NumberColumn("Valor da % DBS", format="%.0f €", disabled=True),
            "Inter": st.column_config.TextColumn("Inter"),
            "% Inter": st.column_config.NumberColumn("% Inter", format="%.2f %%"),
            "Valor da % Inter": st.column_config.NumberColumn("Valor da % Inter", format="%.0f €", disabled=True),
        },
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="tct_editor"
    )
    
    if not edited_tct.equals(df_tct):
        st.session_state.tct_db = edited_tct
        st.session_state.tct_db, _ = sync_financial_math(st.session_state.tct_db)
        st.session_state.tct_db.to_csv(TCT_PATH, index=False, encoding="utf-8-sig")
        st.rerun()

# --- 7. ALCA ---
with tab_alca:
    st.markdown("### Gestão ALCA")
    st.caption("Tabela independente para a ALCA. Podes adicionar novos registos em baixo.")
    
    df_alca = st.session_state.alca_db.copy()
    styled_alca = df_alca.style.map(lambda v: {"⚪ Em Análise": "background-color:#FFF;color:#000", "🟡 Em Concurso": "background-color:#FFD700;color:#000", "🟣 Em Negociação": "background-color:#7B2CBF;color:#FFF", "🟢 Adjudicado": "background-color:#A5D6A7;color:#000", "🔴 Não Adjudicado": "background-color:#FF6B6B;color:#000"}.get(v, ""), subset=["Fase"])
    
    edited_alca = st.data_editor(
        styled_alca,
        column_config={
            "Fase": st.column_config.SelectboxColumn("Fase", options=FASES_ATUAIS),
            "Valor Estimado": st.column_config.NumberColumn("Valor Estimado", format="%.0f €", step=1000.0),
            "% DBS": st.column_config.NumberColumn("% DBS", format="%.2f %%"),
            "Valor da % DBS": st.column_config.NumberColumn("Valor da % DBS", format="%.0f €", disabled=True),
            "Inter": st.column_config.TextColumn("Inter"),
            "% Inter": st.column_config.NumberColumn("% Inter", format="%.2f %%"),
            "Valor da % Inter": st.column_config.NumberColumn("Valor da % Inter", format="%.0f €", disabled=True),
        },
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="alca_editor"
    )
    
    if not edited_alca.equals(df_alca):
        st.session_state.alca_db = edited_alca
        st.session_state.alca_db, _ = sync_financial_math(st.session_state.alca_db)
        st.session_state.alca_db.to_csv(ALCA_PATH, index=False, encoding="utf-8-sig")
        st.rerun()

# --- 8. FAMO ---
with tab_famo:
    st.markdown("### Gestão FAMO")
    st.caption("Tabela independente para a FAMO. Podes adicionar novos registos em baixo.")
    
    df_famo = st.session_state.famo_db.copy()
    styled_famo = df_famo.style.map(lambda v: {"⚪ Em Análise": "background-color:#FFF;color:#000", "🟡 Em Concurso": "background-color:#FFD700;color:#000", "🟣 Em Negociação": "background-color:#7B2CBF;color:#FFF", "🟢 Adjudicado": "background-color:#A5D6A7;color:#000", "🔴 Não Adjudicado": "background-color:#FF6B6B;color:#000"}.get(v, ""), subset=["Fase"])
    
    edited_famo = st.data_editor(
        styled_famo,
        column_config={
            "Fase": st.column_config.SelectboxColumn("Fase", options=FASES_ATUAIS),
            "Valor Estimado": st.column_config.NumberColumn("Valor Estimado", format="%.0f €", step=1000.0),
            "% DBS": st.column_config.NumberColumn("% DBS", format="%.2f %%"),
            "Valor da % DBS": st.column_config.NumberColumn("Valor da % DBS", format="%.0f €", disabled=True),
            "Inter": st.column_config.TextColumn("Inter"),
            "% Inter": st.column_config.NumberColumn("% Inter", format="%.2f %%"),
            "Valor da % Inter": st.column_config.NumberColumn("Valor da % Inter", format="%.0f €", disabled=True),
        },
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="famo_editor"
    )
    
    if not edited_famo.equals(df_famo):
        st.session_state.famo_db = edited_famo
        st.session_state.famo_db, _ = sync_financial_math(st.session_state.famo_db)
        st.session_state.famo_db.to_csv(FAMO_PATH, index=False, encoding="utf-8-sig")
        st.rerun()

# --- 9. CALENDÁRIO ---
with tab_calendario:
    nomes_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    st.session_state.setdefault("followup_calendar_month", date.today().replace(day=1))
    mes_atual = st.session_state["followup_calendar_month"]
    
    coluna_anterior, coluna_titulo, coluna_seguinte = st.columns([1, 3, 1])
    with coluna_anterior:
        if st.button("Anterior", key="cal_prev"):
            mes_index = mes_atual.year * 12 + mes_atual.month - 2
            st.session_state["followup_calendar_month"] = date(mes_index // 12, mes_index % 12 + 1, 1)
            st.session_state["selected_followup_date"] = None
            st.rerun()
    with coluna_seguinte:
        if st.button("Seguinte", key="cal_next"):
            mes_index = mes_atual.year * 12 + mes_atual.month
            st.session_state["followup_calendar_month"] = date(mes_index // 12, mes_index % 12 + 1, 1)
            st.session_state["selected_followup_date"] = None
            st.rerun()

    mes_atual = st.session_state["followup_calendar_month"]
    with coluna_titulo:
        st.markdown(f"### {nomes_meses[mes_atual.month - 1]} {mes_atual.year}")

    eventos_por_dia = {}
    
    try:
        dt_faturas = date(mes_atual.year, mes_atual.month, 10)
        eventos_por_dia.setdefault(dt_faturas, []).append({
            "tipo": "⚠️ Automático", "aba": "Pagamentos", "texto": "Emitir Faturas (Dia 10)", "id": None
        })
    except ValueError: pass

    for idx, row in st.session_state.leads_db.iterrows():
        val_f = row.get("Próximo Follow-up")
        if pd.notna(val_f) and val_f != "":
            dt_f = pd.to_datetime(val_f, errors="coerce")
            if pd.notna(dt_f) and dt_f.year == mes_atual.year and dt_f.month == mes_atual.month:
                p_nome = row.get("Projeto", "")
                c_nome = row.get("Cliente", "")
                ev = {"tipo": "Pipeline", "aba": "Pipeline de Negócios", "texto": f"Pipeline: {p_nome} ({c_nome})", "id": row.get("ID")}
                eventos_por_dia.setdefault(dt_f.date(), []).append(ev)
        
        for i in range(1, 6):
            col_f = f"Follow up Empresa {i}"
            val_f2 = row.get(col_f)
            if pd.notna(val_f2) and val_f2 != "":
                dt_f2 = pd.to_datetime(val_f2, errors="coerce")
                if pd.notna(dt_f2) and dt_f2.year == mes_atual.year and dt_f2.month == mes_atual.month:
                    emp_nome = str(row.get(f"Empresa de Construção {i}", f"Empresa {i}"))
                    p_nome = str(row.get("Projeto", ""))
                    ev2 = {"tipo": "Construtor", "aba": "Interações & Follow-Ups", "texto": f"Orçamento {emp_nome} - {p_nome}", "id": row.get("ID")}
                    eventos_por_dia.setdefault(dt_f2.date(), []).append(ev2)

    if not st.session_state.todo_db.empty:
        for idx, row in st.session_state.todo_db.iterrows():
            val_f = row.get("Follow up")
            if pd.notna(val_f) and val_f != "":
                dt_f = pd.to_datetime(val_f, errors="coerce")
                if pd.notna(dt_f) and dt_f.year == mes_atual.year and dt_f.month == mes_atual.month:
                    t_nome = row.get("Tarefa", "")
                    ev3 = {"tipo": "To Do", "aba": "To do List", "texto": f"Tarefa: {t_nome}", "id": None}
                    eventos_por_dia.setdefault(dt_f.date(), []).append(ev3)

    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    for coluna, dia_semana in zip(st.columns(7), dias_semana):
        coluna.markdown(f"**{dia_semana}**")

    for semana in py_calendar.monthcalendar(mes_atual.year, mes_atual.month):
        for coluna, dia in zip(st.columns(7), semana):
            with coluna:
                with st.container(border=True):
                    if dia == 0:
                        st.write(" ")
                    elif date(mes_atual.year, mes_atual.month, dia) in eventos_por_dia:
                        if st.button(str(dia), key=f"cal_day_{mes_atual.year}_{mes_atual.month}_{dia}", type="primary", use_container_width=True):
                            st.session_state["selected_followup_date"] = date(mes_atual.year, mes_atual.month, dia)
                    else:
                        st.markdown(f"**{dia}**")

    data_selecionada = st.session_state.get("selected_followup_date")
    if data_selecionada and data_selecionada.year == mes_atual.year and data_selecionada.month == mes_atual.month:
        st.markdown(f"### Detalhes de {data_selecionada.strftime('%d/%m/%Y')}")
        eventos_dia = eventos_por_dia.get(data_selecionada, [])
        for i, ev in enumerate(eventos_dia):
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"**{ev['tipo']}** | {ev['texto']}")
            if ev["id"] is not None:
                if c2.button(f"Ir para {ev['aba']}", key=f"btn_go_{i}_{ev['id']}"):
                    st.session_state["selected_project_id"] = int(ev["id"])
                    st.success(f"Projeto colocado na memória. Clica no menu da aba **{ev['aba']}** lá em cima!")

# --- 10. FINANCEIRO ---
with tab_financeiro:
    st.markdown("### Painel Financeiro e Estatístico")
    
    if st.session_state.leads_db.empty:
        st.info("Ainda não existem projectos registados no pipeline.")
    else:
        st.markdown("**Edição e Resumo Financeiro de Projectos**")
        st.caption("Insere as percentagens e os valores em euros serão calculados automaticamente.")
        
        def cor_fase_bg(val):
            colors = {
                "⚪ Em Análise": "background-color: #FFFFFF; color: #000000;",
                "🟡 Em Concurso": "background-color: #FFD700; color: #000000;",
                "🟣 Em Negociação": "background-color: #7B2CBF; color: #FFFFFF;",
                "🟢 Adjudicado": "background-color: #A5D6A7; color: #000000;",
                "🔴 Não Adjudicado": "background-color: #FF6B6B; color: #000000;"
            }
            return colors.get(val, "")
        
        cols_fin = ["Cliente", "Projeto", "Fase", "Valor Estimado", "% DBS", "Valor da % DBS", "Inter", "% Inter", "Valor da % Inter"]
        df_fin = st.session_state.leads_db[cols_fin].copy()
        
        df_fin["Inter"] = df_fin["Inter"].astype(str).replace("nan", "").replace("None", "")

        for col in ["% DBS", "Valor da % DBS", "% Inter", "Valor da % Inter"]:
            df_fin[col] = pd.to_numeric(df_fin[col], errors='coerce').fillna(0.0)
            
        styled_fin = df_fin.style.map(cor_fase_bg, subset=["Fase"])
        
        edited_fin = st.data_editor(
            styled_fin,
            column_config={
                "Fase": st.column_config.SelectboxColumn("Fase", options=FASES_ATUAIS),
                "Valor Estimado": st.column_config.NumberColumn("Valor Estimado", format="%.0f €", step=1000.0),
                "%% DBS": st.column_config.NumberColumn("% DBS", format="%.2f %%"),
                "Valor da % DBS": st.column_config.NumberColumn("Valor da % DBS", format="%.0f €", disabled=True),
                "Inter": st.column_config.TextColumn("Inter"),
                "%% Inter": st.column_config.NumberColumn("% Inter", format="%.2f %%"),
                "Valor da % Inter": st.column_config.NumberColumn("Valor da % Inter", format="%.0f €", disabled=True),
            },
            use_container_width=True,
            hide_index=True,
            key="fin_editor"
        )
        
        if not edited_fin.equals(df_fin):
            for col in cols_fin:
                st.session_state.leads_db[col] = edited_fin[col]
            st.session_state.leads_db, _ = sync_financial_math(st.session_state.leads_db)
            save_data(st.session_state.leads_db)
            st.rerun()

        st.markdown("---")
        st.markdown("### Totais Globais e Médias")
        
        val_estimados = edited_fin["Valor Estimado"].apply(parse_currency)
        total_estimado = val_estimados.sum()
        c_est = (val_estimados > 0).sum()
        media_estimado = total_estimado / c_est if c_est > 0 else 0.0
        
        df_adjudicados = edited_fin[edited_fin["Fase"] == "🟢 Adjudicado"]
        val_adjudicados = df_adjudicados["Valor Estimado"].apply(parse_currency)
        total_adjudicado = val_adjudicados.sum()
        c_adj = (val_adjudicados > 0).sum()
        media_adjudicado = total_adjudicado / c_adj if c_adj > 0 else 0.0
        
        val_dbs = edited_fin["Valor da % DBS"]
        total_perc_dbs = val_dbs.sum()
        c_dbs = (val_dbs > 0).sum()
        media_dbs = total_perc_dbs / c_dbs if c_dbs > 0 else 0.0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Valor Estimado", f"{int(total_estimado):,} €".replace(",", " "), delta=f"Média: {int(media_estimado):,} €".replace(",", " "), delta_color="off")
        c2.metric("Total Valor Adjudicado", f"{int(total_adjudicado):,} €".replace(",", " "), delta=f"Média: {int(media_adjudicado):,} €".replace(",", " "), delta_color="off")
        c3.metric("Total Valor da % DBS", f"{int(total_perc_dbs):,} €".replace(",", " "), delta=f"Média: {int(media_dbs):,} €".replace(",", " "), delta_color="off")

# --- 11. PAGAMENTOS ---
with tab_pagamentos:
    st.markdown("### Mapa Cronológico de Pagamentos")
    
    projetos_cadastrados = st.session_state.leads_db["Projeto"].dropna().loc[lambda x: x!=""].unique().tolist()
    proj_pag = st.selectbox("Selecione o Projeto para gerir o Plano de Pagamentos", [""] + projetos_cadastrados, key="sel_proj_pag_main")

    if proj_pag:
        mask_inst = st.session_state.installments_db["Projeto"] == proj_pag
        has_plan = mask_inst.any()
        
        with st.expander("⚙️ Configurar / Gerar Plano de Pagamentos", expanded=not has_plan):
            with st.form("form_gen_pagamentos", clear_on_submit=False):
                proj_row = st.session_state.leads_db[st.session_state.leads_db["Projeto"] == proj_pag].iloc[0]
                val_dbs_def = pd.to_numeric(proj_row.get("Valor da % DBS", 0.0), errors="coerce")
                val_est_def = parse_currency(proj_row.get("Valor Estimado", 0.0))
                default_val = float(val_dbs_def) if pd.notna(val_dbs_def) and val_dbs_def > 0 else float(val_est_def)
                
                c1, c2, c3, c4 = st.columns(4)
                with c1: val_global = st.number_input("Valor Global (€)", min_value=0.0, value=default_val, step=1000.0)
                with c2: meses_dur = st.number_input("Meses de duração", min_value=1, value=1, step=1)
                with c3: data_inicio = st.date_input("Data de Início", date.today().replace(day=1))
                
                m = int(meses_dur)
                val_mensal = val_global / m if m > 0 else 0.0
                
                try:
                    y_f = data_inicio.year + ((data_inicio.month - 1 + m) // 12)
                    m_f = ((data_inicio.month - 1 + m) % 12) + 1
                    d_f = data_inicio.day
                    while True:
                        try:
                            data_final = date(y_f, m_f, d_f)
                            break
                        except ValueError:
                            d_f -= 1
                except:
                    data_final = data_inicio + timedelta(days=30*m)
                
                with c4: st.markdown(f"<div style='margin-top:28px'><b>Mensalidade Estimada:</b> {val_mensal:,.2f} €<br><b>Data Final:</b> {data_final.strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)
                
                submit_pag = st.form_submit_button("Gerar Plano (Folha Excel)")

                if submit_pag:
                    if has_plan:
                        st.session_state.installments_db = st.session_state.installments_db[~mask_inst]
                        
                    d = data_inicio.replace(day=1)
                    novos_meses = []
                    for _ in range(m):
                        mes_str = d.strftime("%Y-%m")
                        novos_meses.append({
                            "Projeto": proj_pag,
                            "Mês": mes_str,
                            "Mensalidade (€)": float(val_mensal),
                            "IVA (%)": 23.0,
                            "Valor com IVA (€)": float(val_mensal * 1.23),
                            "IVA IF": "",
                            "Estado": "⚪ Não facturado"
                        })
                        year = d.year + (d.month // 12)
                        month = (d.month % 12) + 1
                        d = d.replace(year=year, month=month, day=1)
                        
                    st.session_state.installments_db = pd.concat([st.session_state.installments_db, pd.DataFrame(novos_meses)], ignore_index=True)
                    st.session_state.installments_db["IVA IF"] = st.session_state.installments_db["IVA IF"].astype(str).replace("nan", "").replace("None", "")
                    st.session_state.installments_db.to_csv(INSTALLMENTS_PATH, index=False, encoding="utf-8-sig")
                    
                    if proj_pag in st.session_state.payments_db["Projeto"].values:
                        idx_pag = st.session_state.payments_db.index[st.session_state.payments_db["Projeto"] == proj_pag][0]
                    else:
                        st.session_state.payments_db = pd.concat([st.session_state.payments_db, pd.DataFrame([{"Projeto": proj_pag}])], ignore_index=True)
                        idx_pag = st.session_state.payments_db.index[-1]
                        
                    st.session_state.payments_db.at[idx_pag, "Valor Global"] = float(val_global)
                    st.session_state.payments_db.at[idx_pag, "Meses de duração"] = int(m)
                    st.session_state.payments_db.at[idx_pag, "Valor mensal"] = float(val_mensal)
                    st.session_state.payments_db.at[idx_pag, "Data de Início"] = str(data_inicio)
                    st.session_state.payments_db.at[idx_pag, "Data Final"] = str(data_final)
                    st.session_state.payments_db.to_csv(PAYMENTS_PATH, index=False, encoding="utf-8-sig")
                    
                    st.success("Folha Excel de Pagamentos gerada!")
                    st.rerun()

        mask_inst_updated = st.session_state.installments_db["Projeto"] == proj_pag
        if mask_inst_updated.any():
            st.markdown(f"#### Folha de Faturação: {proj_pag}")
            df_proj_inst = st.session_state.installments_db[mask_inst_updated].copy()
            df_proj_inst["IVA IF"] = df_proj_inst["IVA IF"].astype(str).replace("nan", "").replace("None", "")
            
            edited_inst = st.data_editor(
                df_proj_inst,
                column_config={
                    "Projeto": st.column_config.TextColumn("Projeto", disabled=True),
                    "Mês": st.column_config.TextColumn("Mês", disabled=True),
                    "Mensalidade (€)": st.column_config.NumberColumn("Mensalidade s/ IVA", format="%.2f €"),
                    "IVA (%)": st.column_config.NumberColumn("IVA (%)", format="%.1f %%"),
                    "Valor com IVA (€)": st.column_config.NumberColumn("Valor c/ IVA", format="%.2f €", disabled=True),
                    "IVA IF": st.column_config.TextColumn("Refª Fatura (IVA IF)"),
                    "Estado": st.column_config.SelectboxColumn("Status de Envio da Fatura", options=ESTADOS_PAGAMENTO)
                },
                hide_index=True,
                use_container_width=True,
                key=f"edit_inst_{proj_pag}"
            )
            
            if not edited_inst.equals(df_proj_inst):
                for idx in edited_inst.index:
                    v_base = edited_inst.at[idx, "Mensalidade (€)"]
                    v_iva = edited_inst.at[idx, "IVA (%)"]
                    edited_inst.at[idx, "Valor com IVA (€)"] = v_base * (1 + v_iva / 100.0)
                    st.session_state.installments_db.loc[idx] = edited_inst.loc[idx]
                st.session_state.installments_db["IVA IF"] = st.session_state.installments_db["IVA IF"].astype(str).replace("nan", "").replace("None", "")
                st.session_state.installments_db.to_csv(INSTALLMENTS_PATH, index=False, encoding="utf-8-sig")
                st.rerun()

    st.markdown("---")
    st.markdown("### Quadro Geral de Obras Adjudicadas")
    resumo_data = []
    tot_adj = 0.0
    tot_rec = 0.0
    tot_porpagar = 0.0
    tot_arec = 0.0
    
    leads_adj = st.session_state.leads_db[st.session_state.leads_db["Fase"] == "🟢 Adjudicado"]
    for idx, row in leads_adj.iterrows():
        p = row["Projeto"]
        val_adj = parse_currency(row["Valor Estimado"])
        val_dbs = pd.to_numeric(row.get("Valor da % DBS", 0.0), errors='coerce')
        val_final_adj = float(val_dbs) if pd.notna(val_dbs) and val_dbs > 0 else float(val_adj)
        
        installs = st.session_state.installments_db[st.session_state.installments_db["Projeto"] == p]
        
        val_rec = pd.to_numeric(installs[installs["Estado"] == "🟢 Recebido"]["Mensalidade (€)"], errors="coerce").sum()
        val_por_pagar = pd.to_numeric(installs[installs["Estado"] == "🟡 Fatura por pagar"]["Mensalidade (€)"], errors="coerce").sum()
        val_a_rec = val_final_adj - val_rec
        
        resumo_data.append({
            "Projeto": p,
            "Valor Adjudicado / DBS": val_final_adj,
            "Valor Recebido": val_rec,
            "Faturas por Pagar (🟡)": val_por_pagar,
            "Valor a Receber": val_a_rec
        })
        tot_adj += val_final_adj
        tot_rec += val_rec
        tot_porpagar += val_por_pagar
        tot_arec += val_a_rec
        
    if resumo_data:
        df_resumo = pd.DataFrame(resumo_data)
        st.dataframe(df_resumo.style.format({
            "Valor Adjudicado / DBS": "{:,.0f} €",
            "Valor Recebido": "{:,.0f} €",
            "Faturas por Pagar (🟡)": "{:,.0f} €",
            "Valor a Receber": "{:,.0f} €"
        }), hide_index=True, use_container_width=True)
        
        st.markdown("#### Totais Globais das Obras")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Adjudicado", f"{int(tot_adj):,} €".replace(",", " "))
        c2.metric("Total Recebido", f"{int(tot_rec):,} €".replace(",", " "))
        c3.metric("Faturas por Pagar", f"{int(tot_porpagar):,} €".replace(",", " "))
        c4.metric("Total a Receber", f"{int(tot_arec):,} €".replace(",", " "))
    else:
        st.info("Ainda não existem obras classificadas como '🟢 Adjudicado' na Pipeline.")

# --- 12. TO DO LIST ---
with tab_todo:
    st.markdown("### To Do List")
    st.caption("Gere as tuas tarefas e os teus próximos passos de forma dinâmica.")
    
    with st.form("add_todo"):
        st.markdown("**Adicionar Nova Tarefa**")
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1: t_proj = st.text_input("Tarefa")
        with c2: t_passo = st.text_input("Próximos passos")
        with c3: t_date = st.date_input("Follow up", date.today())
        
        if st.form_submit_button("Adicionar Tarefa"):
            if t_proj.strip() == "" or t_passo.strip() == "":
                st.warning("Preenche a Tarefa e os Próximos passos.")
            else:
                new_t = pd.DataFrame([{"Tarefa": t_proj, "Próximos passos": t_passo, "Follow up": t_date}])
                st.session_state.todo_db = pd.concat([st.session_state.todo_db, new_t], ignore_index=True)
                st.session_state.todo_db.to_csv(TODO_PATH, index=False)
                st.success("Tarefa adicionada e gravada!")
                st.rerun()

    st.markdown("---")
    st.markdown("**Tarefas Pendentes** (Edição Direta)")
    
    if not st.session_state.todo_db.empty:
        col_config_todo = {
            "Tarefa": st.column_config.TextColumn("Tarefa", width="medium"),
            "Próximos passos": st.column_config.TextColumn("Próximos passos", width="large"),
            "Follow up": st.column_config.DateColumn("Follow up")
        }
        
        edited_todo = st.data_editor(
            st.session_state.todo_db,
            column_config=col_config_todo,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            key="todo_editor_grid"
        )
        
        if not edited_todo.equals(st.session_state.todo_db):
            st.session_state.todo_db = edited_todo
            st.session_state.todo_db.to_csv(TODO_PATH, index=False)

        st.markdown("---")
        st.markdown("**Opções: Eliminar Tarefa Específica**")
        del_opts = [""] + [f"{i} | {row.get('Tarefa', '')} - {row['Próximos passos']}" for i, row in st.session_state.todo_db.iterrows()]
        t_del = st.selectbox("Selecione a tarefa a apagar de vez:", del_opts)
        
        if st.button("🗑️ Eliminar Tarefa Selecionada") and t_del != "":
            idx_to_del = int(t_del.split(" | ")[0])
            st.session_state.todo_db = st.session_state.todo_db.drop(idx_to_del).reset_index(drop=True)
            st.session_state.todo_db.to_csv(TODO_PATH, index=False)
            st.success("Tarefa apagada com sucesso.")
            st.rerun()
    else:
        st.info("Não há tarefas na tua lista.")

# --- 13. OBJECTIVOS ---
with tab_objectivos:
    st.markdown("### Quadro Global de Objetivos e KPIs (2027)")
    st.caption("Clica na coluna 'Objetivo' para editares o teu alvo. Usa apenas números.")
    
    def parse_kpi_input(val):
        try:
            if pd.isna(val): return 0.0
            if isinstance(val, (int, float)): return float(val)
            s = str(val).replace("€", "").replace("%", "").strip()
            s = s.replace(" ", "")
            if "." in s and "," in s:
                if s.rfind(".") > s.rfind(","): s = s.replace(",", "")
                else: s = s.replace(".", "").replace(",", ".")
            elif "," in s: s = s.replace(",", ".")
            elif s.count(".") > 1: s = s.replace(".", "")
            return float(s)
        except: return 0.0

    if "Parceria" in st.session_state.architects_db.columns:
        total_parcerias_arq = float((st.session_state.architects_db["Parceria"] == "🟢 Sim").sum())
    else: total_parcerias_arq = 0.0

    if "Parceria" in st.session_state.builders_db.columns:
        total_parcerias_const = float((st.session_state.builders_db["Parceria"] == "🟢 Sim").sum())
    else: total_parcerias_const = 0.0
        
    total_projectos = float(len(st.session_state.leads_db))
    
    if not st.session_state.leads_db.empty:
        total_adjudicados = float((st.session_state.leads_db["Fase"] == "🟢 Adjudicado").sum())
        
        val_estimados_arr = st.session_state.leads_db["Valor Estimado"].apply(parse_currency)
        total_valor_estimado = val_estimados_arr.sum()
        
        df_adjudicados_kpi = st.session_state.leads_db[st.session_state.leads_db["Fase"] == "🟢 Adjudicado"]
        total_valor_adjudicado = df_adjudicados_kpi["Valor Estimado"].apply(parse_currency).sum()
        
        total_valor_dbs = pd.to_numeric(st.session_state.leads_db["Valor da % DBS"], errors='coerce').fillna(0.0).sum()
        perc_valor = float((total_valor_adjudicado / total_valor_estimado * 100) if total_valor_estimado > 0 else 0.0)
    else:
        total_adjudicados = 0.0
        total_valor_estimado = 0.0
        total_valor_adjudicado = 0.0
        total_valor_dbs = 0.0
        perc_valor = 0.0

    val_atuais = [
        total_parcerias_arq,
        total_parcerias_const,
        total_projectos,
        total_adjudicados,
        total_valor_adjudicado,
        total_valor_dbs,
        perc_valor
    ]

    def formatar_kpi(val, idx):
        if pd.isna(val): val = 0.0
        if idx in [4, 5]: return f"{int(val):,} €".replace(",", " ")
        elif idx == 6: return f"{val:.1f} %".replace(".", ",")
        else: return str(int(val))

    val_atuais_fmt = [formatar_kpi(v, i) for i, v in enumerate(val_atuais)]
    objetivos_fmt = [formatar_kpi(v, i) for i, v in enumerate(st.session_state.kpi_db["Objetivo"])]

    nomes_metricas = [
        "Total de Parcerias com Arquitectos",
        "Total de Parcerias com Construtores",
        "Total de Projectos",
        "Total de Projectos Adjudicados",
        "Total de Valor Adjudicado (€)",
        "Total de Valor da % DBS (€)",
        "% de Valor (Adjudicado / Estimado) (%)"
    ]

    df_kpi_display = pd.DataFrame({
        "Métricas Globais": nomes_metricas,
        "Valor Atual": val_atuais_fmt,
        "KPIS 2027": nomes_metricas,
        "Objetivo (Editável)": objetivos_fmt
    })

    col_config_kpi = {
        "Métricas Globais": st.column_config.TextColumn("Métricas Globais", disabled=True),
        "Valor Atual": st.column_config.TextColumn("Valor Atual", disabled=True),
        "KPIS 2027": st.column_config.TextColumn("KPIS 2027", disabled=True),
        "Objetivo (Editável)": st.column_config.TextColumn("Objetivo (Editável)")
    }

    edited_kpi = st.data_editor(
        df_kpi_display,
        column_config=col_config_kpi,
        use_container_width=True,
        hide_index=True,
        key="kpi_editor"
    )

    if not edited_kpi["Objetivo (Editável)"].equals(df_kpi_display["Objetivo (Editável)"]):
        st.session_state.kpi_db["Objetivo"] = edited_kpi["Objetivo (Editável)"].apply(parse_kpi_input)
        st.session_state.kpi_db.to_csv(KPI_PATH, index=False, encoding="utf-8-sig")
        st.rerun()
