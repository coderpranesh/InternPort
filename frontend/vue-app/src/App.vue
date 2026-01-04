<template>
  <div id="app">
    <Toast />
    <router-view />
  </div>
</template>

<script>
import Toast from 'primevue/toast'

export default {
  name: 'App',
  components: {
    Toast
  }
}
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