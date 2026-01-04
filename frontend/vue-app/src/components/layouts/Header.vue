<template>
  <header class="app-header">
    <div class="header-container">
      <div class="header-left">
        <router-link to="/" class="logo">
          <i class="pi pi-briefcase"></i>
          <span>InternPort</span>
        </router-link>
        
        <nav class="main-nav">
          <router-link v-if="userRole === 'student'" to="/student" class="nav-link">
            <i class="pi pi-home"></i>
            <span>Dashboard</span>
          </router-link>
          <router-link v-if="userRole === 'student'" to="/internships" class="nav-link">
            <i class="pi pi-search"></i>
            <span>Internships</span>
          </router-link>
          <router-link v-if="userRole === 'student'" to="/my-applications" class="nav-link">
            <i class="pi pi-list"></i>
            <span>My Applications</span>
          </router-link>
          <router-link v-if="userRole === 'company'" to="/company" class="nav-link">
            <i class="pi pi-home"></i>
            <span>Dashboard</span>
          </router-link>
          <router-link v-if="userRole === 'company'" to="/company/internships" class="nav-link">
            <i class="pi pi-briefcase"></i>
            <span>Internships</span>
          </router-link>
          <router-link v-if="userRole === 'company'" to="/company/applications" class="nav-link">
            <i class="pi pi-users"></i>
            <span>Applications</span>
          </router-link>
          <router-link v-if="userRole === 'admin'" to="/admin" class="nav-link">
            <i class="pi pi-home"></i>
            <span>Admin Panel</span>
          </router-link>
          <router-link to="/profile" class="nav-link">
            <i class="pi pi-user"></i>
            <span>Profile</span>
          </router-link>
        </nav>
      </div>
      
      <div class="header-right">
        <div class="user-info" v-if="user">
          <div class="user-details">
            <div class="user-name">{{ userName }}</div>
            <div class="user-role">{{ userRoleDisplay }}</div>
          </div>
          <Avatar :label="userInitial" shape="circle" />
          <Menu :model="userMenu" :popup="true" ref="menu" />
          <Button
            icon="pi pi-angle-down"
            @click="toggleMenu"
            text
            rounded
            aria-label="User Menu"
          />
        </div>
        
        <Button
          v-else
          label="Login"
          icon="pi pi-sign-in"
          @click="goToLogin"
          outlined
        />
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import Menu from 'primevue/menu'

export default {
  name: 'AppHeader',
  components: {
    Avatar,
    Button,
    Menu
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    const menu = ref()
    
    const user = computed(() => store.state.user)
    const userRole = computed(() => store.getters.userRole)
    const userName = computed(() => store.getters.userName)
    
    const userRoleDisplay = computed(() => {
      const role = userRole.value
      if (role === 'student') return 'Student'
      if (role === 'company') return 'Company'
      if (role === 'admin') return 'Administrator'
      return 'User'
    })
    
    const userInitial = computed(() => {
      if (!userName.value) return 'U'
      return userName.value.charAt(0).toUpperCase()
    })
    
    const userMenu = computed(() => [
      {
        label: 'Profile',
        icon: 'pi pi-user',
        command: () => router.push('/profile')
      },
      {
        separator: true
      },
      {
        label: 'Settings',
        icon: 'pi pi-cog',
        command: () => {
          toast.add({
            severity: 'info',
            summary: 'Coming Soon',
            detail: 'Settings will be available soon',
            life: 3000
          })
        }
      },
      {
        label: 'Help',
        icon: 'pi pi-question-circle',
        command: () => {
          toast.add({
            severity: 'info',
            summary: 'Help',
            detail: 'Contact support@internport.com for assistance',
            life: 5000
          })
        }
      },
      {
        separator: true
      },
      {
        label: 'Logout',
        icon: 'pi pi-sign-out',
        command: handleLogout
      }
    ])
    
    const toggleMenu = (event) => {
      menu.value.toggle(event)
    }
    
    const handleLogout = () => {
      store.dispatch('logout')
      toast.add({
        severity: 'info',
        summary: 'Logged Out',
        detail: 'You have been successfully logged out',
        life: 3000
      })
      router.push('/login')
    }
    
    const goToLogin = () => {
      router.push('/login')
    }
    
    return {
      user,
      userRole,
      userName,
      userRoleDisplay,
      userInitial,
      userMenu,
      menu,
      toggleMenu,
      handleLogout,
      goToLogin
    }
  }
}
</script>

<style scoped>
.app-header {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 0 0;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.25rem;
  color: #2c3e50;
}

.logo i {
  font-size: 1.5rem;
  color: #667eea;
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #5a6c7d;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.nav-link.router-link-active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  color: #667eea;
  font-weight: 500;
}

.nav-link i {
  font-size: 1.1rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-info:hover {
  background: #f8f9fa;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.p-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  width: 36px;
  height: 36px;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 1rem;
  }
  
  .main-nav {
    display: none;
  }
  
  .user-details {
    display: none;
  }
}
</style>