<script setup>
import PostListItem from './PostListItem.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import SkeletonBlock from '@/components/common/SkeletonBlock.vue'
import { CATEGORY_BY_SLUG } from '@/config/region'

defineProps({
  posts: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  showCategory: { type: Boolean, default: false },
  emptyTitle: { type: String, default: '아직 게시글이 없어요' },
  emptyDescription: { type: String, default: '첫 글을 남겨 이 게시판을 시작해보세요.' },
  skeletonRows: { type: Number, default: 5 },
})
</script>

<template>
  <div class="list">
    <ul v-if="loading" class="list__items">
      <li v-for="n in skeletonRows" :key="n" class="list__skeleton">
        <SkeletonBlock height="0.9rem" :width="`${50 + ((n * 13) % 35)}%`" />
        <SkeletonBlock height="0.9rem" width="2.5rem" />
      </li>
    </ul>

    <ul v-else-if="posts.length" class="list__items">
      <PostListItem
        v-for="post in posts"
        :key="post.id"
        :post="post"
        :show-category="showCategory"
        :category-label="CATEGORY_BY_SLUG[post.category]?.label ?? ''"
      />
    </ul>

    <EmptyState v-else :title="emptyTitle" :description="emptyDescription">
      <slot name="empty-action" />
    </EmptyState>
  </div>
</template>

<style scoped>
.list__items {
  display: flex;
  flex-direction: column;
}

.list__skeleton {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 0.25rem;
  border-bottom: 1px solid var(--lh-border);
}
</style>
