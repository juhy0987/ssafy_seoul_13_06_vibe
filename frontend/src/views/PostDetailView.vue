<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseField from '@/components/common/BaseField.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import SkeletonBlock from '@/components/common/SkeletonBlock.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import CommentSection from '@/components/board/CommentSection.vue'
import { formatShortDate } from '@/utils/format'
import { getPost, deletePost, verifyPassword, likePost, unlikePost } from '@/api/posts'

const props = defineProps({
  category: { type: String, required: true },
  id: { type: [String, Number], required: true },
})

const router = useRouter()

const post = ref(null)
const loading = ref(false)
const error = ref('')

// 익명 커뮤니티라 서버는 좋아요 수만 관리하고, 사용자별 누른 상태는 localStorage로 유지한다.
const LIKED_KEY = 'localhub:liked-posts'
const liked = ref(false)
const likeBusy = ref(false)

function getLikedSet() {
  try {
    return new Set(JSON.parse(localStorage.getItem(LIKED_KEY) ?? '[]'))
  } catch {
    return new Set()
  }
}

function saveLikedSet(set) {
  localStorage.setItem(LIKED_KEY, JSON.stringify([...set]))
}

async function toggleLike() {
  if (likeBusy.value || !post.value) return
  likeBusy.value = true
  const set = getLikedSet()
  const wasLiked = liked.value
  try {
    const res = wasLiked ? await unlikePost(props.id) : await likePost(props.id)
    post.value.like_count = res.like_count
    if (wasLiked) set.delete(Number(props.id))
    else set.add(Number(props.id))
    saveLikedSet(set)
    liked.value = !wasLiked
  } catch (err) {
    console.error('좋아요 처리 실패:', err)
  } finally {
    likeBusy.value = false
  }
}

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
      // 백엔드에서 비밀번호를 검증한다(POST /api/posts/{id}/verify).
      // 성공하면(204) 수정 화면으로 이동, 불일치면 403 이 던져진다.
      await verifyPassword(props.id, password.value)
      router.push({
        name: 'post-edit',
        params: { category: props.category, id: props.id },
      })
    } else if (pendingAction.value === 'delete') {
      await deletePost(props.id, password.value)
      router.push({ name: 'board', params: { category: props.category } })
    }
  } catch (err) {
    // 백엔드는 비밀번호 불일치 시 403 을 반환한다.
    passwordError.value =
      err?.status === 403 ? '비밀번호가 일치하지 않습니다.' : '요청 처리 중 오류가 발생했습니다.'
    console.error(err)
  }
}

onMounted(async () => {
  await fetchPost()
  liked.value = getLikedSet().has(Number(props.id))
})
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
        <p v-if="post.spot_name" class="detail__spot">📍 {{ post.spot_name }}</p>
        <div class="detail__meta lh-nums">
          <span>{{ formatShortDate(post.created_at) }}</span>
          <span>조회 {{ post.view_count }}</span>
        </div>
      </header>

      <div class="detail__body">
        {{ post.content }}
      </div>

      <div class="detail__like">
        <button
          type="button"
          class="like-btn"
          :class="{ 'like-btn--on': liked }"
          :aria-pressed="liked"
          :disabled="likeBusy"
          @click="toggleLike"
        >
          <span class="like-btn__icon" aria-hidden="true">{{ liked ? '♥' : '♡' }}</span>
          좋아요 <span class="lh-nums">{{ post.like_count ?? 0 }}</span>
        </button>
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

      <CommentSection :post-id="id" />
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

.detail__spot {
  font-size: var(--lh-text-sm);
  font-weight: 600;
  color: var(--lh-accent-strong);
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

.detail__like {
  display: flex;
  justify-content: center;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1.1rem;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-full);
  background: var(--lh-surface);
  color: var(--lh-ink);
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  transition: border-color 0.15s var(--lh-ease), color 0.15s var(--lh-ease);
}

.like-btn:hover:not(:disabled) {
  border-color: var(--lh-accent);
}

.like-btn--on {
  border-color: var(--lh-accent);
  color: var(--lh-accent);
}

.like-btn__icon {
  font-size: 1.1rem;
  line-height: 1;
}

.like-btn:disabled {
  opacity: 0.6;
  cursor: progress;
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
