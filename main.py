import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# 데이터 불러오기
sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"
df = pd.read_csv(sheet_url)

st.title("📍 Plotly 기반 지도 군집 시각화")

# 데이터 전처리
coords = df[['Latitude', 'Longitude']].dropna()

# 좌표 정규화 (거리 기준 맞추기)
scaler = StandardScaler()
coords_scaled = scaler.fit_transform(coords)

# DBSCAN 클러스터링
db = DBSCAN(eps=0.3, min_samples=3)
labels = db.fit_predict(coords_scaled)
df['cluster'] = labels

# 군집 수 출력
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
st.markdown(f"🔎 군집 개수: `{n_clusters}`")

# Plotly 지도 시각화
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color=df['cluster'].astype(str),
    hover_name="Num",
    zoom=10,
    height=650,
    title="DBSCAN 기반 위치 군집 시각화"
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0, "t":30, "l":0, "b":0})

st.plotly_chart(fig)
