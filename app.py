import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Smart Candidate System", layout="wide")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.main {background-color: #f5f7fa;}
h1 {color: #1f77b4; text-align: center;}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🎯 Smart Candidate Selection System")
st.write("Menggunakan konsep Matematika Terapan lengkap")

# =========================
# SIDEBAR INPUT
# =========================
st.sidebar.header("📝 Input Kandidat")

nama = st.sidebar.text_input("Nama")
tes = st.sidebar.slider("Nilai Tes", 0, 100, 70)
wawancara = st.sidebar.slider("Wawancara", 0, 100, 75)
pengalaman = st.sidebar.slider("Pengalaman", 0, 10, 2)

if "data" not in st.session_state:
    st.session_state.data = []

# =========================
# TAMBAH DATA
# =========================
if st.sidebar.button("➕ Tambah Kandidat"):

    # SPL
    skor = 0.4*tes + 0.3*wawancara + 0.3*(pengalaman*10)

    # LOGIKA KOMPLEKS
    if tes >= 70 and wawancara >= 75 and pengalaman >= 2:
        status = "Sangat Layak"
    elif tes >= 60 and wawancara >= 70:
        status = "Layak"
    else:
        status = "Tidak Layak"

    st.session_state.data.append({
        "Nama": nama,
        "Tes": tes,
        "Wawancara": wawancara,
        "Pengalaman": pengalaman,
        "Skor": skor,
        "Status": status
    })

    st.sidebar.success("Berhasil ditambahkan!")

# =========================
# PROSES DATA
# =========================
if len(st.session_state.data) > 0:

    df = pd.DataFrame(st.session_state.data)
    df = df.sort_values(by="Skor", ascending=False)

    col1, col2 = st.columns(2)

    # =========================
    # DATA
    # =========================
    with col1:
        st.subheader("📊 Data Kandidat")
        st.dataframe(df, use_container_width=True)

    # =========================
    # TERBAIK
    # =========================
    with col2:
        terbaik = df.iloc[0]
        st.subheader("🏆 Kandidat Terbaik")
        st.markdown(f"""
        <div class="card">
        <h2>{terbaik['Nama']}</h2>
        <p>Skor: <b>{terbaik['Skor']:.2f}</b></p>
        <p>Status: {terbaik['Status']}</p>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # MATRIKS
    # =========================
    st.subheader("📐 Matriks")
    matrix = df[["Tes", "Wawancara", "Pengalaman"]].values
    st.write(matrix)

    # =========================
    # DETERMINAN
    # =========================
    if len(matrix) >= 3:
        det = np.linalg.det(matrix[:3])
        st.write("📌 Determinan (3 kandidat pertama):", det)

    # =========================
    # VEKTOR (COSINE)
    # =========================
    st.subheader("📏 Cosine Similarity")

    ideal = np.array([100, 100, 5])

    def cosine(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    df["Similarity"] = [cosine(i, ideal) for i in matrix]
    st.dataframe(df[["Nama", "Similarity"]])

    # =========================
    # HIMPUNAN
    # =========================
    st.subheader("📚 Himpunan")

    lulus_tes = set(df[df["Tes"] >= 70]["Nama"])
    lulus_wawancara = set(df[df["Wawancara"] >= 75]["Nama"])

    st.write("Lulus Tes:", lulus_tes)
    st.write("Lulus Wawancara:", lulus_wawancara)
    st.write("Irisan (∩):", lulus_tes.intersection(lulus_wawancara))
    st.write("Gabungan (∪):", lulus_tes.union(lulus_wawancara))

    # =========================
    # KOMBINATORIKA
    # =========================
    st.subheader("🔢 Kombinatorika")

    kombinasi = list(itertools.combinations(df["Nama"], 2))
    st.write("Kombinasi 2 Kandidat:", kombinasi)

    # =========================
    # BOOLEAN
    # =========================
    st.subheader("⚙️ Boolean")

    def boolean(x, y, z):
        return (x and y) or z

    hasil_boolean = boolean(tes >= 70, wawancara >= 75, pengalaman >= 2)
    st.write("F(x,y,z) = (x ∧ y) ∨ z →", hasil_boolean)

    # =========================
    # GRAFIK
    # =========================
    st.subheader("📈 Grafik Skor")

    fig, ax = plt.subplots()
    ax.bar(df["Nama"], df["Skor"])
    ax.set_title("Perbandingan Skor Kandidat")

    st.pyplot(fig)

# =========================
# MODEL MATEMATIS
# =========================
st.subheader("📘 Model Matematis")

st.markdown("""
- SPL: S = 0.4x + 0.3y + 0.3z  
- Logika: aturan seleksi kompleks  
- Boolean: F(x,y,z) = (x ∧ y) ∨ z  
- Himpunan: ∪ dan ∩  
- Kombinatorika: kombinasi kandidat  
- Matriks: representasi data  
- Determinan: analisis solusi  
- Vektor: cosine similarity  
""")

# =========================
# RESET
# =========================
if st.button("🔄 Reset"):
    st.session_state.data = []
    st.success("Data direset!")