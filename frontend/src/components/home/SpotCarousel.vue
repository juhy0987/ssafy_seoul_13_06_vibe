<script setup>
import { computed, onMounted, ref } from 'vue'
import SpotGrid from './SpotGrid.vue'
import { listSpots } from '@/api/tourism'
import { toApiCategory } from '@/config/region'

// 카테고리 slug 하나에 대한 "사진 포함 관광 카드" 캐러셀(좌/우 페이지네이션).
// 백엔드 /api/spots 의 page·size 를 그대로 사용한다.
const props = defineProps({
  slug: { type: String, required: true },
})

const PAGE_SIZE = 4

const spots = ref([])
const page = ref(1)
const total = ref(0)
const loading = ref(true)
const error = ref('')

// 백엔드 영문 dataset alias 는 일부만 지원 → 모든 카테고리에서 동작하도록 한글 카테고리명 사용
const dataset = computed(() => toApiCategory(props.slug))
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))
const hasPrev = computed(() => page.value > 1)
const hasNext = computed(() => page.value < totalPages.value)

async function load(target = 1) {
  loading.value = true
  error.value = ''
  try {
    // 기본 with_image_only=true → 사진 있는 장소만
    const res = await listSpots(dataset.value, { limit: PAGE_SIZE, page: target })
    spots.value = res.items
    total.value = res.total
    page.value = target
  } catch (err) {
    error.value = `${err.message} — 백엔드 /api/spots 연결을 확인해주세요.`
  } finally {
    loading.value = false
  }
}

function prev() {
  if (hasPrev.value && !loading.value) load(page.value - 1)
}

function next() {
  if (hasNext.value && !loading.value) load(page.value + 1)
}

onMounted(() => load(1))
</script>

<template>
  <div>
    <div class="spots-carousel">
      <button
        class="spots-carousel__nav"
        type="button"
        aria-label="이전"
        :disabled="!hasPrev || loading"
        @click="prev"
      >
        ‹
      </button>

      <div class="spots-carousel__body">
        <SpotGrid :spots="spots" :loading="loading" :error="error" />
      </div>

      <button
        class="spots-carousel__nav"
        type="button"
        aria-label="다음"
        :disabled="!hasNext || loading"
        @click="next"
      >
        ›
      </button>
    </div>

    <p v-if="!error" class="spots-carousel__page lh-nums">{{ page }} / {{ totalPages }}</p>
  </div>
</template>

<style scoped>
.spots-carousel {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spots-carousel__body {
  flex: 1;
  min-width: 0;
}

.spots-carousel__nav {
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  display: grid;
  place-items: center;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-full);
  background: var(--lh-surface);
  color: var(--lh-ink);
  font-size: 1.1rem;
  line-height: 1;
  cursor: pointer;
  box-shadow: var(--lh-shadow-card);
  transition: border-color 0.15s var(--lh-ease), background-color 0.15s var(--lh-ease),
    transform 0.15s var(--lh-ease);
}

.spots-carousel__nav:hover:not(:disabled) {
  border-color: var(--lh-accent);
  transform: translateY(-1px);
}

.spots-carousel__nav:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.spots-carousel__page {
  margin-top: 0.6rem;
  text-align: center;
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}

@media (max-width: 640px) {
  .spots-carousel {
    gap: 0.4rem;
  }

  .spots-carousel__nav {
    width: 2.25rem;
    font-size: 1.25rem;
  }
}
</style>
