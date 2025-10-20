# ProxyMe

> My First AI Agent. Your second self, ProxyMe.

AI Agent가 인간을 대신해서 일하는 세상이 오게 될 것이다. 나는 그걸 실현하는 사람이다. 좋다. 나부터 대신하는 Agent 만들자. 마치, 지킬박사와 하이드처럼.

I guess AI agents will end up doing people’s jobs. It’s one of my responsibilities anyway. So, here we go, let’s make an agent to stand in for me, just like Dr. Jekyll did on himself.

- [Mandatory] Web GUI
- [Mandatory] proxyme agent
- [Mandatory] todo agent
- [Mandatory] email agent
- [Optional] JIRA agent
- [Optional] Github agent

## mvp 시나리오 for v1.0.0
- (GUI) 직관적이고 간단한 UX, Web App
- (email agent) 기간별 메일 조회가 가능하며 아래 기능과 함께 제공한다
    - (email brief Agent) 종합 요약 정보 추가
    - (email priority Agent) 중요도 정보 추가 (내용 분석의 결과로 응답이 필요한지, 신처, 관계자 정보를 바탕으로)
    - (email agent) 메일 쓰레딩 기능
    - (email category agent) 스마트 분류 기능 (LLM을 통한 분류)

## 사용자 시나리오별 요구사항 정의

### 기간별 메일 조회 (email agent)
- 기간별 메일의 raw 데이터를 조회할 수 있다
- 이메일을 메일 서버로 부터 받아와서 개별 DB에 저장한다
- brief, priority, category agent를 사용해서 메타 데이터를 관리한다

### 종합 요약 정보 추가 (email brief Agent)
- 개별 메일을 요약하는데, 관련된 다른 메일 정보를 바탕으로 요약한다
- 주요 키워드를 뽑아서 제공한다

### 중요도 정보 추가 (email priority agent)
- 내용 분석의 결과로 응답이 필요한지 파악한다
- 수신처 정보를 고려해서 파악한다
- 관계자 정보를 바탕으로 파악한다

### 메일 쓰레딩 기능 (email agent)
- 유사도 분석을 통해서 묶어서 볼 수 있게 제공한다

### 스마트 분류 기능 (email category agent)
- 메일 내용 분석에 기반한 분류
