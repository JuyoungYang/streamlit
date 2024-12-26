import streamlit as st
import random
from openai import OpenAI  # OpenAI 모듈 추가
import time

# OpenAI API 키 설정
client = OpenAI(
    api_key = st.secrets["openai"]["api_key"]
)

# 타로 카드 정보 (기존 코드와 동일)
major_arcana = {
    0: {"name": "The Fool", "forward": "새로운 시작, 모험, 순수", "reversed": "어리석음, 경솔함, 위험"},
    1: {"name": "The Magician", "forward": "능력, 창의성, 의지", "reversed": "기만, 속임수, 무능력"},
    2: {"name": "The High Priestess", "forward": "직관, 지혜, 신비", "reversed": "비밀, 은둔, 불안정"},
    3: {"name": "The Empress", "forward": "풍요, 모성, 성장", "reversed": "의존, 나약함, 불안정"},
    4: {"name": "The Emperor", "forward": "권위, 통제, 안정", "reversed": "독재, 억압, 무능력"},
    5: {"name": "The Hierophant", "forward": "전통, 규율, 가르침", "reversed": "독단, 형식주의, 반항"},
    6: {"name": "The Lovers", "forward": "사랑, 조화, 선택", "reversed": "갈등, 불화, 유혹"},
    7: {"name": "The Chariot", "forward": "의지, 성공, 승리", "reversed": "좌절, 통제력 상실, 공격성"},
    8: {"name": "Strength", "forward": "힘, 용기, 인내", "reversed": "나약함, 자기 불신, 분노"},
    9: {"name": "The Hermit", "forward": "성찰, 고독, 지혜", "reversed": "고립, 외로움, 폐쇄"},
    10: {"name": "Wheel of Fortune", "forward": "변화, 운명, 행운", "reversed": "불운, 변화 저항, 통제 불가"},
    11: {"name": "Justice", "forward": "정의, 공정, 책임", "reversed": "불공정, 불균형, 무책임"},
    12: {"name": "The Hanged Man", "forward": "희생, 인내, 새로운 관점", "reversed": "이기심, 집착, 헛된 희생"},
    13: {"name": "Death", "forward": "변화, 끝, 새로운 시작", "reversed": "변화 거부, 죽음, 고통"},
    14: {"name": "Temperance", "forward": "절제, 균형, 조화", "reversed": "불균형, 과도함, 충돌"},
    15: {"name": "The Devil", "forward": "욕망, 유혹, 집착", "reversed": "해방, 저항, 자각"},
    16: {"name": "The Tower", "forward": "갑작스러운 변화, 파괴, 해방", "reversed": "파멸, 억압, 고립"},
    17: {"name": "The Star", "forward": "희망, 영감, 가능성", "reversed": "절망, 불신, 무기력"},
    18: {"name": "The Moon", "forward": "직관, 환상, 무의식", "reversed": "불안, 혼란, 거짓"},
    19: {"name": "The Sun", "forward": "성공, 행복, 활력", "reversed": "실패, 불행, 우울"},
    20: {"name": "Judgement", "forward": "심판, 부활, 각성", "reversed": "후회, 죄책감, 회피"},
    21: {"name": "The World", "forward": "완성, 성취, 통합", "reversed": "미완성, 실패, 정체"},
}

