<script setup lang="ts">
import { RouterView } from 'vue-router'
import { publicConfig } from './config'
</script>

<template>
  <main class="desktop-shell">
    <h1>{{ publicConfig.title || 'Super AI' }}</h1>
    <RouterView />
  </main>
</template>

<style scoped>
.desktop-shell {
  margin: 0 auto;
  max-width: 1200px;
  padding: 2rem;
}
</style>
