def load_logo_base64(path):
    import base64
    with open(path,"rb") as f:
        return base64.b64encode(f.read()).decode()

import streamlit as st
import pandas as pd
import altair as alt
import re
import base64

st.markdown("""
<style>

/* --- Streamlit Default Overrides for Dark Mode --- */

html[data-theme="dark"] body,
html[data-theme="dark"] .stApp {
    color: #ffffff !important;
}

html[data-theme="dark"] .stSelectbox div[data-baseweb="select"] span,
html[data-theme="dark"] .stSelectbox div[data-baseweb="select"] input,
html[data-theme="dark"] .stSelectbox div[data-baseweb="select"] div {
    color: #ffffff !important;
}

html[data-theme="dark"] .stDataFrame,
html[data-theme="dark"] .dataframe {
    color: #ffffff !important;
}

html[data-theme="dark"] .training-card {
    background: rgba(30,30,30,0.85) !important;
    border-left: 6px solid #FFD700 !important;
}

html[data-theme="dark"] .training-card .meta,
html[data-theme="dark"] .training-card .list-item {
    color: #eaeaea !important;
    background: rgba(60,60,60,0.6) !important;
}

html[data-theme="dark"] .training-card .list-item {
    border: 1px solid rgba(255,255,255,0.2) !important;
}


/* INPUT TEXT PERMANENT WHITE (Dark Mode) */
.stTextInput input {
    color: #ffffff !important;
}
.stTextInput input::placeholder {
    color: #dddddd !important;
}
html[data-theme="dark"] .stTextInput input {
    background-color: rgba(40,40,40,0.8) !important;
    border: 1px solid #888 !important;
}


/* SELECTBOX – PERMANENT WHITE TEXT (Dark Mode) */
.stSelectbox div[data-baseweb="select"] div {
    color: #ffffff !important;
}
.stSelectbox div[data-baseweb="select"] input {
    color: #ffffff !important;
}
.stSelectbox svg {
    fill: #ffffff !important;
}
html[data-theme="dark"] .stSelectbox div[data-baseweb="select"] {
    background-color: rgba(40,40,40,0.8) !important;
    border: 1px solid #666 !important;
}
html[data-theme="dark"] .stSelectbox [role="listbox"] {
    background-color: #2e2e2e !important;
}
html[data-theme="dark"] .stSelectbox [role="listbox"] div {
    color: #ffffff !important;
}


/* SELECTBOX ADAPTIF (Light=Hitam, Dark=Putih) */
.stSelectbox div[data-baseweb="select"] div,
.stSelectbox div[data-baseweb="select"] input {
    color: #000000 !important;
}
.stSelectbox svg { fill: #000000 !important; }

html[data-theme="dark"] .stSelectbox div[data-baseweb="select"] div,
html[data-theme="dark"] .stSelectbox div[data-baseweb="select"] input {
    color: #ffffff !important;
}
html[data-theme="dark"] .stSelectbox svg {
    fill: #ffffff !important;
}
html[data-theme="dark"] .stSelectbox div[data-baseweb="select"] {
    background-color: rgba(40,40,40,0.9) !important;
    border: 1px solid #666 !important;
}
html[data-theme="dark"] .stSelectbox [role="listbox"] {
    background-color: #2e2e2e !important;
}
html[data-theme="dark"] .stSelectbox [role="listbox"] div {
    color: #ffffff !important;
}


/* SIDEBAR SELECTBOX ADAPTIF */
/* Light mode text */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div,
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input {
    color: #000000 !important;
}
/* Dark mode text */
html[data-theme="dark"] section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div,
html[data-theme="dark"] section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input {
    color: #ffffff !important;
}
/* Arrow icon */
section[data-testid="stSidebar"] .stSelectbox svg {
    fill: #000000 !important;
}
html[data-theme="dark"] section[data-testid="stSidebar"] .stSelectbox svg {
    fill: #ffffff !important;
}
/* Background box */
html[data-theme="dark"] section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background-color: #333 !important;
    border: 1px solid #777 !important;
}


/* --- Custom Styles --- */

.stApp { background: transparent !important; }
.video-bg {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    object-fit: cover; z-index: -2;
}
.overlay {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.3); z-index: -1;
}
section[data-testid="stSidebar"] {
    background-color: #111 !important;
}
section[data-testid="stSidebar"] * {
    color: #f9f9f9 !important;
}

h1, h2, h3 { color: #FFD700 !important; }
.home-desc {
    color: #FFFFFF !important;
    font-size: 20px;
    font-weight: 700;
    line-height: 1.6;
}

/* Card style for training and contact */
.training-card {
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    border-left: 6px solid #FFD700;
    /* Light Mode */
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.95));
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
/* Dark Mode Overrides for card background */
html[data-theme="dark"] .training-card {
    background: rgba(30,30,30,0.85) !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.3);
}

/* --- ADAPTIVE COLOR FOR CARD CONTENTS (FIXED CONTRAST) --- */

/* Light Mode Styles for Card Text */
.training-card h4 { color: #222 !important; } /* Name: dark in light mode */
.training-card a { color: #007bff !important; } /* Email link: blue in Light Mode */
.training-card .contact-detail, .training-card div:not(.meta) { color: #333 !important; } /* Phone number and generic text: dark gray in Light Mode */
.training-card .meta { color: #444 !important; } /* Meta: slightly lighter dark gray in Light Mode */

/* Dark Mode Overrides for internal card elements */
html[data-theme="dark"] .training-card h4 { color: #FFD700 !important; }
html[data-theme="dark"] .training-card .meta { color: #eaeaea !important; }
html[data-theme="dark"] .training-card a { color: #90CAF9 !important; } /* Link color in Dark Mode (light blue) */
html[data-theme="dark"] .training-card .contact-detail,
html[data-theme="dark"] .training-card div:not(.meta) { color: #eaeaea !important; } /* Phone number and generic text in Dark Mode (light gray) */


.training-card h4 { margin: 0 0 6px 0; }
.training-card .meta { font-size: 13px; margin-bottom: 8px; }

.training-card .list-item { font-size: 13px; margin: 4px 0; padding: 6px; border-radius: 6px; }
/* Dark Mode Overrides for training list item */
html[data-theme="dark"] .training-card .list-item {
    background: rgba(60,60,60,0.6) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
/* Light Mode Defaults for training list item */
.training-card .list-item {
    background: #fff;
    border: 1px solid #f0f0f0;
}


/* Style for the WhatsApp button (MODIFIED TO ENSURE WHITE TEXT AND NO UNDERLINE) */
.whatsapp-button {
    background-color: #25D366 !important;
    color: white !important; /* Memastikan warna teks putih */
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 700;
    border-radius: 20px;
    text-decoration: none !important; /* Menghilangkan garis bawah dengan prioritas tinggi */
    display: inline-block;
    margin-top: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    transition: all 0.2s;
}
.whatsapp-button:hover {
    background-color: #128C7E !important;
    color: white !important;
    text-decoration: none !important; /* Memastikan tanpa garis bawah saat hover dengan prioritas tinggi */
}

</style>
""", unsafe_allow_html=True)

