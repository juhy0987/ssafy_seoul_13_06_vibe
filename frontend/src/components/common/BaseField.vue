<script setup>
import { useId } from 'vue'

defineProps({
  label: { type: String, required: true },
  hint: { type: String, default: '' },
  error: { type: String, default: '' },
  required: { type: Boolean, default: false },
})

const id = useId()
</script>

<template>
  <div class="field">
    <label class="field__label" :for="id">
      {{ label }}
      <span v-if="required" class="field__req" aria-hidden="true">*</span>
    </label>

    <!-- 자식 입력 요소가 label 과 연결되도록 id 를 슬롯으로 넘긴다 -->
    <slot :id="id" :invalid="Boolean(error)" />

    <p v-if="error" class="field__msg field__msg--error" role="alert">{{ error }}</p>
    <p v-else-if="hint" class="field__msg">{{ hint }}</p>
  </div>
</template>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.field__label {
  font-size: var(--lh-text-xs);
  font-weight: 700;
  color: var(--lh-ink-soft);
}

.field__req {
  color: var(--lh-accent);
  margin-left: 0.15rem;
}

.field__msg {
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}

.field__msg--error {
  color: var(--lh-danger);
  font-weight: 600;
}
</style>
