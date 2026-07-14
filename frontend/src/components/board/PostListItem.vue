<script setup>
import { formatShortDate } from '@/utils/format'

defineProps({
  post: { type: Object, required: true },
  showCategory: { type: Boolean, default: false },
  categoryLabel: { type: String, default: '' },
})
</script>

<template>
  <li class="row">
    <RouterLink
      class="row__link"
      :to="{ name: 'post-detail', params: { category: post.category, id: post.id } }"
    >
      <span v-if="showCategory" class="row__badge">{{ categoryLabel }}</span>
      <span class="row__title">{{ post.title }}</span>
      <span class="row__views lh-nums">{{ post.view_count }}</span>
      <span class="row__date lh-nums">{{ formatShortDate(post.created_at) }}</span>
    </RouterLink>
  </li>
</template>

<style scoped>
.row {
  border-bottom: 1px solid var(--lh-border);
}

.row:last-child {
  border-bottom: none;
}

.row__link {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.75rem 0.25rem;
  transition: background-color 0.12s var(--lh-ease);
}

.row__link:hover {
  background: var(--lh-surface-2);
}

.row__link:hover .row__title {
  color: var(--lh-accent-strong);
}

.row__badge {
  flex-shrink: 0;
  font-size: var(--lh-text-xs);
  font-weight: 700;
  color: var(--lh-accent-strong);
  background: var(--lh-accent-soft);
  padding: 0.1rem 0.45rem;
  border-radius: var(--lh-radius-full);
}

.row__title {
  flex: 1;
  min-width: 0;
  font-size: var(--lh-text-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color 0.12s var(--lh-ease);
}

.row__views,
.row__date {
  flex-shrink: 0;
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}

.row__views::before {
  content: '조회 ';
  font-family: var(--lh-font-sans);
}

@media (max-width: 640px) {
  .row__views {
    display: none;
  }
}
</style>
