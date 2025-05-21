import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px

# Data
data = {
    'Provinsi': [
        'Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 
        'Bengkulu', 'Lampung', 'Kepulauan Bangka Belitung', 'Kepulauan Riau', 
        'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'DI Yogyakarta', 'Jawa Timur', 'Banten', 
        'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat', 
        'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 
        'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 
        'Gorontalo', 'Sulawesi Barat', 'Maluku', 'Maluku Utara', 'Papua', 'Papua Barat', 
        'Papua Selatan', 'Papua Tengah', 'Papua Pegunungan'
    ],
    'Latitude': [
        5.5483, 3.5852, -0.3054, 0.5071, -1.4854, -3.3194,
        -3.5778, -4.5586, -2.7411, 3.9457,
        -6.2088, -6.9175, -7.1500, -7.7956, -7.2504, -6.1202,
        -8.4095, -8.6529, -10.1772, -0.0646,
        -1.6815, -3.0035, 0.5247, 3.0160,
        1.4931, -0.8989, -5.1333, -4.1290,
        0.7013, -2.8587, -3.2385, 0.8829,
        -0.8897, -3.8407, -3.9124, -4.7109, -4.2695
    ],
    'Longitude': [
        95.3238, 98.6722, 100.3691, 101.4478, 102.4381, 104.7648,
        102.2655, 105.4264, 106.1398, 108.1429,
        106.8456, 107.6191, 110.1403, 110.3695, 112.7521, 106.1500,
        115.1889, 116.0556, 123.5973, 109.3425,
        113.4784, 114.5886, 117.2490, 117.6686,
        124.8442, 121.5833, 119.4221, 122.5270,
        122.4457, 119.2838, 129.7392, 127.5284,
        133.5498, 137.7403, 138.0569, 138.9026, 137.3870
    ],
    'IPM_2020': [
        71.94, 73.29, 73.62, 73.84, 74.65, 73.48, 72.91, 73.00, 72.28, 74.14,
        76.40, 81.92, 72.61, 71.88, 79.95, 72.49, 72.93, 75.86, 69.22, 66.48,
        68.44, 71.82, 71.75, 77.44, 70.85, 73.79, 71.31, 73.27, 71.56, 70.98,
        69.11, 70.05, 70.92, 67.47, 67.47, 70.92, 70.05
    ],
    'IPM_2021': [
        72.18, 71.70, 72.65, 73.30, 71.63, 70.90, 71.02, 70.45, 73.77, 75.79,
        81.11, 72.45, 72.79, 80.22, 72.14, 72.45, 75.50, 68.58, 65.65, 67.90,
        71.25, 71.15, 76.88, 70.38, 73.30, 70.74, 72.82, 71.02, 70.55, 68.49,
        69.49, 70.32, 72.19, 61.39, 61.39, 72.19, 70.32
    ],
    'IPM_2022': [
        72.80, 72.71, 73.00, 73.71, 72.28, 71.58, 71.61, 71.15, 74.14, 76.40,
        81.65, 72.93, 73.20, 80.64, 72.49, 72.93, 75.86, 69.22, 66.48, 68.44,
        71.82, 71.75, 77.44, 70.85, 73.79, 71.31, 73.27, 71.56, 70.98, 69.11,
        70.05, 70.92, 67.47, 62.79, 67.90, 60.25, 54.43
    ],
    'IPM_2023': [
        73.29, 73.62, 73.84, 74.65, 73.48, 72.91, 73.00, 72.28, 74.14, 76.40,
        81.65, 72.93, 73.20, 80.64, 72.49, 72.93, 75.86, 69.22, 66.48, 68.44,
        71.82, 71.75, 77.44, 70.85, 73.79, 71.31, 73.27, 71.56, 70.98, 69.11,
        70.05, 70.92, 67.47, 62.79, 67.90, 60.25, 54.43
    ],
    'IPM_2024': [
        73.40, 73.37, 73.58, 74.30, 73.60, 72.99, 73.10, 72.50, 74.60, 76.80,
        84.15, 73.10, 73.50, 80.90, 75.35, 73.10, 75.10, 69.80, 67.00, 69.00,
        72.50, 72.30, 78.00, 71.50, 73.80, 72.10, 71.20, 69.50, 70.50, 71.00,
        68.00, 63.50, 68.50, 61.00, 55.00, 70.20, 63.00
    ]
}


df = pd.DataFrame(data)

# Data tetap sama (pakai yang kamu kasih)
def buat_peta(tahun, prov_filter=None):
    kolom_ipm = f'IPM_{tahun}'
    center_coordinates = [-2.548926, 118.0148634]
    m = folium.Map(location=center_coordinates, zoom_start=5)

    df_map = df if prov_filter is None else df[df['Provinsi'] == prov_filter]

    for idx, row in df_map.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=7,
            color='crimson',
            fill=True,
            fill_color='crimson',
            fill_opacity=0.6,
            tooltip=f"{row['Provinsi']}: {row[kolom_ipm]}"
        ).add_to(m)

    return m

