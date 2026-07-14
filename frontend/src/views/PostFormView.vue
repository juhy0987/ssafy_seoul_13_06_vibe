<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseField from '@/components/common/BaseField.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import SkeletonBlock from '@/components/common/SkeletonBlock.vue'
import { getPost, createPost, updatePost } from '@/api/posts'

const props = defineProps({
  category: { type: String, required: true },
  id: { type: [String, Number], default: null },
})

const router = useRouter()
const isEditing = computed(() => !!props.id)

const title = ref('')
const content = ref('')
const password = ref('')
const loading = ref(false)
const fetchLoading = ref(false)
const errors = ref({})

async function loadPostData() {
  if (!isEditing.value) return

  fetchLoading.value = true
  try {
    const post = await getPost(props.id)
    if (post) {
      title.value = post.title
      content.value = post.content
      password.value = post.password || ''
    }
  } catch (err) {
    console.error('게시글 로드 실패:', err)
    errors.value.fetch = '게시글을 불러올 수 없습니다.'
  } finally {
    fetchLoading.value = false
  }
}

function validate() {
  errors.value = {}

  if (!title.value.trim()) {
    errors.value.title = '제목을 입력하세요.'
  }

  if (!content.value.trim()) {
    errors.value.content = '내용을 입력하세요.'
  }

  if (!password.value.trim()) {
    errors.value.password = '비밀번호를 입력하세요.'
  } else if (password.value.length < 4) {
    errors.value.password = '비밀번호는 최소 4자 이상이어야 합니다.'
  }

  return Object.keys(errors.value).length === 0
}

async function submit() {
  if (!validate()) return

  loading.value = true
  try {
    const payload = {
      title: title.value.trim(),
      content: content.value.trim(),
      password: password.value,
      category: props.category,
    }

    if (isEditing.value) {
      await updatePost(props.id, payload)
    } else {
      await createPost(payload)
    }

    router.push({ name: 'board', params: { category: props.category } })
  } catch (err) {
    console.error('저장 실패:', err)
    errors.value.submit = '저장 중 오류가 발생했습니다.'
  } finally {
    loading.value = false
  }
}

function cancel() {
  router.back()
}

onMounted(() => loadPostData())
</script>

<template>
  <div class="lh-container form">
    <header class="form__header">
      <h1 class="form__title">
        {{ isEditing ? '게시글 수정' : '게시글 작성' }}
      </h1>
    </header>

    <!-- Loading state -->
    <div v-if="fetchLoading" class="form__loader">
      <SkeletonBlock height="2.5rem" />
      <SkeletonBlock height="12rem" />
      <SkeletonBlock height="2rem" />
    </div>

    <!-- Form -->
    <form v-else class="form__content" @submit.prevent="submit">
      <!-- Error message -->
      <div v-if="errors.submit" class="form__error">
        ⚠️ {{ errors.submit }}
      </div>

      <!-- Title field -->
      <BaseField
        label="제목"
        :error="errors.title"
        required
      >
        <template #default="{ id }">
          <BaseInput
            :id="id"
            v-model="title"
            placeholder="게시글 제목을 입력하세요"
            :invalid="Boolean(errors.title)"
          />
        </template>
      </BaseField>

      <!-- Content field -->
      <BaseField
        label="내용"
        :error="errors.content"
        required
      >
        <template #default="{ id }">
          <BaseInput
            :id="id"
            as="textarea"
            v-model="content"
            placeholder="게시글 내용을 입력하세요"
            :rows="12"
            :invalid="Boolean(errors.content)"
          />
        </template>
      </BaseField>

      <!-- Password field -->
      <BaseField
        label="비밀번호"
        hint="수정·삭제 시 필요합니다 (영문, 숫자 혼합 권장)"
        :error="errors.password"
        required
      >
        <template #default="{ id }">
          <BaseInput
            :id="id"
            v-model="password"
            type="password"
            placeholder="비밀번호 입력 (4자 이상)"
            :invalid="Boolean(errors.password)"
          />
        </template>
      </BaseField>

      <!-- Actions -->
      <div class="form__actions">
        <BaseButton
          type="submit"
          variant="accent"
          block
          :disabled="loading"
        >
          {{ isEditing ? '수정하기' : '등록하기' }}
        </BaseButton>
        <BaseButton
          type="button"
          variant="ghost"
          block
          @click="cancel"
          :disabled="loading"
        >
          취소
        </BaseButton>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form {
  max-width: 48rem;
  margin: 0 auto;
}

.form__header {
  border-bottom: 2px solid var(--lh-border);
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.form__title {
  font-size: var(--lh-text-lg);
  font-weight: 800;
}

.form__loader {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form__content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form__error {
  padding: 0.75rem 1rem;
  background: var(--lh-danger-soft);
  border: 1px solid var(--lh-danger-soft);
  border-radius: var(--lh-radius-s);
  color: var(--lh-danger);
  font-size: var(--lh-text-sm);
  font-weight: 600;
}

.form__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}
</style>
