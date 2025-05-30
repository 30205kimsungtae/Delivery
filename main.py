import streamlit as st
import pandas as pd
import plotly.express as px

sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/export?format=csv&gid=778451492"

try:
    df = pd.read_csv(sheet_url)
    st.success("데이터 불러오기 성공!")
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류 발생: {e}")
    st.stop()

st.title("Google Sheets 데이터 시각화")

st.subheader("데이터 미리보기")
st.dataframe(df)

st.subheader("데이터 열 이름")
st.write(df.columns.tolist())

# 여기에 맞는 열 이름으로 수정
# 예: 일자, 수치
try:
    df['일자'] = pd.to_datetime(df['일자'], errors='coerce')
    fig = px.line(df, x='일자', y='수치', title='일자별 수치 변화')
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"시각화 중 오류: {e}")
