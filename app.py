import streamlit as st
from google import genai

# ---------------------------------------------------------
# 1. Konfigurasi Halaman & Judul
# ---------------------------------------------------------
st.set_page_config(page_title="E-Asesmen Generator", page_icon="🎓", layout="centered")

st.title("🎓 E-Asesmen Generator")
st.caption("Aplikasi Pembuat Soal Pintar Tingkat MI Ronas (Powered by Gemini)")

# ---------------------------------------------------------
# 2. Sidebar / Form Input Parameter
# ---------------------------------------------------------
st.sidebar.header("🔑 Pengaturan API")
api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

st.subheader("⚙️ Konfigurasi Soal")

# Kotak Input untuk Pengguna
nama_guru = st.text_input("Nama Guru Pengampu", placeholder="Contoh: M Zainal Abidin")
materi_pokok = st.text_input("Materi Pokok", placeholder="Contoh: Thoharoh")
submateri = st.text_input("Submateri", placeholder="Contoh: Najis, Hadast, Wudhu, Tayamum")

col1, col2 = st.columns(2)
with col1:
    bentuk_soal = st.selectbox("Bentuk Soal", ["Pilihan Ganda", "MCMA", "MCC", "Essai"])
with col2:
    jumlah_soal = st.number_input("Jumlah Soal", min_value=1, max_value=50, value=5)

tingkat_kesulitan = st.select_slider("Tingkat Kesulitan Soal", options=["Mudah", "Sedang", "HOTS (Tinggi)"])

# ---------------------------------------------------------
# 3. Proses Generate Soal Menggunakan Gemini API
# ---------------------------------------------------------
if st.button("🚀 Buat Naskah Soal", type="primary"):
    # Validasi input sebelum dijalankan
    if not api_key:
        st.error("Silakan masukkan Gemini API Key terlebih dahulu pada panel di sebelah kiri.")
    elif not materi_pokok:
        st.warning("Mohon isi Materi Pokok terlebih dahulu.")
    else:
        # Menampilkan animasi loading
        with st.spinner("Sedang menyusun naskah soal... Silakan tunggu beberapa saat."):
            try:
                # Menghubungkan ke API Gemini menggunakan SDK terbaru
                client = genai.Client(api_key=api_key)
                
                # Merangkum input pengguna menjadi instruksi (prompt) untuk AI
                prompt = f"""
                Bertindaklah sebagai tim pembuat soal ujian profesional tingkat Madrasah Ibtidaiyah.
                Buatkan naskah asesmen/ujian lengkap dengan kriteria berikut:
                - Nama Guru Pengampu: {nama_guru}
                - Materi Pokok: {materi_pokok}
                - Submateri: {submateri}
                - Bentuk Soal: {bentuk_soal}
                - Jumlah Soal: {jumlah_soal}
                - Tingkat Kesulitan: {tingkat_kesulitan}

                Ketentuan Format Output:
                1. Sertakan Kop/Header Naskah Soal yang rapi.
                2. Buat soal yang jelas, berkualitas, dan sesuai tingkat kesulitan.
                3. Berikan Kunci Jawaban di bagian akhir naskah.
                """

                # Mengirim perintah ke model Gemini Flash
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )

                # Menampilkan hasil teks dari AI ke layar
                st.success("Naskah soal berhasil dibuat!")
                st.markdown("---")
                st.markdown(response.docx)

                # Menambahkan Tombol Unduh (Download)
                st.download_button(
                    label="📥 Download Naskah Soal (.docx)",
                    data=response.docx,
                    file_name=f"Soal_{materi_pokok.replace(' ', '_')}.docx",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi API: {e}")