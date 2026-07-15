<script setup>
import { onMounted, ref } from 'vue'
import HeroBanner from '@/components/home/HeroBanner.vue'
import SeoulMap from '@/components/home/SeoulMap.vue'
import SpotGrid from '@/components/home/SpotGrid.vue'
import PostList from '@/components/board/PostList.vue'
import SectionHeading from '@/components/common/SectionHeading.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { listSpots } from '@/api/tourism'
import { listRecentPosts } from '@/api/posts'
import { CATEGORIES } from '@/config/region'

const attractions = ref([])
const posts = ref([])

const counts = ref({ attractions: 0 })

const loadingSpots = ref(true)
const loadingPosts = ref(true)
const spotsError = ref('')

async function loadSpots() {
  try {
    const response = await listSpots('attractions', { limit: 4 })
    attractions.value = response.items
    counts.value.attractions = response.total
  } catch (err) {
    spotsError.value = `${err.message} — 백엔드 /api/spots 연결을 확인해주세요.`
  } finally {
    loadingSpots.value = false
  }
}

async function loadPosts() {
  posts.value = await listRecentPosts(5)
  loadingPosts.value = false
}

onMounted(() => {
  loadSpots()
  loadPosts()
})
</script>

<template>
  <div class="lh-container home">
    <HeroBanner :spot-count="counts.attractions" />

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

      <SpotGrid :spots="attractions" :loading="loadingSpots" :error="spotsError" />
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
</style>
