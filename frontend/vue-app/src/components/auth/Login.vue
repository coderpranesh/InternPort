<template>
  <div class="login-container">
    <div class="login-left">
      <div class="welcome-section">
        <h1>Welcome to InternPort</h1>
        <p class="subtitle">Your gateway to internship opportunities</p>
        <div class="features">
          <div class="feature">
            <i class="pi pi-briefcase"></i>
            <span>Discover internships</span>
          </div>
          <div class="feature">
            <i class="pi pi-building"></i>
            <span>Connect with companies</span>
          </div>
          <div class="feature">
            <i class="pi pi-chart-line"></i>
            <span>Track your applications</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="login-right">
      <div class="login-card">
        <div class="login-header">
          <h2>Sign In</h2>
          <p>Enter your credentials to access your account</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="field">
            <label for="email">Email Address</label>
            <span class="p-input-icon-left">
              <i class="pi pi-envelope" />
              <InputText
                id="email"
                v-model="form.email"
                type="email"
                placeholder="Enter your email"
                class="w-full"
                :class="{ 'p-invalid': errors.email }"
              />
            </span>
            <small v-if="errors.email" class="p-error">{{ errors.email }}</small>
          </div>
          
          <div class="field">
            <div class="label-row">
              <label for="password">Password</label>
              <router-link to="/forgot-password" class="forgot-link">Forgot password?</router-link>
            </div>
            <span class="p-input-icon-left">
              <i class="pi pi-lock" />
              <Password
                id="password"
                v-model="form.password"
                placeholder="Enter your password"
                class="w-full"
                :class="{ 'p-invalid': errors.password }"
                toggleMask
                :feedback="false"
                autocomplete="current-password"
              />
            </span>
            <small v-if="errors.password" class="p-error">{{ errors.password }}</small>
          </div>
          
          <div class="remember-me">
            <Checkbox
              v-model="form.rememberMe"
              binary
              inputId="remember"
            />
            <label for="remember" class="ml-2">Remember me</label>
          </div>
          
          <Button
            type="submit"
            label="Sign In"
            class="w-full"
            :loading="loading"
            size="large"
          />
          
          <Divider>
            <span class="divider-text">or continue with</span>
          </Divider>
          
          <div class="social-login">
            <Button
              icon="pi pi-google"
              label="Google"
              outlined
              class="w-full"
              @click="socialLogin('google')"
            />
          </div>
        </form>
        
        <div class="login-footer">
          <p>Don't have an account? <router-link to="/register" class="register-link">Create account</router-link></p>
        </div>
        
        <div class="demo-credentials">
          <h4>Demo Accounts</h4>
          <div class="demo-account" @click="fillDemo('admin')">
            <i class="pi pi-shield"></i>
            <div>
              <strong>Admin</strong>
              <span>admin@internport.com / admin123</span>
            </div>
            <i class="pi pi-chevron-right"></i>
          </div>
          <div class="demo-account" @click="fillDemo('student')">
            <i class="pi pi-user"></i>
            <div>
              <strong>Student</strong>
              <span>student@internport.com / student123</span>
            </div>
            <i class="pi pi-chevron-right"></i>
          </div>
          <div class="demo-account" @click="fillDemo('company')">
            <i class="pi pi-building"></i>
            <div>
              <strong>Company</strong>
              <span>company@internport.com / company123</span>
            </div>
            <i class="pi pi-chevron-right"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Divider from 'primevue/divider'
import axios from 'axios'

