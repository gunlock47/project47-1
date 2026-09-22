import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="뇌졸중 예측 실습실",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 뇌졸중 예측 실습실")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/stroke.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8")
    return df


df = load_data()

# ------------------------------------------------------------
# ✏️ 여기에 열 이름별 우리말 뜻을 교재를 보고 직접 채워 넣으세요.
# 큰따옴표 "" 안에 우리말 뜻을 입력하면 아래 표에 바로 반영됩니다.
# ------------------------------------------------------------
column_meaning = {
    "id": "",
    "gender": "",
    "age": "",
    "hypertension": "",
    "heart_disease": "",
    "ever_married": "",
    "work_type": "",
    "Residence_type": "",
    "avg_glucose_level": "",
    "bmi": "",
    "smoking_status": "",
    "stroke": "",
}

# ------------------------------------------------------------
# ✏️ 여기에 데이터 출처를 교재를 보고 직접 채워 넣으세요.
# ------------------------------------------------------------
data_source_text = ""

st.markdown("이 데이터가 어떤 데이터인지 살펴보는 화면입니다.")

# ------------------------------------------------------------
# 큰 숫자 카드 네 개
# ------------------------------------------------------------
total_count = len(df)
total_columns = df.shape[1]
stroke_count = int((df["stroke"] == 1).sum())
stroke_ratio = stroke_count / total_count * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("전체 사람 수", f"{total_count:,} 명")
col2.metric("열 개수", f"{total_columns} 개")
col3.metric("뇌졸중(stroke=1) 인원", f"{stroke_count:,} 명")
col4.metric("뇌졸중 비율", f"{stroke_ratio:.2f} %")

st.divider()


# ------------------------------------------------------------
# 열 정보 표: 열 이름 / 우리말 뜻 / 값의 종류 / 빈 값 개수
# ------------------------------------------------------------
def get_value_kind(column_name):
    series = df[column_name]
    non_null = series.dropna()
    # 서로 다른 값이 적으면 범주형으로 보고 값 목록을 보여줌
    if series.dtype == object or non_null.nunique() <= 5:
        unique_values = sorted(non_null.unique().tolist(), key=lambda x: str(x))
        return ", ".join(str(v) for v in unique_values)
    else:
        return f"{non_null.min()} ~ {non_null.max()} 사이의 숫자"


info_rows = []
for col in df.columns:
    info_rows.append(
        {
            "열 이름": col,
            "우리말 뜻": column_meaning.get(col, ""),
            "값의 종류": get_value_kind(col),
            "빈 값 개수": int(df[col].isna().sum()),
        }
    )

info_df = pd.DataFrame(info_rows)

st.subheader("열(컬럼) 설명")
st.caption("‘우리말 뜻’ 칸은 비어 있습니다. main.py의 column_meaning 딕셔너리에 교재를 보고 직접 채워 넣으세요.")
st.dataframe(info_df, use_container_width=True, hide_index=True)

st.divider()

# ------------------------------------------------------------
# 데이터 미리보기 (처음 다섯 줄)
# ------------------------------------------------------------
st.subheader("데이터 미리보기 (처음 5줄)")
st.dataframe(df.head(), use_container_width=True, hide_index=True)

st.divider()

# ------------------------------------------------------------
# 데이터 출처
# ------------------------------------------------------------
st.subheader("데이터 출처")
if data_source_text:
    st.write(data_source_text)
else:
    st.info("main.py의 data_source_text 변수에 교재를 보고 데이터 출처를 직접 적어 넣으세요.")