# Naikkan batas elemen Pandas Styler
pd.set_option("styler.render.max_elements", 500000)

st.set_page_config(
    page_title="Cek Surat Izin Operator (SIO) & Training",
    layout="wide",
)

# ==== Pilihan Bahasa ====
lang = st.sidebar.selectbox("🌐 Language / Bahasa", ["Indonesia", "English"])

TEXTS = {
    "Indonesia": {
        "home": "Beranda",
        "home_title": "Database Manpower Yard Marketing United Tractors",
        "home_desc": "",
        "website": "www.unitedtractors.com",
        "search": "Cek SIO",
        "search_name": "Masukkan nama karyawan",
        "search_type": "Pilih Jenis LK3",
        "result_found": "✅ Ditemukan {n} hasil",
        "result_not_found": "❌ Tidak ada hasil untuk pencarian ini.",
        "download": "Download Hasil (CSV)",
        "contact": "Kontak & Bantuan",
        "guide": "**Panduan Singkat:**\n1. Pilih menu **Pencarian** di sidebar.\n2. Masukkan nama karyawan atau pilih jenis LK3.\n3. Hasil akan muncul di tabel.\n4. Gunakan tombol **Download** untuk menyimpan hasil ke file CSV.\n\nTerima kasih telah menggunakan aplikasi ini.",
        "chart_pie": "Distribusi Jenis LK3",
        "chart_bar_date": "Tanggal Peng-isu­an SIO",
        "chart_bar_branch": "Jumlah Data per Cabang/Site/Area",
        "data_viz": "Visualisasi Data",
        "axis_date": "Tanggal Pelaksanaan",
        "axis_count": "Jumlah Data",
        "axis_branch": "Cabang / Site / Area",
        "all": "Semua",
        "training": "Cek Training",
        "card_more": "Detail Training",
        "no_training_found": "❌ Tidak ada data training untuk pencarian ini."
    },
    "English": {
        "home": "Home",
        "home_title": "United Tractors Manpower Yard Marketing Database",
        "home_desc": "",
        "website": "www.unitedtractors.com",
        "search": "Permit Check",
        "search_name": "Enter employee name",
        "search_type": "Select LK3 Type",
        "result_found": "✅ {n} results found",
        "result_not_found": "❌ No results for this search.",
        "download": "Download Results (CSV)",
        "contact": "Contact & Support",
        "guide": "**Quick Guide:**\n1. Select **Search** from the sidebar.\n2. Enter employee name or choose LK3 type.\n3. Results will appear in the table.\n4. Use **Download** to save results as CSV.\n\nThank you for using this application.",
        "chart_pie": "Distribution of LK3 Types",
        "chart_bar_date": "SIO Issuance Dates",
        "chart_bar_branch": "Data by Branch/Site/Area",
        "data_viz": "Data Visualization",
        "axis_date": "Event Date",
        "axis_count": "Record Count",
        "axis_branch": "Branch / Site / Area",
        "all": "All",
        "training": "Training Check",
        "card_more": "Training Details",
        "no_training_found": "❌ No training data for this search."
    }
}

