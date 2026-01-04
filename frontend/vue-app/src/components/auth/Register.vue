<template>
  <div class="register-container">
    <div class="register-left">
      <div class="welcome-section">
        <h1>Join InternPort Today</h1>
        <p class="subtitle">Start your journey to the perfect internship</p>
        <div class="benefits">
          <div class="benefit">
            <div class="benefit-icon">
              <i class="pi pi-briefcase"></i>
            </div>
            <div class="benefit-content">
              <h4>For Students</h4>
              <p>Find internships that match your skills and career goals</p>
            </div>
          </div>
          <div class="benefit">
            <div class="benefit-icon">
              <i class="pi pi-building"></i>
            </div>
            <div class="benefit-content">
              <h4>For Companies</h4>
              <p>Discover talented students and build your future workforce</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="register-right">
      <div class="register-card">
        <div class="register-header">
          <h2>Create Account</h2>
          <p>Choose your account type and fill in the details</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="account-type">
            <label>I am a</label>
            <div class="type-options">
              <div 
                class="type-option"
                :class="{ 'selected': form.role === 'student', 'not-selected': form.role === 'company' }"
                @click="form.role = 'student'"
              >
                <i class="pi pi-user"></i>
                <div>
                  <h5>Student</h5>
                  <p>Looking for internships</p>
                </div>
                <i class="pi pi-check" v-if="form.role === 'student'"></i>
              </div>
              <div 
                class="type-option"
                :class="{ 'selected': form.role === 'company', 'not-selected': form.role === 'student' }"
                @click="form.role = 'company'"
              >
                <i class="pi pi-building"></i>
                <div>
                  <h5>Company</h5>
                  <p>Hiring interns</p>
                </div>
                <i class="pi pi-check" v-if="form.role === 'company'"></i>
              </div>
            </div>
          </div>
          
          <div class="form-section">
            <h4>Account Information</h4>
            <div class="field">
              <label for="email">Email Address *</label>
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
            
            <div class="grid-2">
              <div class="field">
                <label for="password">Password *</label>
                  <Password
                    id="password"
                    v-model="form.password"
                    placeholder="Create password"
                    class="w-full"
                    :class="{ 'p-invalid': errors.password }"
                    toggleMask
                    :feedback="true"
                    autocomplete="new-password"
                  />
                <small v-if="errors.password" class="p-error">{{ errors.password }}</small>
              </div>
              
              <div class="field">
                <label for="confirmPassword">Confirm Password *</label>
                <Password
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  placeholder="Confirm password"
                  class="w-full"
                  :class="{ 'p-invalid': errors.confirmPassword }"
                  toggleMask
                  :feedback="false"
                  autocomplete="new-password"
                />
                <small v-if="errors.confirmPassword" class="p-error">{{ errors.confirmPassword }}</small>
              </div>
            </div>
            
            <div class="password-rules">
              <p class="rules-title">Password must contain:</p>
              <div class="rules">
                <span :class="{ 'valid': isLengthValid }">
                  <i :class="isLengthValid ? 'pi pi-check-circle' : 'pi pi-circle'"></i>
                  At least 8 characters
                </span>
                <span :class="{ 'valid': hasUppercase }">
                  <i :class="hasUppercase ? 'pi pi-check-circle' : 'pi pi-circle'"></i>
                  One uppercase letter
                </span>
                <span :class="{ 'valid': hasLowercase }">
                  <i :class="hasLowercase ? 'pi pi-check-circle' : 'pi pi-circle'"></i>
                  One lowercase letter
                </span>
                <span :class="{ 'valid': hasNumber }">
                  <i :class="hasNumber ? 'pi pi-check-circle' : 'pi pi-circle'"></i>
                  One number
                </span>
              </div>
            </div>
          </div>
          
          <div class="form-section" v-if="form.role === 'student'">
            <h4>Student Information</h4>
            <div class="field">
              <label for="fullName">Full Name *</label>
              <span class="p-input-icon-left">
                <i class="pi pi-user" />
                <InputText
                  id="fullName"
                  v-model="form.full_name"
                  placeholder="Enter your full name"
                  class="w-full"
                  :class="{ 'p-invalid': errors.full_name }"
                />
              </span>
              <small v-if="errors.full_name" class="p-error">{{ errors.full_name }}</small>
            </div>
            
            <div class="grid-2">
              <div class="field">
                <label for="university">University</label>
                <InputText
                  id="university"
                  v-model="form.university"
                  placeholder="University name"
                  class="w-full"
                />
              </div>
              
              <div class="field">
                <label for="major">Major/Field</label>
                <InputText
                  id="major"
                  v-model="form.major"
                  placeholder="Your major"
                  class="w-full"
                />
              </div>
            </div>
          </div>
          
          <div class="form-section" v-else-if="form.role === 'company'">
            <h4>Company Information</h4>
            <div class="field">
              <label for="companyName">Company Name *</label>
              <span class="p-input-icon-left">
                <i class="pi pi-building" />
                <InputText
                  id="companyName"
                  v-model="form.company_name"
                  placeholder="Enter company name"
                  class="w-full"
                  :class="{ 'p-invalid': errors.company_name }"
                />
              </span>
              <small v-if="errors.company_name" class="p-error">{{ errors.company_name }}</small>
            </div>
            
            <div class="field">
              <label for="description">Company Description</label>
              <Textarea
                id="description"
                v-model="form.description"
                placeholder="Brief description of your company"
                :rows="3"
                class="w-full"
              />
            </div>
            
            <div class="grid-2">
              <div class="field">
                <label for="website">Website</label>
                <span class="p-input-icon-left">
                  <i class="pi pi-globe" />
                  <InputText
                    id="website"
                    v-model="form.website"
                    placeholder="https://example.com"
                    class="w-full"
                  />
                </span>
              </div>
              
              <div class="field">
                <label for="location">Location</label>
                <span class="p-input-icon-left">
                  <i class="pi pi-map-marker" />
                  <InputText
                    id="location"
                    v-model="form.location"
                    placeholder="City, Country"
                    class="w-full"
                  />
                </span>
              </div>
            </div>
          </div>
          
          <div class="terms-agreement">
            <Checkbox
              v-model="form.agreeTerms"
              binary
              inputId="terms"
              :class="{ 'p-invalid': errors.agreeTerms }"
            />
            <label for="terms" class="ml-2">
              I agree to the <router-link to="/terms" class="terms-link">Terms of Service</router-link> and <router-link to="/privacy" class="terms-link">Privacy Policy</router-link> *
            </label>
            <small v-if="errors.agreeTerms" class="p-error block">{{ errors.agreeTerms }}</small>
          </div>
          
          <Button
            type="submit"
            label="Create Account"
            class="w-full"
            :loading="loading"
            size="large"
          />
        </form>
        
        <div class="register-footer">
          <p>Already have an account? <router-link to="/login" class="login-link">Sign in here</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Textarea from 'primevue/textarea'
