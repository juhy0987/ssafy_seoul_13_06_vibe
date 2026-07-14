import { computed, ref } from 'vue'

const STORAGE_KEY = 'localhub:theme'

// 모듈 스코프에 두어 앱 전체가 같은 상태를 공유한다.
const stored = localStorage.getItem(STORAGE_KEY)
const theme = ref(stored === 'light' || stored === 'dark' ? stored : 'system')

function apply(next) {
  if (next === 'system') {
    document.documentElement.removeAttribute('data-theme')
  } else {
    document.documentElement.setAttribute('data-theme', next)
  }
}

apply(theme.value)

function prefersDark() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

export function useTheme() {
  const isDark = computed(() =>
    theme.value === 'system' ? prefersDark() : theme.value === 'dark',
  )

  function toggle() {
    const next = isDark.value ? 'light' : 'dark'
    theme.value = next
    localStorage.setItem(STORAGE_KEY, next)
    apply(next)
  }

  return { theme, isDark, toggle }
}
