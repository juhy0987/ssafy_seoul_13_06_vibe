<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { CATEGORIES } from '@/config/region'
import { useTheme } from '@/composables/useTheme'

const router = useRouter()
const { isDark, toggle } = useTheme()

const searchOpen = ref(false)
const keyword = ref('')
const searchInput = ref(null)

function openSearch() {
  searchOpen.value = true
  requestAnimationFrame(() => searchInput.value?.focus())
}

function submitSearch() {
  const q = keyword.value.trim()
  if (!q) return
  // 검색은 첫 번째 카테고리 게시판에서 키워드 질의로 처리한다.
  router.push({ name: 'board', params: { category: CATEGORIES[0].slug }, query: { q } })
  searchOpen.value = false
  keyword.value = ''
}
</script>

<template>
  <header class="header">
    <div class="lh-container header__inner">
      <RouterLink to="/" class="brand">
        <span class="brand__mark" aria-hidden="true" />
        <span class="brand__name">LocalHub</span>
        <span class="brand__region">서울</span>
      </RouterLink>

      <nav class="nav" aria-label="게시판">
        <RouterLink
          v-for="category in CATEGORIES"
          :key="category.slug"
          class="nav__link"
          :to="{ name: 'board', params: { category: category.slug } }"
        >
          {{ category.label }}
        </RouterLink>
      </nav>

      <div class="tools">
        <form v-if="searchOpen" class="search" role="search" @submit.prevent="submitSearch">
          <input
            ref="searchInput"
            v-model="keyword"
            class="search__input"
            type="search"
            placeholder="게시글 검색"
            aria-label="게시글 검색"
            @blur="searchOpen = keyword.length > 0"
          />
        </form>

        <button v-else class="icon-btn" type="button" aria-label="검색 열기" @click="openSearch">
          ⌕
        </button>

        <button
          class="icon-btn"
          type="button"
          :aria-label="isDark ? '라이트 모드로 전환' : '다크 모드로 전환'"
          @click="toggle"
        >
          {{ isDark ? '☀' : '☾' }}
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: color-mix(in srgb, var(--lh-surface) 88%, transparent);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--lh-border);
}

.header__inner {
  height: var(--lh-header-h);
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  flex-shrink: 0;
}

.brand__mark {
  width: 9px;
  height: 9px;
  border-radius: 2px;
  background: var(--lh-accent);
}

.brand__name {
  font-weight: 800;
  font-size: var(--lh-text-lg);
  letter-spacing: -0.02em;
}

.brand__region {
  font-size: var(--lh-text-xs);
  font-weight: 700;
  color: var(--lh-accent-strong);
  background: var(--lh-accent-soft);
  padding: 0.1rem 0.4rem;
  border-radius: var(--lh-radius-full);
}

.nav {
  display: flex;
  gap: 0.35rem;
  margin-right: auto;
  overflow-x: auto;
  scrollbar-width: none;
}

.nav::-webkit-scrollbar {
  display: none;
}

.nav__link {
  flex-shrink: 0;
  font-size: var(--lh-text-sm);
  font-weight: 600;
  color: var(--lh-ink-soft);
  padding: 0.35rem 0.7rem;
  border-radius: var(--lh-radius-full);
  white-space: nowrap;
  transition: background-color 0.15s var(--lh-ease), color 0.15s var(--lh-ease);
}

.nav__link:hover {
  background: var(--lh-surface-2);
  color: var(--lh-ink);
}

.nav__link.router-link-active {
  background: var(--lh-ink);
  color: var(--lh-bg);
}

.tools {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-full);
  background: transparent;
  color: var(--lh-ink-soft);
  font-size: var(--lh-text-sm);
  cursor: pointer;
  transition: background-color 0.15s var(--lh-ease), color 0.15s var(--lh-ease);
}

.icon-btn:hover {
  background: var(--lh-surface-2);
  color: var(--lh-ink);
}

.search__input {
  width: 12rem;
  border: 1px solid var(--lh-border-strong);
  border-radius: var(--lh-radius-full);
  background: var(--lh-bg);
  color: var(--lh-ink);
  font-family: inherit;
  font-size: var(--lh-text-sm);
  padding: 0.4rem 0.85rem;
}

.search__input:focus {
  outline: none;
  border-color: var(--lh-accent);
}

@media (max-width: 640px) {
  .header__inner {
    gap: 0.75rem;
  }

  .brand__region {
    display: none;
  }

  .nav {
    gap: 0;
  }

  .nav__link {
    padding: 0.35rem 0.5rem;
    font-size: var(--lh-text-xs);
  }

  .search__input {
    width: 8rem;
  }
}
</style>
