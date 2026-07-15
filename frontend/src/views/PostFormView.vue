<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseField from '@/components/common/BaseField.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import SkeletonBlock from '@/components/common/SkeletonBlock.vue'
import { getPost, createPost, updatePost } from '@/api/posts'
import { listSpotsForCategory } from '@/api/tourism'
import { CATEGORIES } from '@/config/region'

const props = defineProps({
  category: { type: String, required: true },
  id: { type: [String, Number], default: null },
})

const router = useRouter()
const isEditing = computed(() => !!props.id)

// 카테고리는 라우트 param 을 초기값으로만 쓰고, 폼에서 사용자가 바꿀 수 있게 한다.
// (기존엔 라우트 param 으로 고정돼 홈에서 진입하면 항상 관광지로 작성됐다.)
const selectedCategory = ref(props.category)
const title = ref('')
const content = ref('')
const password = ref('')
const spotId = ref('')
const spots = ref([])
const editingSpotName = ref('')
const spotsLoading = ref(false)
const loading = ref(false)
const fetchLoading = ref(false)
const errors = ref({})

// 게시글은 특정 장소(spot_id)에 연결된다. 백엔드가 필수로 요구하므로 선택 UI 를 제공한다.
async function loadSpots() {
  spotsLoading.value = true
  delete errors.value.spots
  try {
    const res = await listSpotsForCategory(selectedCategory.value, { limit: 50 })
    spots.value = res.items ?? []
    // 수정 중인 장소가 목록(최대 50개)에 없으면 선택값이 비지 않도록 보강한다.
    if (spotId.value && !spots.value.some((s) => s.id === spotId.value)) {
      spots.value = [{ id: spotId.value, title: editingSpotName.value || spotId.value }, ...spots.value]
    }
  } catch (err) {
    console.error('장소 목록 로드 실패:', err)
    errors.value.spots = '장소 목록을 불러오지 못했습니다. 백엔드 /api/spots 연결을 확인해주세요.'
  } finally {
    spotsLoading.value = false
  }
}

// 카테고리를 바꾸면 장소 목록이 달라지므로 선택값을 초기화하고 다시 불러온다.
async function onCategoryChange() {
  spotId.value = ''
  editingSpotName.value = ''
  await loadSpots()
}

async function loadPostData() {
  if (!isEditing.value) return

  fetchLoading.value = true
  try {
    const post = await getPost(props.id)
    if (post) {
      title.value = post.title
      content.value = post.content
      spotId.value = post.spot_id ?? ''
      editingSpotName.value = post.spot_name ?? ''
      // 실제 저장된 카테고리로 맞춘다(라우트 param 과 다를 수 있음).
      if (post.category) selectedCategory.value = post.category
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

  if (!spotId.value) {
    errors.value.spot = '장소를 선택하세요.'
  }

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
      category: selectedCategory.value,
      spot_id: spotId.value,
    }

    if (isEditing.value) {
      await updatePost(props.id, payload)
    } else {
      await createPost(payload)
    }

    router.push({ name: 'board', params: { category: selectedCategory.value } })
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

onMounted(async () => {
  // 수정 시엔 저장된 카테고리·spot_id 를 먼저 확정한 뒤 그 카테고리의 장소 목록을 불러온다.
  await loadPostData()
  await loadSpots()
})
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

      <!-- Category field: 게시글 카테고리 선택 -->
      <BaseField label="카테고리" hint="글을 등록할 게시판을 선택하세요" required>
        <template #default="{ id }">
          <select
            :id="id"
            v-model="selectedCategory"
            class="form__select"
            @change="onCategoryChange"
          >
            <option v-for="c in CATEGORIES" :key="c.slug" :value="c.slug">
              {{ c.icon }} {{ c.label }}
            </option>
          </select>
        </template>
      </BaseField>

      <!-- Spot field: 게시글이 연결될 장소(백엔드 필수) -->
      <BaseField
        label="장소"
        hint="글이 소개할 장소를 선택하세요"
        :error="errors.spot || errors.spots"
        required
      >
        <template #default="{ id }">
          <select
            :id="id"
            v-model="spotId"
            class="form__select"
            :class="{ 'form__select--invalid': Boolean(errors.spot) }"
            :disabled="spotsLoading"
          >
            <option value="" disabled>
              {{ spotsLoading ? '장소 불러오는 중…' : '장소를 선택하세요' }}
            </option>
            <option v-for="spot in spots" :key="spot.id" :value="spot.id">
              {{ spot.title }}
            </option>
          </select>
        </template>
      </BaseField>

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

/* BaseInput(.input) 과 동일한 시각 언어로 맞춘 장소 선택 드롭다운 */
.form__select {
  width: 100%;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-s);
  background: var(--lh-surface);
  color: var(--lh-ink);
  font-family: var(--lh-font-sans);
  font-size: var(--lh-text-sm);
  line-height: 1.6;
  padding: 0.6rem 0.75rem;
  transition: border-color 0.15s var(--lh-ease), box-shadow 0.15s var(--lh-ease);
}

.form__select:focus {
  outline: none;
  border-color: var(--lh-accent);
  box-shadow: 0 0 0 3px var(--lh-accent-soft);
}

.form__select:disabled {
  opacity: 0.6;
  cursor: progress;
}

.form__select--invalid {
  border-color: var(--lh-danger);
}
.form__select--invalid:focus {
  box-shadow: 0 0 0 3px var(--lh-danger-soft);
}
</style>
