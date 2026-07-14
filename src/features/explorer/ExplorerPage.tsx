import { useMemo, useState } from 'react'
import { ArrowLeft, ChevronRight, Search, X } from 'lucide-react'
import { cocktails } from '../../data/cocktails'
import type { Alcohol, Cocktail, Strength } from '../../types'
import './explorer.css'

const alcoholLabels: Record<Alcohol, string> = {
  Vodka: '보드카', Gin: '진', Rum: '럼', Whiskey: '위스키', Tequila: '데킬라',
  Brandy: '브랜디', Soju: '소주', Beer: '맥주', Wine: '와인',
}

const strengthLabels: Record<Strength, string> = { Light: '가볍게', Medium: '중간', Strong: '진하게' }

const names: Record<number, string> = {
  1: '시트러스 블룸', 2: '벨벳 아워', 3: '로즈 애프터글로우', 4: '미드나이트 팔로마', 5: '클라우드 나인',
  6: '가든 김렛', 7: '선셋 스프리츠', 8: '스파이스드 오차드', 9: '코스탈 뮬', 10: '콰이어트 스톰',
  11: '허니 피즈', 12: '브램블 누아르', 13: '골든 사워', 14: '아가베 하이볼', 15: '베리 브랜디 스매시',
  16: '코코넛 문', 17: '루비 네그로니', 18: '레몬 샨디', 19: '스모크드 메이플', 20: '페어 블라썸',
}

const descriptions: Record<number, string> = {
  1: '상큼한 시트러스와 은은한 단맛이 어우러진 가볍고 반짝이는 한 잔이에요.',
  2: '부드러운 향신료와 따뜻한 여운이 남는 실키한 나이트캡이에요.',
  3: '장미와 엘더플라워의 은은한 향이 조용한 분위기를 만들어줘요.',
  4: '훈연한 데킬라와 자몽의 쌉쌀한 탄산감이 파티를 깨워줘요.',
  5: '브랜디와 커피의 포근하고 크리미한 맛으로 천천히 쉬어가는 칵테일이에요.',
  6: '오이와 라임의 맑고 산뜻한 향이 긴장을 부드럽게 내려놓게 해줘요.',
  7: '황금빛 과실 향과 탄산감이 어우러진 가벼운 스프리츠예요.',
  8: '따뜻한 사과와 향신료, 위스키의 깊은 풍미가 천천히 퍼져요.',
  9: '진저 비어와 라임의 톡 쏘는 맛이 기분을 빠르게 전환해줘요.',
  10: '다크 럼과 비터스의 깊고 차분한 맛으로 숨을 고르는 한 잔이에요.',
  11: '꿀과 레몬, 탄산이 만나 누구나 편하게 즐길 수 있어요.',
  12: '진한 베리 풍미와 상쾌한 산미가 우아하면서도 playful하게 이어져요.',
  13: '밝은 레몬과 꿀, 위스키의 실키한 질감이 균형을 이뤄요.',
  14: '데킬라와 자몽의 깨끗하고 산뜻한 풍미가 바람처럼 가벼워요.',
  15: '베리와 민트의 싱그러움이 브랜디의 풍부한 맛을 산뜻하게 감싸요.',
  16: '코코넛과 바닐라의 부드러운 향으로 작은 휴가 같은 기분을 줘요.',
  17: '달콤쌉쌀한 레드 베르무트와 진의 의식적인 깊이가 매력적이에요.',
  18: '밀맥주와 레모네이드가 만나 상쾌하고 부담 없이 즐길 수 있어요.',
  19: '메이플과 훈연한 로즈메리가 위스키의 묵직한 풍미를 돋워줘요.',
  20: '배와 플로럴 향이 어우러진 부드럽고 섬세한 한 잔이에요.',
}

const ingredientTranslations: Record<string, string> = {
  'vodka': '보드카', 'aged rum': '숙성 럼', 'dark rum': '다크 럼', 'white rum': '화이트 럼', 'gin': '진',
  'whiskey': '위스키', 'bourbon': '버번', 'rye whiskey': '라이 위스키', 'tequila': '데킬라', 'brandy': '브랜디',
  'soju': '소주', 'wheat beer': '밀맥주', 'sparkling wine': '스파클링 와인', 'red vermouth': '레드 베르무트',
  'coffee liqueur': '커피 리큐르', 'elderflower liqueur': '엘더플라워 리큐르', 'blackberry liqueur': '블랙베리 리큐르',
  'lemon juice': '레몬 주스', 'lime juice': '라임 주스', 'grapefruit juice': '자몽 주스', 'apple cider': '애플 사이다',
  'pear nectar': '배 넥타', 'coconut water': '코코넛 워터', 'ginger beer': '진저 비어', 'grapefruit soda': '자몽 소다',
  'soda water': '탄산수', 'lemonade': '레모네이드', 'maple syrup': '메이플 시럽', 'honey syrup': '허니 시럽',
  'cinnamon syrup': '시나몬 시럽', 'demerara syrup': '데메라라 시럽', 'simple syrup': '심플 시럽', 'vanilla syrup': '바닐라 시럽',
  'rose water': '로즈 워터', 'bitters': '비터스', 'cucumber slices': '오이 슬라이스', 'orange peel': '오렌지 필',
  'lemon wheel': '레몬 휠', 'orange slice': '오렌지 슬라이스', 'rose petal': '장미 꽃잎', 'cinnamon': '시나몬',
  'mint': '민트', 'smoked rosemary': '훈연한 로즈메리', 'handful of berries': '베리 한 줌', 'berries': '베리',
  'egg white (optional)': '달걀흰자 (선택)', 'pinch of salt': '소금 한 꼬집', 'salt rim': '소금 림', 'splash of soda': '탄산수 약간',
  'bottle': '한 병', ' oz': '온스',
}

