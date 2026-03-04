import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import json
import os
from utils import (
    load_data, handle_missing_values, remove_duplicates,
    handle_outliers_iqr, normalize_data,
    convert_df_to_csv, convert_df_to_excel, convert_df_to_json, convert_df_to_xml,
    create_boxplot, detect_outliers_info, get_missing_values_info, create_donut_chart
)
from history import save_to_history, load_history, clear_history, is_file_already_processed

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataClean Pro | ISI",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CREDENTIALS — persistées dans users.json
# ─────────────────────────────────────────────
USERS_FILE = "users.json"

DEFAULT_USERS = {
    "admin": {"password": "admin123", "name": "Admin ISI",   "role": "Gold Member"},
    "user":  {"password": "pass123",  "name": "Henry Klein", "role": "Silver Member"},
}

def load_users():
    if not os.path.exists(USERS_FILE):
        save_users(DEFAULT_USERS)
        return dict(DEFAULT_USERS)
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return dict(DEFAULT_USERS)

def save_users(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, indent=2, ensure_ascii=False)

USERS = load_users()

# ─────────────────────────────────────────────
# GLOBAL CSS — Corona dark theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #191c2e !important;
    color: #d0d4e8 !important;
}
[data-testid="stSidebar"]   { background-color: #1e2139 !important; }
[data-testid="stSidebar"] * { color: #d0d4e8 !important; }
[data-testid="stHeader"]    { background-color: #191c2e !important; }

input, textarea {
    background-color: #252840 !important;
    color: #ffffff !important;
    border: 1px solid #3d4166 !important;
    border-radius: 6px !important;
}
.stTextInput > div > div > input { background-color: #252840 !important; color: #ffffff !important; }

div.stButton > button {
    background-color: #4361ee !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: background 0.2s;
}
div.stButton > button:hover { background-color: #3a56d4 !important; }

button[data-baseweb="tab"] {
    color: #a0a9c0 !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #4361ee !important;
    border-bottom: 2px solid #4361ee !important;
}

div[data-testid="stMetric"] {
    background-color: #252840;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #3d4166;
}
div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.7rem !important; }
div[data-testid="stMetricLabel"] { color: #a0a9c0 !important; }

div[data-baseweb="select"] > div { background-color: #252840 !important; border-color: #3d4166 !important; }
div[data-baseweb="select"] * { color: #ffffff !important; }

details { background-color: #252840 !important; border-radius: 8px !important; border: 1px solid #3d4166 !important; }
summary { color: #d0d4e8 !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #191c2e; }
::-webkit-scrollbar-thumb { background: #3d4166; border-radius: 3px; }

.main-header {
    font-size: 2.5rem;
    color: #ffffff;
    text-align: center;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.sub-header {
    font-size: 1.1rem;
    color: #a0a9c0;
    text-align: center;
    margin-bottom: 2rem;
}

.stat-card {
    background-color: #252840;
    border-radius: 14px;
    padding: 20px 18px;
    border: 1px solid #3d4166;
    position: relative;
    overflow: hidden;
    min-height: 110px;
}
.stat-card .icon  { font-size: 1.8rem; position: absolute; top: 14px; right: 16px; opacity: 0.2; }
.stat-card .label { font-size: 0.78rem; color: #a0a9c0; margin-bottom: 4px; }
.stat-card .value { font-size: 1.7rem; font-weight: 700; color: #ffffff; }
.stat-card .delta { font-size: 0.8rem; margin-top: 4px; }
.delta-pos { color: #2ecc71; }
.delta-neg { color: #e74c3c; }

.file-row {
    display: flex; align-items: center; padding: 10px 0;
    border-bottom: 1px solid #3d4166; gap: 12px;
}
.file-row .ficon {
    width: 40px; height: 40px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
}
.file-row .fname  { font-size: 0.88rem; color: #ffffff; font-weight: 600; }
.file-row .fmeta  { font-size: 0.75rem; color: #a0a9c0; }
.file-row .fright { margin-left: auto; font-size: 0.75rem; color: #a0a9c0; white-space: nowrap; }
.section-title { font-size: 1rem; font-weight: 700; color: #ffffff; margin: 0 0 16px 0; }

.login-card {
    background-color: #252840;
    border-radius: 16px;
    padding: 40px 36px;
    max-width: 420px;
    width: 100%;
    border: 1px solid #3d4166;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "logged_in": False,
        "username": "",
        "current_page": "Dashboard",
        "df_clean": None,
        "processed_filename": None,
        "export_format": "CSV",
        "treatment_done": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ─────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────
def show_login():
    global USERS
    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        st.markdown("""
        <div style="text-align:center; padding: 40px 0 20px 0;">
          <span style="font-size:3rem;">🧹</span>
          <h2 style="color:#ffffff; margin:8px 0 0 0;">DataClean Pro</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔑  Connexion", "📝  Inscription"])

        # ── Connexion ──
        with tab_login:
            st.markdown('<p style="color:#a0a9c0;font-size:0.85rem;margin:12px 0 16px 0;">Bienvenue ! Connectez-vous à votre compte.</p>',
                        unsafe_allow_html=True)
            login_user = st.text_input("Nom d'utilisateur", key="login_user", placeholder="ex: admin")
            login_pass = st.text_input("Mot de passe", key="login_pass", type="password", placeholder="••••••••")

            if st.button("Se Connecter", use_container_width=True, key="btn_login"):
                users = load_users()
                if login_user in users and users[login_user]["password"] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username  = login_user
                    # Rafraîchir le dict global
                    USERS = users
                    st.rerun()
                else:
                    st.error("Identifiants incorrects. Réessayez.")

            st.markdown("""
            <p style="text-align:center;color:#a0a9c0;font-size:0.75rem;margin-top:16px;">
              Comptes démo : <b>admin</b> / admin123 &nbsp;|&nbsp; <b>user</b> / pass123
            </p>
            """, unsafe_allow_html=True)

        # ── Inscription ──
        with tab_register:
            st.markdown('<p style="color:#a0a9c0;font-size:0.85rem;margin:12px 0 16px 0;">Créez un nouveau compte.</p>',
                        unsafe_allow_html=True)
            reg_name    = st.text_input("Nom complet",               key="reg_name",    placeholder="ex: Marie Dupont")
            reg_user    = st.text_input("Nom d'utilisateur",         key="reg_user",    placeholder="ex: marie")
            reg_pass    = st.text_input("Mot de passe",               key="reg_pass",    type="password", placeholder="••••••••")
            reg_confirm = st.text_input("Confirmer le mot de passe", key="reg_confirm", type="password", placeholder="••••••••")

            if st.button("Créer mon compte", use_container_width=True, key="btn_register"):
                users = load_users()
                if not reg_name or not reg_user or not reg_pass:
                    st.error("Veuillez remplir tous les champs.")
                elif reg_pass != reg_confirm:
                    st.error("Les mots de passe ne correspondent pas.")
                elif reg_user in users:
                    st.error(f"Le nom d'utilisateur **{reg_user}** est déjà pris.")
                elif len(reg_pass) < 6:
                    st.error("Le mot de passe doit contenir au moins 6 caractères.")
                else:
                    users[reg_user] = {"password": reg_pass, "name": reg_name, "role": "Member"}
                    save_users(users)
                    USERS = users
                    st.success("Compte créé avec succès ! Connectez-vous dans l'onglet **Connexion**.")

        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
def show_sidebar():
    with st.sidebar:
        users     = load_users()
        user_info = users.get(st.session_state.username, {"name": "User", "role": "Member"})
        initial   = user_info["name"][0].upper()
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;padding:10px 0 20px 0;
             border-bottom:1px solid #3d4166;margin-bottom:20px;">
            <div style="width:42px;height:42px;border-radius:50%;background:#4361ee;display:flex;
                 align-items:center;justify-content:center;font-size:1.1rem;font-weight:700;
                 color:#fff;flex-shrink:0;">{initial}</div>
            <div>
                <div style="font-weight:700;color:#fff;font-size:0.9rem;">{user_info['name']}</div>
                <div style="font-size:0.75rem;color:#a0a9c0;">{user_info['role']}</div>
            </div>
        </div>
        <p style="font-size:0.7rem;color:#a0a9c0;text-transform:uppercase;
           letter-spacing:1px;margin:0 0 8px 0;">Navigation</p>
        """, unsafe_allow_html=True)

        for icon, label in [("📊", "Dashboard"), ("📁", "Upload & Traitement"), ("📜", "Historique")]:
            if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
                st.session_state.current_page = label
                st.rerun()

        st.markdown("---")
        if st.button("🚪  Se Déconnecter", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in     = False
            st.session_state.username      = ""
            st.session_state.current_page  = "Dashboard"
            st.session_state.df_clean      = None
            st.session_state.processed_filename = None
            st.session_state.treatment_done     = False
            st.rerun()


# ─────────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────────
def page_dashboard():
    history       = load_history()
    total_files   = len(history)
    total_rows    = sum(r.get("original_rows", 0) for r in history)
    total_clean   = sum(r.get("cleaned_rows",  0) for r in history)
    total_removed = sum(r.get("rows_removed",  0) for r in history)
    rate = round(total_clean / total_rows * 100, 1) if total_rows > 0 else 0.0

    # Header
    st.markdown('<div class="main-header">🧹 Data Processing API</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Projet Python M1 IAGE — Institut Supérieur d\'Informatique (ISI)</div>', unsafe_allow_html=True)

    # Stat cards
    c1, c2, c3, c4 = st.columns(4)
    def stat_card(col, icon, label, value, delta, cls="delta-pos"):
        col.markdown(f"""
        <div class="stat-card">
            <div class="icon">{icon}</div>
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="delta {cls}">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

    stat_card(c1, "📁", "Fichiers Traités",   str(total_files),      f"+{total_files} total")
    stat_card(c2, "📋", "Lignes Analysées",   f"{total_rows:,}",     f"{total_rows:,} lignes")
    stat_card(c3, "✅", "Lignes Conservées",  f"{total_clean:,}",    f"{rate}% conservé")
    stat_card(c4, "🗑️", "Lignes Supprimées", f"{total_removed:,}",  f"{100-rate:.1f}% nettoyé", cls="delta-neg")

    st.markdown("<br>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1.3], gap="large")

    # ── Donut chart (like Transaction History) ──
    with left_col:
        st.markdown('<p class="section-title">Fichiers Traités par Type</p>', unsafe_allow_html=True)
        if history:
            type_counts = {}
            for r in history:
                ft = str(r.get("file_type", "")).lower().strip(".")
                # Déduire le type depuis le nom de fichier si absent
                if not ft or ft == "unknown":
                    fname = r.get("filename", "")
                    ft = fname.rsplit(".", 1)[-1].lower() if "." in fname else "autre"
                type_counts[ft] = type_counts.get(ft, 0) + 1

            fig = create_donut_chart(type_counts, total_files)
            if fig:
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            type_colors = {
                'csv': '#3498db',   # Bleu
                'xlsx': '#2ecc71',  # Vert
                'xls': '#2ecc71',   # Vert
                'json': '#f39c12',  # Orange
                'xml': '#e74c3c',   # Rouge
            }
            fallback_palette = ['#9b59b6', '#1abc9c', '#e67e22', '#16a085']
            fi = 0
            for i, (ftype, count) in enumerate(type_counts.items()):
                if ftype.lower() in type_colors:
                    color = type_colors[ftype.lower()]
                else:
                    color = fallback_palette[fi % len(fallback_palette)]
                    fi += 1
                pct   = round(count / total_files * 100) if total_files else 0
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                     padding:7px 0;border-bottom:1px solid #3d4166;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <div style="width:10px;height:10px;border-radius:50%;background:{color};"></div>
                        <span style="color:#d0d4e8;font-size:0.85rem;">{ftype.upper()}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;">
                        <span style="color:#fff;font-weight:600;">{count} fichier{'s' if count>1 else ''}</span>
                        <span style="color:#a0a9c0;font-size:0.78rem;">{pct}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun fichier traité pour le moment.")

    # ── Recent files (like Open Projects) ──
    with right_col:
        st.markdown('<p class="section-title">Derniers Fichiers Traités</p>', unsafe_allow_html=True)
        if history:
            ext_styles = {
                "csv":  ("#1a3a5c", "#3498db"),   # Bleu
                "xlsx": ("#1a3d2b", "#2ecc71"),   # Vert
                "xls":  ("#1a3d2b", "#2ecc71"),   # Vert
                "json": ("#3d2b1a", "#f39c12"),   # Orange
                "xml":  ("#3b1a1a", "#e74c3c"),   # Rouge
            }
            for record in history[:8]:
                ext    = str(record.get("file_type", "")).lower().strip(".")
                if not ext or ext == "unknown":
                    ext = record['filename'].rsplit(".", 1)[-1].lower() if "." in record['filename'] else "file"
                bg, fg = ext_styles.get(ext, ("#2a2a4a", "#a0a9c0"))
                ops    = len(record.get("operations", []))
                fname  = record['filename']
                fname_display = (fname[:38] + "…") if len(fname) > 40 else fname
                st.markdown(f"""
                <div class="file-row">
                    <div class="ficon" style="background:{bg};color:{fg};">{ext.upper()[:3]}</div>
                    <div>
                        <div class="fname">{fname_display}</div>
                        <div class="fmeta">{ops} opération{'s' if ops>1 else ''} · {record['cleaned_rows']} lignes</div>
                    </div>
                    <div class="fright">{record['timestamp'][:16]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("L'historique des traitements apparaîtra ici.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕  Traiter un nouveau fichier"):
        st.session_state.current_page = "Upload & Traitement"
        st.rerun()


# ─────────────────────────────────────────────
# UPLOAD & PROCESSING PAGE
# ─────────────────────────────────────────────
def page_upload():
    # ── Zone principale : Upload direct ──
    st.markdown("""
    <h2 style="color:#ffffff;margin-bottom:4px;">📁 Upload & Traitement</h2>
    <p style="color:#a0a9c0;margin-bottom:20px;">Importez votre fichier, configurez le nettoyage, exportez le résultat.</p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Glissez votre fichier ici ou cliquez pour parcourir",
        type=['csv', 'xlsx', 'xls', 'json', 'xml'],
        help="Formats acceptés : CSV, Excel (.xlsx/.xls), JSON, XML"
    )

    if uploaded_file is None:
        st.markdown("""
        <div style="background-color:#252840;border-radius:12px;padding:30px;border:1px solid #3d4166;
             text-align:center;margin-top:10px;">
            <p style="font-size:2.5rem;margin-bottom:8px;">📂</p>
            <p style="color:#ffffff;font-size:1.1rem;font-weight:600;margin-bottom:6px;">
                Aucun fichier chargé
            </p>
            <p style="color:#a0a9c0;font-size:0.85rem;margin-bottom:16px;">
                Utilisez la zone ci-dessus pour importer un fichier à nettoyer.
            </p>
            <div style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;">
                <span style="background:#1a3a5c;color:#3498db;padding:6px 14px;border-radius:20px;font-size:0.8rem;font-weight:600;">CSV</span>
                <span style="background:#1a3d2b;color:#2ecc71;padding:6px 14px;border-radius:20px;font-size:0.8rem;font-weight:600;">EXCEL</span>
                <span style="background:#3d2b1a;color:#f39c12;padding:6px 14px;border-radius:20px;font-size:0.8rem;font-weight:600;">JSON</span>
                <span style="background:#3b1a1a;color:#e74c3c;padding:6px 14px;border-radius:20px;font-size:0.8rem;font-weight:600;">XML</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Sidebar : Configuration de traitement (apparaît après upload) ──
    with st.sidebar:
        st.markdown("---")
        st.subheader("⚙️ Configuration")
        miss_val = st.selectbox(
            "Valeurs Manquantes",
            ['Ne rien faire', 'Supprimer les lignes', 'Moyenne (Mean)', 'Médiane (Median)', 'Mode (Fréquence)']
        )
        st.caption("ℹ️ Colonnes catégorielles → Mode automatique")
        dup_val     = st.checkbox("Supprimer les doublons", value=True)
        out_val     = st.checkbox("Traiter les Aberrants (IQR)", value=False)
        norm_val    = st.selectbox("Normalisation", ['Aucune', 'MinMax (0-1)', 'Standard (Z-Score)'])
        st.markdown("---")
        process_btn = st.button("🚀  LANCER LE TRAITEMENT", use_container_width=True)

    # ── Détection changement de fichier : réinitialiser l'état ──
    if st.session_state.get('_last_uploaded_name') != uploaded_file.name:
        st.session_state['treatment_done'] = False
        st.session_state['df_clean'] = None
        st.session_state['processed_filename'] = None
    st.session_state['_last_uploaded_name'] = uploaded_file.name

    # ── Bannière "déjà traité" (non bloquante) ──
    already_proc, last_rec = is_file_already_processed(uploaded_file.name)
    if already_proc and not st.session_state.get('treatment_done', False):
        st.info(
            f"ℹ️ Le fichier **{uploaded_file.name}** a déjà été traité le "
            f"**{last_rec['timestamp']}** ({last_rec['original_rows']} → {last_rec['cleaned_rows']} lignes). "
            f"Vous pouvez le re-traiter si nécessaire."
        )

    # ── Chargement des données ──
    df = load_data(uploaded_file)
    if isinstance(df, str):
        st.error(f"Erreur de chargement : {df}")
        return

    # ── Onglets ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Données Brutes", "📦 Analyse Outliers", "⚙️ Traitement", "📥 Export"
    ])

    # ── Tab 1 : Données brutes ──
    with tab1:
        st.info(f"Fichier chargé : **{uploaded_file.name}**")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Lignes",    df.shape[0])
        c2.metric("Colonnes",  df.shape[1])
        c3.metric("Doublons",  df.duplicated().sum())
        c4.metric("Val. Manquantes", df.isnull().sum().sum())
        num_cols = df.select_dtypes(include=['number']).columns
        tot_out  = sum(
            df[col].apply(lambda x: (
                x < (df[col].quantile(0.25) - 1.5*(df[col].quantile(0.75)-df[col].quantile(0.25))) or
                x > (df[col].quantile(0.75) + 1.5*(df[col].quantile(0.75)-df[col].quantile(0.25)))
            ) if pd.notnull(x) else False).sum()
            for col in num_cols
        )
        c5.metric("Aberrants (IQR)", tot_out)

        missing_df = get_missing_values_info(df)
        if missing_df is not None:
            with st.expander("🔍 Détails Valeurs Manquantes", expanded=False):
                st.dataframe(missing_df, use_container_width=True)
        with st.expander("Aperçu du tableau", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)

    # ── Tab 2 : Outliers ──
    with tab2:
        st.subheader("📦 Analyse des Valeurs Aberrantes")
        outliers_info = detect_outliers_info(df)
        if outliers_info:
            summary = [{
                "Colonne": c, "Outliers": i['count'],
                "%": f"{i['percentage']:.2f}%",
                "Borne inf.": f"{i['lower_bound']:.2f}",
                "Borne sup.": f"{i['upper_bound']:.2f}"
            } for c, i in outliers_info.items()]
            st.dataframe(pd.DataFrame(summary), use_container_width=True)
            fig = create_boxplot(df, "Distribution et Détection des Outliers")
            if fig:
                st.pyplot(fig)
                plt.close(fig)
        else:
            st.info("Aucune colonne numérique trouvée.")

    # ── Tab 3 : Traitement ──
    with tab3:
        if process_btn:
            with st.spinner("Nettoyage en cours…"):
                time.sleep(0.8)
                df_clean = df.copy()
                ops = []

                if miss_val != 'Ne rien faire':
                    df_clean = handle_missing_values(df_clean, miss_val)
                    ops.append(f"Valeurs manquantes : {miss_val}")
                if dup_val:
                    df_clean = remove_duplicates(df_clean)
                    ops.append("Suppression des doublons")
                if out_val:
                    df_clean = handle_outliers_iqr(df_clean)
                    ops.append("Traitement des outliers (IQR)")
                if norm_val != 'Aucune':
                    df_clean = normalize_data(df_clean, norm_val)
                    ops.append(f"Normalisation : {norm_val}")

            st.success("✅ Traitement terminé avec succès !")

            ext = uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else 'unknown'
            save_to_history(
                filename=uploaded_file.name,
                original_rows=len(df),
                cleaned_rows=len(df_clean),
                operations=ops,
                file_type=ext,
                export_format=st.session_state.get("export_format", "CSV").lower()
            )

            st.session_state['df_clean']           = df_clean
            st.session_state['processed_filename'] = uploaded_file.name
            st.session_state['treatment_done']     = True

        # Afficher les résultats si traitement effectué
        if st.session_state.get('treatment_done', False) and st.session_state.get('df_clean') is not None:
            df_clean = st.session_state['df_clean']

            col_a, col_b = st.columns(2)
            col_a.info("Avant Traitement")
            col_a.write(df.describe())
            col_b.success("Après Traitement")
            col_b.write(df_clean.describe())

            st.write("### Aperçu des données nettoyées")
            st.dataframe(df_clean.head(10), use_container_width=True)

            st.write("### Comparaison Boxplots — Avant vs Après")
            bo1, bo2 = st.columns(2)
            with bo1:
                st.write("**Avant**")
                fig_b = create_boxplot(df, "Avant Traitement")
                if fig_b:
                    st.pyplot(fig_b)
                    plt.close(fig_b)
            with bo2:
                st.write("**Après**")
                fig_a = create_boxplot(df_clean, "Après Traitement")
                if fig_a:
                    st.pyplot(fig_a)
                    plt.close(fig_a)
        else:
            st.info("⚙️ Configurez les options dans la barre latérale et cliquez sur **LANCER LE TRAITEMENT**.")

    # ── Tab 4 : Export ──
    with tab4:
        st.markdown("### 📥 Télécharger le fichier nettoyé")
        if st.session_state.get('df_clean') is not None:
            df_exp    = st.session_state['df_clean']
            raw_name  = st.session_state.get('processed_filename') or 'fichier'
            base_name = raw_name.rsplit('.', 1)[0] if '.' in raw_name else raw_name

            st.markdown("#### Choisissez le format d'export :")
            export_fmt = st.radio(
                "Format d'export",
                options=["CSV", "Excel (.xlsx)", "JSON", "XML"],
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state['export_format'] = export_fmt
            st.markdown("---")

            EXPORT_MAP = {
                "CSV":          (convert_df_to_csv,   f"clean_{base_name}.csv",  "text/csv"),
                "Excel (.xlsx)":(convert_df_to_excel, f"clean_{base_name}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                "JSON":         (convert_df_to_json,  f"clean_{base_name}.json", "application/json"),
                "XML":          (convert_df_to_xml,   f"clean_{base_name}.xml",  "application/xml"),
            }
            fn_convert, file_name, mime = EXPORT_MAP[export_fmt]
            data = fn_convert(df_exp)

            st.download_button(
                label=f"💾  Télécharger en {export_fmt}",
                data=data,
                file_name=file_name,
                mime=mime,
                use_container_width=True,
            )
            st.caption(f"Fichier : `{file_name}`  —  {len(df_exp):,} lignes · {len(df_exp.columns)} colonnes")

            with st.expander("👁️ Aperçu des données à exporter", expanded=False):
                st.dataframe(df_exp.head(10), use_container_width=True)
        else:
            st.warning("⚠️ Veuillez d'abord lancer le traitement dans l'onglet **⚙️ Traitement**.")


# ─────────────────────────────────────────────
# HISTORY PAGE
# ─────────────────────────────────────────────
def page_history():
    st.markdown("""
    <h2 style="color:#ffffff;margin-bottom:4px;">📜 Historique des Traitements</h2>
    <p style="color:#a0a9c0;margin-bottom:24px;">Tous les fichiers traités depuis le début.</p>
    """, unsafe_allow_html=True)

    history = load_history()

    if history:
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🗑️ Effacer l'historique"):
                clear_history()
                st.rerun()

        history_df  = pd.DataFrame(history)
        wanted_cols = ['timestamp', 'filename', 'file_type', 'original_rows', 'cleaned_rows', 'rows_removed']
        cols_show   = [c for c in wanted_cols if c in history_df.columns]
        rename_map  = {
            'timestamp':    'Date & Heure',
            'filename':     'Fichier',
            'file_type':    'Type',
            'original_rows':'Lignes Init.',
            'cleaned_rows': 'Lignes Finales',
            'rows_removed': 'Supprimées',
        }
        display_df = history_df[cols_show].rename(columns=rename_map)
        st.dataframe(display_df, use_container_width=True, height=350)

        st.write("### Détails des derniers traitements")
        for record in history[:5]:
            with st.expander(f"📄 {record['filename']} — {record['timestamp']}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("Lignes avant", record.get('original_rows', '-'))
                c2.metric("Lignes après", record.get('cleaned_rows',  '-'))
                c3.metric("Supprimées",   record.get('rows_removed',  '-'))
                st.write("**Opérations :**")
                for op in record.get('operations', []):
                    st.write(f"&nbsp;&nbsp;▸ {op}")
    else:
        st.info("Aucun fichier traité. L'historique apparaîtra ici après le premier traitement.")


# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    show_login()
else:
    show_sidebar()
    page = st.session_state.current_page

    if page == "Dashboard":
        page_dashboard()
    elif page == "Upload & Traitement":
        page_upload()
    elif page == "Historique":
        page_history()
