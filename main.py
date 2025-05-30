import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import plotly.colors as pc

# 데이터 로드
sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"
df = pd.read_csv(sheet_url)

st.title("🔧 DBSCAN 군집 시각화 — eps 슬라이더 조절")

coords = df[['Latitude', 'Longitude']].dropna()
scaler = StandardScaler()
coords_scaled = scaler.fit_transform(coords)

# 슬라이더: eps 값 조절 (0.1 ~ 1.0)
eps_value = st.slider("eps (클러스터 반경) 선택", 0.1, 1.0, 0.4, 0.05)

# 군집 실행
db = DBSCAN(eps=eps_value, min_samples=4)
labels = db.fit_predict(coords_scaled)
df['cluster'] = labels

# 군집 개수 출력
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
st.markdown(f"🔎 현재 군집 개수: **{n_clusters}**")

# 색상 팔레트 설정
unique_clusters = sorted(set(labels))
if -1 in unique_clusters:
    unique_clusters.remove(-1)

colors = pc.qualitative.Dark24
cluster_color_map = {c: colors[i % len(colors)] for i, c in enumerate(unique_clusters)}
cluster_color_map[-1] = 'lightgray'  # 이상치 색

df['color'] = df['cluster'].map(cluster_color_map)

# 시각화
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color='color',
    hover_name="Num",
    zoom=10,
    height=650,
    title=f"DBSCAN 군집 시각화 (eps={eps_value})"
)

fig.update_traces(marker=dict(size=12, opacity=1, line=dict(width=1, color='black')))
fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":30,"l":0,"b":0}, showlegend=False)

st.plotly_chart(fig)