import axios from 'axios'

export default {
  components: {
    InputText,
    Password,
    Button,
    Checkbox,
    Textarea
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    
    const form = ref({
      role: 'student',
      email: '',
      password: '',
      confirmPassword: '',
      full_name: '',
      university: '',
      major: '',
      company_name: '',
      description: '',
      website: '',
      location: '',
      agreeTerms: false
    })
    
    const errors = ref({})
    const loading = ref(false)
    
    const passwordRules = computed(() => {
      const password = form.value.password
      return {
        isLengthValid: password.length >= 8,
        hasUppercase: /[A-Z]/.test(password),
        hasLowercase: /[a-z]/.test(password),
        hasNumber: /[0-9]/.test(password),
        hasSpecial: /[!@#$%^&*]/.test(password)
      }
    })
    
    const { isLengthValid, hasUppercase, hasLowercase, hasNumber } = passwordRules
    
    const validateForm = () => {
      errors.value = {}
      
      if (!form.value.email) {
        errors.value.email = 'Email is required'
      } else if (!/\S+@\S+\.\S+/.test(form.value.email)) {
        errors.value.email = 'Please enter a valid email address'
      }
      
      if (!form.value.password) {
        errors.value.password = 'Password is required'
      } else if (form.value.password.length < 8) {
        errors.value.password = 'Password must be at least 8 characters'
      } else if (!/[A-Z]/.test(form.value.password)) {
        errors.value.password = 'Password must contain at least one uppercase letter'
      } else if (!/[a-z]/.test(form.value.password)) {
        errors.value.password = 'Password must contain at least one lowercase letter'
      } else if (!/[0-9]/.test(form.value.password)) {
        errors.value.password = 'Password must contain at least one number'
      }
      
      if (form.value.password !== form.value.confirmPassword) {
        errors.value.confirmPassword = 'Passwords do not match'
      }
      
      if (form.value.role === 'student' && !form.value.full_name?.trim()) {
        errors.value.full_name = 'Full name is required'
      }
      
      if (form.value.role === 'company' && !form.value.company_name?.trim()) {
        errors.value.company_name = 'Company name is required'
      }
      
      if (!form.value.agreeTerms) {
        errors.value.agreeTerms = 'You must agree to the terms and conditions'
      }
      
      return Object.keys(errors.value).length === 0
    }
    
    const handleRegister = async () => {
      if (!validateForm()) return
      
      loading.value = true
      
      try {
        const payload = {
          email: form.value.email,
          password: form.value.password,
          role: form.value.role
        }
        
        if (form.value.role === 'student') {
          payload.full_name = form.value.full_name
          if (form.value.university) payload.university = form.value.university
          if (form.value.major) payload.major = form.value.major
        } else if (form.value.role === 'company') {
          payload.company_name = form.value.company_name
          if (form.value.description) payload.description = form.value.description
          if (form.value.website) payload.website = form.value.website
          if (form.value.location) payload.location = form.value.location
        }
        
        const response = await axios.post('/register', payload)
        
        store.dispatch('login', {
          token: response.data.token,
          user: response.data.user
        })
        
        toast.add({
          severity: 'success',
          summary: 'Account Created!',
          detail: 'Registration successful. Welcome to InternPort!',
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
        const errorMessage = error.response?.data?.error || 'Registration failed. Please try again.'
        toast.add({
          severity: 'error',
          summary: 'Registration Failed',
          detail: errorMessage,
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
      isLengthValid,
      hasUppercase,
      hasLowercase,
      hasNumber,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.register-left {
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

.benefits {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.benefit {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.benefit-icon {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 12px;
  flex-shrink: 0;
}

.benefit-icon i {
  font-size: 1.5rem;
}

.benefit-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.benefit-content p {
  margin: 0;
  opacity: 0.9;
  line-height: 1.6;
}

.register-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

.register-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.register-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.register-header h2 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.register-header p {
  color: #7f8c8d;
  margin: 0;
}

.register-form {
  margin-bottom: 2rem;
}

.account-type {
  margin-bottom: 2.5rem;
}

.account-type label {
  display: block;
  margin-bottom: 0.75rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.95rem;
}

.type-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.type-option {
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.type-option.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.type-option.not-selected {
  opacity: 0.6;
}

.type-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.type-option i:first-child {
  font-size: 2rem;
  color: #667eea;
}

.type-option div {
  flex: 1;
}

.type-option h5 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.type-option p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.type-option i:last-child {
  color: #667eea;
  font-size: 1.25rem;
}

.form-section {
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e0e0e0;
}

.form-section h4 {
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.95rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.p-input-icon-left {
  display: block;
}

.p-input-icon-left i {
  color: #7f8c8d;
}

.password-rules {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.rules-title {
  margin: 0 0 0.75rem 0;
  color: #5a6c7d;
  font-size: 0.9rem;
  font-weight: 500;
}

.rules {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.rules span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #7f8c8d;
  font-size: 0.85rem;
}

.rules span.valid {
  color: #4caf50;
}

.rules i {
  font-size: 0.9rem;
}

.terms-agreement {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: flex-start;
}

.terms-agreement label {
  color: #5a6c7d;
  line-height: 1.5;
  margin: 0;
}

.terms-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.terms-link:hover {
  text-decoration: underline;
}

.block {
  display: block;
  margin-top: 0.5rem;
}

.register-footer {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
  color: #7f8c8d;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.login-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

@media (max-width: 992px) {
  .register-container {
    flex-direction: column;
  }
  
  .register-left {
    padding: 2rem;
  }
  
  .welcome-section h1 {
    font-size: 2rem;
  }
  
  .type-options {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
  
  .rules {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {
  .register-card {
    padding: 2rem;
  }
  
  .register-left {
    padding: 2rem 1rem;
  }
  
  .benefit {
    flex-direction: column;
    text-align: center;
  }
  
  .benefit-icon {
    align-self: center;
  }
}
</style>