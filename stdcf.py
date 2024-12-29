import streamlit as st
import pandas as pd

st.title("DCF 계산기")

# 입력 검증 함수
def validate_inputs(inputs):
    for key, value in inputs.items():
        if value == "":
            st.error(f"{key} 값을 입력해주세요.")
            return False
        
        if key == "초기 연도 매출액" and float(value) <= 0:
            st.error("초기 연도 매출액은 0보다 커야 합니다.")
            return False
        
        if key != "초기 연도 매출액" and (float(value) < 0 or float(value) > 100):
            st.error(f"{key} 값은 0에서 100 사이여야 합니다.")
            return False
    return True

# DCF 계산 함수
def calculate_dcf(inputs, discount_rate, terminal_growth_rate):
    revenue = float(inputs["초기 연도 매출액"])
    growth_rate = float(inputs["매출 성장률 (%)"]) / 100
    operating_margin = float(inputs["영업이익률 (%)"]) / 100
    tax_rate = float(inputs["세율 (%)"]) / 100
    reinvestment_rate = float(inputs["재투자율 (%)"]) / 100

    years = 5
    fcf = []
    
    for year in range(1, years + 1):
        revenue *= (1 + growth_rate)
        operating_income = revenue * operating_margin
        tax = operating_income * tax_rate
        net_operating_profit_after_tax = operating_income - tax
        free_cash_flow = net_operating_profit_after_tax * (1 - reinvestment_rate)
        fcf.append(free_cash_flow)

    discounted_fcf = [fcf[t] / ((1 + discount_rate) ** (t + 1)) for t in range(years)]

    terminal_value = fcf[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)
    
    enterprise_value = sum(discounted_fcf) + discounted_terminal_value

    return enterprise_value, discounted_fcf, discounted_terminal_value

# 민감도 분석 함수
def run_sensitivity_analysis(inputs, discount_rate, terminal_growth_rate):
    discount_rates = [discount_rate - 0.01, discount_rate, discount_rate + 0.01]
    growth_rates = [terminal_growth_rate - 0.01, terminal_growth_rate, terminal_growth_rate + 0.01]

    sensitivity = pd.DataFrame(index=[f"{r*100:.1f}%" for r in discount_rates], 
                               columns=[f"{g*100:.1f}%" for g in growth_rates])

    for r in discount_rates:
        for g in growth_rates:
            ev, _, _ = calculate_dcf(inputs, r, g)
            sensitivity.loc[f"{r*100:.1f}%"][f"{g*100:.1f}%"] = round(ev, 2)
    
    return sensitivity

# 상태 초기화
if "inputs" not in st.session_state:
    st.session_state.inputs = {}

# 입력 필드
inputs = st.session_state.inputs
inputs["할인율 (%)"] = st.number_input("할인율 (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
inputs["초기 연도 매출액"] = st.number_input("초기 연도 매출액", min_value=0.0, value=1000000.0, step=1000.0)
inputs["매출 성장률 (%)"] = st.number_input("매출 성장률 (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
inputs["영업이익률 (%)"] = st.number_input("영업이익률 (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
inputs["세율 (%)"] = st.number_input("세율 (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
inputs["재투자율 (%)"] = st.number_input("재투자율 (%)", min_value=0.0, max_value=100.0, value=30.0, step=0.1)
inputs["영구 성장률 (%)"] = st.number_input("영구 성장률 (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)

# 계산 버튼
if st.button("계산"):
    if validate_inputs(inputs):
        discount_rate = float(inputs["할인율 (%)"]) / 100
        terminal_growth_rate = float(inputs["영구 성장률 (%)"]) / 100

        # DCF 계산
        enterprise_value, discounted_fcf, discounted_terminal_value = calculate_dcf(inputs, discount_rate, terminal_growth_rate)
        st.subheader("DCF 계산 결과")
        st.write(f"할인된 현금흐름 합계: {round(sum(discounted_fcf), 2):,.2f}")
        st.write(f"할인된 잔여가치: {round(discounted_terminal_value, 2):,.2f}")
        st.write(f"기업 가치(Enterprise Value): {round(enterprise_value, 2):,.2f}")

        # 민감도 분석
        sensitivity = run_sensitivity_analysis(inputs, discount_rate, terminal_growth_rate)
        st.subheader("민감도 분석 (할인율 vs 영구 성장률)")
        st.dataframe(sensitivity)
