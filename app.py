import streamlit as st


# -----------------------------
# 1. 추천 데이터
# -----------------------------
# 술, 페어링, 음악을 서로 독립된 리스트로 관리합니다.
# 초보자라면 이 부분의 문장과 항목을 먼저 수정해도 됩니다.

DRINKS = [
    {
        "name": "모엣 샹동 임페리얼 브뤼",
        "type": "샴페인",
        "price": "고가",
        "proof": "적당",
        "flavors": ["탄산감있는", "드라이한", "오렌지"],
        "mood": ["기분 좋은"],
        "occasion": ["친구들과", "연인과", "가족들과"],
        "level": "입문 추천",
        "story": "샴페인 특유의 밝은 탄산과 산뜻한 과일 향을 비교적 편하게 경험할 수 있는 대표적인 입문 선택입니다.",
        "serving": "차갑게 준비해 잔에 따르고, 처음에는 탄산감과 사과·감귤 계열의 향을 느껴보세요.",
    },
    {
        "name": "돔 페리뇽 빈티지",
        "type": "샴페인",
        "price": "프리미엄",
        "proof": "적당",
        "flavors": ["드라이한", "탄산감있는", "오크향"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["연인과", "가족들과"],
        "level": "프리미엄 경험",
        "story": "축하의 상징으로 잘 알려진 프리미엄 샴페인입니다. 섬세한 탄산과 구운 빵 같은 향을 천천히 감상하기 좋습니다.",
        "serving": "차갑게 마시되 너무 빠르게 마시지 말고, 향이 올라오는 과정을 천천히 즐겨보세요.",
    },
    {
        "name": "글렌피딕 12년",
        "type": "위스키",
        "price": "중간",
        "proof": "적당",
        "flavors": ["달달한", "오크향"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "친구들과"],
        "level": "입문 추천",
        "story": "배와 사과처럼 부드러운 과일 향이 있어 위스키를 처음 접하는 사람도 향의 차이를 느끼기 좋은 대표적인 싱글몰트입니다.",
        "serving": "처음에는 그대로 한 모금 마시고, 그다음 물을 몇 방울 넣어 향이 어떻게 달라지는지 비교해보세요.",
    },
    {
        "name": "맥캘란 12년 더블 캐스크",
        "type": "위스키",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "오크향", "꿀"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "바닐라와 꿀을 떠올리게 하는 달콤한 향, 부드러운 오크 향이 균형을 이루어 차분한 밤에 잘 어울립니다.",
        "serving": "니트 또는 큰 얼음 하나와 함께 천천히 마시며 향을 먼저 즐겨보세요.",
    },
    {
        "name": "라프로익 10년",
        "type": "위스키",
        "price": "고가",
        "proof": "높은",
        "flavors": ["훈연", "오크향", "드라이한"],
        "mood": ["차분하고 조용한"],
        "occasion": ["혼술", "친구들과"],
        "level": "개성 강한 선택",
        "story": "모닥불과 바다를 떠올리게 하는 강한 훈연 향이 특징입니다. 호불호가 있지만 위스키의 개성을 경험하고 싶을 때 좋습니다.",
        "serving": "처음이라면 물을 조금 넣어 향의 강도를 낮추고, 무리해서 한 번에 많이 마시지 마세요.",
    },
    {
        "name": "루이 자도 부르고뉴 피노 누아",
        "type": "와인",
        "price": "중간",
        "proof": "적당",
        "flavors": ["달달한", "오렌지", "드라이한"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["연인과", "가족들과", "친구들과"],
        "level": "입문 추천",
        "story": "체리와 붉은 과일을 떠올리게 하는 향과 부드러운 질감이 있어 와인의 향을 처음 알아가기 좋습니다.",
        "serving": "너무 차갑지 않게 준비하고, 잔을 살짝 흔들어 과일 향을 먼저 느껴보세요.",
    },
]


PAIRINGS = [
    {"name": "캐비어와 블리니", "price": "프리미엄", "types": ["샴페인"], "reason": "짭짤한 캐비어와 바삭한 블리니가 샴페인의 산미와 탄산감을 돋보이게 합니다."},
    {"name": "굴과 레몬", "price": "프리미엄", "types": ["샴페인"], "reason": "굴의 바다 향과 짠맛을 샴페인의 산뜻한 산미가 깔끔하게 정리합니다."},
    {"name": "푸아그라와 브리오슈", "price": "프리미엄", "types": ["위스키", "와인"], "reason": "푸아그라의 진하고 부드러운 질감이 위스키의 오크 향과 와인의 과일 향을 풍성하게 느끼게 합니다."},
    {"name": "숙성 치즈", "price": "일상 접근 가능", "types": ["위스키", "와인", "샴페인"], "reason": "치즈의 짠맛과 크리미한 질감이 술의 향을 부드럽게 연결해 줍니다."},
    {"name": "다크초콜릿", "price": "일상 접근 가능", "types": ["위스키", "와인"], "reason": "초콜릿의 쌉쌀하고 달콤한 맛이 오크 향과 바닐라 향을 자연스럽게 강조합니다."},
    {"name": "말린 무화과와 견과류", "price": "일상 접근 가능", "types": ["위스키", "와인"], "reason": "말린 과일과 견과류의 고소한 향이 위스키의 꿀·오크 향과 잘 어울립니다."},
    {"name": "훈제 연어와 크림치즈", "price": "일상 접근 가능", "types": ["샴페인", "와인"], "reason": "훈제 향과 크림치즈의 부드러움을 산뜻한 술이 균형 있게 받쳐줍니다."},
]


MUSIC = [
    {"name": "Norah Jones - Don't Know Why", "mood": ["차분하고 조용한", "위로받는"], "reason": "부드러운 보컬과 피아노가 위스키의 느린 향 감상과 잘 어울립니다."},
    {"name": "Cigarettes After Sex - Apocalypse", "mood": ["차분하고 조용한", "연인과"], "reason": "몽환적이고 느린 사운드가 샴페인이나 와인을 마시는 조용한 밤의 분위기를 만들어줍니다."},
    {"name": "Laufey - From The Start", "mood": ["기분 좋은", "연인과"], "reason": "재즈를 바탕으로 한 세련된 팝이 가벼운 샴페인과 즐거운 대화에 잘 맞습니다."},
    {"name": "HYUKOH - Comes And Goes", "mood": ["위로받는", "차분하고 조용한"], "reason": "담백하고 쓸쓸한 분위기가 하루를 정리하는 혼술 시간에 잘 어울립니다."},
    {"name": "Men I Trust - Show Me How", "mood": ["차분하고 조용한", "위로받는"], "reason": "부드러운 인디 사운드가 강한 자극 없이 술과 음식의 향에 집중하게 합니다."},
    {"name": "The Marías - No One Noticed", "mood": ["기분 좋은", "연인과"], "reason": "세련된 드림팝의 리듬이 와인이나 샴페인의 가벼운 분위기를 살려줍니다."},
]


def score_drink(drink, occasion, drink_type, mood, proof, flavors, budget):
    """사용자 답변과 술의 태그가 얼마나 맞는지 계산합니다."""
    score = 0
    score += 3 if occasion in drink["occasion"] else 0
    score += 3 if drink_type == "전체" or drink_type == drink["type"] else 0
    score += 3 if mood in drink["mood"] else 0
    score += 2 if proof == drink["proof"] else 0
    score += sum(2 for flavor in flavors if flavor in drink["flavors"])
    score += 2 if budget == drink["price"] else 0
    return score


def recommend_drinks(occasion, drink_type, mood, proof, flavors, budget, exclude_names=None):
    exclude_names = exclude_names or set()
    ranked = sorted(
        [drink for drink in DRINKS if drink["name"] not in exclude_names],
        key=lambda drink: score_drink(drink, occasion, drink_type, mood, proof, flavors, budget),
        reverse=True,
    )
    return ranked[:3]


def recommend_pairings(drink, budget):
    # 프리미엄 술에는 특별한 페어링을 우선 보여주고,
    # 그 외에는 집에서 쉽게 구할 수 있는 페어링을 우선 보여줍니다.
    if budget == "프리미엄":
        preferred = [p for p in PAIRINGS if p["price"] == "프리미엄" and drink["type"] in p["types"]]
        if preferred:
            return preferred[:2]
    accessible = [p for p in PAIRINGS if p["price"] == "일상 접근 가능" and drink["type"] in p["types"]]
    return accessible[:3]


def recommend_music(mood, occasion):
    ranked = sorted(
        MUSIC,
        key=lambda song: (2 if mood in song["mood"] else 0) + (1 if occasion in song["mood"] else 0),
        reverse=True,
    )
    return ranked[:3]


# -----------------------------
# 2. 화면
# -----------------------------

st.set_page_config(page_title="오늘의 프리미엄 주류 경험", page_icon="🥂", layout="centered")

st.title("🥂 오늘의 프리미엄 주류 경험")
st.write("술을 잘 알아야 하는 서비스가 아닙니다. 지금의 분위기와 취향에 맞춰 첫 경험을 안내해 드립니다.")

st.subheader("먼저 오늘의 취향을 알려주세요")

occasion = st.selectbox("1. 누구와 즐기나요?", ["혼술", "친구들과", "가족들과", "연인과", "기타"])
mood = st.selectbox("2. 어떤 분위기인가요?", ["차분하고 조용한", "기분 좋은", "위로받는"])
drink_type = st.selectbox("3. 어떤 주종을 경험해보고 싶나요?", ["전체", "와인", "위스키", "샴페인"])
proof = st.select_slider("4. 원하는 도수는 어느 정도인가요?", options=["낮은", "적당", "높은"], value="적당")
st.caption("낮은: 가볍게 즐기고 싶은 날 / 적당: 일반적인 주류 도수 / 높은: 향과 알코올감이 뚜렷한 술")

flavors = st.multiselect(
    "5. 좋아하는 맛과 향을 골라주세요.",
    ["달달한", "탄산감있는", "드라이한", "오크향", "오렌지", "훈연", "꿀"],
    default=["달달한"],
)
budget = st.select_slider("6. 오늘의 예산은 어느 정도인가요?", options=["저가", "중간", "고가", "프리미엄"], value="중간")

if st.button("나에게 맞는 경험 추천받기", type="primary", use_container_width=True):
    results = recommend_drinks(occasion, drink_type, mood, proof, flavors, budget)
    st.session_state["results"] = results
    st.session_state["answers"] = (occasion, drink_type, mood, proof, flavors, budget)


if "results" in st.session_state:
    occasion, drink_type, mood, proof, flavors, budget = st.session_state["answers"]
    st.divider()
    st.header("오늘의 추천")
    st.write(f"**{mood} 분위기**에 어울리고, {occasion} 즐기기에 좋은 선택을 골랐습니다.")
    if drink_type != "전체":
        st.write(f"관심 주종은 **{drink_type}**으로 반영했습니다.")

    for index, drink in enumerate(st.session_state["results"]):
        with st.container(border=True):
            st.subheader(f"{index + 1}. {drink['name']}")
            st.caption(f"{drink['type']} · {drink['price']} · {drink['proof']} 도수 · {drink['level']}")
            st.write(f"**선택한 이유**: {drink['story']}")
            st.write(f"**처음 마시는 방법**: {drink['serving']}")

            pairings = recommend_pairings(drink, budget)
            songs = recommend_music(mood, occasion)

            # 술과 페어링을 연결해 표시하는 핵심 코드입니다.
            st.markdown("**함께 먹기 좋은 페어링**")
            for pairing in pairings:
                st.write(f"- **{pairing['name']}**: {pairing['reason']}")

            st.markdown("**함께 들을 음악**")
            for song in songs:
                st.write(f"- **{song['name']}**: {song['reason']}")

    if st.button("다른 주류도 추천받기", use_container_width=True):
        current_names = {drink["name"] for drink in st.session_state["results"]}
        alternatives = recommend_drinks(
            occasion,
            drink_type,
            mood,
            proof,
            flavors,
            budget,
            exclude_names=current_names,
        )
        st.session_state["results"] = alternatives
        st.rerun()

st.divider()
st.caption("※ 추천은 취향 탐색을 위한 참고용입니다. 과음하지 말고, 음주 후 운전하지 마세요.")
