<script setup>
defineProps({
  eyebrow: { type: String, default: '' },
  title: { type: String, required: true },
  description: { type: String, default: '' },
})
</script>

<template>
  <div class="heading">
    <div class="heading__text">
      <span v-if="eyebrow" class="lh-eyebrow">{{ eyebrow }}</span>
      <h2 class="heading__title">{{ title }}</h2>
      <p v-if="description" class="heading__desc">{{ description }}</p>
    </div>
    <div v-if="$slots.action" class="heading__action">
      <slot name="action" />
    </div>
  </div>
</template>

<style scoped>
.heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.heading__text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.heading__title {
  font-size: var(--lh-text-xl);
}

.heading__desc {
  font-size: var(--lh-text-sm);
  color: var(--lh-ink-soft);
}
</style>