# ==== Translasi Header Kolom ====
COLUMN_TRANSLATIONS = {
    "Indonesia": {
        "NAMA ASESI": "NAMA ASESI",
        "JENIS LK3": "JENIS LK3",
        "TANGGAL PELAKSANAAN": "TANGGAL PELAKSANAAN",
        "CABANG": "CABANG",
        "NO SERTIFIKAT": "NO SERTIFIKAT",
        "MASA BERLAKU": "MASA BERLAKU",
        "NO INDUK": "NO INDUK",
        "DIVISI": "DIVISI"
    },
    "English": {
        "NAMA ASESI": "Employee Name",
        "JENIS LK3": "LK3 Type",
        "TANGGAL PELAKSANAAN": "Event Date",
        "CABANG": "Branch / Site / Area",
        "NO SERTIFIKAT": "Certificate Number",
        "MASA BERLAKU": "Validity Period",
        "NO INDUK": "Employee ID",
        "DIVISI": "Division"
    }
}


# URL Google Sheets (SIO existing)
sheet_url = "https://docs.google.com/spreadsheets/d/1sEKL0sFJJljsWPtCAPvglL4uLhOg-xE0/export?format=csv"

# Training sheet (user-provided)
training_sheet_id = "1xBHZe1gQesaBbWBKCARQpVB1Nad_ENYHk8_qCAFfMfs"
training_sheet_url = f"https://docs.google.com/spreadsheets/d/{training_sheet_id}/export?format=csv"

