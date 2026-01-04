<template>
  <div class="forgot-password-container">
    <div class="forgot-left">
      <div class="welcome-section">
        <h1>Reset Your Password</h1>
        <p class="subtitle">Enter your email to receive a password reset link</p>
        <div class="features">
          <div class="feature">
            <i class="pi pi-envelope"></i>
            <span>We'll send you a reset link</span>
          </div>
          <div class="feature">
            <i class="pi pi-shield"></i>
            <span>Secure password reset process</span>
          </div>
          <div class="feature">
            <i class="pi pi-clock"></i>
            <span>Link expires in 24 hours</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="forgot-right">
      <div class="forgot-card">
        <div class="forgot-header">
          <h2>Forgot Password</h2>
          <p>Enter your email address associated with your account</p>
        </div>
        
        <form @submit.prevent="handleReset" class="forgot-form">
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
                autocomplete="email"
              />
            </span>
            <small v-if="errors.email" class="p-error">{{ errors.email }}</small>
          </div>
          
          <Button
            type="submit"
            label="Send Reset Link"
            class="w-full"
            :loading="loading"
            size="large"
          />
          
          <Divider />
          
          <div class="back-to-login">
            <router-link to="/login" class="login-link">
              <i class="pi pi-arrow-left"></i>
              Back to Login
            </router-link>
          </div>
        </form>
        
        <div class="forgot-footer">
          <p>Don't have an account? <router-link to="/register" class="register-link">Create account</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Divider from 'primevue/divider'

export default {
  components: {
    InputText,
    Button,
    Divider
  },
  setup() {
    const router = useRouter()
    const toast = useToast()
    
    const form = ref({
      email: ''
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
      
      return Object.keys(errors.value).length === 0
    }
    
    const handleReset = async () => {
      if (!validateForm()) return
      
      loading.value = true
      
      try {
        // This would be a real API call in production
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        toast.add({
          severity: 'success',
          summary: 'Reset Link Sent',
          detail: 'Check your email for password reset instructions',
          life: 5000
        })
        
        router.push('/login')
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to send reset link. Please try again.',
          life: 5000
        })
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      errors,
      loading,
      handleReset
    }
  }
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.forgot-left {
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

.forgot-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.forgot-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
}

.forgot-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.forgot-header h2 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.forgot-header p {
  color: #7f8c8d;
  margin: 0;
}

.forgot-form {
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

.p-input-icon-left {
  display: block;
}

.p-input-icon-left i {
  color: #7f8c8d;
}

.back-to-login {
  text-align: center;
  margin-top: 1.5rem;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s;
}

.login-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.forgot-footer {
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

@media (max-width: 992px) {
  .forgot-password-container {
    flex-direction: column;
  }
  
  .forgot-left {
    padding: 2rem;
  }
  
  .welcome-section h1 {
    font-size: 2rem;
  }
}

@media (max-width: 576px) {
  .forgot-card {
    padding: 2rem;
  }
  
  .forgot-left {
    padding: 2rem 1rem;
  }
}
</style>