<script setup>
defineProps({
  icon: { type: String, default: '🗂' },
  title: { type: String, required: true },
  description: { type: String, default: '' },
})
</script>

<template>
  <div class="empty">
    <span class="empty__icon" aria-hidden="true">{{ icon }}</span>
    <p class="empty__title">{{ title }}</p>
    <p v-if="description" class="empty__desc">{{ description }}</p>
    <div v-if="$slots.default" class="empty__action">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  padding: 3rem 1.5rem;
  text-align: center;
  border: 1px dashed var(--lh-border-strong);
  border-radius: var(--lh-radius-m);
  background: var(--lh-surface);
}

.empty__icon {
  font-size: 1.6rem;
  margin-bottom: 0.2rem;
}

.empty__title {
  font-weight: 700;
  font-size: var(--lh-text-base);
}

.empty__desc {
  font-size: var(--lh-text-sm);
  color: var(--lh-ink-soft);
  max-width: 42ch;
}

.empty__action {
  margin-top: 0.6rem;
}
</style>
