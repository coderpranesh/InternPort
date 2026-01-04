<template>
  <div class="dashboard-redirect">
    <div class="redirect-message">
      <ProgressSpinner />
      <p>Redirecting to your dashboard...</p>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import ProgressSpinner from 'primevue/progressspinner'

export default {
  name: 'DashboardRedirect',
  components: {
    ProgressSpinner
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    
    onMounted(() => {
      const userRole = store.getters.userRole
      
      if (userRole === 'student') {
        router.replace('/student')
      } else if (userRole === 'company') {
        router.replace('/company')
      } else if (userRole === 'admin') {
        router.replace('/admin')
      } else {
        router.replace('/login')
      }
    })
    
    return {}
  }
}
</script>

<style scoped>
.dashboard-redirect {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.redirect-message {
  background: white;
  padding: 3rem;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.redirect-message p {
  margin-top: 1rem;
  color: #2c3e50;
  font-weight: 500;
}
</style>