# Fungsi konversi Google Drive (Tidak digunakan di SIO/Training sheet, tapi dipertahankan)
def convert_drive_link(url: str) -> str:
    if pd.isna(url):
        return None
    url = str(url).strip()
    match = re.search(r"/d/(.*?)(/|$)", url)
    if match:
        return f"https://drive.google.com/uc?id={match.group(1)}"
    match = re.search(r"uc\\?id=([^&]+)", url)
    if match:
        return f"https://drive.google.com/uc?id={match.group(1)}"
    return url

# Menu navigasi
menu = st.sidebar.radio(
    "Navigasi",
    [TEXTS[lang]["home"], TEXTS[lang]["search"], TEXTS[lang]["training"], TEXTS[lang]["contact"]]
)

# -------------------------
# BERANDA
# -------------------------
if menu == TEXTS[lang]["home"]:

    # Load video background
    try:
        with open("static/bg.mp4", "rb") as f:
            video_bytes = f.read()
        video_b64 = base64.b64encode(video_bytes).decode("utf-8")

        st.markdown(
            f"""
            <video autoplay muted loop playsinline class="video-bg">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            <div class="overlay"></div>
            """,
            unsafe_allow_html=True,
        )
    except:
        # Jika file video tidak ada, tetap tampilkan logo dan judul
        pass

    # Load logo (base64)
    # Catatan: Asumsi file 'UT-member-of-ASTRA-verticalCWHITE.png' ada di direktori yang sama
    try:
        logo_b64 = load_logo_base64("UT-member-of-ASTRA-verticalCWHITE.png")
    except:
        logo_b64 = None # Handle jika logo tidak ditemukan

    st.markdown(
        """
        <div style="width:100%; text-align:center; margin-top:60px;">
        """,
        unsafe_allow_html=True,
    )

    if logo_b64:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="data:image/png;base64,{logo_b64}"
                     style="width:530px; max-width:90%; margin-bottom:10px;" />
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <h1 style="text-align:center; color:#FFD700 !important; margin-top:15px; font-weight:900;">
            {TEXTS[lang]["home_title"]}
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <p style="text-align:center; font-size:20px; font-weight:700; max-width:900px;
                 margin:0 auto; color:white; line-height:1.6;">
            {TEXTS[lang]["home_desc"]}
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:30px;">
            <a href="https://{TEXTS[lang]['website']}" target="_blank"
               style="background-color:#FFD700; color:black; padding:14px 32px;
                      font-size:18px; font-weight:700; border-radius:32px;
                      text-decoration:none; display:inline-block;
                      box-shadow:0 4px 12px rgba(0,0,0,0.3);">
                {TEXTS[lang]['website']}
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------
# CEK SIO
# -------------------------
elif menu == TEXTS[lang]["search"]:
    try:
        df = pd.read_csv(sheet_url)

        df = df.dropna(axis=1, how='all')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.dropna(how='all')

        lk3_col = next((col for col in df.columns if "JENIS LK3" in col.upper()), None)
        if lk3_col is None:
            st.error("Kolom 'JENIS LK3' tidak ditemukan di file.")
        else:
            col1, col2 = st.columns([2, 1])
            with col1:
                nama = st.text_input(TEXTS[lang]["search_name"]).strip().lower()
            with col2:
                jenis_filter = st.selectbox(TEXTS[lang]["search_type"], [TEXTS[lang]["all"]] + sorted(df[lk3_col].dropna().unique().tolist()))

            hasil = df.copy()

            # === Hilangkan .000000 di kolom No & NRP ===
            for col in hasil.columns:
                if col.strip().lower() in ["no", "nrp"]:
                    hasil[col] = hasil[col].apply(
                        lambda x: str(int(float(x))) if pd.notna(x) and str(x).replace('.', '', 1).isdigit() else x
                    )

            if nama:
                hasil = hasil[hasil['NAMA ASESI'].astype(str).str.lower().str.contains(nama)]
            if jenis_filter != TEXTS[lang]["all"]:
                hasil = hasil[hasil[lk3_col] == jenis_filter]

            if not hasil.empty:
                st.markdown(TEXTS[lang]["result_found"].format(n=len(hasil)))

                def highlight_sio(row):
                    if pd.isnull(row[lk3_col]):
                        return [''] * len(row)
                    if "SIO" in str(row[lk3_col]).upper():
                        return ['background-color: #FFF9C4; font-weight: bold;'] * len(row)
                    return [''] * len(row)

                hasil_display = hasil.rename(columns=lambda c: COLUMN_TRANSLATIONS[lang].get(c, c))
                if len(hasil_display) <= 2000:
                    # Hanya aplikasikan style jika jumlah baris tidak terlalu banyak
                    styled_df = hasil_display.style.apply(highlight_sio, axis=1)
                    st.dataframe(styled_df, use_container_width=True)
                else:
                    st.dataframe(hasil_display, use_container_width=True)

                st.subheader(TEXTS[lang]["data_viz"])
                
                # --- Pie Chart Jenis LK3 ---
                pie_data = hasil[lk3_col].value_counts().reset_index()
                pie_data.columns = ["Jenis LK3", "Jumlah"]
                pie_data["Persentase"] = (pie_data["Jumlah"] / pie_data["Jumlah"].sum() * 100).round(1)
                pie_chart = alt.Chart(pie_data).mark_arc().encode(
                    theta="Jumlah", color="Jenis LK3",
                    tooltip=["Jenis LK3", "Jumlah", "Persentase"]
                ).properties(title=TEXTS[lang]["chart_pie"])
                st.altair_chart(pie_chart, use_container_width=True)

                # --- Bar Chart Tanggal Pelaksanaan ---
                if "TANGGAL PELAKSANAAN" in hasil.columns:
                    bar_data = hasil["TANGGAL PELAKSANAAN"].value_counts().reset_index()
                    bar_data.columns = ["Tanggal", "Jumlah"]
                    bar_data["Persentase"] = (bar_data["Jumlah"] / bar_data["Jumlah"].sum() * 100).round(1)
                    bar_chart = alt.Chart(bar_data).mark_bar().encode(
                        y=alt.Y("Tanggal", sort='-x', axis=alt.Axis(labelAngle=0, title=TEXTS[lang]["axis_date"])),
                        x=alt.X("Jumlah", title=TEXTS[lang]["axis_count"]),
                        tooltip=["Tanggal", "Jumlah", "Persentase"]
                    ).properties(height=600, title=TEXTS[lang]["chart_bar_date"])
                    st.altair_chart(bar_chart, use_container_width=True)

                # --- Bar Chart Cabang / Site ---
                cabang_col = next((col for col in hasil.columns if "CABANG" in col.upper()), None)
                if cabang_col:
                    cabang_data = hasil[cabang_col].value_counts().reset_index()
                    cabang_data.columns = ["Cabang", "Jumlah"]
                    cabang_data["Persentase"] = (cabang_data["Jumlah"] / cabang_data["Jumlah"].sum() * 100).round(1)
                    cabang_chart = alt.Chart(cabang_data).mark_bar().encode(
                        x=alt.X("Cabang", sort='-y', axis=alt.Axis(labelAngle=-45, title=TEXTS[lang]["axis_branch"])),
                        y=alt.Y("Jumlah", title=TEXTS[lang]["axis_count"]),
                        tooltip=["Cabang", "Jumlah", "Persentase"]
                    ).properties(height=400, title=TEXTS[lang]["chart_bar_branch"])
                    st.altair_chart(cabang_chart, use_container_width=True)

                # --- Tombol Download ---
                csv_data = hasil.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=TEXTS[lang]["download"],
                    data=csv_data,
                    file_name="hasil_pencarian_sio.csv",
                    mime="text/csv"
                )
            else:
                st.warning(TEXTS[lang]["result_not_found"])
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca data: {e}")

