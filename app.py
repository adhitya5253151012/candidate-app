import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# ======================
# FONT + ICON
# ======================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ======================
# CSS (PIXEL + ANIMASI)
# ======================
st.markdown("""
<style>
body {
    font-family: 'DM Sans', sans-serif;
    background: #f1f5f9;
}

/* HEADER */
.header {
    background: linear-gradient(90deg,#4338ca,#7c3aed);
    padding: 20px;
    border-radius: 10px;
    color: white;
    margin-bottom: 10px;
}

/* SIDEBAR */
.sidebar-canva {
    background: linear-gradient(180deg,#4338ca,#6366f1);
    padding: 20px;
    border-radius: 12px;
    color: white;
    height: 90vh;
}

/* NAV */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    border-radius: 8px;
    cursor: pointer;
    color: rgba(255,255,255,0.8);
    transition: all 0.3s ease;
    position: relative;
}

.nav-item:hover {
    background: rgba(255,255,255,0.15);
    color: white;
    transform: translateX(5px) scale(1.02);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
}

.nav-active {
    background: rgba(255,255,255,0.25);
    color: white;
}

/* CARD */
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

.best-card {
    background: linear-gradient(135deg,#312e81,#4338ca,#6366f1);
    color: white;
}

/* ANIMASI */
@keyframes fadeIn {
    from {opacity:0; transform:translateY(-10px);}
    to {opacity:1; transform:translateY(0);}
}

.card {
    animation: fadeIn 0.5s ease;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown("""
<div class="header">
<h2>🎯 Sistem Pemilihan Kandidat Terbaik</h2>
<p>Analisis berbasis data & matematika modern</p>
</div>
""", unsafe_allow_html=True)

# ======================
# LAYOUT
# ======================
left, right = st.columns([1,4])

# ======================
# SIDEBAR
# ======================
with left:
    st.markdown("""
<div class="sidebar-canva">
    <h3>🏆 Sistem Kandidat</h3>

    st.write("")

    st.subheader("Input Kandidat")

    nama = st.text_input("Nama")
    tes = st.number_input("Tes", 0, 100, 75)
    waw = st.number_input("Wawancara", 0, 100, 75)
    exp = st.number_input("Pengalaman", 0, 10, 2)

    if "data" not in st.session_state:
        st.session_state.data = []

    if st.button("Tambah Kandidat"):
        skor = 0.4*tes + 0.35*waw + 0.25*(exp*10)

        st.session_state.data.append({
            "Nama": nama,
            "Tes": tes,
            "Waw": waw,
            "Exp": exp,
            "Skor": skor
        })

# ======================
# KONTEN
# ======================
with right:

    data = st.session_state.data

    if data:
        df = pd.DataFrame(data).sort_values("Skor", ascending=False)

        # BEST
        best = df.iloc[0]

        st.markdown(f"""
        <div class="card best-card">
            <h3>🏆 Kandidat Terbaik</h3>
            <h2>{best['Nama']}</h2>
            <h1>{round(best['Skor'],2)}</h1>
            <p>Tes: {best['Tes']} | Waw: {best['Waw']} | Exp: {best['Exp']}</p>
        </div>
        """, unsafe_allow_html=True)

        # GRID 1
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="card"><h4>Data Kandidat</h4></div>', unsafe_allow_html=True)
            st.dataframe(df)

        with c2:
            st.markdown('<div class="card"><h4>Cosine Similarity</h4></div>', unsafe_allow_html=True)

            ideal = np.array([100,100,5])

            def cos(a,b):
                return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

            matrix = df[["Tes","Waw","Exp"]].values
            df["Sim"] = [cos(i, ideal) for i in matrix]

            st.dataframe(df[["Nama","Sim"]])

        with c3:
            st.markdown('<div class="card"><h4>Boolean</h4></div>', unsafe_allow_html=True)
            df["Boolean"] = df["Skor"] >= 70
            st.dataframe(df[["Nama","Boolean"]])

        # GRID 2
        c4, c5, c6 = st.columns(3)

        with c4:
            st.markdown('<div class="card"><h4>Matriks</h4></div>', unsafe_allow_html=True)
            st.write(matrix)

        with c5:
            st.markdown('<div class="card"><h4>Determinan</h4></div>', unsafe_allow_html=True)
            if len(matrix) >= 3:
                det = np.linalg.det(matrix[:3])
                st.write(round(det,2))

        with c6:
            st.markdown('<div class="card"><h4>Grafik</h4></div>', unsafe_allow_html=True)
            st.bar_chart(df.set_index("Nama")["Skor"])

        # HIMPUNAN
        st.markdown('<div class="card"><h4>Himpunan</h4></div>', unsafe_allow_html=True)

        A = set(df[df["Tes"]>=70]["Nama"])
        B = set(df[df["Waw"]>=75]["Nama"])

        st.write("A:", A)
        st.write("B:", B)
        st.write("A ∩ B:", A & B)
        st.write("A ∪ B:", A | B)

        # KOMBINASI
        st.markdown('<div class="card"><h4>Kombinasi</h4></div>', unsafe_allow_html=True)

        from itertools import combinations
        comb = list(combinations(df["Nama"],2))
        st.write(comb)

# ======================
# MODEL
# ======================
st.markdown('<div class="card"><h4>Model Matematis</h4></div>', unsafe_allow_html=True)

st.write("S = 0.4x + 0.35y + 0.25z")
st.write("F(x,y,z) = (x ∧ y) ∨ z")
