<script setup>
defineProps({
  as: { type: String, default: 'input' }, // input | textarea
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  invalid: { type: Boolean, default: false },
  rows: { type: Number, default: 8 },
})

const model = defineModel({ type: String, default: '' })
</script>

<template>
  <component
    :is="as"
    :value="model"
    @input="model = $event.target.value"
    class="input"
    :class="{ 'input--invalid': invalid, 'input--area': as === 'textarea' }"
    :type="as === 'input' ? type : undefined"
    :rows="as === 'textarea' ? rows : undefined"
    :placeholder="placeholder"
    :aria-invalid="invalid || undefined"
  />
</template>

<style scoped>
.input {
  width: 100%;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-s);
  background: var(--lh-surface);
  color: var(--lh-ink);
  font-family: var(--lh-font-sans);
  font-size: var(--lh-text-sm);
  line-height: 1.6;
  padding: 0.6rem 0.75rem;
  transition: border-color 0.15s var(--lh-ease), box-shadow 0.15s var(--lh-ease);
}

.input::placeholder {
  color: var(--lh-ink-faint);
}

.input:focus {
  outline: none;
  border-color: var(--lh-accent);
  box-shadow: 0 0 0 3px var(--lh-accent-soft);
}

.input--area {
  resize: vertical;
  min-height: 8rem;
}

.input--invalid {
  border-color: var(--lh-danger);
}
.input--invalid:focus {
  box-shadow: 0 0 0 3px var(--lh-danger-soft);
}
</style>