# -------------------------
# TRAINING (baru)
# -------------------------
elif menu == TEXTS[lang]["training"]:
    try:
        # baca CSV export dari Google Sheets (user-provided)
        df_t = pd.read_csv(training_sheet_url)

        # normalisasi: hapus kolom kosong, Unnamed, dan baris kosong
        df_t = df_t.dropna(axis=1, how='all')
        df_t = df_t.loc[:, ~df_t.columns.str.contains('^Unnamed')]
        df_t = df_t.dropna(how='all')

        # ==== hapus kolom tanggal lahir kalau ada ====
        drop_keys = ["TGL LAHIR", "TANGGAL LAHIR", "DOB", "DATE OF BIRTH"]
        cols_to_drop = [c for c in df_t.columns if any(k in c.upper() for k in drop_keys)]
        if cols_to_drop:
            df_t = df_t.drop(columns=cols_to_drop)

        # cari kolom penting secara case-insensitive / kemungkinan variasi header
        def find_col(dfcols, keywords):
            for k in dfcols:
                up = k.upper()
                for kw in keywords:
                    if kw in up:
                        return k
            return None

        inst_col = find_col(df_t.columns, ["INSTITUSI", "INSTITUT", "INSTITUTION"])
        nrp_col = find_col(df_t.columns, ["NRP", "NO INDUK", "NIP", "EMPLOYEE ID"])
        nama_col = find_col(df_t.columns, ["NAMA", "NAME", "NAMA ASESI"])
        jenis_col = find_col(df_t.columns, ["JENIS TRAINING", "JENIS", "TRAINING"])
        tanggal_col = find_col(df_t.columns, ["TANGGAL PELAKSANAAN", "TANGGAL", "DATE"])
        no_sert_col = find_col(df_t.columns, ["NO SERTIFIKAT", "NOMOR SERTIFIKAT", "SERTIFIKAT"])
        no_form_col = find_col(df_t.columns, ["NO FORMULIR", "FORMULIR", "NO FORM"])

        # subset hanya kolom yg diminta; jika tidak tersedia, buat kolom kosong
        chosen_cols = {}
        chosen_cols['INSTITUSI'] = inst_col if inst_col else None
        chosen_cols['NRP'] = nrp_col if nrp_col else None
        chosen_cols['NAMA'] = nama_col if nama_col else None
        chosen_cols['JENIS TRAINING'] = jenis_col if jenis_col else None
        chosen_cols['TANGGAL PELAKSANAAN'] = tanggal_col if tanggal_col else None
        chosen_cols['NO SERTIFIKAT'] = no_sert_col if no_sert_col else None
        chosen_cols['NO FORMULIR'] = no_form_col if no_form_col else None

        # buat dataframe baru dengan kolom standar (jika header asli beda)
        df_clean = pd.DataFrame()
        for std_col, orig in chosen_cols.items():
            if orig:
                df_clean[std_col] = df_t[orig].astype(str).fillna('').replace('nan','')
            else:
                df_clean[std_col] = ''

        # bersihkan nilai yang kosong-total
        df_clean = df_clean.replace({'': pd.NA}).dropna(how='all').fillna('')

        # remove .0 decimal artifacts pada NRP dan nomor
        def clean_numeric_str(x):
            try:
                xs = str(x).strip()
                if xs == 'nan' or xs == '':
                    return ''
                # if looks like float representing int:
                if re.fullmatch(r'\d+\.0+', xs):
                    return str(int(float(xs)))
                # if digits with decimal like 123.0 or 123.000
                if re.fullmatch(r'\d+\.\d+', xs):
                    # Try to cast to int if it effectively is integer
                    try:
                        f = float(xs)
                        if f.is_integer():
                            return str(int(f))
                    except:
                        pass
                return xs
            except:
                return str(x)

        if 'NRP' in df_clean.columns:
            df_clean['NRP'] = df_clean['NRP'].apply(clean_numeric_str)
        if 'NO SERTIFIKAT' in df_clean.columns:
            df_clean['NO SERTIFIKAT'] = df_clean['NO SERTIFIKAT'].apply(clean_numeric_str)
        if 'NO FORMULIR' in df_clean.columns:
            df_clean['NO FORMULIR'] = df_clean['NO FORMULIR'].apply(clean_numeric_str)

        # Filter & Search UI
        col1, col2 = st.columns([2, 1])
        with col1:
            search_name = st.text_input("Masukkan nama karyawan").strip().lower()
        with col2:
            # Menggunakan kolom 'INSTITUSI' dari df_clean
            institusi_options = df_clean['INSTITUSI'].replace('', 'Lain-lain').unique().tolist()
            choose_inst = st.selectbox("Filter Institusi", options=[TEXTS[lang]["all"]] + sorted(institusi_options))

        df_filtered = df_clean.copy()
        if search_name:
            df_filtered = df_filtered[df_filtered['NAMA'].astype(str).str.lower().str.contains(search_name)]
        if choose_inst and choose_inst != TEXTS[lang]["all"]:
            # Filter berdasarkan nilai asli atau string kosong jika 'Lain-lain' dipilih
            if choose_inst == 'Lain-lain':
                df_filtered = df_filtered[df_filtered['INSTITUSI'] == '']
            else:
                df_filtered = df_filtered[df_filtered['INSTITUSI'] == choose_inst]

        if df_filtered.empty:
            st.warning(TEXTS[lang]["no_training_found"])
        else:
            # Group by Nama + NRP + Institusi -> gabungkan jenis,tanggal,no sertifikat,no formulir
            agg = df_filtered.groupby(['NAMA', 'NRP', 'INSTITUSI'], dropna=False).agg({
                'JENIS TRAINING': lambda x: ' | '.join([str(i).strip() for i in x if str(i).strip()]),
                'TANGGAL PELAKSANAAN': lambda x: ' | '.join([str(i).strip() for i in x if str(i).strip()]),
                'NO SERTIFIKAT': lambda x: ' | '.join([str(i).strip() for i in x if str(i).strip()]),
                'NO FORMULIR': lambda x: ' | '.join([str(i).strip() for i in x if str(i).strip()]),
            }).reset_index()

            st.markdown(TEXTS[lang]["result_found"].format(n=len(agg)))
            
            # tampilkan ringkasan tabel
            st.dataframe(agg, use_container_width=True)

            # tombol download ringkasan CSV
            csv_data = agg.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=TEXTS[lang]["download"],
                data=csv_data,
                file_name="training_summary.csv",
                mime="text/csv"
            )

            # Card-style grid: tampilkan beberapa card per row
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader(TEXTS[lang]["card_more"])
            
            # hitung kolom grid responsif
            num_cols = 3
            rows = []
            for i in range(0, len(agg), num_cols):
                rows.append(agg.iloc[i:i+num_cols])

            for row in rows:
                cols = st.columns(len(row))
                for idx, (_, r) in enumerate(row.iterrows()):
                    with cols[idx]:
                        # Siapkan list training detail per item (split by ' | ' preserving order)
                        jenis_list = [s.strip() for s in str(r['JENIS TRAINING']).split(' | ') if s.strip()]
                        tanggal_list = [s.strip() for s in str(r['TANGGAL PELAKSANAAN']).split(' | ') if s.strip()]
                        sert_list = [s.strip() for s in str(r['NO SERTIFIKAT']).split(' | ') if s.strip()]
                        form_list = [s.strip() for s in str(r['NO FORMULIR']).split(' | ') if s.strip()]

                        # Build HTML card
                        # Perhatikan: tidak ada inline style untuk warna, hanya menggunakan class CSS
                        html = f"""<div class="training-card">
                                    <h4>{r['NAMA']}</h4>
                                    <div class="meta"><strong>NRP:</strong> {r['NRP']} &nbsp; | &nbsp; <strong>Institusi:</strong> {r['INSTITUSI'] if r['INSTITUSI'] else 'Lain-lain'}</div>
                                    <div>
                                """
                        # construct training rows (pairwise)
                        maxlen = max(len(jenis_list), len(tanggal_list), len(sert_list), len(form_list))
                        if maxlen == 0:
                            html += "<div class='list-item'>Tidak ada informasi training detail.</div>"
                        else:
                            for i2 in range(maxlen):
                                j = jenis_list[i2] if i2 < len(jenis_list) else ""
                                t = tanggal_list[i2] if i2 < len(tanggal_list) else ""
                                s = sert_list[i2] if i2 < len(sert_list) else ""
                                f = form_list[i2] if i2 < len(form_list) else ""
                                # Pastikan teks di list-item kontras
                                html += f"<div class='list-item'><strong>{j}</strong><br/>{t}<br/>Sert: {s} | Form: {f}</div>"

                        html += "</div></div>"
                        st.markdown(html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca data training: {e}")

# -------------------------
# KONTAK & BANTUAN (Telah diperbarui untuk adaptasi Dark Mode yang lebih baik)
# -------------------------
elif menu == TEXTS[lang]["contact"]:
    st.header(TEXTS[lang]["contact"])
    
    # --- Data Kontak ---
    kontak_data = [
        {"nama": "Helmalya RP", "email": "HelmalyaRP@unitedtractors.com", "telepon": "085859823983"},
        {"nama": "Tito A", "email": "TitoA@unitedtractors.com", "telepon": "082299733414"},
        {"nama": "M Joe Devin B", "email": "MJoe@unitedtractors.com", "telepon": "0895396065641"},
    ]

    # Fungsi untuk membuat tombol WhatsApp
    def create_whatsapp_button(phone_num):
        # Membersihkan nomor telepon dan memastikan format wa.me yang benar
        clean_num = "".join(filter(str.isdigit, phone_num))
        return f'<a href="https://wa.me/{clean_num}" target="_blank" class="whatsapp-button">WhatsApp</a>'

    # Fungsi untuk membuat card kontak (Inline style warna dihapus)
    def create_contact_card(nama, email, telepon):
        whatsapp_btn = create_whatsapp_button(telepon)
        
        # Membersihkan nomor telepon dan memformatnya untuk tampilan
        clean_num = "".join(filter(str.isdigit, telepon))
        
        # Logic formatting telepon display
        display_telepon = telepon # Default
        if len(clean_num) == 12:
            display_telepon = f"{clean_num[:4]} {clean_num[4:8]} {clean_num[8:]}"
        elif len(clean_num) == 11:
            display_telepon = f"{clean_num[:4]} {clean_num[4:7]} {clean_num[7:]}"
        elif len(clean_num) == 13:
            # Contoh untuk nomor 0895396065641
            display_telepon = f"{clean_num[:4]} {clean_num[4:8]} {clean_num[8:]}" 

        # Inline style warna dihapus dari <a> dan <div> telepon
        html = f"""
        <div class="training-card" style="text-align:center;">
            <h4 style="margin-bottom: 5px;">{nama}</h4>
            <a href="mailto:{email}" style="text-decoration: none;">{email}</a>
            <div class="contact-detail" style="font-size: 16px; margin-top: 5px;">{display_telepon}</div>
            {whatsapp_btn}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    # Tampilkan kontak dalam layout 3 kolom
    cols = st.columns(len(kontak_data))
    for i, kontak in enumerate(kontak_data):
        with cols[i]:
            create_contact_card(kontak["nama"], kontak["email"], kontak["telepon"])

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(TEXTS[lang]["guide"])