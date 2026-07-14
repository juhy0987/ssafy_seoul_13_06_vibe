<script setup>
import { REGION } from '@/config/region'

defineProps({
  spotCount: { type: Number, default: 0 },
  festivalCount: { type: Number, default: 0 },
})
</script>

<template>
  <section class="hero">
    <div class="hero__text">
      <span class="hero__kicker">{{ REGION.name }} · {{ REGION.nameEn }}</span>
      <h1 class="hero__title">{{ REGION.tagline }}</h1>
      <p class="hero__desc">{{ REGION.description }}</p>
    </div>

    <dl class="hero__stats lh-nums">
      <div class="hero__stat">
        <dt>관광지</dt>
        <dd>{{ spotCount.toLocaleString('ko-KR') }}</dd>
      </div>
      <div class="hero__stat">
        <dt>축제·행사</dt>
        <dd>{{ festivalCount.toLocaleString('ko-KR') }}</dd>
      </div>
    </dl>
  </section>
</template>

<style scoped>
.hero {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
  padding: 2rem 1.75rem;
  border-radius: var(--lh-radius-l);
  background: linear-gradient(135deg, var(--lh-accent) 0%, var(--lh-accent-strong) 100%);
  color: var(--lh-accent-ink);
}

.hero__text {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.hero__kicker {
  font-size: var(--lh-text-xs);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.85;
}

.hero__title {
  font-size: clamp(1.6rem, 3.4vw, 2.1rem);
  font-weight: 800;
  letter-spacing: -0.025em;
}

.hero__desc {
  font-size: var(--lh-text-sm);
  opacity: 0.92;
}

.hero__stats {
  display: flex;
  gap: 2rem;
  margin: 0;
}

.hero__stat {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.hero__stat dt {
  font-size: var(--lh-text-xs);
  font-weight: 600;
  opacity: 0.8;
}

.hero__stat dd {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 800;
  line-height: 1.1;
}

.hero__stat dd::after {
  content: '건';
  font-family: var(--lh-font-sans);
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.15rem;
  opacity: 0.8;
}
</style>
