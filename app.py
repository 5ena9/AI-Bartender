import random
from urllib.parse import quote_plus

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
    {
        "name": "뵈브 클리코 옐로 레이블",
        "type": "샴페인",
        "price": "고가",
        "proof": "적당",
        "flavors": ["탄산감있는", "드라이한", "오렌지"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["친구들과", "연인과", "가족들과"],
        "level": "입문 추천",
        "story": "상쾌한 탄산과 사과·감귤 계열의 향이 또렷해 샴페인의 기본적인 매력을 알아가기 좋습니다.",
        "serving": "충분히 차갑게 준비하고, 작은 모금으로 탄산과 산미의 균형을 느껴보세요.",
    },
    {
        "name": "볼랭저 스페셜 쿠베",
        "type": "샴페인",
        "price": "프리미엄",
        "proof": "적당",
        "flavors": ["드라이한", "탄산감있는", "오크향"],
        "mood": ["차분하고 조용한", "기분 좋은"],
        "occasion": ["연인과", "친구들과"],
        "level": "프리미엄 경험",
        "story": "잘 익은 과일과 구운 빵을 떠올리게 하는 향이 있어 축하하는 날의 샴페인을 한 단계 깊게 경험하기 좋습니다.",
        "serving": "차갑게 마시되 잔을 비우기 전에 향이 어떻게 변하는지 천천히 비교해보세요.",
    },
    {
        "name": "발베니 12년 더블우드",
        "type": "위스키",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "오크향", "꿀"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "꿀과 바닐라처럼 부드러운 향이 있어 위스키의 오크 향을 부담 없이 처음 경험하기 좋습니다.",
        "serving": "처음에는 그대로 향을 맡고, 이후 물을 몇 방울 넣어 달콤한 향의 변화를 느껴보세요.",
    },
    {
        "name": "조니워커 블랙 라벨",
        "type": "위스키",
        "price": "중간",
        "proof": "높은",
        "flavors": ["훈연", "오크향", "드라이한"],
        "mood": ["차분하고 조용한", "기분 좋은"],
        "occasion": ["혼술", "친구들과"],
        "level": "입문 추천",
        "story": "과일의 달콤함과 은은한 훈연 향이 함께 있어 여러 위스키 원액이 만드는 균형을 알아가기 좋습니다.",
        "serving": "얼음 하나 또는 물을 조금 넣어 향의 강도를 조절하며 천천히 마셔보세요.",
    },
    {
        "name": "클라우디 베이 소비뇽 블랑",
        "type": "와인",
        "price": "고가",
        "proof": "적당",
        "flavors": ["드라이한", "오렌지"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["연인과", "가족들과", "친구들과"],
        "level": "입문 추천",
        "story": "상큼한 감귤과 허브를 떠올리게 하는 향이 분명해 화이트와인의 산뜻한 매력을 배우기 좋습니다.",
        "serving": "차갑게 준비하고, 잔을 가볍게 흔든 뒤 감귤과 허브 향을 먼저 느껴보세요.",
    },
    {
        "name": "카시예로 델 디아블로 카베르네 소비뇽",
        "type": "와인",
        "price": "중간",
        "proof": "적당",
        "flavors": ["드라이한", "오크향", "달달한"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "가족들과", "친구들과"],
        "level": "입문 추천",
        "story": "검은 과일과 은은한 오크 향이 느껴지는 대중적인 레드와인으로, 드라이한 와인을 처음 경험하기 좋습니다.",
        "serving": "마시기 전 잔에 잠시 따라 두고, 과일 향과 살짝 떫은 느낌을 천천히 비교해보세요.",
    },
    {
        "name": "닥터 루젠 블루 슬레이트 리슬링",
        "type": "와인",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["달달한", "오렌지"],
        "mood": ["기분 좋은", "위로받는"],
        "occasion": ["혼술", "연인과", "친구들과"],
        "level": "입문 추천",
        "story": "사과와 감귤 같은 산뜻한 향에 은은한 단맛이 있어 화이트와인 입문자가 부담 없이 시작하기 좋습니다.",
        "serving": "차갑게 준비해 작은 모금으로 단맛과 산미의 균형을 느껴보세요.",
    },
    {
        "name": "오이스터 베이 소비뇽 블랑",
        "type": "와인",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["드라이한", "오렌지"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["연인과", "친구들과", "가족들과"],
        "level": "입문 추천",
        "story": "감귤과 허브를 떠올리게 하는 선명한 향이 있어 드라이한 화이트와인의 특징을 배우기 좋습니다.",
        "serving": "차갑게 마시고 잔을 가볍게 흔들어 감귤과 허브 향을 먼저 느껴보세요.",
    },
    {
        "name": "모스카토 다스티",
        "type": "와인",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["달달한", "탄산감있는", "오렌지"],
        "mood": ["기분 좋은", "위로받는"],
        "occasion": ["연인과", "친구들과", "가족들과"],
        "level": "입문 추천",
        "story": "복숭아와 꽃 향, 가벼운 탄산과 낮은 도수로 고급 와인을 처음 경험하는 사람에게 편안한 선택입니다.",
        "serving": "충분히 차갑게 준비해 디저트와 함께 가볍게 즐겨보세요.",
    },
    {
        "name": "킴 크로포드 소비뇽 블랑",
        "type": "와인",
        "price": "고가",
        "proof": "낮은",
        "flavors": ["드라이한", "오렌지"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["연인과", "친구들과"],
        "level": "입문 추천",
        "story": "상큼한 감귤과 허브 향이 분명해 화이트와인의 향을 비교하며 즐기기 좋은 인지도 높은 선택입니다.",
        "serving": "차갑게 마시고 한 모금 뒤 물을 마셔 산미가 어떻게 느껴지는지 비교해보세요.",
    },
    {
        "name": "떼땅져 브뤼 리저브",
        "type": "샴페인",
        "price": "고가",
        "proof": "적당",
        "flavors": ["탄산감있는", "드라이한", "오렌지"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["연인과", "친구들과", "가족들과"],
        "level": "입문 추천",
        "story": "사과와 시트러스, 고운 탄산이 균형을 이루어 샴페인의 기본 스타일을 차분하게 알아가기 좋습니다.",
        "serving": "차갑게 준비하고 잔을 가득 채우기보다 향이 머물 공간을 남겨보세요.",
    },
    {
        "name": "루이나르 블랑 드 블랑",
        "type": "샴페인",
        "price": "프리미엄",
        "proof": "적당",
        "flavors": ["탄산감있는", "드라이한", "오렌지"],
        "mood": ["차분하고 조용한", "기분 좋은"],
        "occasion": ["연인과", "가족들과"],
        "level": "프리미엄 경험",
        "story": "섬세한 탄산과 레몬·흰 꽃 향이 중심인 프리미엄 샴페인으로 우아한 스타일을 경험하기 좋습니다.",
        "serving": "차갑게 마시되 너무 빠르게 마시지 말고 산미와 꽃 향의 변화를 느껴보세요.",
    },
    {
        "name": "글렌모렌지 오리지널 10년",
        "type": "위스키",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "오렌지", "오크향"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "오렌지와 바닐라를 떠올리게 하는 부드러운 향이 있어 싱글몰트의 기본을 편안하게 경험하기 좋습니다.",
        "serving": "처음에는 그대로 향을 맡고, 물을 몇 방울 넣어 시트러스 향의 변화를 느껴보세요.",
    },
    {
        "name": "카테나 말벡",
        "type": "와인",
        "price": "고가",
        "proof": "적당",
        "flavors": ["드라이한", "오크향", "달달한"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "친구들과", "가족들과"],
        "level": "입문 추천",
        "story": "검은 과일과 부드러운 오크 향이 어우러져 레드와인의 묵직함을 처음 경험하기 좋은 선택입니다.",
        "serving": "잔에 따라 잠시 두었다가 검은 과일 향과 부드러운 떫은맛을 천천히 느껴보세요.",
    },
    {
        "name": "메이커스 마크",
        "type": "위스키",
        "price": "중간",
        "proof": "높은",
        "flavors": ["달달한", "꿀", "오크향"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["혼술", "친구들과"],
        "level": "입문 추천",
        "story": "카라멜과 바닐라처럼 달콤한 향이 분명해 버번 위스키를 처음 경험하는 사람에게 친숙한 선택입니다.",
        "serving": "큰 얼음 하나와 함께 마시며 달콤한 향과 알코올감의 균형을 느껴보세요.",
    },
    {
        "name": "우드포드 리저브",
        "type": "위스키",
        "price": "고가",
        "proof": "높은",
        "flavors": ["오크향", "달달한", "훈연"],
        "mood": ["차분하고 조용한", "기분 좋은"],
        "occasion": ["혼술", "친구들과"],
        "level": "입문 추천",
        "story": "오크와 바닐라, 말린 과일 향이 균형을 이루어 버번의 깊이를 단계적으로 경험하기 좋습니다.",
        "serving": "니트로 먼저 향을 느끼고, 이후 얼음이나 물을 더해 질감 변화를 비교해보세요.",
    },
    {
        "name": "하이랜드 파크 12년",
        "type": "위스키",
        "price": "고가",
        "proof": "높은",
        "flavors": ["훈연", "달달한", "오크향"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "친구들과"],
        "level": "개성 강한 선택",
        "story": "은은한 훈연과 꿀, 오크 향이 함께 있어 피트 위스키를 처음 넓혀보고 싶을 때 좋은 중간 단계입니다.",
        "serving": "물 몇 방울로 훈연 향의 강도를 조절하며 천천히 마셔보세요.",
    },
    {
        "name": "버팔로 트레이스",
        "type": "위스키",
        "price": "중간",
        "proof": "높은",
        "flavors": ["달달한", "오크향", "꿀"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["혼술", "친구들과"],
        "level": "입문 추천",
        "story": "캐러멜과 바닐라, 오크 향이 부드럽게 이어져 진한 도수의 버번을 처음 시도하기 좋은 선택입니다.",
        "serving": "처음에는 얼음 하나를 넣어 알코올감을 낮추고 달콤한 향에 집중해보세요.",
    },
    {
        "name": "Citrus Bloom",
        "type": "보드카",
        "price": "중간",
        "proof": "적당",
        "flavors": ["달달한", "오렌지", "탄산감있는"],
        "mood": ["기분 좋은"],
        "occasion": ["친구들과", "연인과"],
        "level": "입문 추천",
        "story": "레몬과 꿀, 탄산이 어우러진 밝은 칵테일로 프리미엄 칵테일 경험을 가볍게 시작하기 좋습니다.",
        "serving": "차갑게 준비해 레몬 향과 가벼운 탄산을 먼저 느껴보세요.",
    },
    {
        "name": "Velvet Hour",
        "type": "럼",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "오크향", "꿀"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "숙성 럼과 메이플, 비터스의 따뜻한 향이 어우러져 달콤한 나이트캡을 경험하기 좋습니다.",
        "serving": "큰 얼음 하나와 함께 천천히 마시며 오렌지 향을 느껴보세요.",
    },
    {
        "name": "Rose Afterglow",
        "type": "진",
        "price": "고가",
        "proof": "낮은",
        "flavors": ["달달한", "오렌지"],
        "mood": ["기분 좋은", "위로받는"],
        "occasion": ["연인과", "혼술"],
        "level": "입문 추천",
        "story": "엘더플라워와 장미 향이 은은한 가벼운 칵테일로 진의 향을 부드럽게 시작할 수 있습니다.",
        "serving": "차갑게 준비한 쿠페 잔에 담아 꽃 향을 먼저 느껴보세요.",
    },
    {
        "name": "Midnight Paloma",
        "type": "테킬라",
        "price": "고가",
        "proof": "높은",
        "flavors": ["탄산감있는", "오렌지", "드라이한"],
        "mood": ["기분 좋은"],
        "occasion": ["친구들과"],
        "level": "개성 강한 선택",
        "story": "자몽과 라임, 탄산이 테킬라의 아가베 향과 만나 활기찬 밤에 어울리는 선명한 칵테일이 됩니다.",
        "serving": "소금 림을 더하고 천천히 마시며 자몽의 쌉쌀함을 느껴보세요.",
    },
    {
        "name": "Cloud Nine",
        "type": "브랜디",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "꿀"],
        "mood": ["위로받는", "차분하고 조용한"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "브랜디와 커피 리큐어, 오트밀크가 만나 부드럽고 포근한 디저트 같은 경험을 줍니다.",
        "serving": "차갑게 흔들어 크리미한 질감을 살리고 시나몬을 가볍게 뿌려보세요.",
    },
    {
        "name": "Garden Gimlet",
        "type": "진",
        "price": "고가",
        "proof": "높은",
        "flavors": ["드라이한", "오렌지"],
        "mood": ["차분하고 조용한"],
        "occasion": ["혼술", "친구들과"],
        "level": "개성 강한 선택",
        "story": "오이와 라임의 산뜻함이 진의 허브 향을 선명하게 보여주는 깔끔한 칵테일입니다.",
        "serving": "차갑게 흔든 뒤 오이 향을 먼저 맡고 한 모금 마셔보세요.",
    },
    {
        "name": "Sunset Spritz",
        "type": "와인",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["탄산감있는", "오렌지", "달달한"],
        "mood": ["기분 좋은"],
        "occasion": ["친구들과", "연인과", "가족들과"],
        "level": "입문 추천",
        "story": "스파클링 와인과 오렌지 향이 가볍게 어우러져 와인을 처음 접하는 날 부담 없이 즐기기 좋습니다.",
        "serving": "얼음이 담긴 잔에 천천히 따르고 오렌지 향을 즐겨보세요.",
    },
    {
        "name": "Spiced Orchard",
        "type": "위스키",
        "price": "고가",
        "proof": "높은",
        "flavors": ["달달한", "오크향", "꿀"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "버번과 사과, 시나몬이 만나 위스키의 달콤한 향을 칵테일로 쉽게 경험하게 해줍니다.",
        "serving": "얼음 위에 담고 사과와 시나몬 향을 번갈아 느껴보세요.",
    },
    {
        "name": "Coastal Mule",
        "type": "보드카",
        "price": "중간",
        "proof": "적당",
        "flavors": ["탄산감있는", "오렌지", "드라이한"],
        "mood": ["기분 좋은"],
        "occasion": ["친구들과", "연인과"],
        "level": "입문 추천",
        "story": "진저비어와 라임의 청량함이 보드카와 만나 처음 마시는 사람도 쉽게 즐길 수 있습니다.",
        "serving": "차가운 잔에 담아 진저의 알싸함과 탄산을 먼저 느껴보세요.",
    },
    {
        "name": "Quiet Storm",
        "type": "럼",
        "price": "고가",
        "proof": "높은",
        "flavors": ["달달한", "드라이한", "오크향"],
        "mood": ["위로받는", "차분하고 조용한"],
        "occasion": ["혼술"],
        "level": "개성 강한 선택",
        "story": "다크 럼과 라임, 비터스의 깊고 쌉쌀한 맛이 복잡한 하루를 정리하는 데 어울립니다.",
        "serving": "차갑게 준비해 한 모금씩 천천히 마셔보세요.",
    },
    {
        "name": "Honey Fizz",
        "type": "소주",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["달달한", "탄산감있는", "오렌지"],
        "mood": ["기분 좋은", "위로받는"],
        "occasion": ["혼술", "친구들과"],
        "level": "입문 추천",
        "story": "소주에 꿀과 레몬, 탄산을 더해 익숙한 술을 조금 더 세련된 방식으로 경험할 수 있습니다.",
        "serving": "레몬 향을 먼저 느낀 뒤 탄산감과 은은한 단맛을 즐겨보세요.",
    },
    {
        "name": "Bramble Noir",
        "type": "진",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "오렌지", "드라이한"],
        "mood": ["연인과", "기분 좋은"],
        "occasion": ["연인과", "친구들과"],
        "level": "입문 추천",
        "story": "베리의 달콤함과 레몬의 산미가 진의 허브 향을 감싸 로맨틱한 분위기에 잘 어울립니다.",
        "serving": "부순 얼음 위에 담아 베리 향과 산미를 천천히 비교해보세요.",
    },
    {
        "name": "Golden Sour",
        "type": "위스키",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "오렌지", "꿀"],
        "mood": ["기분 좋은", "위로받는"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "레몬과 꿀, 위스키의 균형이 좋아 위스키를 칵테일로 처음 경험하기 좋은 선택입니다.",
        "serving": "차갑게 흔들어 산미와 꿀의 부드러움을 함께 느껴보세요.",
    },
    {
        "name": "Agave Highball",
        "type": "테킬라",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["탄산감있는", "드라이한", "오렌지"],
        "mood": ["기분 좋은", "차분하고 조용한"],
        "occasion": ["친구들과", "연인과"],
        "level": "입문 추천",
        "story": "자몽 탄산과 라임이 테킬라의 아가베 향을 가볍게 만들어 입문자도 접근하기 좋습니다.",
        "serving": "소금 림을 선택하고 차갑게 마시며 자몽의 산뜻함을 느껴보세요.",
    },
    {
        "name": "Berry Brandy Smash",
        "type": "브랜디",
        "price": "고가",
        "proof": "적당",
        "flavors": ["달달한", "오렌지"],
        "mood": ["기분 좋은", "연인과"],
        "occasion": ["연인과", "친구들과"],
        "level": "입문 추천",
        "story": "베리와 민트, 레몬이 브랜디의 따뜻한 과일 향을 밝고 쉽게 풀어낸 칵테일입니다.",
        "serving": "베리를 가볍게 으깨고 얼음과 함께 시원하게 즐겨보세요.",
    },
    {
        "name": "Coconut Moon",
        "type": "럼",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["달달한", "오렌지"],
        "mood": ["위로받는", "기분 좋은"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "코코넛과 바닐라, 라임이 부드럽게 어우러져 럼을 처음 경험하기 좋은 휴식 같은 칵테일입니다.",
        "serving": "차갑게 준비해 코코넛의 부드러운 향을 먼저 느껴보세요.",
    },
    {
        "name": "Ruby Negroni",
        "type": "와인",
        "price": "고가",
        "proof": "높은",
        "flavors": ["드라이한", "오렌지", "오크향"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "친구들과"],
        "level": "개성 강한 선택",
        "story": "레드 베르무트와 진, 비터 아페리티프의 쌉쌀함이 깊은 밤의 감상에 어울립니다.",
        "serving": "큰 얼음 하나에 담고 오렌지 껍질 향을 먼저 표현해보세요.",
    },
    {
        "name": "Lemon Shandy",
        "type": "맥주",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["탄산감있는", "오렌지", "달달한"],
        "mood": ["기분 좋은"],
        "occasion": ["친구들과", "가족들과"],
        "level": "입문 추천",
        "story": "밀맥주와 레모네이드가 만나 맥주의 쌉쌀함을 낮춘 가벼운 입문용 선택입니다.",
        "serving": "차가운 잔에 레모네이드를 먼저 넣고 맥주를 천천히 따라보세요.",
    },
    {
        "name": "Smoked Maple",
        "type": "위스키",
        "price": "고가",
        "proof": "높은",
        "flavors": ["훈연", "달달한", "오크향"],
        "mood": ["차분하고 조용한", "연인과"],
        "occasion": ["혼술", "연인과"],
        "level": "개성 강한 선택",
        "story": "라이 위스키와 메이플, 훈연한 로즈마리가 촛불 아래 깊은 대화를 위한 분위기를 만듭니다.",
        "serving": "큰 얼음 하나에 담고 로즈마리의 훈연 향을 가볍게 느껴보세요.",
    },
    {
        "name": "Pear Blossom",
        "type": "소주",
        "price": "중간",
        "proof": "낮은",
        "flavors": ["달달한", "오렌지"],
        "mood": ["차분하고 조용한", "위로받는"],
        "occasion": ["혼술", "연인과"],
        "level": "입문 추천",
        "story": "배와 엘더플라워의 은은한 향이 소주를 부드럽고 향기롭게 즐기는 경험을 만들어줍니다.",
        "serving": "차갑게 흔들어 스템드 잔에 담고 배 향을 먼저 느껴보세요.",
    },
]


PAIRINGS = [
    {"name": "캐비어와 블리니", "price": "프리미엄", "types": ["샴페인"], "flavors": ["탄산감있는", "드라이한"], "reason": "짭짤한 캐비어와 바삭한 블리니가 샴페인의 산미와 탄산감을 돋보이게 합니다."},
    {"name": "굴과 레몬", "price": "프리미엄", "types": ["샴페인"], "flavors": ["탄산감있는", "드라이한", "오렌지"], "reason": "굴의 바다 향과 짠맛을 샴페인의 산뜻한 산미가 깔끔하게 정리합니다."},
    {"name": "푸아그라와 브리오슈", "price": "프리미엄", "types": ["위스키", "와인"], "flavors": ["오크향", "달달한", "드라이한"], "reason": "푸아그라의 진하고 부드러운 질감이 위스키의 오크 향과 와인의 과일 향을 풍성하게 느끼게 합니다."},
    {"name": "트러플 감자칩", "price": "프리미엄", "types": ["샴페인", "와인"], "flavors": ["탄산감있는", "오크향", "드라이한"], "reason": "트러플의 깊은 향과 감자의 짠맛이 샴페인의 탄산감과 와인의 구조감을 살려줍니다."},
    {"name": "가리비 카르파초", "price": "프리미엄", "types": ["샴페인", "와인"], "flavors": ["탄산감있는", "드라이한", "오렌지"], "reason": "가리비의 은은한 단맛과 레몬 향이 산뜻한 샴페인과 화이트와인에 잘 연결됩니다."},
    {"name": "숙성 치즈", "price": "일상 접근 가능", "types": ["위스키", "와인", "샴페인"], "flavors": ["오크향", "드라이한", "달달한"], "reason": "치즈의 짠맛과 크리미한 질감이 술의 향을 부드럽게 연결해 줍니다."},
    {"name": "다크초콜릿", "price": "일상 접근 가능", "types": ["위스키", "와인"], "flavors": ["달달한", "오크향", "훈연"], "reason": "초콜릿의 쌉쌀하고 달콤한 맛이 오크 향과 바닐라 향을 자연스럽게 강조합니다."},
    {"name": "말린 무화과와 견과류", "price": "일상 접근 가능", "types": ["위스키", "와인"], "flavors": ["달달한", "꿀", "오크향"], "reason": "말린 과일과 견과류의 고소한 향이 위스키의 꿀·오크 향과 잘 어울립니다."},
    {"name": "훈제 연어와 크림치즈", "price": "일상 접근 가능", "types": ["샴페인", "와인"], "flavors": ["탄산감있는", "드라이한", "훈연"], "reason": "훈제 향과 크림치즈의 부드러움을 산뜻한 술이 균형 있게 받쳐줍니다."},
    {"name": "블루치즈와 꿀", "price": "일상 접근 가능", "types": ["위스키", "와인"], "flavors": ["달달한", "꿀", "오크향"], "reason": "블루치즈의 강한 풍미와 꿀의 단맛이 달콤한 위스키와 묵직한 와인을 부드럽게 만듭니다."},
    {"name": "애플 타르트", "price": "일상 접근 가능", "types": ["위스키", "와인"], "flavors": ["달달한", "꿀", "오크향"], "reason": "사과와 시나몬의 따뜻한 향이 과일 향과 꿀 향이 있는 위스키에 자연스럽게 이어집니다."},
    {"name": "브리치즈와 포도", "price": "일상 접근 가능", "types": ["샴페인", "와인"], "flavors": ["탄산감있는", "드라이한", "달달한"], "reason": "부드러운 치즈와 포도의 은은한 단맛이 산뜻한 샴페인과 와인의 균형을 잡아줍니다."},
    {"name": "올리브와 아몬드", "price": "일상 접근 가능", "types": ["샴페인", "와인"], "flavors": ["드라이한", "오렌지"], "reason": "올리브의 짠맛과 아몬드의 고소함이 드라이한 술의 풍미를 또렷하게 해줍니다."},
    {"name": "버섯 크림 브루스케타", "price": "일상 접근 가능", "types": ["위스키", "와인"], "flavors": ["오크향", "훈연", "드라이한"], "reason": "버섯의 흙내음과 크림의 질감이 오크 향이나 은은한 훈연 향과 잘 어울립니다."},
    {"name": "감귤과 허브를 곁들인 올리브", "price": "일상 접근 가능", "types": ["보드카", "진", "테킬라"], "flavors": ["오렌지", "드라이한"], "reason": "감귤의 산뜻함과 허브 향이 깔끔한 증류주를 처음 마실 때 부담을 덜어줍니다."},
    {"name": "진저 라임 새우", "price": "일상 접근 가능", "types": ["보드카", "럼", "테킬라"], "flavors": ["탄산감있는", "오렌지", "드라이한"], "reason": "생강과 라임의 상쾌한 향이 하이볼이나 칵테일 스타일의 술과 잘 맞습니다."},
    {"name": "브리치즈와 베리 크로스티니", "price": "일상 접근 가능", "types": ["브랜디", "럼", "와인"], "flavors": ["달달한", "오렌지", "오크향"], "reason": "부드러운 치즈와 베리의 단맛이 과일 향과 오크 향이 있는 술을 쉽게 즐기게 해줍니다."},
    {"name": "코코넛 라임 새우", "price": "일상 접근 가능", "types": ["럼", "테킬라"], "flavors": ["달달한", "오렌지", "탄산감있는"], "reason": "코코넛의 부드러운 단맛과 라임의 산미가 열대 과일 느낌의 술과 어울립니다."},
    {"name": "배와 엘더플라워 타르트", "price": "일상 접근 가능", "types": ["소주", "브랜디", "와인"], "flavors": ["달달한", "꿀", "오렌지"], "reason": "배와 꽃 향의 은은한 단맛이 부드러운 술을 입문자도 편하게 마시도록 도와줍니다."},
    {"name": "레몬 셔벗", "price": "일상 접근 가능", "types": ["보드카", "진", "샴페인", "와인", "맥주"], "flavors": ["탄산감있는", "오렌지", "달달한"], "reason": "차갑고 상큼한 레몬 맛이 탄산감 있는 술의 첫인상을 깔끔하게 정리해줍니다."},
]


MUSIC = [
    {"name": "Norah Jones - Don't Know Why", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술", "연인과"], "drink_types": ["위스키", "와인"], "flavors": ["달달한", "오크향"], "reason": "부드러운 보컬과 피아노가 달콤한 위스키나 와인의 향을 천천히 감상하게 합니다."},
    {"name": "Cigarettes After Sex - Apocalypse", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술", "연인과"], "drink_types": ["샴페인", "와인"], "flavors": ["드라이한", "오렌지"], "reason": "몽환적인 사운드가 드라이한 샴페인과 와인을 마시는 늦은 밤의 분위기를 만듭니다."},
    {"name": "Laufey - From The Start", "mood": ["기분 좋은", "연인과"], "occasion": ["연인과", "친구들과"], "drink_types": ["샴페인", "와인", "진", "보드카"], "flavors": ["탄산감있는", "달달한"], "reason": "재즈를 바탕으로 한 산뜻한 팝이 가벼운 샴페인과 깔끔한 진·보드카의 즐거운 분위기에 잘 맞습니다."},
    {"name": "HYUKOH - Comes And Goes", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술"], "drink_types": ["위스키", "와인"], "flavors": ["드라이한", "오크향"], "reason": "담백하고 쓸쓸한 분위기가 하루를 정리하는 혼술 시간과 잘 어울립니다."},
    {"name": "Men I Trust - Show Me How", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술", "연인과"], "drink_types": ["위스키", "와인"], "flavors": ["달달한", "꿀"], "reason": "부드러운 드림팝 사운드가 꿀과 바닐라처럼 달콤한 향에 집중하게 합니다."},
    {"name": "The Marías - No One Noticed", "mood": ["기분 좋은", "연인과"], "occasion": ["연인과", "친구들과"], "drink_types": ["와인", "샴페인"], "flavors": ["탄산감있는", "오렌지"], "reason": "세련된 드림팝 리듬이 와인이나 샴페인의 가벼운 분위기를 살려줍니다."},
    {"name": "Khruangbin - Friday Morning", "mood": ["기분 좋은", "차분하고 조용한"], "occasion": ["친구들과", "혼술"], "drink_types": ["와인", "샴페인", "럼", "테킬라"], "flavors": ["오렌지", "드라이한"], "reason": "여유로운 기타 연주가 산뜻한 와인뿐 아니라 럼·테킬라의 여유로운 저녁에도 잘 어울립니다."},
    {"name": "Sufjan Stevens - Mystery of Love", "mood": ["위로받는", "연인과"], "occasion": ["연인과", "혼술"], "drink_types": ["와인", "샴페인", "브랜디", "소주"], "flavors": ["드라이한", "오렌지"], "reason": "섬세한 어쿠스틱 사운드가 조용한 와인과 브랜디, 부드러운 소주를 마시는 순간을 연결합니다."},
    {"name": "Beach House - Space Song", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술", "연인과"], "drink_types": ["위스키", "와인"], "flavors": ["오크향", "훈연"], "reason": "깊고 몽환적인 사운드가 오크와 훈연 향이 있는 술의 긴 여운과 잘 맞습니다."},
    {"name": "Bon Iver - Holocene", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술"], "drink_types": ["위스키", "와인"], "flavors": ["드라이한", "오크향"], "reason": "넓고 잔잔한 사운드가 하루를 천천히 내려놓는 시간에 어울립니다."},
    {"name": "Phoebe Bridgers - Garden Song", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술", "연인과"], "drink_types": ["위스키", "와인"], "flavors": ["달달한", "드라이한"], "reason": "담담한 인디 포크가 부드러운 위스키나 레드와인의 차분한 분위기를 살립니다."},
    {"name": "Radiohead - Weird Fishes/Arpeggi", "mood": ["차분하고 조용한"], "occasion": ["혼술", "친구들과"], "drink_types": ["위스키"], "flavors": ["훈연", "오크향"], "reason": "층층이 쌓이는 기타 사운드가 개성 강한 훈연 위스키를 천천히 감상하게 합니다."},
    {"name": "The National - I Need My Girl", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술", "연인과"], "drink_types": ["위스키", "와인"], "flavors": ["오크향", "드라이한"], "reason": "낮고 깊은 보컬이 묵직한 위스키와 조용히 대화하는 밤에 잘 어울립니다."},
    {"name": "Mitski - My Love Mine All Mine", "mood": ["위로받는", "연인과"], "occasion": ["연인과", "혼술"], "drink_types": ["와인", "샴페인"], "flavors": ["달달한", "드라이한"], "reason": "따뜻한 보컬이 과일 향이 있는 와인과 감정적인 밤의 분위기를 채워줍니다."},
    {"name": "FKJ - Ylang Ylang", "mood": ["기분 좋은", "차분하고 조용한"], "occasion": ["친구들과", "연인과"], "drink_types": ["샴페인", "와인"], "flavors": ["탄산감있는", "오렌지"], "reason": "부드러운 전자음과 재즈 리듬이 샴페인의 탄산감을 가볍고 세련되게 살립니다."},
    {"name": "Mac DeMarco - Chamber of Reflection", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술"], "drink_types": ["위스키"], "flavors": ["오크향", "꿀"], "reason": "느긋하고 빈티지한 사운드가 꿀과 오크 향이 있는 위스키의 여운과 어울립니다."},
    {"name": "Tame Impala - Borderline", "mood": ["기분 좋은", "차분하고 조용한"], "occasion": ["친구들과", "연인과"], "drink_types": ["샴페인", "와인"], "flavors": ["탄산감있는", "달달한"], "reason": "몽환적인 그루브가 샴페인과 가벼운 와인을 즐기는 기분 좋은 순간을 돋보이게 합니다."},
    {"name": "우효 - 민들레", "mood": ["위로받는", "기분 좋은"], "occasion": ["혼술", "연인과"], "drink_types": ["와인", "샴페인", "브랜디", "소주"], "flavors": ["달달한", "오렌지"], "reason": "맑고 따뜻한 인디 팝이 과일 향이 있는 와인과 브랜디, 편안한 소주에 잘 어울립니다."},
    {"name": "Alice Phoebe Lou - Something Holy", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술", "연인과"], "drink_types": ["와인", "위스키"], "flavors": ["드라이한", "오크향"], "reason": "따뜻한 보컬과 느슨한 리듬이 드라이한 와인과 위스키의 긴 여운을 편안하게 받쳐줍니다."},
    {"name": "Japanese Breakfast - Be Sweet", "mood": ["기분 좋은"], "occasion": ["친구들과", "연인과"], "drink_types": ["샴페인", "와인"], "flavors": ["탄산감있는", "달달한"], "reason": "밝은 인디 팝의 에너지가 샴페인의 탄산감과 축하하는 분위기를 살려줍니다."},
    {"name": "Big Thief - Simulation Swarm", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술"], "drink_types": ["위스키", "와인"], "flavors": ["드라이한", "오크향"], "reason": "섬세하게 쌓이는 포크 사운드가 차분한 혼술과 깊은 향의 술에 어울립니다."},
    {"name": "Daughter - Youth", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술", "연인과"], "drink_types": ["위스키", "와인"], "flavors": ["훈연", "드라이한"], "reason": "잔잔하지만 깊은 기타와 보컬이 스모키한 위스키의 여운을 길게 이어줍니다."},
    {"name": "The xx - Intro", "mood": ["차분하고 조용한"], "occasion": ["혼술", "연인과"], "drink_types": ["위스키", "샴페인"], "flavors": ["오크향", "탄산감있는"], "reason": "미니멀한 리듬이 술의 향과 잔 부딪히는 소리에 집중하게 합니다."},
    {"name": "L'Impératrice - Vanille fraise", "mood": ["기분 좋은", "연인과"], "occasion": ["연인과", "친구들과"], "drink_types": ["샴페인", "와인"], "flavors": ["달달한", "탄산감있는"], "reason": "프렌치 디스코의 세련된 리듬이 달콤한 향의 샴페인과 가벼운 와인에 잘 맞습니다."},
    {"name": "Men I Trust - Lauren", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술", "연인과"], "drink_types": ["와인", "위스키"], "flavors": ["달달한", "꿀"], "reason": "느긋한 기타와 보컬이 꿀과 과일 향이 있는 술의 부드러움을 살려줍니다."},
    {"name": "Tom Misch - Movie", "mood": ["기분 좋은", "연인과"], "occasion": ["연인과", "친구들과"], "drink_types": ["샴페인", "와인", "럼", "테킬라"], "flavors": ["오렌지", "탄산감있는"], "reason": "재즈와 소울이 섞인 리듬이 산뜻한 술과 럼·테킬라를 곁들인 즐거운 대화 사이를 채워줍니다."},
    {"name": "Arlo Parks - Eugene", "mood": ["위로받는", "차분하고 조용한"], "occasion": ["혼술", "연인과"], "drink_types": ["와인", "샴페인"], "flavors": ["드라이한", "오렌지"], "reason": "담백한 인디 소울이 과일 향 와인을 마시며 감정을 정리하는 시간에 잘 어울립니다."},
    {"name": "Soccer Mommy - circle the drain", "mood": ["위로받는"], "occasion": ["혼술"], "drink_types": ["위스키", "와인"], "flavors": ["드라이한", "오크향"], "reason": "차분한 기타 사운드가 하루의 피로를 내려놓는 혼술 시간과 잘 맞습니다."},
    {"name": "Clairo - Bags", "mood": ["차분하고 조용한", "연인과"], "occasion": ["연인과", "혼술"], "drink_types": ["와인", "샴페인"], "flavors": ["달달한", "드라이한"], "reason": "섬세하고 가까운 보컬이 부드러운 와인과 조용한 대화의 분위기를 만듭니다."},
    {"name": "Snail Mail - Pristine", "mood": ["기분 좋은", "위로받는"], "occasion": ["친구들과", "혼술"], "drink_types": ["와인", "샴페인"], "flavors": ["오렌지", "드라이한"], "reason": "맑은 기타와 청춘의 에너지가 산뜻한 와인과 가벼운 모임에 어울립니다."},
    {"name": "The Japanese House - Saw You In A Dream", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술", "연인과"], "drink_types": ["샴페인", "와인"], "flavors": ["탄산감있는", "오렌지"], "reason": "몽환적인 전자음이 샴페인의 섬세한 탄산과 감귤 향을 부드럽게 확장합니다."},
    {"name": "윤지영 - 우우우린", "mood": ["위로받는", "연인과"], "occasion": ["연인과", "혼술"], "drink_types": ["와인", "위스키"], "flavors": ["달달한", "드라이한"], "reason": "담담한 한국 인디 음악이 과일 향 와인이나 부드러운 위스키와 조용히 어울립니다."},
    {"name": "새소년 - 긴 꿈", "mood": ["차분하고 조용한", "위로받는"], "occasion": ["혼술", "친구들과"], "drink_types": ["위스키", "와인"], "flavors": ["훈연", "오크향"], "reason": "개성 있는 기타와 보컬이 훈연 위스키의 강한 향을 감상하는 시간을 만들어줍니다."},
    {"name": "검정치마 - Everything", "mood": ["연인과", "위로받는"], "occasion": ["연인과", "혼술"], "drink_types": ["와인", "샴페인"], "flavors": ["달달한", "오렌지"], "reason": "로맨틱한 인디 록이 달콤한 향의 와인과 연인과의 느린 저녁에 잘 맞습니다."},
    {"name": "실리카겔 - Tik Tak Tok", "mood": ["기분 좋은"], "occasion": ["친구들과", "연인과"], "drink_types": ["샴페인", "위스키"], "flavors": ["탄산감있는", "훈연"], "reason": "실험적인 리듬이 톡 쏘는 샴페인이나 개성 강한 위스키와 재미있는 대비를 만듭니다."},
    {"name": "페퍼톤스 - 공원여행", "mood": ["기분 좋은"], "occasion": ["친구들과", "가족들과"], "drink_types": ["와인", "샴페인", "맥주"], "flavors": ["탄산감있는", "오렌지"], "reason": "밝고 산뜻한 밴드 사운드가 가벼운 와인과 샴페인, 맥주를 즐기는 낮의 분위기를 살립니다."},
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
    available_drinks = [drink for drink in DRINKS if drink["name"] not in exclude_names]
    # 점수가 같은 술은 목록 앞쪽의 기존 술만 반복되지 않도록 순서를 섞습니다.
    random.shuffle(available_drinks)
    ranked = sorted(
        available_drinks,
        key=lambda drink: score_drink(drink, occasion, drink_type, mood, proof, flavors, budget),
        reverse=True,
    )
    # 기존 술과 새 술을 구분하지 않고, 동일한 점수 순서로 상위 3개를 보여줍니다.
    # 조건에 맞는 후보가 없어도 빈 화면 대신 최소 한 개를 보여줍니다.
    return ranked[:3] or available_drinks[:1] or DRINKS[:1]


def recommend_pairings(drink, budget):
    """주종·예산·술의 맛과 향을 함께 반영해 페어링을 추천합니다."""
    candidates = [p for p in PAIRINGS if drink["type"] in p["types"]]
    shuffled = candidates.copy()
    random.shuffle(shuffled)

    def pairing_score(pairing):
        price_score = 3 if budget == "프리미엄" and pairing["price"] == "프리미엄" else 0
        flavor_score = sum(2 for flavor in drink["flavors"] if flavor in pairing.get("flavors", []))
        return price_score + flavor_score

    ranked = sorted(shuffled, key=pairing_score, reverse=True)
    return ranked[:3] or PAIRINGS[:3]


def recommend_music(drink, mood, occasion):
    """분위기·상황·주종·맛을 반영하고, 이전 곡과 겹치지 않게 추천합니다."""
    music_cache = st.session_state.setdefault("music_cache", {})
    request_key = "|".join(
        [
            drink["name"],
            drink["type"],
            mood,
            occasion,
            ",".join(sorted(drink.get("flavors", []))),
        ]
    )
    if request_key in music_cache:
        return music_cache[request_key]

    shuffled = MUSIC.copy()
    random.shuffle(shuffled)

    def music_score(song):
        return (
            (3 if mood in song["mood"] else 0)
            + (2 if drink["type"] in song["drink_types"] else 0)
            + (1 if occasion in song["occasion"] else 0)
            + sum(1 for flavor in drink["flavors"] if flavor in song["flavors"])
        )

    ranked = sorted(shuffled, key=music_score, reverse=True)
    history = set(st.session_state.get("music_history", []))
    fresh = [song for song in ranked if song["name"] not in history]

    # 현재 세션에서 거의 모든 곡을 사용했다면 기록을 한 번 비우고 다시 순환합니다.
    if len(fresh) < 3:
        history = set()
        fresh = ranked

    selected = fresh[:3] or MUSIC[:3]
    st.session_state["music_history"] = list(history | {song["name"] for song in selected})
    music_cache[request_key] = selected
    return selected

def youtube_search_url(song_name):
    """특정 영상이 삭제되어도 작동하도록 YouTube 검색 결과로 연결합니다."""
    return f"https://www.youtube.com/results?search_query={quote_plus(song_name)}"


# -----------------------------
# 2. 화면
# -----------------------------

st.set_page_config(page_title="오늘의 프리미엄 주류 경험", page_icon="🥂", layout="centered")

st.title("🥂 오늘의 프리미엄 주류 경험")
st.write("술을 잘 알아야 하는 서비스가 아닙니다. 지금의 분위기와 취향에 맞춰 첫 경험을 안내해 드립니다.")

st.subheader("먼저 오늘의 취향을 알려주세요")

occasion = st.selectbox("1. 누구와 즐기나요?", ["혼술", "친구들과", "가족들과", "연인과", "기타"])
mood = st.selectbox("2. 어떤 분위기인가요?", ["차분하고 조용한", "기분 좋은", "위로받는"])
drink_type = st.selectbox(
    "3. 어떤 주종을 경험해보고 싶나요?",
    ["전체", "와인", "위스키", "샴페인", "보드카", "럼", "진", "테킬라", "브랜디", "소주", "맥주"],
)
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
            songs = recommend_music(drink, mood, occasion)

            # 술과 페어링을 연결해 표시하는 핵심 코드입니다.
            st.markdown("**함께 먹기 좋은 페어링**")
            for pairing in pairings:
                st.write(f"- **{pairing['name']}**: {pairing['reason']}")

            st.markdown("**함께 들을 음악**")
            for song in songs:
                youtube_url = youtube_search_url(song["name"])
                st.markdown(f"- **[{song['name']}]({youtube_url})**: {song['reason']}")

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
