import streamlit as st
import pandas as pd
import altair as alt
import re
import base64

# Naikkan batas elemen Pandas Styler
pd.set_option("styler.render.max_elements", 500000)

st.set_page_config(
    page_title="Cek Surat Izin Operator (SIO)",
    layout="wide",
)

# ==== Pilihan Bahasa ====
lang = st.sidebar.selectbox("🌐 Language / Bahasa", ["Indonesia", "English"])

TEXTS = {
    "Indonesia": {
        "home": "Beranda",
        "home_title": "Cek Surat Izin Operator (SIO)",
        "home_desc": "Aplikasi ini memudahkan Anda untuk mencari, memfilter, dan mengunduh data SIO karyawan secara cepat dan akurat.",
        "website": "www.unitedtractors.com",
        "search": "Pencarian",
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
        "all": "Semua"
    },
    "English": {
        "home": "Home",
        "home_title": "Operator License Check (SIO)",
        "home_desc": "This app helps you quickly search, filter, and download employee SIO data with ease and accuracy.",
        "website": "www.unitedtractors.com",
        "search": "Search",
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
        "data_viz": "📊 Data Visualization",
        "axis_date": "Event Date",
        "axis_count": "Record Count",
        "axis_branch": "Branch / Site / Area",
        "all": "All"
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

# ==== CSS Fix ====
st.markdown("""
<style>
/* Buat background utama transparan supaya video terlihat */
.stApp {
    background: transparent !important;
}

/* Video background */
.video-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -2;
}
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.3);
    z-index: -1;
}

/* Sidebar dark */
section[data-testid="stSidebar"] {
    background-color: #111 !important;
}
section[data-testid="stSidebar"] * {
    color: #f9f9f9 !important;
}

/* Dropdown bahasa agar teks selalu kontras */
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] input,
.stSelectbox div[data-baseweb="select"] div {
    color: #000000 !important;
}

/* Judul beranda warna kuning UT */
h1, h2, h3 {
    color: #FFD700 !important;
}

/* Teks deskripsi bawah judul warna putih lebih bold dan besar */
.home-desc {
    color: #FFFFFF !important;
    font-size: 20px;
    font-weight: 700;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# URL Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1sEKL0sFJJljsWPtCAPvglL4uLhOg-xE0/export?format=csv"

# Fungsi konversi link Google Drive
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

# Menu navigasi di sidebar
menu = st.sidebar.radio(
    "Navigasi",
    [TEXTS[lang]["home"], TEXTS[lang]["search"], TEXTS[lang]["contact"]]
)

# -------------------------
# BERANDA
# -------------------------
if menu == TEXTS[lang]["home"]:
    try:
        with open("static/bg.mp4", "rb") as f:
            video_bytes = f.read()
        video_b64 = base64.b64encode(video_bytes).decode("utf-8")
        st.markdown(f"""<video autoplay muted loop playsinline class="video-bg"><source src="data:video/mp4;base64,{video_b64}" type="video/mp4"></video><div class="overlay"></div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"⚠️ Video gagal dimuat: {e}")

    # Logo dengan indentasi
    st.markdown("<div style='margin-left: 50px;'>", unsafe_allow_html=True)
    st.image("United-Tractors-New-Thumbnail1.png", width=630)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<h1 style='margin-left: 50px;'>{TEXTS[lang]['home_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='home-desc' style='margin-left: 50px;'>{TEXTS[lang]['home_desc']}</p>", unsafe_allow_html=True)

    # Tombol link website dengan indentasi sejajar
    st.markdown(
        f"""
        <div style="margin-left: 50px; margin-top: 20px;">
            <a href="https://{TEXTS[lang]['website']}" target="_blank"
               style="
                    background-color: #FFD700;
                    color: black;
                    font-size: 18px;
                    font-weight: 600;
                    padding: 12px 28px;
                    border-radius: 30px;
                    text-decoration: none;
                    display: inline-block;
               ">
                {TEXTS[lang]['website']}
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# PENCARIAN
# -------------------------
elif menu == TEXTS[lang]["search"]:
    try:
        df = pd.read_csv(sheet_url)
        
        # Hapus kolom kosong atau unnamed
        df = df.dropna(axis=1, how='all')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Hapus baris kosong
        df = df.dropna(how='all')

        lk3_col = None
        for col in df.columns:
            if "JENIS LK3" in col.upper():
                lk3_col = col
                break
        if lk3_col is None:
            st.error("Kolom 'JENIS LK3' tidak ditemukan di file.")
        else:
            col1, col2 = st.columns([2, 1])
            with col1:
                nama = st.text_input(TEXTS[lang]["search_name"]).strip().lower()
            with col2:
                jenis_filter = st.selectbox(TEXTS[lang]["search_type"], [TEXTS[lang]["all"]] + sorted(df[lk3_col].dropna().unique().tolist()))
            hasil = df.copy()
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
                    styled_df = hasil_display.style.apply(highlight_sio, axis=1)
                    st.dataframe(styled_df, use_container_width=True)
                else:
                    st.dataframe(hasil_display, use_container_width=True)

                # ================== GRAFIK ==================

                # --- Pie Chart Jenis LK3 dengan persentase ---
                pie_data = hasil[lk3_col].value_counts().reset_index()
                pie_data.columns = ["Jenis LK3", "Jumlah"]
                pie_data["Persentase"] = (pie_data["Jumlah"] / pie_data["Jumlah"].sum() * 100).round(1)

                pie_chart = alt.Chart(pie_data).mark_arc().encode(
                    theta="Jumlah",
                    color="Jenis LK3",
                    tooltip=["Jenis LK3", "Jumlah", "Persentase"]
                ).properties(
                    title="Distribusi Jenis LK3"
                )

                st.altair_chart(pie_chart, use_container_width=True)

                # --- Bar Chart Tanggal Pelaksanaan (Horizontal) dengan persentase ---
                if "TANGGAL PELAKSANAAN" in hasil.columns:
                    bar_data = hasil["TANGGAL PELAKSANAAN"].value_counts().reset_index()
                    bar_data.columns = ["Tanggal", "Jumlah"]
                    bar_data["Persentase"] = (bar_data["Jumlah"] / bar_data["Jumlah"].sum() * 100).round(1)

                    bar_chart = alt.Chart(bar_data).mark_bar().encode(
                        y=alt.Y("Tanggal", sort='-x', axis=alt.Axis(labelAngle=0, title="Tanggal Pelaksanaan")),
                        x=alt.X("Jumlah", title="Jumlah Data"),
                        tooltip=["Tanggal", "Jumlah", "Persentase"]
                    ).properties(
                        height=600,
                        title="Tanggal Peng-isu­an SIO"
                    )

                    st.altair_chart(bar_chart, use_container_width=True)

                # --- Bar Chart per Cabang / Site / Area dengan persentase ---
                cabang_col = next((col for col in hasil.columns if "CABANG" in col.upper()), None)

                if cabang_col:
                    cabang_data = hasil[cabang_col].value_counts().reset_index()
                    cabang_data.columns = ["Cabang", "Jumlah"]
                    cabang_data["Persentase"] = (cabang_data["Jumlah"] / cabang_data["Jumlah"].sum() * 100).round(1)

                    cabang_chart = alt.Chart(cabang_data).mark_bar().encode(
                        x=alt.X("Cabang", sort='-y', axis=alt.Axis(labelAngle=-45, title="Cabang / Site / Area")),
                        y=alt.Y("Jumlah", title="Jumlah Data"),
                        tooltip=["Cabang", "Jumlah", "Persentase"]
                    ).properties(
                        height=400,
                        title="Jumlah Data per Cabang/Site/Area"
                    )

                    st.altair_chart(cabang_chart, use_container_width=True)

                # ================== DOWNLOAD ==================
                csv_data = hasil.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Hasil (CSV)",
                    data=csv_data,
                    file_name="hasil_pencarian.csv",
                    mime="text/csv"
                )
            else:
                st.warning("❌ Tidak ada hasil untuk pencarian ini.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca data: {e}")

# -------------------------
# KONTAK & BANTUAN
# -------------------------
elif menu == TEXTS[lang]["contact"]:
    st.header(TEXTS[lang]["contact"])
    st.markdown("""
    **Helmalya RP**  
    📧 HelmalyaRP@unitedtractors.com  
    📱 0858 5982 3983  

    **Tito A**  
    📧 TitoA@unitedtractors.com  
    📱 0822 9973 3414  
    """)
    st.markdown(TEXTS[lang]["guide"])

