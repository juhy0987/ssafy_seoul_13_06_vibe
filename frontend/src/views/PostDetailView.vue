<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseField from '@/components/common/BaseField.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import SkeletonBlock from '@/components/common/SkeletonBlock.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import { formatShortDate } from '@/utils/format'
import { getPost, deletePost } from '@/api/posts'

const props = defineProps({
  category: { type: String, required: true },
  id: { type: [String, Number], required: true },
})

const router = useRouter()

const post = ref(null)
const loading = ref(false)
const error = ref('')

const showPasswordModal = ref(false)
const pendingAction = ref(null)
const password = ref('')
const passwordError = ref('')

async function fetchPost() {
  loading.value = true
  error.value = ''
  try {
    post.value = await getPost(props.id)
    if (!post.value) {
      error.value = '게시글을 찾을 수 없습니다.'
    }
  } catch (err) {
    error.value = '게시글 조회에 실패했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function openPasswordModal(action) {
  pendingAction.value = action
  password.value = ''
  passwordError.value = ''
  showPasswordModal.value = true
}

async function confirmPassword() {
  if (!password.value.trim()) {
    passwordError.value = '비밀번호를 입력하세요.'
    return
  }

  try {
    if (pendingAction.value === 'edit') {
      // 비밀번호 검증 (실제로는 백엔드에서 검증해야 함)
      // 여기서는 수정 화면으로 이동하는 것으로 처리
      if (post.value.password === password.value) {
        router.push({
          name: 'post-edit',
          params: { category: props.category, id: props.id },
        })
      } else {
        passwordError.value = '비밀번호가 일치하지 않습니다.'
      }
    } else if (pendingAction.value === 'delete') {
      await deletePost(props.id, password.value)
      router.push({ name: 'board', params: { category: props.category } })
    }
  } catch (err) {
    passwordError.value = '요청 처리 중 오류가 발생했습니다.'
    console.error(err)
  }
}

onMounted(() => fetchPost())
</script>

<template>
  <div class="lh-container detail">
    <!-- Loading -->
    <div v-if="loading" class="detail__loader">
      <SkeletonBlock height="2rem" width="60%" />
      <SkeletonBlock height="1rem" width="40%" class="mt-2" />
      <SkeletonBlock height="6rem" width="100%" class="mt-4" />
    </div>

    <!-- Error -->
    <EmptyState v-else-if="error" icon="⚠️" :title="error">
      <BaseButton variant="ghost" :to="{ name: 'board', params: { category } }">
        게시판으로 돌아가기
      </BaseButton>
    </EmptyState>

    <!-- Content -->
    <article v-else-if="post" class="detail__article">
      <header class="detail__header">
        <h1 class="detail__title">{{ post.title }}</h1>
        <div class="detail__meta lh-nums">
          <span>{{ formatShortDate(post.created_at) }}</span>
          <span>조회 {{ post.view_count }}</span>
        </div>
      </header>

      <div class="detail__body">
        {{ post.content }}
      </div>

      <footer class="detail__footer">
        <BaseButton
          :to="{ name: 'board', params: { category } }"
          variant="ghost"
        >
          목록으로
        </BaseButton>

        <div class="detail__actions">
          <BaseButton
            variant="quiet"
            @click="openPasswordModal('edit')"
          >
            수정
          </BaseButton>
          <BaseButton
            variant="quiet"
            @click="openPasswordModal('delete')"
          >
            삭제
          </BaseButton>
        </div>
      </footer>
    </article>

    <!-- Password Modal -->
    <BaseModal
      :open="showPasswordModal"
      :title="`${pendingAction === 'edit' ? '수정' : '삭제'}하려면 비밀번호를 입력하세요`"
      @close="showPasswordModal = false"
    >
      <form class="password-form" @submit.prevent="confirmPassword">
        <BaseField
          label="비밀번호"
          :error="passwordError"
          required
        >
          <template #default="{ id }">
            <BaseInput
              :id="id"
              v-model="password"
              type="password"
              placeholder="비밀번호 입력"
              :invalid="Boolean(passwordError)"
            />
          </template>
        </BaseField>

        <div class="password-form__actions">
          <BaseButton
            type="submit"
            variant="accent"
            block
          >
            확인
          </BaseButton>
          <BaseButton
            type="button"
            variant="ghost"
            block
            @click="showPasswordModal = false"
          >
            취소
          </BaseButton>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<style scoped>
.detail {
  max-width: 48rem;
  margin: 0 auto;
}

.detail__loader {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail__article {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail__header {
  border-bottom: 2px solid var(--lh-border);
  padding-bottom: 1rem;
}

.detail__title {
  font-size: var(--lh-text-lg);
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.detail__meta {
  display: flex;
  gap: 1.5rem;
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}

.detail__body {
  font-size: var(--lh-text-sm);
  line-height: 1.8;
  color: var(--lh-ink);
  white-space: pre-wrap;
  word-break: break-word;
}

.detail__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  border-top: 1px solid var(--lh-border);
  padding-top: 1rem;
}

.detail__actions {
  display: flex;
  gap: 0.5rem;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.password-form__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mt-2 {
  margin-top: 0.5rem;
}

.mt-4 {
  margin-top: 1rem;
}

@media (max-width: 640px) {
  .detail__footer {
    flex-direction: column;
  }

  .detail__actions {
    width: 100%;
  }
}
</style>
