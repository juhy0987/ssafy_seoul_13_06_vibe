<script setup>
defineProps({
  height: { type: String, default: '1rem' },
  width: { type: String, default: '100%' },
  radius: { type: String, default: 'var(--lh-radius-s)' },
})
</script>

<template>
  <span class="skeleton" :style="{ height, width, borderRadius: radius }" aria-hidden="true" />
</template>

<style scoped>
.skeleton {
  display: block;
  background: var(--lh-surface-2);
  position: relative;
  overflow: hidden;
}

.skeleton::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent,
    color-mix(in srgb, var(--lh-surface) 70%, transparent),
    transparent
  );
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style>