# 마이너 아르카나 카드 (슈트별로 분리, 정방향/역방향 의미 포함)
minor_arcana = {
    "Wands": {
        "Ace": {"forward": "새로운 시작, 창의력, 열정", "reversed": "미완성, 좌절, 무기력"},
        "2": {"forward": "계획, 결정, 미래", "reversed": "불안, 망설임, 두려움"},
        "3": {"forward": "확장, 성장, 진전", "reversed": "방해, 지연, 미성숙"},
        "4": {"forward": "안정, 축하, 성취", "reversed": "불안정, 갈등, 불만"},
        "5": {"forward": "경쟁, 갈등, 도전", "reversed": "회피, 화해, 협력"},
        "6": {"forward": "승리, 인정, 성공", "reversed": "실패, 좌절, 불명예"},
        "7": {"forward": "용기, 방어, 인내", "reversed": "불안, 항복, 무기력"},
        "8": {"forward": "신속, 변화, 움직임", "reversed": "지연, 혼란, 정체"},
        "9": {"forward": "회복, 저항, 경계", "reversed": "피로, 불안, 무방비"},
        "10": {"forward": "압박, 부담, 책임", "reversed": "해방, 가벼움, 휴식"},
        "Page": {"forward": "영감, 창조, 가능성", "reversed": "미숙, 어리석음, 질투"},
        "Knight": {"forward": "모험, 열정, 행동", "reversed": "충동, 공격성, 과격함"},
        "Queen": {"forward": "창의력, 리더십, 매력", "reversed": "변덕, 질투, 불안정"},
        "King": {"forward": "영감, 리더십, 권위", "reversed": "독선, 억압, 폭력"},
    },
    "Cups": {
        "Ace": {"forward": "사랑, 행복, 직관", "reversed": "결핍, 슬픔, 고립"},
        "2": {"forward": "관계, 조화, 사랑", "reversed": "불화, 갈등, 이별"},
        "3": {"forward": "축하, 우정, 기쁨", "reversed": "과도함, 방종, 불만"},
        "4": {"forward": "무관심, 권태, 실망", "reversed": "새로운 기회, 열정, 만족"},
        "5": {"forward": "상실, 슬픔, 후회", "reversed": "회복, 용서, 희망"},
        "6": {"forward": "추억, 향수, 순수", "reversed": "과거 집착, 퇴보, 불행"},
        "7": {"forward": "환상, 선택, 유혹", "reversed": "현실 직시, 실망, 거짓"},
        "8": {"forward": "포기, 변화, 떠남", "reversed": "미련, 고집, 후회"},
        "9": {"forward": "만족, 행복, 소원 성취", "reversed": "불만, 탐욕, 불안"},
        "10": {"forward": "완성, 조화, 행복", "reversed": "불화, 불만족, 이별"},
        "Page": {"forward": "감성, 사랑, 직관", "reversed": "미성숙, 변덕, 질투"},
        "Knight": {"forward": "로맨스, 매력, 낭만", "reversed": "변덕, 감정 과잉, 충동"},
        "Queen": {"forward": "직관, 공감, 감성", "reversed": "감정적 불안정, 의존, 나약함"},
        "King": {"forward": "사랑, 공감, 지혜", "reversed": "억압, 감정 결핍, 냉정"},
    },
    "Swords": {
        "Ace": {"forward": "진실, 명확함, 새로운 시작", "reversed": "혼란, 잘못된 판단, 불확실성"},
        "2": {"forward": "균형, 선택, 결정", "reversed": "갈등, 회피, 속임수"},
        "3": {"forward": "상처, 슬픔, 고통", "reversed": "회복, 용서, 치유"},
        "4": {"forward": "휴식, 회복, 평화", "reversed": "고립, 불안, 소외"},
        "5": {"forward": "패배, 갈등, 손실", "reversed": "승리, 화해, 굴복"},
        "6": {"forward": "변화, 이동, 안정", "reversed": "정체, 불안정, 두려움"},
        "7": {"forward": "속임수, 기만, 회피", "reversed": "정직, 진실, 용기"},
        "8": {"forward": "갇힘, 무력함, 제한", "reversed": "자유, 해방, 주체성"},
        "9": {"forward": "걱정, 불안, 악몽", "reversed": "희망, 진실, 평화"},
        "10": {"forward": "파멸, 고통, 끝", "reversed": "새로운 시작, 부활, 희망"},
        "Page": {"forward": "호기심, 탐구, 진실", "reversed": "충동적, 경솔함, 무지"},
        "Knight": {"forward": "용기, 행동, 진실", "reversed": "공격성, 충동, 과격함"},
        "Queen": {"forward": "지혜, 냉철함, 진실", "reversed": "냉혹함, 비판적, 고립"},
        "King": {"forward": "지식, 정의, 권위", "reversed": "독선적, 폭력적, 억압"},
    },
    "Pentacles": {
        "Ace": {"forward": "번영, 기회, 물질적 풍요", "reversed": "결핍, 불안정, 손실"},
        "2": {"forward": "균형, 조절, 유연성", "reversed": "불균형, 혼란, 불안"},
        "3": {"forward": "협력, 창의력, 실력", "reversed": "미완성, 부족함, 실패"},
        "4": {"forward": "안정, 소유, 통제", "reversed": "탐욕, 집착, 인색함"},
        "5": {"forward": "어려움, 손실, 빈곤", "reversed": "회복, 희망, 지원"},
        "6": {"forward": "관대함, 나눔, 베풂", "reversed": "탐욕, 질투, 불균형"},
        "7": {"forward": "성장, 노력, 보상", "reversed": "지연, 좌절, 불확실성"},
        "8": {"forward": "기술, 숙련, 완성", "reversed": "부족, 실수, 미숙함"},
        "9": {"forward": "풍요, 번영, 독립", "reversed": "의존, 불안, 손실"},
        "10": {"forward": "안정, 풍요, 유산", "reversed": "불안정, 손실, 가족 갈등"},
        "Page": {"forward": "학습, 성장, 새로운 기회", "reversed": "미숙함, 태만, 낭비"},
        "Knight": {"forward": "실용적, 효율, 신뢰", "reversed": "탐욕, 게으름, 의존"},
        "Queen": {"forward": "안정, 풍요, 현실", "reversed": "집착, 불안, 의존"},
        "King": {"forward": "성공, 안정, 번영", "reversed": "탐욕, 독선, 불안정"},
    },
}

