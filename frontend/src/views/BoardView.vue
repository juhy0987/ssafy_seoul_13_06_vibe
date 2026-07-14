<script setup>
import { computed, onMounted, ref } from 'vue'
import PostList from '@/components/board/PostList.vue'
import BasePagination from '@/components/common/BasePagination.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseField from '@/components/common/BaseField.vue'
import { findCategory } from '@/config/region'
import { listPosts } from '@/api/posts'

const props = defineProps({
  category: { type: String, required: true },
})

const meta = computed(() => findCategory(props.category))

const search = ref('')
const page = ref(1)
const pageSize = 10

const posts = ref([])
const total = ref(0)
const loading = ref(false)

async function fetchPosts() {
  loading.value = true
  try {
    const result = await listPosts({
      category: props.category,
      q: search.value,
      page: page.value,
      size: pageSize,
    })
    posts.value = result.items
    total.value = result.total
  } catch (err) {
    console.error('게시글 목록 조회 실패:', err)
  } finally {
    loading.value = false
  }
}

function onSearch() {
  page.value = 1
  fetchPosts()
}

function onPageChange(next) {
  page.value = next
  fetchPosts()
}

onMounted(() => fetchPosts())
</script>

<template>
  <div class="lh-container board">
    <header class="board__header">
      <div class="board__title-wrap">
        <h1 class="board__title">{{ meta?.label ?? '게시판' }}</h1>
      </div>

      <div class="board__toolbar">
        <BaseField label="검색" hint="">
          <template #default="{ id }">
            <div class="search-wrap">
              <BaseInput
                :id="id"
                v-model="search"
                placeholder="제목·내용으로 검색"
                @keydown.enter="onSearch"
              />
              <BaseButton size="sm" @click="onSearch">검색</BaseButton>
            </div>
          </template>
        </BaseField>

        <BaseButton :to="{ name: 'post-create', params: { category } }" variant="accent">
          + 글쓰기
        </BaseButton>
      </div>
    </header>

    <PostList
      :posts="posts"
      :loading="loading"
      :empty-title="search ? '검색 결과가 없어요' : '아직 게시글이 없어요'"
      :empty-description="search ? '다른 검색어를 시도해보세요.' : '첫 글을 남겨 이 게시판을 시작해보세요.'"
    />

    <BasePagination
      :page="page"
      :total="total"
      :size="pageSize"
      @change="onPageChange"
    />
  </div>
</template>

<style scoped>
.board {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.board__header {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.board__title-wrap {
  border-bottom: 2px solid var(--lh-border);
  padding-bottom: 1rem;
}

.board__title {
  font-size: var(--lh-text-lg);
  font-weight: 800;
}

.board__toolbar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 32rem;
}

.search-wrap {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
}

.search-wrap :deep(.input) {
  flex: 1;
}

@media (max-width: 640px) {
  .board__toolbar {
    flex-direction: row;
    max-width: none;
    align-items: center;
  }

  .search-wrap {
    flex: 1;
  }
}
</style>
