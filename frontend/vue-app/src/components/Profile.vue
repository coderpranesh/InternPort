<template>
  <div class="profile">
    <div class="header">
      <h1>My Profile</h1>
      <Button
        label="Back to Dashboard"
        icon="pi pi-arrow-left"
        @click="goToDashboard"
        outlined
      />
    </div>
    
    <div class="profile-container">
      <Card class="profile-card">
        <template #title>Profile Information</template>
        <template #content>
          <div v-if="loading" class="loading">
            <ProgressSpinner />
          </div>
          
          <form v-else @submit.prevent="updateProfile">
            <div class="field">
              <label for="email">Email</label>
              <InputText
                id="email"
                v-model="profile.email"
                type="email"
                disabled
                class="w-full"
              />
            </div>
            
            <div v-if="userRole === 'student'" class="student-fields">
              <div class="field">
                <label for="full_name">Full Name *</label>
                <InputText
                  id="full_name"
                  v-model="profile.full_name"
                  placeholder="Enter your full name"
                  class="w-full"
                  :class="{ 'p-invalid': errors.full_name }"
                />
                <small v-if="errors.full_name" class="p-error">{{ errors.full_name }}</small>
              </div>
              
              <div class="grid-2">
                <div class="field">
                  <label for="university">University</label>
                  <InputText
                    id="university"
                    v-model="profile.university"
                    placeholder="Enter your university"
                    class="w-full"
                  />
                </div>
                
                <div class="field">
                  <label for="major">Major</label>
                  <InputText
                    id="major"
                    v-model="profile.major"
                    placeholder="Enter your major"
                    class="w-full"
                  />
                </div>
              </div>
              
              <div class="grid-2">
                <div class="field">
                  <label for="year_of_study">Year of Study</label>
                  <Dropdown
                    id="year_of_study"
                    v-model="profile.year_of_study"
                    :options="yearOptions"
                    placeholder="Select year"
                    class="w-full"
                  />
                </div>
                
                <div class="field">
                  <label for="phone">Phone</label>
                  <InputText
                    id="phone"
                    v-model="profile.phone"
                    placeholder="Enter phone number"
                    class="w-full"
                  />
                </div>
              </div>
              
              <div class="field">
                <label>Resume</label>
                <div class="resume-section">
                  <p v-if="profile.resume_path" class="resume-info">
                    Current resume: {{ profile.resume_path.split('_').pop() }}
                  </p>
                  <p v-else class="resume-info no-resume">No resume uploaded</p>
                  <Button
                    label="Upload Resume"
                    icon="pi pi-upload"
                    @click="uploadResume"
                    outlined
                  />
                  <small class="resume-help">Accepted formats: PDF, DOC, DOCX (Max: 16MB)</small>
                </div>
              </div>
            </div>
            
            <div v-else-if="userRole === 'company'" class="company-fields">
              <div class="field">
                <label for="company_name">Company Name *</label>
                <InputText
                  id="company_name"
                  v-model="profile.company_name"
                  placeholder="Enter company name"
                  class="w-full"
                  :class="{ 'p-invalid': errors.company_name }"
                />
                <small v-if="errors.company_name" class="p-error">{{ errors.company_name }}</small>
              </div>
              
              <div class="field">
                <label for="description">Description</label>
                <Textarea
                  id="description"
                  v-model="profile.description"
                  :rows="4"
                  placeholder="Describe your company"
                  class="w-full"
                />
              </div>
              
              <div class="grid-2">
                <div class="field">
                  <label for="website">Website</label>
                  <InputText
                    id="website"
                    v-model="profile.website"
                    placeholder="https://example.com"
                    class="w-full"
                  />
                </div>
                
                <div class="field">
                  <label for="location">Location</label>
                  <InputText
                    id="location"
                    v-model="profile.location"
                    placeholder="Company location"
                    class="w-full"
                  />
                </div>
              </div>
            </div>
            
            <div class="form-actions">
              <Button
                type="submit"
                label="Save Changes"
                icon="pi pi-check"
                :loading="saving"
                severity="success"
              />
              <Button
                label="Cancel"
                icon="pi pi-times"
                @click="fetchProfile"
                severity="secondary"
              />
            </div>
          </form>
        </template>
      </Card>
      
      <Card class="account-card" v-if="userRole !== 'admin'">
        <template #title>Account Statistics</template>
        <template #content>
          <div v-if="userRole === 'student'" class="student-stats">
            <div class="stat-item">
              <i class="pi pi-briefcase"></i>
              <div>
                <p class="stat-value">{{ stats.applications || 0 }}</p>
                <p class="stat-label">Applications</p>
              </div>
            </div>
            <div class="stat-item">
              <i class="pi pi-clock"></i>
              <div>
                <p class="stat-value">{{ stats.pending || 0 }}</p>
                <p class="stat-label">Pending</p>
              </div>
            </div>
            <div class="stat-item">
              <i class="pi pi-check-circle"></i>
              <div>
                <p class="stat-value">{{ stats.selected || 0 }}</p>
                <p class="stat-label">Selected</p>
              </div>
            </div>
          </div>
          
          <div v-else-if="userRole === 'company'" class="company-stats">
            <div class="stat-item">
              <i class="pi pi-briefcase"></i>
              <div>
                <p class="stat-value">{{ stats.internships || 0 }}</p>
                <p class="stat-label">Internships</p>
              </div>
            </div>
            <div class="stat-item">
              <i class="pi pi-users"></i>
              <div>
                <p class="stat-value">{{ stats.applications || 0 }}</p>
                <p class="stat-label">Applications</p>
              </div>
            </div>
            <div class="stat-item">
              <i class="pi pi-check-circle"></i>
              <div>
                <p class="stat-value">{{ stats.selected || 0 }}</p>
                <p class="stat-label">Selected</p>
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>
    
    <Toast />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Dropdown from 'primevue/dropdown'
