<script setup>
import { nextTick, ref, useTemplateRef } from 'vue'
import { sendChatMessage } from '@/api/chat'

const SUGGESTIONS = ['이번 주 서울 축제 알려줘', '경복궁 근처 가볼 만한 곳', '비 오는 날 실내 명소']

const open = ref(false)
const pending = ref(false)
const draft = ref('')
const messages = ref([
  { role: 'assistant', text: '안녕하세요! 서울 지역 정보를 물어보세요 🙂' },
])

const threadEl = useTemplateRef('thread')
const inputEl = useTemplateRef('input')

async function scrollToBottom() {
  await nextTick()
  if (threadEl.value) threadEl.value.scrollTop = threadEl.value.scrollHeight
}

async function toggle() {
  open.value = !open.value
  if (open.value) {
    await scrollToBottom()
    inputEl.value?.focus()
  }
}

async function send(text = draft.value) {
  const message = text.trim()
  if (!message || pending.value) return

  messages.value.push({ role: 'user', text: message })
  draft.value = ''
  pending.value = true
  await scrollToBottom()

  // 백엔드에는 직전 대화 히스토리를 함께 넘겨 맥락을 유지한다.
  const history = messages.value.slice(-9, -1).map((m) => ({ role: m.role, content: m.text }))

  try {
    const reply = await sendChatMessage(message, history)
    messages.value.push({ role: 'assistant', text: reply })
  } finally {
    pending.value = false
    await scrollToBottom()
  }
}
</script>

<template>
  <div class="chat">
    <Transition name="panel">
      <section v-if="open" class="panel" aria-label="LocalHub 챗봇">
        <header class="panel__head">
          <span class="panel__brand">
            <span class="panel__dot" aria-hidden="true" />
            LocalHub 챗봇
          </span>
          <button class="panel__close" type="button" aria-label="챗봇 닫기" @click="toggle">
            ✕
          </button>
        </header>

        <div ref="thread" class="thread" role="log" aria-live="polite">
          <p
            v-for="(msg, i) in messages"
            :key="i"
            class="bubble"
            :class="`bubble--${msg.role}`"
          >
            {{ msg.text }}
          </p>

          <p v-if="pending" class="bubble bubble--assistant bubble--typing">
            <span /><span /><span />
          </p>
        </div>

        <div v-if="messages.length === 1" class="chips">
          <button
            v-for="s in SUGGESTIONS"
            :key="s"
            class="chip"
            type="button"
            @click="send(s)"
          >
            {{ s }}
          </button>
        </div>

        <form class="composer" @submit.prevent="send()">
          <input
            ref="input"
            v-model="draft"
            class="composer__input"
            type="text"
            placeholder="메시지를 입력하세요"
            aria-label="챗봇에게 보낼 메시지"
            :disabled="pending"
          />
          <button
            class="composer__send"
            type="submit"
            aria-label="전송"
            :disabled="pending || !draft.trim()"
          >
            ➤
          </button>
        </form>
      </section>
    </Transition>

    <button
      v-show="!open"
      class="fab"
      type="button"
      aria-label="챗봇 열기"
      @click="toggle"
    >
      💬
    </button>
  </div>
</template>

<style scoped>
.chat {
  position: fixed;
  right: 1.5rem;
  bottom: 1.5rem;
  z-index: 80;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.75rem;
}

.fab {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border: none;
  border-radius: var(--lh-radius-full);
  background: var(--lh-ink);
  color: var(--lh-bg);
  font-size: 1.25rem;
  cursor: pointer;
  box-shadow: var(--lh-shadow-float);
  transition: transform 0.15s var(--lh-ease), background-color 0.15s var(--lh-ease);
}

.fab:hover {
  transform: translateY(-2px);
  background: var(--lh-accent);
  color: var(--lh-accent-ink);
}

.panel {
  display: flex;
  flex-direction: column;
  width: 22rem;
  height: 30rem;
  background: var(--lh-ink);
  color: var(--lh-bg);
  border-radius: var(--lh-radius-l);
  overflow: hidden;
  box-shadow: var(--lh-shadow-float);
}

.panel__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.panel__brand {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-weight: 700;
  font-size: var(--lh-text-sm);
}

.panel__dot {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  background: var(--lh-accent);
}

.panel__close {
  border: none;
  background: transparent;
  color: inherit;
  opacity: 0.7;
  font-size: var(--lh-text-sm);
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
}
.panel__close:hover {
  opacity: 1;
}

.thread {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  overflow-y: auto;
}

.bubble {
  max-width: 80%;
  padding: 0.55rem 0.8rem;
  border-radius: 14px;
  font-size: var(--lh-text-sm);
  line-height: 1.55;
  white-space: pre-wrap;
}

.bubble--assistant {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.08);
  border-bottom-left-radius: 4px;
}

.bubble--user {
  align-self: flex-end;
  background: var(--lh-accent);
  color: var(--lh-accent-ink);
  border-bottom-right-radius: 4px;
}

.bubble--typing {
  display: flex;
  gap: 0.25rem;
  padding: 0.7rem 0.8rem;
}

.bubble--typing span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.5;
  animation: blink 1.2s infinite;
}
.bubble--typing span:nth-child(2) {
  animation-delay: 0.2s;
}
.bubble--typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%,
  60%,
  100% {
    opacity: 0.25;
  }
  30% {
    opacity: 0.9;
  }
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  padding: 0 1rem 0.25rem;
}

.chip {
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
  color: inherit;
  border-radius: var(--lh-radius-full);
  padding: 0.3rem 0.65rem;
  font-size: var(--lh-text-xs);
  cursor: pointer;
  transition: background-color 0.15s var(--lh-ease);
}
.chip:hover {
  background: rgba(255, 255, 255, 0.12);
}

.composer {
  display: flex;
  gap: 0.5rem;
  padding: 0.8rem 1rem 1rem;
}

.composer__input {
  flex: 1;
  min-width: 0;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: var(--lh-radius-full);
  background: rgba(255, 255, 255, 0.06);
  color: inherit;
  font-family: inherit;
  font-size: var(--lh-text-sm);
  padding: 0.5rem 0.9rem;
}

.composer__input::placeholder {
  color: rgba(255, 255, 255, 0.45);
}

.composer__input:focus {
  outline: none;
  border-color: var(--lh-accent);
}

.composer__send {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border: none;
  border-radius: var(--lh-radius-full);
  background: var(--lh-accent);
  color: var(--lh-accent-ink);
  font-size: var(--lh-text-sm);
  cursor: pointer;
}

.composer__send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.panel-enter-active,
.panel-leave-active {
  transition: opacity 0.18s var(--lh-ease), transform 0.18s var(--lh-ease);
}
.panel-enter-from,
.panel-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.97);
}

/* 모바일에서는 대화창을 전체 화면으로 띄운다 (의뢰서 [참고 4] ⑤) */
@media (max-width: 640px) {
  .chat {
    right: 1rem;
    bottom: 1rem;
  }

  .panel {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    border-radius: 0;
  }
}
</style>
