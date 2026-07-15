<script setup>
import { computed, onMounted, ref } from 'vue'
import HeroBanner from '@/components/home/HeroBanner.vue'
import SeoulMap from '@/components/home/SeoulMap.vue'
import SpotGrid from '@/components/home/SpotGrid.vue'
import PostList from '@/components/board/PostList.vue'
import SectionHeading from '@/components/common/SectionHeading.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { listSpots, getSpotsSummary } from '@/api/tourism'
import { listRecentPosts } from '@/api/posts'
import { CATEGORIES } from '@/config/region'

const attractions = ref([])
const posts = ref([])

// 히어로 배너에 표시할 전체 장소 수(모든 카테고리 합계)
const totalSpots = ref(0)

const loadingSpots = ref(true)
const loadingPosts = ref(true)
const spotsError = ref('')

// 관광지 카드 좌/우 페이지네이션 (백엔드 /api/spots 의 page·size 사용)
const SPOTS_PAGE_SIZE = 4
const spotsPage = ref(1)
const spotsTotal = ref(0)
const totalSpotPages = computed(() =>
  Math.max(1, Math.ceil(spotsTotal.value / SPOTS_PAGE_SIZE)),
)
const hasPrevSpots = computed(() => spotsPage.value > 1)
const hasNextSpots = computed(() => spotsPage.value < totalSpotPages.value)

async function loadSpots(page = 1) {
  loadingSpots.value = true
  spotsError.value = ''
  try {
    const response = await listSpots('attractions', { limit: SPOTS_PAGE_SIZE, page })
    attractions.value = response.items
    spotsTotal.value = response.total
    spotsPage.value = page
  } catch (err) {
    spotsError.value = `${err.message} — 백엔드 /api/spots 연결을 확인해주세요.`
  } finally {
    loadingSpots.value = false
  }
}

function prevSpots() {
  if (hasPrevSpots.value && !loadingSpots.value) loadSpots(spotsPage.value - 1)
}

function nextSpots() {
  if (hasNextSpots.value && !loadingSpots.value) loadSpots(spotsPage.value + 1)
}

async function loadSummary() {
  try {
    const summary = await getSpotsSummary()
    totalSpots.value = summary.total
  } catch (err) {
    console.error('전체 장소 수 조회 실패:', err)
  }
}

async function loadPosts() {
  posts.value = await listRecentPosts(5)
  loadingPosts.value = false
}

onMounted(() => {
  loadSpots()
  loadSummary()
  loadPosts()
})
</script>

<template>
  <div class="lh-container home">
    <HeroBanner :spot-count="totalSpots" />

    <section class="home__section">
      <SectionHeading
        eyebrow="Map"
        title="지도로 보기"
        description="카테고리를 선택하면 해당 장소들이 지도에 표시됩니다"
      />

      <SeoulMap />
    </section>

    <section class="home__section">
      <SectionHeading
        eyebrow="Attractions"
        title="서울의 관광지"
        description="한국관광공사 TourAPI 기준 대표 명소"
      >
        <template #action>
          <BaseButton variant="quiet" size="sm" :to="{ name: 'board', params: { category: 'attraction' } }">
            게시판 보기 ›
          </BaseButton>
        </template>
      </SectionHeading>

      <div class="spots-carousel">
        <button
          class="spots-carousel__nav"
          type="button"
          aria-label="이전 관광지"
          :disabled="!hasPrevSpots || loadingSpots"
          @click="prevSpots"
        >
          ‹
        </button>

        <div class="spots-carousel__body">
          <SpotGrid :spots="attractions" :loading="loadingSpots" :error="spotsError" />
        </div>

        <button
          class="spots-carousel__nav"
          type="button"
          aria-label="다음 관광지"
          :disabled="!hasNextSpots || loadingSpots"
          @click="nextSpots"
        >
          ›
        </button>
      </div>

      <p v-if="!spotsError" class="spots-carousel__page lh-nums">
        {{ spotsPage }} / {{ totalSpotPages }}
      </p>
    </section>

    <section class="home__section">
      <SectionHeading title="최근 게시글" description="이웃과 관광객이 남긴 최신 이야기">
        <template #action>
          <BaseButton
            variant="accent"
            size="sm"
            :to="{ name: 'post-create', params: { category: CATEGORIES[0].slug } }"
          >
            + 글쓰기
          </BaseButton>
        </template>
      </SectionHeading>

      <div class="home__posts">
        <PostList :posts="posts" :loading="loadingPosts" show-category />
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: var(--lh-gap-7);
}

.home__section {
  display: flex;
  flex-direction: column;
  gap: var(--lh-gap-4);
}

.home__posts {
  background: var(--lh-surface);
  border: 1px solid var(--lh-border);
  border-radius: var(--lh-radius-m);
  padding: 0.25rem 1rem;
  box-shadow: var(--lh-shadow-card);
}

.spots-carousel {
  display: flex;
  align-items: stretch;
  gap: 0.75rem;
}

.spots-carousel__body {
  flex: 1;
  min-width: 0;
}

.spots-carousel__nav {
  flex-shrink: 0;
  width: 2.75rem;
  display: grid;
  place-items: center;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-m);
  background: var(--lh-surface);
  color: var(--lh-ink);
  font-size: 1.5rem;
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
