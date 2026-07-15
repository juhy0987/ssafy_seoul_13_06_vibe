<script setup>
import { computed, onMounted, ref } from 'vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseField from '@/components/common/BaseField.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import { formatFullDate } from '@/utils/format'
import {
  listComments,
  createComment,
  updateComment,
  deleteComment,
} from '@/api/comments'

const props = defineProps({
  postId: { type: [String, Number], required: true },
})

const comments = ref([])
const loading = ref(false)
const loadError = ref('')

// 새 댓글 작성
const newContent = ref('')
const newPassword = ref('')
const creating = ref(false)
const createErrors = ref({})

// 인라인 수정
const editingId = ref(null)
const editContent = ref('')
const editPassword = ref('')
const savingEdit = ref(false)
const editErrors = ref({})

// 삭제(비밀번호 모달)
const deleteTargetId = ref(null)
const deletePassword = ref('')
const deleteError = ref('')
const deleting = ref(false)

const count = computed(() => comments.value.length)

async function load() {
  loading.value = true
  loadError.value = ''
  try {
    comments.value = await listComments(props.postId)
  } catch (err) {
    console.error('댓글 조회 실패:', err)
    loadError.value = '댓글을 불러오지 못했습니다. 백엔드 연결을 확인해주세요.'
  } finally {
    loading.value = false
  }
}

async function submitNew() {
  createErrors.value = {}
  if (!newContent.value.trim()) createErrors.value.content = '내용을 입력하세요.'
  if (!newPassword.value.trim()) createErrors.value.password = '비밀번호를 입력하세요.'
  if (Object.keys(createErrors.value).length) return

  creating.value = true
  try {
    await createComment(props.postId, {
      content: newContent.value.trim(),
      password: newPassword.value,
    })
    newContent.value = ''
    newPassword.value = ''
    await load()
  } catch (err) {
    console.error('댓글 등록 실패:', err)
    createErrors.value.submit = '댓글 등록에 실패했습니다.'
  } finally {
    creating.value = false
  }
}

function startEdit(comment) {
  editingId.value = comment.id
  editContent.value = comment.content
  editPassword.value = ''
  editErrors.value = {}
}

function cancelEdit() {
  editingId.value = null
}

async function saveEdit(comment) {
  editErrors.value = {}
  if (!editContent.value.trim()) editErrors.value.content = '내용을 입력하세요.'
  if (!editPassword.value.trim()) editErrors.value.password = '비밀번호를 입력하세요.'
  if (Object.keys(editErrors.value).length) return

  savingEdit.value = true
  try {
    await updateComment(props.postId, comment.id, {
      content: editContent.value.trim(),
      password: editPassword.value,
    })
    editingId.value = null
    await load()
  } catch (err) {
    console.error('댓글 수정 실패:', err)
    editErrors.value.submit =
      err?.status === 403 ? '비밀번호가 일치하지 않습니다.' : '댓글 수정에 실패했습니다.'
  } finally {
    savingEdit.value = false
  }
}

function askDelete(comment) {
  deleteTargetId.value = comment.id
  deletePassword.value = ''
  deleteError.value = ''
}

