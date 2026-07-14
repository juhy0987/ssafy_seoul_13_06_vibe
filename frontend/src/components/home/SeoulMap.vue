<script setup>
import { onBeforeUnmount, onMounted, useTemplateRef } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// 서울 시청 좌표를 중심으로 권역 전체가 보이도록 확대한다.
const SEOUL_CENTER = [37.5665, 126.978]
const SEOUL_ZOOM = 11

const mapEl = useTemplateRef('mapEl')
let map = null

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
})

onBeforeUnmount(() => {
  map?.remove()
  map = null
})
</script>

<template>
  <div class="map-card">
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
</style>
