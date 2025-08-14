import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="RCM 데이터 분석 도구",
    page_icon="📊",
    layout="wide"
)

# 메인 타이틀
st.title("📊 RCM (Revenue Cycle Management) 데이터 분석 도구")

# 사이드바에서 파일 업로드
st.sidebar.header("📁 파일 업로드")
uploaded_file = st.sidebar.file_uploader(
    "Excel 파일을 업로드하세요",
    type=['xlsx', 'xls'],
    help="RCM 데이터가 포함된 Excel 파일을 업로드하세요"
)

# 샘플 데이터 생성 함수
def create_sample_data():
    """샘플 RCM 데이터 생성"""
    np.random.seed(42)
    
    # 샘플 환자 데이터
    patients = [f"P{str(i).zfill(4)}" for i in range(1, 101)]
    departments = ['내과', '외과', '소아과', '산부인과', '정형외과', '신경과']
    insurance_types = ['건강보험', '의료급여', '자동차보험', '산재보험']
    
    data = []
    for patient in patients:
        dept = np.random.choice(departments)
        insurance = np.random.choice(insurance_types)
        
        # 수익 사이클 데이터 (단계별)
        admission_charge = np.random.randint(100000, 2000000)  # 입원료
        treatment_charge = np.random.randint(50000, 1500000)   # 치료비
        medication_charge = np.random.randint(10000, 500000)   # 약제비
        examination_charge = np.random.randint(20000, 300000)  # 검사비
        
        total_charge = admission_charge + treatment_charge + medication_charge + examination_charge
        insurance_coverage = total_charge * np.random.uniform(0.7, 0.9)
        patient_payment = total_charge - insurance_coverage
        
        collection_rate = np.random.uniform(0.85, 0.98)
        actual_collection = patient_payment * collection_rate
        
        data.append({
            '환자ID': patient,
            '진료과': dept,
            '보험유형': insurance,
            '입원료': admission_charge,
            '치료비': treatment_charge,
            '약제비': medication_charge,
            '검사비': examination_charge,
            '총진료비': total_charge,
            '보험급여': insurance_coverage,
            '환자부담금': patient_payment,
            '수납율': collection_rate,
            '실제수납액': actual_collection,
            '미수금': patient_payment - actual_collection,
            '진료일': pd.date_range('2024-01-01', '2024-12-31', periods=100)[np.random.randint(0, 100)]
        })
    
    return pd.DataFrame(data)

# 행 상세 정보 표시 함수
def display_row_details(row_data):
    """선택된 행의 상세 정보를 보기 좋게 표시"""
    st.subheader(f"🏥 환자 정보: {row_data['환자ID']}")
    
    # 기본 정보 컬럼
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("진료과", row_data['진료과'])
        st.metric("보험유형", row_data['보험유형'])
    
    with col2:
        st.metric("진료일", str(row_data['진료일']).split()[0])
        st.metric("수납율", f"{row_data['수납율']:.1%}")
    
    with col3:
        st.metric("총진료비", f"₩{row_data['총진료비']:,.0f}")
        st.metric("미수금", f"₩{row_data['미수금']:,.0f}")
    
    # 상세 금액 정보
    st.subheader("💰 상세 금액 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 진료비 세부내역**")
        detail_data = {
            '항목': ['입원료', '치료비', '약제비', '검사비'],
            '금액': [
                f"₩{row_data['입원료']:,.0f}",
                f"₩{row_data['치료비']:,.0f}",
                f"₩{row_data['약제비']:,.0f}",
                f"₩{row_data['검사비']:,.0f}"
            ]
        }
        st.dataframe(pd.DataFrame(detail_data), hide_index=True, use_container_width=True)
    
    with col2:
        st.write("**💳 결제 정보**")
        payment_data = {
            '구분': ['보험급여', '환자부담금', '실제수납액', '미수금'],
            '금액': [
                f"₩{row_data['보험급여']:,.0f}",
                f"₩{row_data['환자부담금']:,.0f}",
                f"₩{row_data['실제수납액']:,.0f}",
                f"₩{row_data['미수금']:,.0f}"
            ]
        }
        st.dataframe(pd.DataFrame(payment_data), hide_index=True, use_container_width=True)

# 데이터 로드
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.sidebar.success("✅ 파일이 성공적으로 업로드되었습니다!")
    except Exception as e:
        st.sidebar.error(f"❌ 파일 읽기 오류: {str(e)}")
        df = None
else:
    # 샘플 데이터 사용
    st.info("📝 샘플 데이터를 사용하고 있습니다. 왼쪽에서 Excel 파일을 업로드하세요.")
    df = create_sample_data()

