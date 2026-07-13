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

  const filteredCocktails = useMemo(() => cocktails.filter(cocktail => {
    const matchesAlcohol = selectedAlcohol === 'All' || cocktail.alcohol === selectedAlcohol
    const matchesStrength = selectedStrength === 'All' || cocktail.level === selectedStrength
    const searchable = `${cocktail.name} ${cocktail.description} ${cocktail.ingredients.join(' ')}`.toLowerCase()
    return matchesAlcohol && matchesStrength && searchable.includes(query.toLowerCase().trim())
  }), [query, selectedAlcohol, selectedStrength])

  if (selected) return <main className="explorer-page"><CocktailDetail cocktail={selected} onBack={() => setSelected(null)} /></main>

  return <main className="explorer-page">
    <header className="explorer-heading"><div><span className="explorer-eyebrow">THE HOUSE COLLECTION</span><h1>오늘은 어떤 한 잔을<br /><em>발견해볼까요?</em></h1></div><p>기분과 취향에 맞는 주류를 둘러보고, 마음에 드는 레시피를 찾아보세요.</p></header>
    <label className="explorer-search"><Search size={17} /><input value={query} onChange={event => setQuery(event.target.value)} placeholder="주류 이름이나 재료 검색" />{query && <button type="button" onClick={() => setQuery('')} aria-label="검색어 지우기"><X size={16} /></button>}</label>
    <div className="explorer-filters"><div><span>주종</span><div className="explorer-filter-row"><button className={selectedAlcohol === 'All' ? 'active' : ''} onClick={() => setSelectedAlcohol('All')}>전체</button>{(Object.keys(alcoholLabels) as Alcohol[]).map(alcohol => <button key={alcohol} className={selectedAlcohol === alcohol ? 'active' : ''} onClick={() => setSelectedAlcohol(alcohol)}>{alcoholLabels[alcohol]}</button>)}</div></div><div><span>도수</span><div className="explorer-filter-row"><button className={selectedStrength === 'All' ? 'active' : ''} onClick={() => setSelectedStrength('All')}>전체</button>{(Object.keys(strengthLabels) as Strength[]).map(strength => <button key={strength} className={selectedStrength === strength ? 'active' : ''} onClick={() => setSelectedStrength(strength)}>{strengthLabels[strength]}</button>)}</div></div></div>
    <div className="explorer-result-meta"><span>{filteredCocktails.length}개의 주류</span>{(selectedAlcohol !== 'All' || selectedStrength !== 'All' || query) && <button type="button" onClick={() => { setSelectedAlcohol('All'); setSelectedStrength('All'); setQuery('') }}>필터 초기화</button>}</div>
    {filteredCocktails.length ? <div className="explorer-grid">{filteredCocktails.map(cocktail => <button className="explorer-card" key={cocktail.id} type="button" onClick={() => setSelected(cocktail)}><CocktailArtwork cocktail={cocktail} /><div className="explorer-card-copy"><span>{alcoholLabels[cocktail.alcohol]} · {strengthLabels[cocktail.level]}</span><h2>{cocktail.name}</h2><p>{cocktail.description}</p><div className="explorer-card-footer"><div>{getFlavorTags(cocktail).slice(0, 2).map(tag => <i key={tag}>{tag}</i>)}</div><ChevronRight size={17} /></div></div></button>)}</div> : <div className="explorer-empty"><h2>조건에 맞는 주류가 없어요.</h2><p>필터를 조금 넓혀 다른 주류를 찾아보세요.</p></div>}
  </main>
}
