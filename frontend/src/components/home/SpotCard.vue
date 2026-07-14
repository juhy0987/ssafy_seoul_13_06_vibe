<script setup>
import { shortAddress } from '@/utils/format'

defineProps({
  spot: { type: Object, required: true },
  badge: { type: String, default: '' },
})
</script>

<template>
  <article class="card">
    <div class="card__media">
      <img
        v-if="spot.thumbnail"
        class="card__img"
        :src="spot.thumbnail"
        :alt="spot.title"
        loading="lazy"
      />
      <span v-if="badge" class="card__badge">{{ badge }}</span>
    </div>

    <div class="card__body">
      <h3 class="card__title">{{ spot.title }}</h3>
      <p v-if="spot.address" class="card__addr">{{ shortAddress(spot.address) }}</p>
    </div>
  </article>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  background: var(--lh-surface);
  border: 1px solid var(--lh-border);
  border-radius: var(--lh-radius-m);
  overflow: hidden;
  box-shadow: var(--lh-shadow-card);
  transition: border-color 0.15s var(--lh-ease), transform 0.15s var(--lh-ease);
}

.card:hover {
  border-color: var(--lh-border-strong);
  transform: translateY(-2px);
}

.card__media {
  position: relative;
  aspect-ratio: 4 / 3;
  background: var(--lh-surface-2);
}

.card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card:hover .card__img {
  filter: saturate(1.05);
}

.card__badge {
  position: absolute;
  top: 0.6rem;
  left: 0.6rem;
  font-size: var(--lh-text-xs);
  font-weight: 700;
  color: var(--lh-accent-ink);
  background: var(--lh-accent);
  padding: 0.15rem 0.5rem;
  border-radius: var(--lh-radius-full);
}

.card__body {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.8rem 0.9rem 0.95rem;
}

.card__title {
  font-size: var(--lh-text-sm);
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card__addr {
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}
</style>
