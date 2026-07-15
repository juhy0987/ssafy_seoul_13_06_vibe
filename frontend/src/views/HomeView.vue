<script setup>
import { onMounted, ref } from 'vue'
import HeroBanner from '@/components/home/HeroBanner.vue'
import SeoulMap from '@/components/home/SeoulMap.vue'
import SpotCarousel from '@/components/home/SpotCarousel.vue'
import PostList from '@/components/board/PostList.vue'
import SectionHeading from '@/components/common/SectionHeading.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { getSpotsSummary } from '@/api/tourism'
import { listRecentPosts } from '@/api/posts'
import { CATEGORIES } from '@/config/region'

const posts = ref([])

// 히어로 배너에 표시할 전체 장소 수(모든 카테고리 합계)
const totalSpots = ref(0)

const loadingPosts = ref(true)

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

    <!-- 카테고리별 관광 카드 캐러셀 (관광지·레포츠·문화시설·쇼핑·숙박·여행코스·축제행사) -->
    <section v-for="category in CATEGORIES" :key="category.slug" class="home__section">
      <SectionHeading :title="`서울의 ${category.label}`" :description="category.description">
        <template #action>
          <BaseButton
            variant="quiet"
            size="sm"
            :to="{ name: 'board', params: { category: category.slug } }"
          >
            게시판 보기 ›
          </BaseButton>
        </template>
      </SectionHeading>

      <SpotCarousel :slug="category.slug" />
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
