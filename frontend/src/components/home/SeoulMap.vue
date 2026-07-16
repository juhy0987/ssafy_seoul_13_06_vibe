<script setup>
import { onBeforeUnmount, onMounted, ref, useTemplateRef } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { CATEGORIES } from '@/config/region'
import { randomSpotsForCategory } from '@/api/tourism'

const router = useRouter()

// 서울 시청 좌표를 중심으로 권역 전체가 보이도록 확대한다.
const SEOUL_CENTER = [37.5665, 126.978]
const SEOUL_ZOOM = 11

// 번들러 환경에서 Leaflet 기본 마커 이미지 경로가 깨지므로 CSS 핀(divIcon)을 쓴다.
const pinIcon = L.divIcon({
  className: 'seoul-map-pin',
  html:
    '<span style="display:block;width:14px;height:14px;border-radius:50% 50% 50% 0;' +
    'transform:rotate(-45deg);background:#e5484d;border:2px solid #fff;' +
    'box-shadow:0 1px 4px rgba(0,0,0,.45)"></span>',
  iconSize: [18, 18],
  iconAnchor: [9, 16],
  popupAnchor: [0, -14],
})

const mapEl = useTemplateRef('mapEl')
const activeSlug = ref(CATEGORIES[0].slug)
const count = ref(0)
const loading = ref(false)
const error = ref('')

let map = null
let markerLayer = null

