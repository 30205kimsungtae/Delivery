import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# 데이터 불러오기
sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"
df = pd.read_csv(sheet_url)

st.title("📍 Plotly 군집 시각화 - 마커 크기 및 군집 정보 강화")

# 좌표 전처리
coords = df[['Latitude', 'Longitude']].dropna()

scaler = StandardScaler()
coords_scaled = scaler.fit_transform(coords)

# DBSCAN 클러스터링
db = DBSCAN(eps=0.3, min_samples=3)
labels = db.fit_predict(coords_scaled)
df['cluster'] = labels

# 군집별 포인트 개수 계산
cluster_counts = df['cluster'].value_counts().to_dict()

# 각 행마다 해당 군집 크기를 추가
df['cluster_size'] = df['cluster'].map(cluster_counts)

# 군집 수
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
st.markdown(f"🔎 군집 개수: `{n_clusters}`")

# 마커 크기 조정 (최소 10, 최대 40 크기 범위)
size_min = 10
size_max = 40

# 군집 크기 기준 마커 크기 함수
def size_mapper(count):
    # 군집 크기 스케일링
    max_count = max(cluster_counts.values())
    scaled = (count / max_count) * (size_max - size_min) + size_min
    return scaled

df['marker_size'] = df['cluster_size'].apply(size_mapper)

# Plotly 시각화
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color=df['cluster'].astype(str),
    size='marker_size',
    hover_name="Num",
    hover_data={'cluster':True, 'cluster_size':True, 'marker_size':False},
    zoom=10,
    height=650,
    title="DBSCAN 군집 시각화 (마커 크기 = 군집 크기)"
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0, "t":30, "l":0, "b":0})

st.plotly_chart(fig)
