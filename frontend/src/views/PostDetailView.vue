<script setup>
import EmptyState from '@/components/common/EmptyState.vue'
import BaseButton from '@/components/common/BaseButton.vue'

defineProps({
  category: { type: String, required: true },
  id: { type: [String, Number], required: true },
})
</script>

<template>
  <div class="lh-container">
    <EmptyState
      icon="🚧"
      :title="`게시글 #${id} 상세 — 다음 단계에서 구현합니다`"
      description="본문 표시와 수정·삭제 시 비밀번호 확인 모달을 붙입니다. BaseModal, BaseField, BaseInput 은 이미 준비되어 있습니다."
    >
      <BaseButton variant="ghost" to="/">홈으로 돌아가기</BaseButton>
    </EmptyState>
  </div>
</template>
