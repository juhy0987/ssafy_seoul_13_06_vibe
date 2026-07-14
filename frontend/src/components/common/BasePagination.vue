<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: { type: Number, required: true },
  total: { type: Number, required: true },
  size: { type: Number, default: 10 },
  window: { type: Number, default: 5 },
})

const emit = defineEmits(['change'])

const lastPage = computed(() => Math.max(1, Math.ceil(props.total / props.size)))

const pages = computed(() => {
  const half = Math.floor(props.window / 2)
  let start = Math.max(1, props.page - half)
  const end = Math.min(lastPage.value, start + props.window - 1)
  start = Math.max(1, end - props.window + 1)
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

function go(next) {
  if (next < 1 || next > lastPage.value || next === props.page) return
  emit('change', next)
}
</script>

<template>
  <nav v-if="lastPage > 1" class="pagination lh-nums" aria-label="페이지 이동">
    <button
      class="pagination__btn"
      type="button"
      :disabled="page === 1"
      aria-label="이전 페이지"
      @click="go(page - 1)"
    >
      ‹
    </button>

    <button
      v-for="n in pages"
      :key="n"
      class="pagination__btn"
      :class="{ 'is-current': n === page }"
      type="button"
      :aria-current="n === page ? 'page' : undefined"
      @click="go(n)"
    >
      {{ n }}
    </button>

    <button
      class="pagination__btn"
      type="button"
      :disabled="page === lastPage"
      aria-label="다음 페이지"
      @click="go(page + 1)"
    >
      ›
    </button>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.3rem;
}

.pagination__btn {
  min-width: 2rem;
  height: 2rem;
  padding: 0 0.4rem;
  border: none;
  border-radius: var(--lh-radius-full);
  background: transparent;
  color: var(--lh-ink-soft);
  font-size: var(--lh-text-xs);
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s var(--lh-ease), color 0.15s var(--lh-ease);
}

.pagination__btn:hover:not(:disabled):not(.is-current) {
  background: var(--lh-surface-2);
  color: var(--lh-ink);
}

.pagination__btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.pagination__btn.is-current {
  background: var(--lh-ink);
  color: var(--lh-bg);
  font-weight: 700;
}
</style>
