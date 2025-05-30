import streamlit as st
import pandas as pd
import plotly.express as px

# 구글 시트에서 CSV 불러오기
sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"

try:
    df = pd.read_csv(sheet_url)
    st.success("데이터 불러오기 성공!")
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류 발생: {e}")
    st.stop()

st.title("위도/경도 지도 시각화")
st.dataframe(df)

# 위도 경도 시각화
if 'Latitude' in df.columns and 'Longitude' in df.columns:
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        zoom=10,
        height=600,
        hover_name="Num",
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
else:
    st.warning("Latitude 또는 Longitude 열이 없습니다.")

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

st.plotly_chart(fig)
