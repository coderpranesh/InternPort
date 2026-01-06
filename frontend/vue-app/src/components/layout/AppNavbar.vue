<template>
  <div class="navbar">
    <div class="logo">InternPort</div>

    <div class="actions">
      <Button
        label="Logout"
        icon="pi pi-sign-out"
        severity="danger"
        @click="confirmLogout"
      />
    </div>

    <ConfirmDialog />
  </div>
</template>

<script setup>
import Button from "primevue/button"
import ConfirmDialog from "primevue/confirmdialog"
import { useConfirm } from "primevue/useconfirm"
import { useRouter } from "vue-router"

const confirm = useConfirm()
const router = useRouter()

const confirmLogout = () => {
  confirm.require({
    message: 'Are you sure you want to logout?',
    header: 'Logout Confirmation',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')

      // Redirect to login page (SPA)
      router.replace('/login')
    }
  })
}
</script>

<style scoped>
.navbar {
  height: 64px;
  background: #0f172a;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 12px;
}
</style>