export default {
  components: {
    InputText,
    Password,
    Button,
    Checkbox,
    Divider
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    
    const form = ref({
      email: '',
      password: '',
      rememberMe: false
    })
    
    const errors = ref({})
    const loading = ref(false)
    
    const validateForm = () => {
      errors.value = {}
      
      if (!form.value.email) {
        errors.value.email = 'Email is required'
      } else if (!/\S+@\S+\.\S+/.test(form.value.email)) {
        errors.value.email = 'Please enter a valid email address'
      }
      
      if (!form.value.password) {
        errors.value.password = 'Password is required'
      }
      
      return Object.keys(errors.value).length === 0
    }
    
    const handleLogin = async () => {
      if (!validateForm()) return
      
      loading.value = true
      
      try {
        const response = await axios.post('/login', {
          email: form.value.email,
          password: form.value.password
        })
        
        store.dispatch('login', {
          token: response.data.token,
          user: response.data.user
        })
        
        if (form.value.rememberMe) {
          localStorage.setItem('rememberedEmail', form.value.email)
        }
        
        toast.add({
          severity: 'success',
          summary: 'Welcome back!',
          detail: 'Login successful',
          life: 3000
        })
        
        const userRole = response.data.user.role
        switch (userRole) {
          case 'student':
            router.push('/student')
            break
          case 'company':
            router.push('/company')
            break
          case 'admin':
            router.push('/admin')
            break
          default:
            router.push('/')
        }
      } catch (error) {
        const errorMessage = error.response?.data?.error || 'Login failed. Please check your credentials.'
        toast.add({
          severity: 'error',
          summary: 'Authentication Failed',
          detail: errorMessage,
          life: 5000
        })
      } finally {
        loading.value = false
      }
    }
    
    const fillDemo = (role) => {
      switch (role) {
        case 'admin':
          form.value.email = 'admin@internport.com'
          form.value.password = 'admin123'
          break
        case 'student':
          form.value.email = 'student@internport.com'
          form.value.password = 'student123'
          break
        case 'company':
          form.value.email = 'company@internport.com'
          form.value.password = 'company123'
          break
      }
      
      toast.add({
        severity: 'info',
        summary: 'Demo Credentials Loaded',
        detail: `Click Sign In to continue as ${role}`,
        life: 3000
      })
    }
    
    const socialLogin = (provider) => {
      toast.add({
        severity: 'info',
        summary: 'Coming Soon',
        detail: `${provider} login will be available soon`,
        life: 3000
      })
    }
    
    onMounted(() => {
      const rememberedEmail = localStorage.getItem('rememberedEmail')
      if (rememberedEmail) {
        form.value.email = rememberedEmail
      }
    })
    
    return {
      form,
      errors,
      loading,
      handleLogin,
      fillDemo,
      socialLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem;
  display: flex;
  align-items: center;
}

.welcome-section {
  max-width: 500px;
}

.welcome-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 3rem;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.1rem;
}

.feature i {
  font-size: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem;
  border-radius: 50%;
}

.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.login-header h2 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.login-header p {
  color: #7f8c8d;
  margin: 0;
}

.login-form {
  margin-bottom: 2rem;
}

.field {
  margin-bottom: 1.75rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.95rem;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.forgot-link {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.p-input-icon-left {
  display: block;
}

.p-input-icon-left i {
  color: #7f8c8d;
}

.remember-me {
  display: flex;
  align-items: center;
  margin-bottom: 1.75rem;
}

.remember-me label {
  margin: 0;
  color: #5a6c7d;
  cursor: pointer;
}

.divider-text {
  color: #7f8c8d;
  padding: 0 1rem;
  background: white;
  font-size: 0.9rem;
}

.social-login {
  margin-top: 1.5rem;
}

.login-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
  color: #7f8c8d;
}

.register-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.register-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.demo-credentials {
  margin-top: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  border: 1px solid #dee2e6;
}

.demo-credentials h4 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-size: 1rem;
  text-align: center;
}

.demo-account {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e0e0e0;
}

.demo-account:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.demo-account i:first-child {
  font-size: 1.25rem;
  color: #667eea;
}

.demo-account div {
  flex: 1;
}

.demo-account strong {
  display: block;
  color: #2c3e50;
  font-size: 0.9rem;
}

.demo-account span {
  display: block;
  color: #7f8c8d;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.demo-account i:last-child {
  color: #7f8c8d;
}

@media (max-width: 992px) {
  .login-container {
    flex-direction: column;
  }
  
  .login-left {
    padding: 2rem;
  }
  
  .welcome-section h1 {
    font-size: 2rem;
  }
}

@media (max-width: 576px) {
  .login-card {
    padding: 2rem;
  }
  
  .login-left {
    padding: 2rem 1rem;
  }
}
</style>