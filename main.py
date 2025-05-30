import streamlit as st
import pandas as pd
import plotly.express as px

# 수정된 CSV 링크
sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"

# 데이터 불러오기
try:
    df = pd.read_csv(sheet_url)
    st.success("데이터 불러오기 성공!")
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류 발생: {e}")
    st.stop()

st.title("Google Sheets 데이터 시각화")
st.dataframe(df)

# 시각화
if '날짜' in df.columns and '값' in df.columns:
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    fig = px.line(df, x='날짜', y='값', title='날짜별 값 추이')
    st.plotly_chart(fig)
else:
    st.warning("시각화할 수 있는 '날짜' 또는 '값' 열이 없습니다.")
