import streamlit as st
import pandas as pd
import plotly.express as px

# 구글 스프레드시트에서 데이터 가져오기
sheet_url = "https://docs.google.com/spreadsheets/d/1QN1pWq2dLvLLl3Rejwxa_vIwcGg9pQic9dK6pZC-TT4/gviz/tq?tqx=out:csv&gid=778451492"
df = pd.read_csv(sheet_url)

st.title("Google Sheets 데이터 시각화")

# 데이터프레임 보여주기
st.subheader("원본 데이터")
st.dataframe(df)

# 예: 특정 열을 선택해서 시각화
if '날짜' in df.columns and '값' in df.columns:
    df['날짜'] = pd.to_datetime(df['날짜'])  # 날짜 형식 변환

    fig = px.line(df, x='날짜', y='값', title='날짜별 값 변화')
    st.plotly_chart(fig)
else:
    st.warning("시각화할 수 있는 '날짜' 또는 '값' 열이 없습니다.")
