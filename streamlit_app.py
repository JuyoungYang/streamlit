import streamlit as st
import random
from openai import OpenAI

# OpenAI API 키 설정
client = OpenAI(
    api_key = st.secrets["openai"]["api_key"]
)

CARD_BACK_SVG = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 140">
    <!-- SVG 내용 -->
    <text x="50" y="135" fill="#9d4edd" font-size="8" text-anchor="middle">카드 {}</text>
</svg>
'''

# 메이저 아르카나 카드 정의
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

# 마이너 아르카나 카드 정의
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

def get_all_cards():
    """모든 카드 목록을 반환하는 함수"""
    all_cards = []
    
    # 메이저 아르카나 카드 추가
    for card_num, card_info in major_arcana.items(): 
        all_cards.append({
            "type": "Major Arcana",
            "name": card_info["name"],  
            "forward": card_info["forward"],
            "reversed": card_info["reversed"]
        })
    
    # 마이너 아르카나 카드 추가
    for suit, cards in minor_arcana.items():
        for rank, meanings in cards.items():
            all_cards.append({
                "type": "Minor Arcana",
                "suit": suit,
                "rank": rank,
                "name": f"{rank} of {suit}",
                "forward": meanings["forward"],
                "reversed": meanings["reversed"]
            })
    
    return all_cards

def get_random_card_info(card):
    """카드에 랜덤한 방향을 추가하는 함수"""
    direction = random.choice(['forward', 'reversed'])
    card_info = card.copy()
    card_info['direction'] = direction
    card_info['interpretation'] = card_info['forward'] if direction == 'forward' else card_info['reversed']
    return card_info


def display_card_grid(available_cards, selected_cards):
    # 가능한 카드들을 랜덤하게 섞기
    shuffled_cards = available_cards.copy()
    random.shuffle(shuffled_cards)
    num_cards = len(shuffled_cards)
    
    # CSS 스타일 정의
    st.markdown("""
        <style>
        .card-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 80px;  /* 컨테이너 너비 조정 */
            margin: 0 auto;  /* 중앙 정렬 */
            gap: 5px;
        }
        .card {
            width: 80px;  /* 카드 크기 축소 */
            height: 112px;  /* 비율 유지하며 축소 (140 * 0.8) */
            margin: 0;
            padding: 0;
        }
        .selected-card {
            filter: grayscale(100%);
        }
        /* 열 간격 조정 */
        .st-emotion-cache-1r6slb0 {
            gap: 0.5rem !important;
        }
        /* 비활성화된 버튼 스타일 */
        .stButton button:disabled {
            background-color: #e0e0e0 !important;
            color: #888888 !important;
            opacity: 0.7;
            cursor: not-allowed;
            border-color: #cccccc !important;
        }
        /* 버튼 호버 효과 제거 */
        .stButton button:disabled:hover {
            background-color: #e0e0e0 !important;
            color: #888888 !important;
            border-color: #cccccc !important;
        }
        /* 버튼 크기와 위치 조정 */
        .stButton button {
            min-height: 0px !important;
            width: 40px !important;  /* 버튼 너비 축소 */
            padding: 0px 8px !important;
            margin: 2px auto !important;  /* 상하 여백 추가 */
            line-height: 1.6 !important;
            display: block !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 카드 그리드를 생성
    cols = st.columns(8)
    
    # 선택된 위치 추적
    if 'selected_positions' not in st.session_state:
        st.session_state.selected_positions = set()
    
    # 카드 배치
    for i, card in enumerate(shuffled_cards):
        col_idx = i % 8
        with cols[col_idx]:
            # 카드와 버튼을 감싸는 컨테이너
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            
            # 카드 이미지 표시
            is_selected = i in st.session_state.selected_positions
            st.markdown(f"""
                <div class="card {'selected-card' if is_selected else ''}">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 140" width="80" height="112">
                        <rect width="100" height="140" rx="10" fill="#2a0845"/>
                        <rect x="5" y="7" width="90" height="126" rx="8" fill="none" stroke="#9d4edd" stroke-width="2"/>
                        <path d="M50 45L57 65L78 65L61 78L68 98L50 85L32 98L39 78L22 65L43 65Z" 
                                fill="none" stroke="#9d4edd" stroke-width="2"/>
                        <circle cx="15" cy="15" r="5" fill="#9d4edd"/>
                        <circle cx="85" cy="15" r="5" fill="#9d4edd"/>
                        <circle cx="15" cy="125" r="5" fill="#9d4edd"/>
                        <circle cx="85" cy="125" r="5" fill="#9d4edd"/>
                        <text x="50" y="135" fill="#9d4edd" font-size="8" text-anchor="middle">카드 {i + 1}</text>
                    </svg>
                </div>
            """, unsafe_allow_html=True)
            
            # 버튼 생성
            st.button(
                "💜", 
                key=f"card_{i}", 
                disabled=is_selected
            )
            
            # 컨테이너 닫기
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 버튼이 클릭되고 활성화된 상태일 때만 처리
            if not is_selected and st.session_state.get(f"card_{i}"):
                card_info = get_random_card_info(card)
                st.session_state.selected_cards.append(card_info)
                st.session_state.selected_positions.add(i)
                st.rerun()
    
    # 빈 열 채우기
    remaining = 8 - (num_cards % 8) if num_cards % 8 != 0 else 0
    for i in range(remaining):
        with cols[-(i+1)]:
            st.write("")

def generate_ai_interpretation(question, cards):
    cards_info = "\n".join([f"- {card['name']} ({card['direction']}): {card['interpretation']}" for card in cards])

    with st.spinner("해석중이다냥😾 기다려라냥! 🐾"):
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "당신은 최고의 타로카드 해석가입니다. 사용자가 뽑은 카드와 질문을 기반으로 구체적인 해석을 제공합니다. 카드별로 새로운 문단으로 해석해줘. 모든 문장은 '~다'로 끝나며, 그 뒤에 '냥'을 붙여서 말해줘. '있어냥'과 같은 표현은 사용하지 말고, 모든 문장은 '냥'으로 끝내야 한다냥. 마지막에 해석을 요약해서 말해주고 두줄 아래 새로운 줄에 '내 해석이 어떠냥😼'으로 끝내줘. 만약 이해할 수 없는 질문이나 타로와 상관없는 질문을 하면 해석하지 말고 '나를 바보로 아냐냥!👿'만 출력해줘."},
                {"role": "user", "content": f"질문: {question}\n카드: {cards_info}\n이 카드를 기반으로 해석을 해주세요."}
            ],
            model="gpt-4o-mini",
        )
        return response.choices[0].message.content.strip()

# 1. 같은 폴더에 있는 이미지, 페이지 너비에 맞게 자동으로 조정
st.image("images/cat_tarot.jpg", use_column_width=True)

# 타이틀 표시
st.title("🔮 냥타로")

# 부제목 위 여백 추가
st.markdown("<br>", unsafe_allow_html=True)

# 부제목 표시
st.subheader("오백냥을 내면 뭐든지 알려주겠다냥!😼🐾")


# 세션 스테이트 초기화
if 'asked_questions' not in st.session_state:
    st.session_state.asked_questions = set()
if 'selected_cards' not in st.session_state:
    st.session_state.selected_cards = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
if 'selected_positions' not in st.session_state:
    st.session_state.selected_positions = set()

# 사용자의 질문 입력
question = st.text_input("묻고 싶은게 뭐냥😸", key="question_input")

if question:
    # 질문이 바뀌었을 때 카드 초기화
    if question != st.session_state.current_question:
        st.session_state.selected_cards = []
        st.session_state.selected_positions = set()  # 추가
        st.session_state.current_question = question
    
    # 질문 중복 체크
    if question in st.session_state.asked_questions:
        st.error("나를 바보로 아는거냥!😾")
    else:
        st.divider()
        
        # 카드 선택 UI
        if len(st.session_state.selected_cards) < 3:
            st.write(f"### {len(st.session_state.selected_cards) + 1}번째 카드를 선택하라냥")
            
            # 선택된 카드를 제외한 사용 가능한 카드 목록 생성
            available_cards = [
                card for card in get_all_cards()
                if not any(c['name'] == card['name'] for c in st.session_state.selected_cards)
            ]
            
            display_card_grid(available_cards, st.session_state.selected_cards)

        # 카드가 선택되었다면 결과 표시
        if st.session_state.selected_cards:
            st.header("오호라🐱")
            for idx, card in enumerate(st.session_state.selected_cards, 1):
                direction_text = "정방향" if card['direction'] == 'forward' else "역방향"
                st.write(f"**{idx}. {card['name']}** ({direction_text}): {card['interpretation']}")
            
            # 모든 카드가 선택되었을 때만 해석 표시
            if len(st.session_state.selected_cards) == 3:
                st.divider()
                st.header("의미를 알려주겠다냥!😺")
                ai_interpretation = generate_ai_interpretation(question, st.session_state.selected_cards)
                st.write(ai_interpretation)
                
                # 해석이 완료되면 질문을 기록
                st.session_state.asked_questions.add(question)
                                
                # 리셋 버튼
                st.divider()
                if st.button("츄르값 주고 물어봐라냥😼!"):
                    st.session_state.selected_cards = []
                    st.session_state.current_question = ""
                    st.session_state.question_input = ""  # 입력창 비우기
                    st.rerun()