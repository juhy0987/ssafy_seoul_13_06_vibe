<template>
  <footer class="footer">
    <div class="lh-container footer__inner">
      <p class="footer__brand">LocalHub · 서울 지역 정보 공유 커뮤니티</p>
      <p class="footer__meta">
        데이터 출처: 한국관광공사 TourAPI 4.0 (공공누리 제1유형) · 수집일 2026.06.22
      </p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: var(--lh-gap-8);
  border-top: 1px solid var(--lh-border);
  padding-block: 1.75rem;
}

.footer__inner {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.footer__brand {
  font-size: var(--lh-text-sm);
  font-weight: 600;
  color: var(--lh-ink-soft);
}

.footer__meta {
  font-size: var(--lh-text-xs);
  color: var(--lh-ink-faint);
}
</style>
