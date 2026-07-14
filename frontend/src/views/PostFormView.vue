<script setup>
import EmptyState from '@/components/common/EmptyState.vue'
import BaseButton from '@/components/common/BaseButton.vue'

defineProps({
  category: { type: String, required: true },
  id: { type: [String, Number], default: null },
})
</script>

<template>
  <div class="lh-container">
    <EmptyState
      icon="🚧"
      :title="id ? '게시글 수정 — 다음 단계에서 구현합니다' : '게시글 작성 — 다음 단계에서 구현합니다'"
      description="제목·내용·수정용 비밀번호 입력 폼을 붙입니다. BaseField, BaseInput, BaseButton 은 이미 준비되어 있습니다."
    >
      <BaseButton variant="ghost" to="/">홈으로 돌아가기</BaseButton>
    </EmptyState>
  </div>
</template>
