<script setup>
import { computed } from 'vue'
import EmptyState from '@/components/common/EmptyState.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { findCategory } from '@/config/region'

const props = defineProps({
  category: { type: String, required: true },
})

const meta = computed(() => findCategory(props.category))
</script>

<template>
  <div class="lh-container">
    <EmptyState
      icon="🚧"
      :title="`${meta?.label ?? '게시판'} — 다음 단계에서 구현합니다`"
      description="목록 조회·검색·페이지네이션은 홈 화면 확정 후 이어서 붙입니다. 필요한 공용 컴포넌트(PostList, BasePagination, BaseInput)는 이미 준비되어 있습니다."
    >
      <BaseButton variant="ghost" to="/">홈으로 돌아가기</BaseButton>
    </EmptyState>
  </div>
</template>
