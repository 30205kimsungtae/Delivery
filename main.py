import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="배달 위치 K-Means 클러스터링", layout="wide")

st.title("🚚 배달 위치 K-Means 클러스터링 지도")
st.markdown("구글 스프레드시트 데이터를 불러와 K-Means 군집화 후 지도에 시각화합니다.")

# 구글 스프레드시트 csv 링크 (export?format=csv&gid=숫자 형태)
sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"
df = pd.read_csv(sheet_url)

st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 위도/경도 컬럼명
lat_col = 'Latitude'
lon_col = 'Longitude'

# 클러스터 개수 선택
n_clusters = st.slider("클러스터 개수 선택 (K)", min_value=2, max_value=10, value=3)

coords = df[[lat_col, lon_col]]

# K-Means 클러스터링
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(coords)

# 지도 중앙 좌표 계산
center = [df[lat_col].mean(), df[lon_col].mean()]
m = folium.Map(location=center, zoom_start=12)

colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']

# 마커 추가
for i, row in df.iterrows():
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=6,
        color=colors[int(row['Cluster']) % len(colors)],
        fill=True,
        fill_opacity=0.8,
        popup=f"Cluster {row['Cluster']}"
    ).add_to(m)

st.subheader("클러스터링 결과 지도")
st_folium(m, width=900, height=600)

st.subheader("클러스터링 결과 데이터")
st.dataframe(df)

st.plotly_chart(fig)