const stepTranslations: [RegExp, string][] = [
  [/^Shake .*with ice\.?/i, '얼음과 함께 셰이커에 넣고 흔들어요.'],
  [/^Dry shake .*\.?/i, '얼음 없이 먼저 흔들어요.'],
  [/^Stir .*ice\.?/i, '얼음과 함께 부드럽게 저어요.'],
  [/^Build .*ice.*\.?/i, '잔에 얼음을 넣고 재료를 바로 쌓아요.'],
  [/^Pour .*\.?/i, '잔에 부어요.'],
  [/^Fill .*\.?/i, '잔을 채워요.'],
  [/^Strain .*\.?/i, '잔에 걸러 따라요.'],
  [/^Double strain .*\.?/i, '고운 체로 한 번 더 걸러 따라요.'],
  [/^Top with .*\.?/i, '마지막에 탄산을 채워요.'],
  [/^Float .*\.?/i, '위에 조심스럽게 띄워요.'],
  [/^Express .*\.?/i, '껍질의 향을 짜서 더해요.'],
  [/^Add .*\.?/i, '재료를 더해요.'],
  [/^Rim .*\.?/i, '잔 가장자리에 소금을 묻혀요.'],
  [/^Muddle .*\.?/i, '재료를 가볍게 으깨요.'],
  [/^Garnish .*\.?/i, '가니시를 올려 마무리해요.'],
]

function translateIngredient(value: string) {
  return Object.entries(ingredientTranslations).reduce((result, [source, target]) => result.replace(new RegExp(source, 'gi'), target), value)
}

function translateStep(value: string) {
  const translated = stepTranslations.find(([pattern]) => pattern.test(value))
  return translated ? translated[1] : value
}

function localizeCocktail(cocktail: Cocktail): Cocktail {
  return {
    ...cocktail,
    name: names[cocktail.id] ?? cocktail.name,
    description: descriptions[cocktail.id] ?? cocktail.description,
    ingredients: cocktail.ingredients.map(translateIngredient),
    steps: cocktail.steps.map(translateStep),
  }
}

const moodFlavorTags: Record<Cocktail['mood'], string[]> = {
  Happy: ['상큼한', '스파클링'], Relaxed: ['부드러운', '따뜻한'], Romantic: ['플로럴', '우아한'],
  Party: ['활기찬', '볼드한'], Stressed: ['깊은', '차분한'], Tired: ['편안한', '달콤한'],
}

const pairingByAlcohol: Record<Alcohol, string[]> = {
  Vodka: ['가벼운 샐러드', '치즈 플래터'], Gin: ['해산물', '허브 샐러드'], Rum: ['그릴 요리', '다크 초콜릿'],
  Whiskey: ['스테이크', '숙성 치즈'], Tequila: ['타코', '매콤한 요리'], Brandy: ['디저트', '견과류'],
  Soju: ['전', '매콤한 안주'], Beer: ['치킨', '감자튀김'], Wine: ['파스타', '과일과 치즈'],
}

function getFlavorTags(cocktail: Cocktail) {
  return [...moodFlavorTags[cocktail.mood], strengthLabels[cocktail.level]]
}

function CocktailArtwork({ cocktail }: { cocktail: Cocktail }) {
  return <div className="explorer-art" style={{ background: cocktail.colors }} aria-hidden="true"><span>{cocktail.emoji}</span></div>
}

