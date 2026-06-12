import streamlit as st
import pandas as pd

# 웹 페이지 제목 및 설명
st.title("🩸 개인 혈당 기록 및 진단 프로그램")
st.write("혈당 수치를 입력하고 기록을 확인해 보세요.")

# 1. 스트림릿 세션 상태(Session State) 초기화
# 페이지가 새로고침되어도 데이터가 유지되도록 배열(리스트)을 생성합니다.
if "blood_history" not in st.session_state:
    st.session_state.blood_history = []

# 2. 사용자 입력 위젯
# 숫자 입력창과 데이터 추가 버튼 생성
sugar_input = st.number_input(
    "혈당량을 입력하세요 (mg/dL)", 
    min_value=0, 
    max_value=500, 
    value=100, 
    step=1
)

# 버튼 디자인을 위해 레이아웃 분할
col1, col2 = st.columns([1, 4])

with col1:
    add_button = st.button("기록 추가", type="primary")
with col2:
    reset_button = st.button("기록 초기화")

# 3. 데이터 추가 및 판정 로직
if add_button:
    if sugar_input > 0:
        # 혈당량에 따른 상태 판정
        if sugar_input < 70:
            status = "저혈당"
            color_func = st.error # 빨간색 알림
        elif sugar_input < 100:
            status = "정상"
            color_func = st.success # 초록색 알림
        elif sugar_input < 126:
            status = "당뇨위험군"
            color_func = st.warning # 노란색 알림
        else:
            status = "고혈당(당뇨 가능성)"
            color_func = st.error # 빨간색 알림
        
        # 세션 상태 리스트에 (입력값, 판정결과) 추가
        st.session_state.blood_history.append({"혈당량": sugar_input, "상태": status})
        
        # 현재 입력 결과 출력
        color_func(f"입력하신 혈당은 **{sugar_input} mg/dL** 이며, **[{status}]** 상태입니다.")
    else:
        st.info("0보다 큰 올바른 혈당 수치를 입력해 주세요.")

# 초기화 버튼을 누른 경우
if reset_button:
    st.session_state.blood_history = []
    st.rerun()

# 4. 결과 출력 (누적 데이터 시각화)
st.markdown("---")
st.subheader("📊 누적 혈당 기록")

if st.session_state.blood_history:
    # 리스트 데이터를 데이터프레임으로 변환하여 웹에 표로 출력
    df = pd.DataFrame(st.session_state.blood_history)
    
    # 깔끔한 표(DataFrame)로 출력
    st.dataframe(df, use_container_width=True)
    
    # 통계치 제공 (보너스 기능!)
    avg_sugar = df["혈당량"].mean()
    st.metric(label="현재까지의 평균 혈당", value=f"{avg_sugar:.1f} mg/dL")
else:
    st.info("아직 입력된 기록이 없습니다. 혈당을 입력하고 '기록 추가'를 눌러보세요.")