# 타로카드 해석 함수
def interpret_card(card_name, direction):
    if direction == "forward":
        return card_name['forward']
    else:
        return card_name['reversed']

# 타로카드를 뽑는 로직
def draw_tarot():
    # 랜덤으로 3장 카드 뽑기
    selected_cards = random.sample(list(major_arcana.values()), 3)
    
    cards = []
    for card in selected_cards:
        # 정방향 또는 역방향 설정
        direction = random.choice(['forward', 'reversed'])
        cards.append({
            "name": card["name"],
            "direction": direction,
            "interpretation": interpret_card(card, direction)
        })
    return cards

# AI 해석 함수
def generate_ai_interpretation(question, cards):
    # 카드 정보를 문자열로 정리
    cards_info = "\n".join([f"- {card['name']} ({card['direction']}): {card['interpretation']}" for card in cards])

    # 데이터 로딩
    with st.spinner("해석중이당😾 기다려라냥! 🐾"):
        
        # OpenAI ChatCompletion 호출
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "당신은 타로카드 해석가입니다. 사용자가 뽑은 카드와 질문을 기반으로 해석을 제공합니다. 모든 문장은 ~다로 끝나고, 그 뒤에 '냥'을 붙여 말해줘. 문단 마지막에 고양이 이모지(예: 🐱, 😺, 😼, 😻)를 자연스럽게 넣어줘. 마지막에는 '내 해석이 어떠냥😼'으로 끝내줘."},
                {"role": "user", "content": f"질문: {question}\n카드: {cards_info}\n이 카드를 기반으로 해석을 해주세요."}
            ],
            model="gpt-4",
        )

        # 응답 결과 가져오기
        ai_interpretation = (response.choices[0].message.content.strip())
        return ai_interpretation

# Streamlit UI
st.title("🔮 냥타로")

# 서브헤더로 안내 문구 표시
st.subheader("오백냥을 내면 뭐든지 알려주겠당!😼🐾")

# 사용자의 질문 입력
question = st.text_input("묻고 싶은게 뭐냥😸")

if question:
    # 타로카드 뽑기
    cards = draw_tarot()
    
    st.divider()
    
    # 뽑은 카드 정보 출력
    st.header("니가 뽑은 타로카드 이렇게 세개당!😸")
    for card in cards:
        st.write(f"**{card['name']}** ({card['direction']}): {card['interpretation']}")

    st.divider()
    
    # AI 해석 결과 가져오기
    ai_interpretation = generate_ai_interpretation(question, cards)

    # 응답 결과 가져오기
    st.header("의미를 알려주겠땅!")
    st.write(ai_interpretation)