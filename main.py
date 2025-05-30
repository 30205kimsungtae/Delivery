import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"
df = pd.read_csv(sheet_url)

st.title("✨ 군집 점 잘 보이도록 DBSCAN 튜닝 시각화")

coords = df[['Latitude', 'Longitude']].dropna()
scaler = StandardScaler()
coords_scaled = scaler.fit_transform(coords)

# DBSCAN 파라미터 조정
db = DBSCAN(eps=0.5, min_samples=5)
labels = db.fit_predict(coords_scaled)
df['cluster'] = labels

n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
st.markdown(f"🔎 군집 개수: `{n_clusters}`")

# 군집별 포인트 개수
cluster_counts = df['cluster'].value_counts().to_dict()
df['cluster_size'] = df['cluster'].map(cluster_counts)

# 군집 크기별 마커 크기
size_min = 10
size_max = 40
max_count = max(cluster_counts.values())

def size_mapper(count):
    return (count / max_count) * (size_max - size_min) + size_min

df['marker_size'] = df['cluster_size'].apply(size_mapper)

# 군집 번호가 -1인 이상치는 투명도 낮게 처리
df['opacity'] = df['cluster'].apply(lambda x: 0.3 if x == -1 else 0.8)

fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color=df['cluster'].astype(str),
    size='marker_size',
    opacity=df['opacity'],
    hover_name="Num",
    hover_data={'cluster':True, 'cluster_size':True},
    zoom=10,
    height=650,
    title="DBSCAN 튜닝 군집 시각화"
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

st.plotly_chart(fig)
