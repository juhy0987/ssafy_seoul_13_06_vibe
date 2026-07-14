<script setup>
import SpotCard from './SpotCard.vue'
import SkeletonBlock from '@/components/common/SkeletonBlock.vue'
import EmptyState from '@/components/common/EmptyState.vue'

defineProps({
  spots: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  badge: { type: String, default: '' },
  skeletonCount: { type: Number, default: 4 },
})
</script>

<template>
  <div v-if="loading" class="grid">
    <div v-for="n in skeletonCount" :key="n" class="grid__skeleton">
      <SkeletonBlock height="0" width="100%" radius="var(--lh-radius-m)" />
      <SkeletonBlock height="0.85rem" width="70%" />
      <SkeletonBlock height="0.7rem" width="45%" />
    </div>
  </div>

  <EmptyState
    v-else-if="error"
    icon="⚠"
    title="데이터를 불러오지 못했습니다"
    :description="error"
  />

  <div v-else class="grid">
    <SpotCard v-for="spot in spots" :key="spot.id" :spot="spot" :badge="badge" />
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.grid__skeleton {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* 카드 이미지 자리(4:3)를 스켈레톤에서도 그대로 확보한다. */
.grid__skeleton > :first-child {
  aspect-ratio: 4 / 3;
  height: auto;
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