if df is not None:
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🔍 데이터 필터링 & 상세보기", "📊 전체 데이터 테이블", "📈 대시보드"])
    
    with tab1:
        st.header("🔍 데이터 필터링 & 상세보기")
        
        # 필터링 옵션
        col1, col2, col3 = st.columns(3)
        
        # 가능한 컬럼들 체크
        available_columns = df.columns.tolist()
        
        with col1:
            if '진료과' in available_columns:
                departments = st.multiselect(
                    "진료과 선택",
                    options=df['진료과'].unique(),
                    default=df['진료과'].unique(),
                    key="dept_filter"
                )
            else:
                departments = None
        
        with col2:
            if '보험유형' in available_columns:
                insurance_types = st.multiselect(
                    "보험유형 선택",
                    options=df['보험유형'].unique(),
                    default=df['보험유형'].unique(),
                    key="insurance_filter"
                )
            else:
                insurance_types = None
        
        with col3:
            if '총진료비' in available_columns:
                min_charge, max_charge = st.slider(
                    "총진료비 범위",
                    min_value=int(df['총진료비'].min()),
                    max_value=int(df['총진료비'].max()),
                    value=(int(df['총진료비'].min()), int(df['총진료비'].max())),
                    key="charge_filter"
                )
            else:
                min_charge, max_charge = None, None
        
        # 필터 적용
        filtered_df = df.copy()
        
        if departments:
            filtered_df = filtered_df[filtered_df['진료과'].isin(departments)]
        if insurance_types:
            filtered_df = filtered_df[filtered_df['보험유형'].isin(insurance_types)]
        if min_charge is not None and max_charge is not None:
            filtered_df = filtered_df[
                (filtered_df['총진료비'] >= min_charge) & 
                (filtered_df['총진료비'] <= max_charge)
            ]
        
        st.write(f"📊 필터링된 데이터: {len(filtered_df)}개 행")
        
        # 행 선택을 위한 selectbox
        if not filtered_df.empty:
            # 표시용 라벨 생성
            display_labels = []
            for idx, row in filtered_df.iterrows():
                label = f"{row['환자ID']} - {row['진료과']} - ₩{row['총진료비']:,.0f}"
                display_labels.append(label)
            
            selected_label = st.selectbox(
                "상세보기할 환자를 선택하세요:",
                options=display_labels,
                key="patient_select"
            )
            
            if selected_label:
                # 선택된 인덱스 찾기
                selected_idx = display_labels.index(selected_label)
                selected_row = filtered_df.iloc[selected_idx]
                
                # 상세 정보 표시
                display_row_details(selected_row)
        else:
            st.warning("⚠️ 필터 조건에 맞는 데이터가 없습니다.")
    
    with tab2:
        st.header("📊 전체 데이터 테이블")
        
        # 데이터 요약 정보
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 환자 수", len(df))
        
        with col2:
            if '총진료비' in df.columns:
                st.metric("평균 진료비", f"₩{df['총진료비'].mean():,.0f}")
        
        with col3:
            if '미수금' in df.columns:
                st.metric("총 미수금", f"₩{df['미수금'].sum():,.0f}")
        
        with col4:
            if '수납율' in df.columns:
                st.metric("평균 수납율", f"{df['수납율'].mean():.1%}")
        
        # 전체 테이블 표시
        st.subheader("📋 전체 데이터")
        
        # 테이블 표시 옵션
        show_all = st.checkbox("모든 데이터 표시", value=False)
        
        if show_all:
            st.dataframe(df, use_container_width=True, height=600)
        else:
            st.dataframe(df.head(100), use_container_width=True, height=600)
            if len(df) > 100:
                st.info(f"처음 100개 행만 표시됩니다. 전체 {len(df)}개 행을 보려면 '모든 데이터 표시'를 체크하세요.")
    
    with tab3:
        st.header("📈 대시보드")
        
        # 기본 통계 차트들
        if all(col in df.columns for col in ['진료과', '총진료비', '수납율', '미수금']):
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 진료과별 평균 진료비
                dept_avg = df.groupby('진료과')['총진료비'].mean().sort_values(ascending=True)
                st.subheader("진료과별 평균 진료비")
                st.bar_chart(dept_avg)
            
            with col2:
                # 보험유형별 수납율
                if '보험유형' in df.columns:
                    insurance_collection = df.groupby('보험유형')['수납율'].mean().sort_values(ascending=True)
                    st.subheader("보험유형별 평균 수납율")
                    st.bar_chart(insurance_collection)
            
            # 월별 트렌드 (진료일이 있는 경우)
            if '진료일' in df.columns:
                st.subheader("월별 진료비 트렌드")
                df['월'] = pd.to_datetime(df['진료일']).dt.to_period('M')
                monthly_trend = df.groupby('월')['총진료비'].sum()
                st.line_chart(monthly_trend)
        
        else:
            st.info("대시보드를 표시하기 위해서는 특정 컬럼들이 필요합니다.")

# 하단 정보
st.markdown("---")
st.markdown("""
### 사용법
1. **파일 업로드**: 왼쪽 사이드바에서 RCM 데이터가 포함된 Excel 파일을 업로드하세요
2. **데이터 필터링**: 첫 번째 탭에서 조건을 설정하여 데이터를 필터링하고 개별 환자 정보를 상세하게 확인하세요
3. **전체 테이블**: 두 번째 탭에서 전체 데이터를 테이블 형태로 확인하세요
4. **대시보드**: 세 번째 탭에서 데이터 시각화와 통계를 확인하세요

### 지원되는 Excel 컬럼 예시
- 환자ID, 진료과, 보험유형, 진료일
- 입원료, 치료비, 약제비, 검사비, 총진료비
- 보험급여, 환자부담금, 실제수납액, 미수금, 수납율
""")