import ProgressSpinner from 'primevue/progressspinner'
import Toast from 'primevue/toast'
import axios from 'axios'

export default {
  components: {
    Card,
    Button,
    InputText,
    Textarea,
    Dropdown,
    ProgressSpinner,
    Toast
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    
    const profile = ref({})
    const loading = ref(true)
    const saving = ref(false)
    const errors = ref({})
    const stats = ref({})
    
    const userRole = computed(() => store.getters.userRole)
    
    const yearOptions = [
      '1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year', 'Graduate'
    ]
    
    const fetchProfile = async () => {
      loading.value = true
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const response = await axios.get('/api/profile', { headers })
        profile.value = response.data
        
        fetchStats()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load profile',
          life: 5000
        })
      } finally {
        loading.value = false
      }
    }
    
    const fetchStats = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        if (userRole.value === 'student') {
          const response = await axios.get('/api/my-applications', { headers })
          const applications = response.data
          stats.value = {
            applications: applications.length,
            pending: applications.filter(a => a.status === 'APPLIED').length,
            selected: applications.filter(a => a.status === 'SELECTED').length
          }
        } else if (userRole.value === 'company') {
          const [internshipsRes, applicationsRes] = await Promise.all([
            axios.get('/api/internships', { headers }),
            axios.get('/api/applications/all', { headers }).catch(() => ({ data: [] }))
          ])
          
          const applications = applicationsRes.data
          stats.value = {
            internships: internshipsRes.data.length,
            applications: applications.length,
            selected: applications.filter(a => a.status === 'SELECTED').length
          }
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }
    
    const validateProfile = () => {
      errors.value = {}
      
      if (userRole.value === 'student') {
        if (!profile.value.full_name?.trim()) {
          errors.value.full_name = 'Full name is required'
        }
      } else if (userRole.value === 'company') {
        if (!profile.value.company_name?.trim()) {
          errors.value.company_name = 'Company name is required'
        }
      }
      
      return Object.keys(errors.value).length === 0
    }
    
    const updateProfile = async () => {
      if (!validateProfile()) return
      
      saving.value = true
      
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        await axios.put('/api/profile', profile.value, { headers })
        
        store.dispatch('updateUser', {
          full_name: profile.value.full_name,
          company_name: profile.value.company_name
        })
        
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Profile updated successfully',
          life: 3000
        })
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: error.response?.data?.error || 'Failed to update profile',
          life: 5000
        })
      } finally {
        saving.value = false
      }
    }
    
    const uploadResume = () => {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = '.pdf,.doc,.docx'
      
      input.onchange = async (e) => {
        const file = e.target.files[0]
        if (!file) return
        
        const formData = new FormData()
        formData.append('resume', file)
        
        try {
          const token = store.state.token
          const headers = {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
          
          const response = await axios.post('/api/upload-resume', formData, { headers })
          profile.value.resume_path = response.data.filename
          
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Resume uploaded successfully',
            life: 3000
          })
          
          fetchStats()
        } catch (error) {
          toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.error || 'Failed to upload resume',
            life: 5000
          })
        }
      }
      
      input.click()
    }
    
    const goToDashboard = () => {
      router.push('/')
    }
    
    onMounted(fetchProfile)
    
    return {
      profile,
      loading,
      saving,
      errors,
      stats,
      userRole,
      yearOptions,
      fetchProfile,
      updateProfile,
      uploadResume,
      goToDashboard
    }
  }
}
</script>

<style scoped>
.profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #2c3e50;
  margin: 0;
}

.profile-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

@media (max-width: 900px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
}

.profile-card,
.account-card {
  height: fit-content;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.resume-section {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.resume-info {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.resume-info.no-resume {
  color: #999;
  font-style: italic;
}

.resume-help {
  display: block;
  margin-top: 0.5rem;
  color: #7f8c8d;
  font-size: 0.85rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.student-stats,
.company-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.stat-item i {
  font-size: 1.5rem;
  color: #667eea;
}

.stat-value {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.stat-label {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}
</style>