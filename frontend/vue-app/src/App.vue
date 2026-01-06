<template>
  <AppNavbar v-if="showNavbar" />
  <router-view />
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import AppNavbar from "./components/layout/AppNavbar.vue"

const route = useRoute()

// Show Navbar only on protected pages
const showNavbar = computed(() => {
  const publicRoutes = ["/login", "/register", "/forgot-password", "/terms", "/privacy"]
  return !publicRoutes.includes(route.path)
})
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

#app {
  min-height: 100vh;
  background-color: #f5f7fa;
}
</style>
