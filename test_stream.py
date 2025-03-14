import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import random
import time

# 페이지 구성 설정
st.set_page_config(
    page_title="침해사고 분석 시스템",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 설정
st.sidebar.title("침해사고 타임라인 분석 시스템")
st.sidebar.image("https://www.kisa.or.kr/images/common/logo.png", width=200)

# 메뉴 선택
menu = st.sidebar.selectbox(
    "메뉴 선택",
    ["대시보드", "타임라인 분석", "RAG 검색 시스템", "질의응답(QA)"]
)

# 테스트 데이터 생성 함수
def generate_sample_logs(num_entries=100):
    log_types = ["네트워크 로그", "시스템 로그", "애플리케이션 로그", "보안장비 로그", "방화벽 로그"]
    event_types = ["로그인 시도", "접근 거부", "파일 수정", "패킷 스캔", "계정 생성", "권한 변경", "데이터 유출 시도"]
    ip_addresses = [f"192.168.1.{i}" for i in range(1, 20)] + [f"10.0.0.{i}" for i in range(1, 20)]
    users = ["admin", "user1", "user2", "system", "root", "guest", "unknown"]
    
    start_date = datetime.datetime(2025, 4, 1, 0, 0, 0)
    
    logs = []
    for i in range(num_entries):
        timestamp = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        log_type = random.choice(log_types)
        event_type = random.choice(event_types)
        source_ip = random.choice(ip_addresses)
        destination_ip = random.choice(ip_addresses)
        while destination_ip == source_ip:
            destination_ip = random.choice(ip_addresses)
        user = random.choice(users)
        severity = random.choice(["낮음", "중간", "높음", "심각"])
        
        logs.append({
            "타임스탬프": timestamp,
            "로그유형": log_type,
            "이벤트": event_type,
            "출발지IP": source_ip,
            "목적지IP": destination_ip,
            "사용자": user,
            "심각도": severity
        })
    
    return pd.DataFrame(logs)

# 클러스터링된 타임라인 단계 샘플 생성
def generate_timeline_clusters():
    stages = [
        {"단계": "초기 접근", "시작시간": "2025-04-02 08:23:15", "종료시간": "2025-04-02 09:45:30", "설명": "공격자의 초기 시스템 접근 시도", "로그수": 28},
        {"단계": "권한 상승", "시작시간": "2025-04-02 10:12:43", "종료시간": "2025-04-02 11:30:22", "설명": "시스템 권한 획득 시도", "로그수": 45},
        {"단계": "내부 정찰", "시작시간": "2025-04-02 13:05:17", "종료시간": "2025-04-02 15:28:45", "설명": "내부 네트워크 탐색 활동", "로그수": 67},
        {"단계": "데이터 수집", "시작시간": "2025-04-03 09:14:32", "종료시간": "2025-04-03 11:45:18", "설명": "민감 정보 수집 시도", "로그수": 39},
        {"단계": "데이터 유출", "시작시간": "2025-04-03 14:20:55", "종료시간": "2025-04-03 16:10:42", "설명": "외부로 데이터 전송 시도", "로그수": 52}
    ]
    return pd.DataFrame(stages)

# RAG 검색 결과 시뮬레이션
def simulate_rag_search(query, n=5):
    search_results = [
        {"제목": "APT 공격 침해사고 분석 보고서", "관련도": 0.92, "내용": "APT 공격에서는 초기 접근 후 권한 상승 시도가 일반적으로 관찰됩니다. 공격자는 주로 피싱 이메일을 통해 초기 접근을 시도하며..."},
        {"제목": "랜섬웨어 공격 패턴 분석", "관련도": 0.87, "내용": "랜섬웨어 공격자는 시스템 접근 후 주요 데이터를 식별하고 암호화하기 위해 내부 정찰을 수행합니다..."},
        {"제목": "내부 정찰 기술 분석", "관련도": 0.85, "내용": "공격자는 일반적으로 네트워크 스캐닝 도구와 PowerShell 스크립트를 사용하여 내부 네트워크를 탐색합니다..."},
        {"제목": "권한 상승 공격 기법", "관련도": 0.81, "내용": "권한 상승을 위해 공격자는 취약한 서비스, 패치되지 않은 소프트웨어, 설정 오류 등을 이용합니다..."},
        {"제목": "데이터 유출 탐지 방법", "관련도": 0.78, "내용": "데이터 유출은 비정상적인 네트워크 트래픽 패턴, 대용량 파일 전송, 비정상적인 시간대의 활동 등을 통해 탐지할 수 있습니다..."},
        {"제목": "MITRE ATT&CK 프레임워크", "관련도": 0.75, "내용": "MITRE ATT&CK 프레임워크는 침해사고의 다양한 단계와 기법을 체계적으로 분류하여 제공합니다..."},
        {"제목": "네트워크 보안 모니터링", "관련도": 0.72, "내용": "효과적인 네트워크 보안 모니터링은 침해사고의 조기 탐지에 필수적이며, 이상 트래픽 패턴을 식별하는 데 중요합니다..."}
    ]
    
    # 쿼리에 따라 관련도 약간 조정 (시뮬레이션)
    for result in search_results:
        noise = random.uniform(-0.1, 0.1)
        result["관련도"] = min(0.99, max(0.5, result["관련도"] + noise))
    
    # 관련도 순으로 정렬
    search_results = sorted(search_results, key=lambda x: x["관련도"], reverse=True)
    
    return search_results[:n]

# LLM 분석 결과 시뮬레이션
def simulate_llm_analysis(timeline_data):
    analysis = """
    ### 침해사고 분석 요약

    분석된 로그 데이터에 따르면, 이 침해사고는 전형적인 APT(Advanced Persistent Threat) 공격 패턴을 보이고 있습니다. 공격 과정은 다음과 같이 요약할 수 있습니다:

    1. **초기 접근 (2025-04-02 08:23:15 ~ 09:45:30)**
       - 피싱 이메일을 통해 내부 시스템에 최초 접근
       - 사용자 계정 인증 정보 탈취 시도 흔적 발견

    2. **권한 상승 (2025-04-02 10:12:43 ~ 11:30:22)**
       - 취약한 서비스 이용한 권한 상승 시도
       - 관리자 권한 획득 흔적 발견

    3. **내부 정찰 (2025-04-02 13:05:17 ~ 15:28:45)**
       - 내부 네트워크 스캔 활동 다수 발견
       - 주요 서버 및 데이터베이스 위치 식별 시도

    4. **데이터 수집 (2025-04-03 09:14:32 ~ 11:45:18)**
       - 주요 데이터베이스 접근 시도
       - 대용량 데이터 쿼리 및 수집 활동

    5. **데이터 유출 (2025-04-03 14:20:55 ~ 16:10:42)**
       - 외부 C&C 서버로의 데이터 전송 시도
       - 암호화된 채널을 통한 데이터 유출 흔적

    공격 IP 주소와 악성 도메인 분석 결과, 이 공격은 알려진 위협 그룹 'APT-X'의 공격 패턴과 유사성을 보입니다. 해당 그룹은 주로 금융 및 기술 기업을 대상으로 지적 재산권 및 고객 데이터 유출을 목적으로 합니다.

    권장 대응 조치:
    - 영향 받은 시스템 격리 및 포렌식 분석
    - 관리자 계정 패스워드 전체 리셋
    - 네트워크 세그먼테이션 강화
    - 의심스러운 외부 연결 차단
    - EDR 솔루션 배포 및 모니터링 강화
    """
    return analysis

# 질의응답 시뮬레이션
def simulate_qa(question):
    qa_responses = {
        "공격의 주요 단계는 무엇인가요?": "이 침해사고의 주요 단계는 1) 초기 접근, 2) 권한 상승, 3) 내부 정찰, 4) 데이터 수집, 5) 데이터 유출의 5단계로 진행되었습니다. 이는 전형적인 APT 공격의 킬체인 패턴을 따르고 있습니다.",
        "초기 접근은 어떻게 이루어졌나요?": "로그 분석 결과, 초기 접근은 피싱 이메일을 통해 이루어진 것으로 추정됩니다. 사용자가 악성 첨부파일을 실행하면서 공격자가 시스템에 최초 접근했습니다.",
        "어떤 데이터가 유출되었나요?": "로그 분석에 따르면 주로 고객 정보 데이터베이스와 내부 기술 문서에 접근한 흔적이 발견되었습니다. 약 2GB 상당의 데이터가 외부 서버로 전송된 것으로 추정됩니다.",
        "추천하는 대응 조치는 무엇인가요?": "권장 대응 조치로는 1) 영향 받은 시스템 격리 및 포렌식 분석, 2) 관리자 계정 패스워드 전체 리셋, 3) 네트워크 세그먼테이션 강화, 4) 의심스러운 외부 연결 차단, 5) EDR 솔루션 배포 및 모니터링 강화가 있습니다.",
        "공격자는 누구인가요?": "공격 패턴과 사용된 도구, 그리고 C&C 서버 분석 결과, 이 공격은 'APT-X'라는 알려진 위협 그룹과 연관성이 높습니다. 이 그룹은 주로 금융 및 기술 기업을 대상으로 한 지적 재산권 및 고객 데이터 유출 활동을 전개해 왔습니다."
    }
    
    # 기본 응답
    default_response = "해당 질문에 대한 정확한 답변을 제공하기 위해 더 많은 분석이 필요합니다. 추가 정보가 있으시면 알려주세요."
    
    # 질문에 대한 가장 연관성 높은 응답 찾기
    best_answer = default_response
    best_score = 0
    
    for key_q, answer in qa_responses.items():
        # 간단한 키워드 매칭 (실제로는 더 복잡한 유사도 측정 필요)
        score = sum(word in question.lower() for word in key_q.lower().split())
        if score > best_score:
            best_score = score
            best_answer = answer
    
    # 비슷한 질문이 없으면 일부 키워드에 기반하여 추측
    if best_score == 0:
        if "단계" in question.lower() or "과정" in question.lower():
            best_answer = qa_responses["공격의 주요 단계는 무엇인가요?"]
        elif "접근" in question.lower() or "시작" in question.lower():
            best_answer = qa_responses["초기 접근은 어떻게 이루어졌나요?"]
        elif "데이터" in question.lower() or "유출" in question.lower():
            best_answer = qa_responses["어떤 데이터가 유출되었나요?"]
        elif "대응" in question.lower() or "조치" in question.lower() or "방어" in question.lower():
            best_answer = qa_responses["추천하는 대응 조치는 무엇인가요?"]
        elif "공격자" in question.lower() or "누구" in question.lower() or "그룹" in question.lower():
            best_answer = qa_responses["공격자는 누구인가요?"]
    
    return best_answer

# 샘플 데이터 생성
logs_df = generate_sample_logs(150)
timeline_df = generate_timeline_clusters()

# 1. 대시보드
if menu == "대시보드":
    st.title("침해사고 분석 대시보드")
    
    # 주요 지표 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="탐지된 로그 수", value=f"{len(logs_df):,}")
    with col2:
        st.metric(label="탐지된 타임라인 단계", value=len(timeline_df))
    with col3:
        st.metric(label="영향 받은 시스템", value="12")
    with col4:
        st.metric(label="심각도", value="높음", delta="증가")
    
    # 타임라인 요약 표
    st.subheader("침해사고 타임라인 요약")
    
    # 타임라인 데이터 표시
    st.dataframe(timeline_df)
    
    # 로그 유형 및 심각도 분포
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("로그 유형 분포")
        log_type_counts = logs_df["로그유형"].value_counts()
        st.bar_chart(log_type_counts)
        
    with col2:
        st.subheader("심각도 분포")
        severity_counts = logs_df["심각도"].value_counts()
        st.bar_chart(severity_counts)
    
    # 최근 로그 표시
    st.subheader("최근 로그")
    st.dataframe(logs_df.sort_values("타임스탬프", ascending=False).head(10))
    
    # LLM 분석 결과 표시
    st.subheader("침해사고 분석 요약")
    st.markdown(simulate_llm_analysis(timeline_df))

# 2. 타임라인 분석
elif menu == "타임라인 분석":
    st.title("침해사고 타임라인 분석")
    
    st.markdown("""
    타임라인 분석에서는 로그 클러스터링을 통해 자동으로 생성된 침해사고 타임라인을 상세히 살펴볼 수 있습니다.
    각 단계에서 어떤 활동이 발생했는지, 그리고 단계 간의 관계를 분석하여 공격의 진행 과정을 이해할 수 있습니다.
    """)
    
    # 단계별 상세 정보 표시
    for i, row in timeline_df.iterrows():
        with st.expander(f"{row['단계']} ({row['시작시간']} ~ {row['종료시간']})"):
            st.markdown(f"**설명**: {row['설명']}")
            st.markdown(f"**로그 수**: {row['로그수']}")
            
            # 해당 단계의 로그 표시 (시뮬레이션)
            stage_start = datetime.datetime.strptime(row['시작시간'], "%Y-%m-%d %H:%M:%S")
            stage_end = datetime.datetime.strptime(row['종료시간'], "%Y-%m-%d %H:%M:%S")
            
            # 해당 시간대의 로그 필터링
            stage_logs = logs_df[(logs_df["타임스탬프"] >= stage_start) & (logs_df["타임스탬프"] <= stage_end)]
            
            if not stage_logs.empty:
                st.markdown("#### 주요 로그")
                st.dataframe(stage_logs.head(5))
                
                # 로그 유형 분포
                log_types = stage_logs["로그유형"].value_counts()
                st.bar_chart(log_types)
                
                # 단계별 분석 결과 (시뮬레이션)
                st.markdown("#### 분석 결과")
                
                if row['단계'] == "초기 접근":
                    st.markdown("""
                    이 단계에서는 공격자가 피싱 이메일을 통해 내부 시스템에 접근한 것으로 분석됩니다.
                    사용자 계정 인증 시도가 비정상적인 시간대에 다수 발생했으며, 의심스러운 IP 주소로부터의 접근이 확인되었습니다.
                    """)
                elif row['단계'] == "권한 상승":
                    st.markdown("""
                    이 단계에서는 공격자가 취약한 서비스를 이용하여 일반 사용자 권한에서 관리자 권한으로 상승을 시도했습니다.
                    로그 분석 결과, 여러 번의 권한 상승 시도가 확인되었으며, 결국 성공한 것으로 보입니다.
                    """)
                elif row['단계'] == "내부 정찰":
                    st.markdown("""
                    이 단계에서는 공격자가 내부 네트워크를 탐색하며 주요 서버와 데이터베이스의 위치를 파악했습니다.
                    네트워크 스캔 도구와 PowerShell 스크립트를 사용한 흔적이 발견되었습니다.
                    """)
                elif row['단계'] == "데이터 수집":
                    st.markdown("""
                    이 단계에서는 공격자가 주요 데이터베이스에 접근하여 대용량 데이터를 수집한 것으로 보입니다.
                    특히 고객 정보와 내부 기술 문서에 접근한 흔적이 확인되었습니다.
                    """)
                elif row['단계'] == "데이터 유출":
                    st.markdown("""
                    이 단계에서는 수집된 데이터가 외부 C&C 서버로 전송된 것으로 분석됩니다.
                    암호화된 채널을 통해 약 2GB 상당의 데이터가 유출된 것으로 추정됩니다.
                    """)
    
    # MITRE ATT&CK 매핑
    st.subheader("MITRE ATT&CK 매핑")
    st.markdown("""
    탐지된 타임라인 단계는 MITRE ATT&CK 프레임워크의 다음 전술에 매핑됩니다:
    - **초기 접근**: Initial Access (TA0001)
    - **권한 상승**: Privilege Escalation (TA0004)
    - **내부 정찰**: Discovery (TA0007)
    - **데이터 수집**: Collection (TA0009)
    - **데이터 유출**: Exfiltration (TA0010)
    """)
    
    # 간소화된 타임라인 시각화
    st.subheader("타임라인 시각화")
    
    # 타임라인 데이터를 표 형식으로 표시
    st.table(timeline_df[['단계', '시작시간', '종료시간', '로그수']])
    
    # 단계별 로그수를 바 차트로 표시
    st.bar_chart(timeline_df.set_index('단계')['로그수'])

# 3. RAG 검색 시스템
elif menu == "RAG 검색 시스템":
    st.title("RAG 기반 침해사고 분석 검색 시스템")
    
    st.markdown("""
    RAG(Retrieval-Augmented Generation) 시스템을 사용하여 과거 침해사고 분석 자료, 위협 인텔리전스, 보안 모범 사례 등에서
    관련 정보를 검색하고 현재 분석 중인 사례에 적용할 수 있습니다.
    """)
    
    # 검색창
    query = st.text_input("검색어를 입력하세요:", "APT 공격 패턴")
    
    if query:
        with st.spinner("관련 정보를 검색 중입니다..."):
            # 실제로는 여기서 임베딩 및 벡터 검색을 수행
            time.sleep(1)  # 검색 시간 시뮬레이션
            search_results = simulate_rag_search(query)
        
        # 검색 결과 표시
        st.subheader("검색 결과")
        
        for i, result in enumerate(search_results):
            with st.expander(f"{result['제목']} (관련도: {result['관련도']:.2f})"):
                st.markdown(result['내용'])
                st.progress(result['관련도'])
        
        # 통합 분석 결과
        st.subheader("통합 분석")
        
        # 검색어에 따라 다른 분석 결과 표시 (시뮬레이션)
        if "APT" in query:
            st.markdown("""
            ### APT 공격 분석

            검색 결과를 바탕으로, 현재 분석 중인 침해사고는 APT 공격의 특성을 보이고 있습니다:

            1. **지속성**: 장기간에 걸친 공격 패턴
            2. **표적성**: 특정 데이터나 시스템을 목표로 한 공격
            3. **은밀성**: 탐지를 회피하기 위한 다양한 기법 사용
            4. **고도화**: 복잡한 공격 기법과 도구 활용

            이런 특성을 고려할 때, 추가적인 조사가 필요한 영역:
            - 침해 시스템 외 다른 시스템으로의 측면 이동 흔적
            - 지속성 확보를 위한 백도어 설치 여부
            - 주요 인증 시스템에 대한 손상 여부
            """)
        elif "랜섬웨어" in query:
            st.markdown("""
            ### 랜섬웨어 공격 분석

            검색 결과를 바탕으로, 현재 분석 중인 침해사고에서는 랜섬웨어 공격의 특징이 발견되지 않았습니다. 일반적인 랜섬웨어 공격 패턴과는 다음과 같은 차이점이 있습니다:

            1. **암호화 시도 없음**: 파일 암호화 시도 흔적이 발견되지 않음
            2. **몸값 요구 없음**: 공격자의 몸값 요구 메시지가 없음
            3. **데이터 유출 중심**: 암호화보다 데이터 유출에 중점을 둔 공격 패턴

            이는 랜섬웨어보다는 데이터 유출을 목적으로 하는 스파이웨어 또는 APT 공격에 가까운 특성을 보입니다.
            """)
        else:
            st.markdown("""
            ### 침해사고 분석

            검색 결과를 바탕으로, 현재 침해사고의 특성을 분석한 결과는 다음과 같습니다:

            1. **공격 유형**: 지능형 표적 공격(APT) 특성을 보임
            2. **주요 목적**: 민감한 데이터 유출로 추정
            3. **공격 단계**: 전형적인 사이버 킬체인 패턴을 따름
            4. **위협 수준**: 높음 (표적화된 공격으로 판단)

            현재 침해사고에 대응하기 위해서는 단계별 특성을 고려한 맞춤형 대응이 필요합니다.
            """)
        
        # 유사 침해사고 사례
        st.subheader("유사 침해사고 사례")
        
        similar_cases = [
            {"제목": "2024년 금융권 APT 공격 사례", "유사도": 0.89, "설명": "국내 주요 금융사를 대상으로 한 APT 공격 사례로, 유사한 타임라인과 공격 패턴을 보임"},
            {"제목": "2023년 제조업 표적 데이터 유출 사례", "유사도": 0.75, "설명": "자동차 부품 제조사를 대상으로 한 지적재산 유출 공격 사례"}
        ]
        
        for case in similar_cases:
            st.markdown(f"**{case['제목']}** (유사도: {case['유사도']:.2f})")
            st.markdown(case['설명'])
            st.progress(case['유사도'])
        
        # 대응 권장사항
        st.subheader("대응 권장사항")
        
        st.markdown("""
        현재 침해사고에 대한 검색 결과 분석을 바탕으로 다음과 같은 대응 조치를 권장합니다:
        
        1. **즉시 조치사항**:
           - 영향 받은 시스템 네트워크 격리
           - 관리자 계정 패스워드 전체 리셋
           - 의심스러운 외부 연결 차단
        
        2. **조사 확대**:
           - 내부 네트워크 전체에 대한 IOC 검색
           - 유사한 침해 징후 모니터링
           - 백도어 및 지속성 확보 수단 검색
        
        3. **장기 대응**:
           - 네트워크 세그먼테이션 강화
           - EDR 솔루션 도입 또는 강화
           - 계정 접근 통제 및 모니터링 강화
        """)

# 4. 질의응답(QA)
elif menu == "질의응답(QA)":
    st.title("침해사고 분석 질의응답 시스템")
    
    st.markdown("""
    침해사고 분석 결과를 바탕으로 질문을 입력하면, AI가 관련 정보를 검색하고 답변을 제공합니다.
    구체적인 질문을 통해 침해사고의 다양한 측면에 대한 정보를 얻을 수 있습니다.
    """)
    
    # 사전 정의된 질문 예시
    example_questions = [
        "공격의 주요 단계는 무엇인가요?",
        "초기 접근은 어떻게 이루어졌나요?",
        "어떤 데이터가 유출되었나요?",
        "추천하는 대응 조치는 무엇인가요?",
        "공격자는 누구인가요?"
    ]
    
    # 예시 질문 표시
    st.subheader("질문 예시")
    example_q = st.selectbox("예시 질문을 선택하거나 직접 질문을 입력하세요:", [""] + example_questions)
    
    # 질문 입력
    question = st.text_input("질문:", example_q)
    
    if question:
        with st.spinner("답변을 생성 중입니다..."):
            # 실제로는 여기서 RAG + LLM 기반 질의응답 수행
            time.sleep(1)  # 응답 시간 시뮬레이션
            answer = simulate_qa(question)
        
        # 답변 표시
        st.subheader("답변")
        st.markdown(f"**Q: {question}**")
        st.markdown(f"**A:** {answer}")
        
        # 관련 증거 표시
        st.subheader("관련 증거")
        
        # 증거 탭(로그, 타임라인, 참고자료)
        tab1, tab2, tab3 = st.tabs(["관련 로그", "타임라인 상관관계", "참고 문서"])
        
        with tab1:
            # 질문과 관련된 로그 표시 (시뮬레이션)
            if "초기 접근" in question:
                filtered_logs = logs_df[logs_df["이벤트"].isin(["로그인 시도", "접근 거부"])]
            elif "권한" in question:
                filtered_logs = logs_df[logs_df["이벤트"].isin(["권한 변경", "계정 생성"])]
            elif "데이터" in question or "유출" in question:
                filtered_logs = logs_df[logs_df["이벤트"].isin(["데이터 유출 시도", "파일 수정"])]
            else:
                filtered_logs = logs_df.sample(5)  # 무작위 샘플
            
            st.dataframe(filtered_logs)
        
        with tab2:
            # 질문과 관련된 타임라인 단계 강조
            highlight_stages = []
            
            if "초기 접근" in question:
                highlight_stages = ["초기 접근"]
            elif "권한" in question:
                highlight_stages = ["권한 상승"]
            elif "정찰" in question:
                highlight_stages = ["내부 정찰"]
            elif "수집" in question:
                highlight_stages = ["데이터 수집"]
            elif "유출" in question:
                highlight_stages = ["데이터 유출"]
            elif "단계" in question or "과정" in question:
                highlight_stages = timeline_df["단계"].tolist()
            
            # 간소화된 타임라인 표시
            highlighted_timeline = timeline_df.copy()
            highlighted_timeline["강조"] = highlighted_timeline["단계"].apply(lambda x: "✓" if x in highlight_stages else "")
            
            st.dataframe(highlighted_timeline[["단계", "시작시간", "종료시간", "강조", "로그수"]])
        
        with tab3:
            # 질문과 관련된 참고 문서 (시뮬레이션)
            st.markdown("#### 관련 참고 문서")
            
            if "초기 접근" in question:
                st.markdown("""
                - **[MITRE ATT&CK] Initial Access**: 피싱, 드라이브 바이 다운로드 등 다양한 초기 접근 기법에 대한 설명
                - **[침해사고 대응 가이드] 초기 침해 탐지 방법**: 초기 접근 단계에서의 침해 탐지 기법
                - **[보안 보고서] 피싱 공격을 통한 APT 침해사례 분석**: 유사 사례 분석 보고서
                """)
            elif "권한 상승" in question:
                st.markdown("""
                - **[MITRE ATT&CK] Privilege Escalation**: 권한 상승을 위한 다양한 기법
                - **[취약점 보고서] CVE-2023-XXXX**: 이번 공격에 사용된 것으로 추정되는 취약점 상세
                - **[보안 가이드] 권한 상승 공격 방어 기법**: 권한 상승 공격 방어를 위한 권장 조치
                """)
            elif "데이터 유출" in question:
                st.markdown("""
                - **[MITRE ATT&CK] Exfiltration**: 데이터 유출 기법 및 탐지 방법
                - **[데이터 보호 가이드] 데이터 유출 탐지 및 방지**: 데이터 유출 방지를 위한 기술적 조치
                - **[위협 인텔리전스] APT-X 그룹의 데이터 유출 전술**: 유사 공격 그룹의 데이터 유출 패턴
                """)
            else:
                st.markdown("""
                - **[MITRE ATT&CK 프레임워크]**: 사이버 공격 전술 및 기법 분류
                - **[침해사고 대응 가이드]**: 침해사고 대응을 위한 단계별 가이드
                - **[사이버 위협 인텔리전스 보고서]**: 최신 사이버 위협 동향 및 공격 그룹 정보
                """)
        
        # 추가 질문 제안
        st.subheader("추가 질문 제안")
        suggested_questions = []
        
        if "초기 접근" in question:
            suggested_questions = ["이 공격에 사용된 피싱 이메일의 특징은 무엇인가요?", "초기 접근을 탐지하기 위한 방법은 무엇인가요?"]
        elif "권한 상승" in question:
            suggested_questions = ["권한 상승에 사용된 취약점은 무엇인가요?", "권한 상승을 방지하기 위한 조치는 무엇인가요?"]
        elif "데이터 유출" in question:
            suggested_questions = ["데이터 유출을 탐지하는 방법은 무엇인가요?", "유출된 데이터의 복구 가능성은 어떤가요?"]
        elif "공격자" in question:
            suggested_questions = ["이 공격 그룹의 다른 공격 사례는 어떤 것이 있나요?", "이 공격 그룹의 일반적인 목표는 무엇인가요?"]
        else:
            suggested_questions = ["이 침해사고의 전체 타임라인은 어떻게 되나요?", "이 침해사고와 유사한 과거 사례가 있나요?"]
        
        for sq in suggested_questions:
            if st.button(f"🔍 {sq}"):
                # 버튼 클릭 시 해당 질문으로 텍스트 입력 필드를 업데이트하는 로직이 필요하나,
                # Streamlit의 한계로 페이지 새로고침 발생. 실제 구현에서는 세션 상태 활용 필요
                st.session_state.question = sq
                st.experimental_rerun()