function escapeHtml(value) {
  return String(value ?? '').replace(
    /[&<>"']/g,
    (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch],
  )
}

// 마커 팝업(풍선) DOM 구성 — 네이버 지도 / 게시판 이동 버튼 포함.
// Leaflet 팝업은 HTML 문자열이라 라우터 이동이 안 되므로, DOM 요소에 직접 리스너를 단다.
function buildPopupContent(spot) {
  const category = activeSlug.value // 현재 선택된 카테고리(마커 출처)를 캡처
  const el = document.createElement('div')
  el.className = 'spot-popup'
  el.innerHTML =
    `<strong class="spot-popup__title">${escapeHtml(spot.title)}</strong>` +
    (spot.address ? `<div class="spot-popup__addr">${escapeHtml(spot.address)}</div>` : '')

  const actions = document.createElement('div')
  actions.className = 'spot-popup__actions'

  const mapBtn = document.createElement('button')
  mapBtn.type = 'button'
  mapBtn.className = 'spot-popup__btn'
  mapBtn.innerHTML = '<span aria-hidden="true">🗺️</span> 지도'
  mapBtn.setAttribute('aria-label', `${spot.title} 네이버 지도에서 보기`)
  mapBtn.addEventListener('click', () => {
    window.open(
      `https://map.naver.com/p/search/${encodeURIComponent(spot.title ?? '')}`,
      '_blank',
      'noopener',
    )
  })

  const boardBtn = document.createElement('button')
  boardBtn.type = 'button'
  boardBtn.className = 'spot-popup__btn'
  boardBtn.innerHTML = '<span aria-hidden="true">📝</span> 게시판'
  boardBtn.setAttribute('aria-label', '이 카테고리 게시판으로 이동')
  boardBtn.addEventListener('click', () => {
    router.push({ name: 'board', params: { category } })
  })

  actions.append(mapBtn, boardBtn)
  el.append(actions)
  return el
}

function renderMarkers(spots) {
  if (!map || !markerLayer) return
  markerLayer.clearLayers()

  const located = spots.filter((s) => s.lat != null && s.lng != null)
  for (const spot of located) {
    L.marker([spot.lat, spot.lng], { icon: pinIcon })
      .bindPopup(buildPopupContent(spot))
      .addTo(markerLayer)
  }

  count.value = located.length
  if (located.length) {
    map.fitBounds(
      L.latLngBounds(located.map((s) => [s.lat, s.lng])),
      { padding: [32, 32], maxZoom: 15 },
    )
  } else {
    map.setView(SEOUL_CENTER, SEOUL_ZOOM)
  }
}

async function selectCategory(slug) {
  activeSlug.value = slug
  loading.value = true
  error.value = ''
  try {
    const res = await randomSpotsForCategory(slug, { size: 50 })
    renderMarkers(res.items ?? [])
  } catch (err) {
    console.error('장소 조회 실패:', err)
    error.value = '장소를 불러오지 못했습니다. 백엔드 /api/spots 연결을 확인해주세요.'
    renderMarkers([])
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  map = L.map(mapEl.value, {
    center: SEOUL_CENTER,
    zoom: SEOUL_ZOOM,
    scrollWheelZoom: false,
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)

  markerLayer = L.layerGroup().addTo(map)
  selectCategory(activeSlug.value)
})

onBeforeUnmount(() => {
  map?.remove()
  map = null
  markerLayer = null
})
</script>

<template>
  <div class="map-card">
    <div class="map-card__toolbar" role="tablist" aria-label="관광 카테고리">
      <button
        v-for="category in CATEGORIES"
        :key="category.slug"
        type="button"
        role="tab"
        class="chip"
        :class="{ 'chip--active': category.slug === activeSlug }"
        :aria-selected="category.slug === activeSlug"
        :disabled="loading"
        @click="selectCategory(category.slug)"
      >
        <span aria-hidden="true">{{ category.icon }}</span>
        {{ category.label }}
      </button>
    </div>

    <div class="map-card__status" aria-live="polite">
      <span v-if="loading">불러오는 중…</span>
      <span v-else-if="error" class="map-card__error">{{ error }}</span>
      <span v-else>지도에 표시된 장소 {{ count }}곳</span>
    </div>

    <div ref="mapEl" class="map-card__canvas" aria-label="서울 지역 지도" />
  </div>
</template>

<style scoped>
.map-card {
  background: var(--lh-surface);
  border: 1px solid var(--lh-border);
  border-radius: var(--lh-radius-m);
  box-shadow: var(--lh-shadow-card);
  overflow: hidden;
  /* Leaflet 내부의 높은 z-index(줌 컨트롤·팝업 등 ~1000)를 이 카드 안에 가둔다.
     그렇지 않으면 루트 쌓임 맥락으로 새어나와 챗봇 위젯(z-index 80)을 덮는다. */
  isolation: isolate;
}

.map-card__toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding: 0.85rem 0.85rem 0.6rem;
  border-bottom: 1px solid var(--lh-border);
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-full);
  background: var(--lh-surface);
  color: var(--lh-ink);
  font-family: inherit;
  font-size: var(--lh-text-sm);
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s var(--lh-ease), background-color 0.15s var(--lh-ease),
    color 0.15s var(--lh-ease);
}

.chip:hover:not(:disabled) {
  border-color: var(--lh-accent);
}

.chip--active {
  background: var(--lh-accent);
  border-color: var(--lh-accent);
  color: var(--lh-accent-ink);
}

.chip:disabled {
  opacity: 0.6;
  cursor: progress;
}

.map-card__status {
  padding: 0.5rem 0.9rem;
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}

.map-card__error {
  color: var(--lh-danger);
}

.map-card__canvas {
  width: 100%;
  height: 22rem;
}

@media (max-width: 640px) {
  .map-card__canvas {
    height: 16rem;
  }
}

/* 마커 팝업(풍선) — Leaflet이 동적 생성하는 DOM이라 :deep 로 도달한다 */
:deep(.spot-popup__title) {
  font-size: 13px;
  font-weight: 700;
}

:deep(.spot-popup__addr) {
  margin-top: 2px;
  color: var(--lh-ink-faint);
  font-size: 12px;
}

:deep(.spot-popup__actions) {
  display: flex;
  gap: 6px;
  margin-top: 8px;
}

:deep(.spot-popup__btn) {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-full);
  background: var(--lh-surface);
  color: var(--lh-ink);
  font: inherit;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

:deep(.spot-popup__btn:hover) {
  border-color: var(--lh-accent);
  color: var(--lh-accent);
}
</style>
