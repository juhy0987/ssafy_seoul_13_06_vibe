<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, required: true },
})

const emit = defineEmits(['close'])
const panel = ref(null)

function onKeydown(e) {
  if (e.key === 'Escape' && props.open) emit('close')
}

watch(
  () => props.open,
  (isOpen) => {
    document.body.style.overflow = isOpen ? 'hidden' : ''
    if (isOpen) {
      // 열리는 순간 첫 입력 요소로 포커스를 옮긴다.
      requestAnimationFrame(() => {
        panel.value?.querySelector('input, button, [tabindex]')?.focus()
      })
    }
  },
)

onMounted(() => document.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="open" class="overlay" @click.self="emit('close')">
        <div ref="panel" class="panel" role="dialog" aria-modal="true" :aria-label="title">
          <header class="panel__head">
            <h2 class="panel__title">{{ title }}</h2>
            <button class="panel__close" type="button" aria-label="닫기" @click="emit('close')">
              ✕
            </button>
          </header>
          <div class="panel__body">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  background: rgba(20, 22, 27, 0.45);
  backdrop-filter: blur(2px);
}

.panel {
  width: 100%;
  max-width: 22rem;
  background: var(--lh-surface);
  border: 1px solid var(--lh-border);
  border-radius: var(--lh-radius-m);
  box-shadow: var(--lh-shadow-modal);
  overflow: hidden;
}

.panel__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--lh-border);
}

.panel__title {
  font-size: var(--lh-text-base);
}

.panel__close {
  border: none;
  background: transparent;
  color: var(--lh-ink-faint);
  font-size: var(--lh-text-sm);
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
}
.panel__close:hover {
  color: var(--lh-ink);
}

.panel__body {
  padding: 1.25rem;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.18s var(--lh-ease);
}
.modal-enter-active .panel,
.modal-leave-active .panel {
  transition: transform 0.18s var(--lh-ease);
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .panel,
.modal-leave-to .panel {
  transform: translateY(8px) scale(0.98);
}
</style>
