<script setup>
import EmptyState from '@/components/common/EmptyState.vue'
import BaseButton from '@/components/common/BaseButton.vue'
</script>

<template>
  <div class="lh-container">
    <EmptyState
      icon="🧭"
      title="페이지를 찾을 수 없습니다"
      description="주소가 바뀌었거나 삭제된 페이지일 수 있어요."
    >
      <BaseButton variant="accent" to="/">홈으로 돌아가기</BaseButton>
    </EmptyState>
  </div>
</template>
