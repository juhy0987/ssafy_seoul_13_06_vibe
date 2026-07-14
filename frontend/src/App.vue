<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ChatWidget from '@/components/chat/ChatWidget.vue'
</script>

<template>
  <div class="shell">
    <AppHeader />

    <main class="shell__main">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <AppFooter />
    <ChatWidget />
  </div>
</template>

<style scoped>
.shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.shell__main {
  flex: 1;
  padding-block: var(--lh-gap-6);
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.16s var(--lh-ease);
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