async function confirmDelete() {
  if (!deletePassword.value.trim()) {
    deleteError.value = '비밀번호를 입력하세요.'
    return
  }
  deleting.value = true
  try {
    await deleteComment(props.postId, deleteTargetId.value, deletePassword.value)
    deleteTargetId.value = null
    await load()
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
    deleteError.value =
      err?.status === 403 ? '비밀번호가 일치하지 않습니다.' : '댓글 삭제에 실패했습니다.'
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>

<template>
  <section class="comments">
    <h2 class="comments__title">댓글 {{ count }}</h2>

    <!-- 목록 -->
    <p v-if="loading" class="comments__hint">불러오는 중…</p>
    <p v-else-if="loadError" class="comments__hint comments__hint--error">{{ loadError }}</p>
    <p v-else-if="!comments.length" class="comments__hint">첫 댓글을 남겨보세요.</p>

    <ul v-else class="comments__list">
      <li v-for="comment in comments" :key="comment.id" class="comment">
        <!-- 수정 모드 -->
        <div v-if="editingId === comment.id" class="comment__edit">
          <BaseField label="내용" :error="editErrors.content">
            <template #default="{ id }">
              <BaseInput
                :id="id"
                as="textarea"
                v-model="editContent"
                :rows="3"
                :invalid="Boolean(editErrors.content)"
              />
            </template>
          </BaseField>
          <BaseField label="비밀번호" :error="editErrors.password || editErrors.submit">
            <template #default="{ id }">
              <BaseInput
                :id="id"
                v-model="editPassword"
                type="password"
                placeholder="작성 시 입력한 비밀번호"
                :invalid="Boolean(editErrors.password || editErrors.submit)"
              />
            </template>
          </BaseField>
          <div class="comment__actions">
            <BaseButton size="sm" variant="accent" :disabled="savingEdit" @click="saveEdit(comment)">
              저장
            </BaseButton>
            <BaseButton size="sm" variant="ghost" :disabled="savingEdit" @click="cancelEdit">
              취소
            </BaseButton>
          </div>
        </div>

        <!-- 보기 모드 -->
        <template v-else>
          <p class="comment__body">{{ comment.content }}</p>
          <div class="comment__meta">
            <span class="comment__date lh-nums">{{ formatFullDate(comment.created_at) }}</span>
            <span class="comment__buttons">
              <button class="comment__link" type="button" @click="startEdit(comment)">수정</button>
              <button class="comment__link" type="button" @click="askDelete(comment)">삭제</button>
            </span>
          </div>
        </template>
      </li>
    </ul>

    <!-- 작성 폼 -->
    <form class="comments__form" @submit.prevent="submitNew">
      <BaseField label="댓글 작성" :error="createErrors.content || createErrors.submit">
        <template #default="{ id }">
          <BaseInput
            :id="id"
            as="textarea"
            v-model="newContent"
            :rows="3"
            placeholder="댓글을 입력하세요"
            :invalid="Boolean(createErrors.content || createErrors.submit)"
          />
        </template>
      </BaseField>

      <div class="comments__form-row">
        <BaseField label="비밀번호" :error="createErrors.password">
          <template #default="{ id }">
            <BaseInput
              :id="id"
              v-model="newPassword"
              type="password"
              placeholder="수정·삭제 시 필요"
              :invalid="Boolean(createErrors.password)"
            />
          </template>
        </BaseField>
        <BaseButton type="submit" variant="accent" :disabled="creating">등록</BaseButton>
      </div>
    </form>

    <!-- 삭제 확인 모달 -->
    <BaseModal
      :open="deleteTargetId !== null"
      title="댓글을 삭제하려면 비밀번호를 입력하세요"
      @close="deleteTargetId = null"
    >
      <form class="delete-form" @submit.prevent="confirmDelete">
        <BaseField label="비밀번호" :error="deleteError" required>
          <template #default="{ id }">
            <BaseInput
              :id="id"
              v-model="deletePassword"
              type="password"
              placeholder="비밀번호 입력"
              :invalid="Boolean(deleteError)"
            />
          </template>
        </BaseField>
        <div class="delete-form__actions">
          <BaseButton type="submit" variant="accent" block :disabled="deleting">확인</BaseButton>
          <BaseButton type="button" variant="ghost" block @click="deleteTargetId = null">
            취소
          </BaseButton>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<style scoped>
.comments {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  border-top: 1px solid var(--lh-border);
  padding-top: 1.5rem;
}

.comments__title {
  font-size: var(--lh-text-base);
  font-weight: 800;
}

.comments__hint {
  font-size: var(--lh-text-sm);
  color: var(--lh-ink-faint);
}

.comments__hint--error {
  color: var(--lh-danger);
}

.comments__list {
  display: flex;
  flex-direction: column;
}

.comment {
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--lh-border);
}

.comment:first-child {
  padding-top: 0;
}

.comment__body {
  font-size: var(--lh-text-sm);
  line-height: 1.7;
  color: var(--lh-ink);
  white-space: pre-wrap;
  word-break: break-word;
}

.comment__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 0.4rem;
}

.comment__date {
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}

.comment__buttons {
  display: flex;
  gap: 0.75rem;
}

.comment__link {
  border: none;
  background: transparent;
  color: var(--lh-ink-faint);
  font-size: var(--lh-text-xs);
  cursor: pointer;
  padding: 0;
}

.comment__link:hover {
  color: var(--lh-accent-strong);
}

.comment__edit {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.comment__actions {
  display: flex;
  gap: 0.5rem;
}

.comments__form {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: 0.5rem;
}

.comments__form-row {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
}

.comments__form-row :deep(.field) {
  flex: 1;
}

.delete-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.delete-form__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