def buat_radar_chart(tahun_list):
    fig = go.Figure()
    for year in tahun_list:
        fig.add_trace(go.Scatterpolar(
            r=df[f'IPM_{year}'],
            theta=df['Provinsi'],
            fill='toself',
            name=f'IPM {year}'
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[60, 100])
        ),
        title=dict(text=f"Radar Chart IPM Tahun {' & '.join(map(str, tahun_list))}", x=0.5, font=dict(size=20, family="Arial Black")),
        legend=dict(title="Tahun", font=dict(size=12), orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

def buat_bar_chart(tahun, prov_filter=None):
    kolom_ipm = f'IPM_{tahun}'
    df_bar = df if prov_filter is None else df[df['Provinsi'] == prov_filter]
    fig = px.bar(df_bar.sort_values(kolom_ipm, ascending=False), 
                 x='Provinsi', y=kolom_ipm,
                 labels={kolom_ipm: f'IPM {tahun}', 'Provinsi': 'Provinsi'},
                 title=f"IPM Provinsi Tahun {tahun}")
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def summary_ipm(tahun, prov_filter=None):
    kolom_ipm = f'IPM_{tahun}'
    df_stat = df if prov_filter is None else df[df['Provinsi'] == prov_filter]
    avg = df_stat[kolom_ipm].mean()
    min_val = df_stat[kolom_ipm].min()
    max_val = df_stat[kolom_ipm].max()
    return avg, min_val, max_val

st.set_page_config(page_title="Dashboard IPM Indonesia", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("Kontrol Dashboard")

# Pilihan tahun peta dan grafik bar
tahun = st.sidebar.selectbox("Pilih Tahun untuk Peta & Grafik Bar:", options=["2020", "2021", "2022", "2023", "2024"])

# Filter provinsi
provinsi_list = ["Semua"] + list(df['Provinsi'].unique())
provinsi = st.sidebar.selectbox("Filter Provinsi (opsional):", options=provinsi_list)
prov_filter = None if provinsi == "Semua" else provinsi

# Pilihan radar chart: semua tahun atau pilih beberapa tahun
st.sidebar.markdown("---")
st.sidebar.subheader("Pengaturan Radar Chart")
opsi_radar = st.sidebar.radio("Pilih Radar Chart:", options=["Semua Tahun (2020-2024)", "Pilih Tahun"])

if opsi_radar == "Semua Tahun (2020-2024)":
    radar_tahun = list(range(2020, 2025))
else:
    radar_tahun = st.sidebar.multiselect("Pilih Tahun Radar Chart:", options=[2020,2021,2022,2023,2024], default=[2023,2024])
    if not radar_tahun:
        st.sidebar.warning("Pilih minimal satu tahun untuk radar chart!")

# --- Layout utama ---

st.title("Dashboard Sebaran IPM Indonesia")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Data IPM Tahun {tahun} {'- '+provinsi if prov_filter else ''}")
    st.dataframe(
        df[['Provinsi', f'IPM_{tahun}']][df['Provinsi'] == prov_filter] if prov_filter else df[['Provinsi', f'IPM_{tahun}']].sort_values(by=f'IPM_{tahun}', ascending=False),
        use_container_width=True
    )

with col2:
    st.subheader(f"Peta Sebaran IPM Tahun {tahun} {'- '+provinsi if prov_filter else ''}")
    peta = buat_peta(tahun, prov_filter)
    st_folium(peta, width=700, height=500)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Grafik Bar IPM")
    bar_chart = buat_bar_chart(tahun, prov_filter)
    st.plotly_chart(bar_chart, use_container_width=True)

with col4:
    st.subheader("Summary Statistik IPM")
    avg, min_val, max_val = summary_ipm(tahun, prov_filter)
    st.metric(label=f"Rata-rata IPM {tahun}", value=f"{avg:.2f}")
    st.metric(label=f"IPM Terendah {tahun}", value=f"{min_val:.2f}")
    st.metric(label=f"IPM Tertinggi {tahun}", value=f"{max_val:.2f}")

st.markdown("---")

if radar_tahun:
    st.subheader(f"Radar Chart IPM Tahun {' & '.join(map(str, radar_tahun))}")
    radar_chart = buat_radar_chart(radar_tahun)
    st.plotly_chart(radar_chart, use_container_width=True)
else:
    st.info("Pilih setidaknya satu tahun radar chart di sidebar.")

st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    <footer>
        Dibuat Oleh Kelompok 6
    </footer>
    """,
    unsafe_allow_html=True
)



