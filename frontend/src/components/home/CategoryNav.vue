<script setup>
import { CATEGORIES } from '@/config/region'
</script>

<template>
  <nav class="cats" aria-label="카테고리 바로가기">
    <RouterLink
      v-for="category in CATEGORIES"
      :key="category.slug"
      class="cat"
      :to="{ name: 'board', params: { category: category.slug } }"
    >
      <span class="cat__icon" aria-hidden="true">{{ category.icon }}</span>
      <span class="cat__label">{{ category.label }}</span>
      <span class="cat__desc">{{ category.description }}</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.cats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
  gap: 0.75rem;
}

.cat {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 1.1rem 1.1rem 1rem;
  background: var(--lh-surface);
  border: 1px solid var(--lh-border);
  border-radius: var(--lh-radius-m);
  box-shadow: var(--lh-shadow-card);
  transition: border-color 0.15s var(--lh-ease), transform 0.15s var(--lh-ease);
}

.cat:hover {
  border-color: var(--lh-accent);
  transform: translateY(-2px);
}

.cat__icon {
  font-size: 1.25rem;
  line-height: 1.4;
}

.cat__label {
  font-weight: 700;
  font-size: var(--lh-text-base);
}

.cat__desc {
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}

@media (max-width: 640px) {
  .cats {
    grid-template-columns: 1fr;
  }

  .cat {
    flex-direction: row;
    align-items: center;
    gap: 0.7rem;
    padding: 0.85rem 1rem;
  }

  .cat__desc {
    display: none;
  }
}
</style>
