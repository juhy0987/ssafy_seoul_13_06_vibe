<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary', // primary | accent | ghost | danger | quiet
  },
  size: {
    type: String,
    default: 'md', // sm | md
  },
  to: { type: [String, Object], default: null },
  type: { type: String, default: 'button' },
  disabled: { type: Boolean, default: false },
  block: { type: Boolean, default: false },
})

const tag = computed(() => (props.to ? RouterLink : 'button'))
</script>

<template>
  <component
    :is="tag"
    class="btn"
    :class="[`btn--${variant}`, `btn--${size}`, { 'btn--block': block }]"
    :to="to ?? undefined"
    :type="to ? undefined : type"
    :disabled="to ? undefined : disabled"
  >
    <slot />
  </component>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  border: 1px solid transparent;
  border-radius: var(--lh-radius-s);
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.15s var(--lh-ease), border-color 0.15s var(--lh-ease),
    color 0.15s var(--lh-ease), transform 0.1s var(--lh-ease);
}

.btn:active:not(:disabled) {
  transform: translateY(1px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--sm {
  padding: 0.4rem 0.75rem;
  font-size: var(--lh-text-xs);
}

.btn--md {
  padding: 0.55rem 1rem;
  font-size: var(--lh-text-sm);
}

.btn--block {
  width: 100%;
}

.btn--primary {
  background: var(--lh-ink);
  color: var(--lh-bg);
}
.btn--primary:hover:not(:disabled) {
  background: var(--lh-ink-soft);
}

.btn--accent {
  background: var(--lh-accent);
  color: var(--lh-accent-ink);
}
.btn--accent:hover:not(:disabled) {
  background: var(--lh-accent-strong);
}

.btn--ghost {
  background: transparent;
  border-color: var(--lh-border-strong);
  color: var(--lh-ink-soft);
}
.btn--ghost:hover:not(:disabled) {
  background: var(--lh-surface-2);
  color: var(--lh-ink);
}

.btn--danger {
  background: transparent;
  border-color: var(--lh-danger-soft);
  color: var(--lh-danger);
}
.btn--danger:hover:not(:disabled) {
  background: var(--lh-danger-soft);
}

.btn--quiet {
  background: transparent;
  color: var(--lh-accent-strong);
  padding-inline: 0.25rem;
}
.btn--quiet:hover:not(:disabled) {
  color: var(--lh-accent);
}
</style>