function CocktailDetail({ cocktail, onBack }: { cocktail: Cocktail; onBack: () => void }) {
  const pairings = pairingByAlcohol[cocktail.alcohol]
  return <section className="explorer-detail" aria-label={`${cocktail.name} 상세 정보`}>
    <button className="explorer-back" type="button" onClick={onBack}><ArrowLeft size={17} /> 목록으로 돌아가기</button>
    <CocktailArtwork cocktail={cocktail} />
    <div className="explorer-detail-copy">
      <div className="explorer-eyebrow">{alcoholLabels[cocktail.alcohol]} · {strengthLabels[cocktail.level]}</div>
      <h1>{cocktail.name}</h1>
      <p className="explorer-description">{cocktail.description}</p>
      <div className="explorer-tags">{getFlavorTags(cocktail).map(tag => <span key={tag}>{tag}</span>)}</div>
    </div>
    <div className="explorer-detail-grid">
      <section><h2>재료</h2><ul>{cocktail.ingredients.map(item => <li key={item}>{item}</li>)}</ul></section>
      <section><h2>만드는 법</h2><ol>{cocktail.steps.map((step, index) => <li key={step}><b>{String(index + 1).padStart(2, '0')}</b>{step}</li>)}</ol></section>
    </div>
    <section className="explorer-pairing"><h2>이런 음식과 잘 어울려요</h2><div>{pairings.map(pairing => <span key={pairing}>{pairing}</span>)}</div></section>
  </section>
}

export default function ExplorerPage() {
  const [selectedAlcohol, setSelectedAlcohol] = useState<Alcohol | 'All'>('All')
  const [selectedStrength, setSelectedStrength] = useState<Strength | 'All'>('All')
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState<Cocktail | null>(null)
  const localizedCocktails = useMemo(() => cocktails.map(localizeCocktail), [])

  const filteredCocktails = useMemo(() => localizedCocktails.filter(cocktail => {
    const matchesAlcohol = selectedAlcohol === 'All' || cocktail.alcohol === selectedAlcohol
    const matchesStrength = selectedStrength === 'All' || cocktail.level === selectedStrength
    const searchable = `${cocktail.name} ${cocktail.description} ${cocktail.ingredients.join(' ')} ${cocktail.steps.join(' ')} ${getFlavorTags(cocktail).join(' ')}`.toLowerCase()
    return matchesAlcohol && matchesStrength && searchable.includes(query.toLowerCase().trim())
  }), [localizedCocktails, query, selectedAlcohol, selectedStrength])

  if (selected) return <main className="explorer-page"><CocktailDetail cocktail={selected} onBack={() => setSelected(null)} /></main>

  return <main className="explorer-page">
    <header className="explorer-heading"><div><span className="explorer-eyebrow">THE HOUSE COLLECTION</span><h1>오늘은 어떤 한 잔을<br /><em>발견해볼까요?</em></h1></div><p>기분과 취향에 맞는 주류를 둘러보고, 마음에 드는 레시피를 찾아보세요.</p></header>
    <label className="explorer-search"><Search size={17} /><input value={query} onChange={event => setQuery(event.target.value)} placeholder="주류 이름이나 재료 검색" />{query && <button type="button" onClick={() => setQuery('')} aria-label="검색어 지우기"><X size={16} /></button>}</label>
    <div className="explorer-filters"><div><span>주종</span><div className="explorer-filter-row"><button className={selectedAlcohol === 'All' ? 'active' : ''} onClick={() => setSelectedAlcohol('All')}>전체</button>{(Object.keys(alcoholLabels) as Alcohol[]).map(alcohol => <button key={alcohol} className={selectedAlcohol === alcohol ? 'active' : ''} onClick={() => setSelectedAlcohol(alcohol)}>{alcoholLabels[alcohol]}</button>)}</div></div><div><span>도수</span><div className="explorer-filter-row"><button className={selectedStrength === 'All' ? 'active' : ''} onClick={() => setSelectedStrength('All')}>전체</button>{(Object.keys(strengthLabels) as Strength[]).map(strength => <button key={strength} className={selectedStrength === strength ? 'active' : ''} onClick={() => setSelectedStrength(strength)}>{strengthLabels[strength]}</button>)}</div></div></div>
    <div className="explorer-result-meta"><span>{filteredCocktails.length}개의 주류</span>{(selectedAlcohol !== 'All' || selectedStrength !== 'All' || query) && <button type="button" onClick={() => { setSelectedAlcohol('All'); setSelectedStrength('All'); setQuery('') }}>필터 초기화</button>}</div>
    {filteredCocktails.length ? <div className="explorer-grid">{filteredCocktails.map(cocktail => <button className="explorer-card" key={cocktail.id} type="button" onClick={() => setSelected(cocktail)}><CocktailArtwork cocktail={cocktail} /><div className="explorer-card-copy"><span>{alcoholLabels[cocktail.alcohol]} · {strengthLabels[cocktail.level]}</span><h2>{cocktail.name}</h2><p>{cocktail.description}</p><div className="explorer-card-footer"><div>{getFlavorTags(cocktail).slice(0, 2).map(tag => <i key={tag}>{tag}</i>)}</div><ChevronRight size={17} /></div></div></button>)}</div> : <div className="explorer-empty"><h2>조건에 맞는 주류가 없어요.</h2><p>필터를 조금 넓혀 다른 주류를 찾아보세요.</p></div>}
  </main>
}
