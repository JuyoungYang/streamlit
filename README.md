# 🔮 냥타로 (NyangTarot)

고양이 점술가가 타로카드를 해석해주는 귀염뽀짝 Streamlit 앱!

---

## 📦 프로젝트 소개

**냥타로**는 사용자가 질문을 입력하고 직접 타로카드를 3장 뽑으면,  
GPT가 **고양이 말투**로 정성껏 해석해주는 타로 서비스입니다.  
귀여운 SVG 카드와 고양이의 해석이 결합된 감성 타로 체험을 제공합니다.  
(본 프로젝트는 개인 포트폴리오 용도로 제작되었습니다.)

---

## 🐾 주요 기능

- 질문 입력 → 타로 카드 3장 직접 선택
- 카드별 방향(정방향/역방향)에 따라 해석 내용 자동 적용
- GPT-4o-mini 모델을 활용한 **고양이 말투 해석** 생성
- 카드마다 SVG로 그려진 시각적 구성
- 질문 중복 방지 및 상태 저장 (세션 기반)

---

## 🚀 실행 방법

### 1. 로컬에서 실행

```bash
git clone https://github.com/JuyoungYang/streamlit.git
cd streamlit

# 가상환경 생성 및 패키지 설치
pip install -r requirements.txt

# secrets 설정
mkdir .streamlit
echo '[openai]\napi_key = "YOUR_API_KEY"' > .streamlit/secrets.toml

# 실행
streamlit run streamlit_app.py
```

---

## 📁 파일 구조

```
├── streamlit_app.py          # 메인 앱
├── card_display.py           # 카드 그리드 UI
├── interpretation.py         # GPT 기반 해석 생성
├── tarot_cards.py            # 카드 데이터 및 해석 사전
├── images/
│   └── cat_tarot.jpg         # 상단 배너 이미지
└── .streamlit/
    └── secrets.toml          # API 키 설정
```

---

## 😺 예시 질문

- "내가 이번 시험에 붙을 수 있을까?"
- "그 사람과 잘 될까?"
- "새로운 도전을 해도 될까?"

---

## ⚠️ 주의 사항

- 같은 질문을 두 번 하면 고양이한테 혼난다냥.
- OpenAI API 키가 없으면 해석은 작동하지 않는다냥.

---

## 📜 라이선스

- MIT License

---

## 🙋‍♀️ 만든 사람

- 냥타로 집사: [JuyoungYang](https://github.com/JuyoungYang)
