<template>
  <div class="internship-list">
    <div class="header">
      <h1>Available Internships</h1>
      <Button
        label="Refresh"
        icon="pi pi-refresh"
        @click="fetchInternships"
      />
    </div>
    
    <div class="filters">
      <InputText
        v-model="filters.search"
        placeholder="Search internships..."
        class="search-input"
      />
      <Dropdown
        v-model="filters.location"
        :options="locations"
        placeholder="Filter by location"
        showClear
      />
      <Button
        label="Clear Filters"
        severity="secondary"
        @click="clearFilters"
      />
    </div>
    
    <div class="internship-grid">
      <Card v-for="internship in filteredInternships" :key="internship.id" class="internship-card">
        <template #title>{{ internship.title }}</template>
        <template #subtitle>{{ internship.company_name }}</template>
        <template #content>
          <div class="internship-details">
            <p class="description">{{ internship.description.substring(0, 200) }}...</p>
            <div class="details-grid">
              <div class="detail">
                <i class="pi pi-map-marker"></i>
                <span>{{ internship.location || 'Remote' }}</span>
              </div>
              <div class="detail">
                <i class="pi pi-money-bill"></i>
                <span>{{ internship.stipend ? `₹${internship.stipend}/month` : 'Unpaid' }}</span>
              </div>
              <div class="detail">
                <i class="pi pi-calendar"></i>
                <span>Apply by {{ formatDate(internship.last_date) }}</span>
              </div>
            </div>
            <div v-if="hasApplied(internship.id)" class="applied-badge">
              <i class="pi pi-check"></i>
              Applied
            </div>
          </div>
        </template>
        <template #footer>
          <div class="card-footer">
            <Button
              label="View Details"
              icon="pi pi-eye"
              @click="viewInternship(internship.id)"
              outlined
            />
            <Button
              v-if="!hasApplied(internship.id)"
              label="Apply Now"
              icon="pi pi-send"
              @click="applyForInternship(internship)"
              :disabled="isPastDeadline(internship.last_date)"
              severity="success"
            />
            <Button
              v-else
              label="View Application"
              icon="pi pi-file"
              @click="viewApplication(internship.id)"
              severity="info"
            />
          </div>
        </template>
      </Card>
    </div>
    
    <Dialog
      v-model:visible="showInternshipDialog"
      :header="selectedInternship?.title"
      :style="{ width: '50vw' }"
      :modal="true"
    >
      <div v-if="selectedInternship" class="internship-details-dialog">
        <div class="company-info">
          <h3>{{ selectedInternship.company_name }}</h3>
          <p>{{ selectedInternship.company_description }}</p>
        </div>
        
        <div class="section">
          <h4>Description</h4>
          <p>{{ selectedInternship.description }}</p>
        </div>
        
        <div v-if="selectedInternship.requirements" class="section">
          <h4>Requirements</h4>
          <p>{{ selectedInternship.requirements }}</p>
        </div>
        
        <div class="details-summary">
          <div class="detail-item">
            <i class="pi pi-map-marker"></i>
            <div>
              <strong>Location</strong>
              <p>{{ selectedInternship.location || 'Remote' }}</p>
            </div>
          </div>
          <div class="detail-item">
            <i class="pi pi-money-bill"></i>
            <div>
              <strong>Stipend</strong>
              <p>{{ selectedInternship.stipend ? `₹${selectedInternship.stipend}/month` : 'Unpaid' }}</p>
            </div>
          </div>
          <div class="detail-item">
            <i class="pi pi-calendar"></i>
            <div>
              <strong>Last Date to Apply</strong>
              <p>{{ formatDate(selectedInternship.last_date) }}</p>
            </div>
          </div>
          <div class="detail-item">
            <i class="pi pi-clock"></i>
            <div>
              <strong>Posted On</strong>
              <p>{{ formatDate(selectedInternship.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <Button
          label="Close"
          icon="pi pi-times"
          @click="showInternshipDialog = false"
          text
        />
        <Button
          v-if="!hasApplied(selectedInternship?.id)"
          label="Apply Now"
          icon="pi pi-send"
          @click="applyForInternship(selectedInternship)"
          :disabled="isPastDeadline(selectedInternship?.last_date)"
          severity="success"
        />
      </template>
    </Dialog>
    
    <Dialog
      v-model:visible="showApplyDialog"
      header="Apply for Internship"
      :style="{ width: '40vw' }"
      :modal="true"
    >
      <div class="apply-form">
        <div class="field">
          <label>Internship</label>
          <p class="internship-title">{{ applyData.internship_title }}</p>
        </div>
        
        <div class="field">
          <label>Cover Letter</label>
          <Textarea
            v-model="applyData.cover_letter"
            :rows="5"
            placeholder="Write your cover letter here..."
            class="w-full"
          />
        </div>
        
        <div class="field">
          <label>Resume</label>
          <div class="resume-upload">
            <p v-if="currentResume">{{ currentResume }}</p>
            <p v-else class="no-resume">No resume uploaded</p>
            <Button
              label="Upload Resume"
              icon="pi pi-upload"
              @click="uploadResume"
              outlined
              size="small"
            />
          </div>
        </div>
      </div>
      <template #footer>
        <Button
          label="Cancel"
          icon="pi pi-times"
          @click="showApplyDialog = false"
          text
        />
        <Button
          label="Submit Application"
          icon="pi pi-send"
          @click="submitApplication"
          :disabled="!currentResume"
          severity="success"
        />
      </template>
    </Dialog>
    
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
import Dropdown from 'primevue/dropdown'
import Dialog from 'primevue/dialog'
import Textarea from 'primevue/textarea'
import Toast from 'primevue/toast'
import axios from 'axios'

export default {
  components: {
    Card,
    Button,
    InputText,
    Dropdown,
    Dialog,
    Textarea,
    Toast
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    
    const internships = ref([])
    const myApplications = ref([])
    const filters = ref({
      search: '',
      location: ''
    })
    const locations = ref([])
    const showInternshipDialog = ref(false)
    const selectedInternship = ref(null)
    const showApplyDialog = ref(false)
    const applyData = ref({
      internship_id: null,
      internship_title: '',
      cover_letter: ''
    })
    const currentResume = ref('')
    
    const fetchInternships = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const [internshipsRes, applicationsRes] = await Promise.all([
          axios.get('/api/internships', { headers }),
          axios.get('/api/my-applications', { headers })
        ])
        
        internships.value = internshipsRes.data
        myApplications.value = applicationsRes.data
        
        const uniqueLocations = [...new Set(internships.value
          .map(i => i.location)
          .filter(Boolean)
        )]
        locations.value = uniqueLocations
        
        fetchCurrentResume()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load internships',
          life: 5000
        })
      }
    }
    
    const fetchCurrentResume = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const response = await axios.get('/api/profile', { headers })
        if (response.data.resume_path) {
          currentResume.value = response.data.resume_path.split('_').pop()
        }
      } catch (error) {
        console.error('Error fetching resume:', error)
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
          currentResume.value = file.name
          
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Resume uploaded successfully',
            life: 3000
          })
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
    
    const filteredInternships = computed(() => {
      return internships.value.filter(internship => {
        const matchesSearch = !filters.value.search ||
          internship.title.toLowerCase().includes(filters.value.search.toLowerCase()) ||
          internship.company_name.toLowerCase().includes(filters.value.search.toLowerCase()) ||
          internship.description.toLowerCase().includes(filters.value.search.toLowerCase())
        
        const matchesLocation = !filters.value.location ||
          internship.location === filters.value.location
        
        return matchesSearch && matchesLocation
      })
    })
    
    const hasApplied = (internshipId) => {
      return myApplications.value.some(app => app.internship_id === internshipId)
    }
    
    const isPastDeadline = (lastDate) => {
      if (!lastDate) return false
      return new Date(lastDate) < new Date()
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const viewInternship = (internshipId) => {
      selectedInternship.value = internships.value.find(i => i.id === internshipId)
      showInternshipDialog.value = true
    }
    
    const viewApplication = (internshipId) => {
      router.push('/my-applications')
    }
    
    const applyForInternship = (internship) => {
      if (isPastDeadline(internship.last_date)) {
        toast.add({
          severity: 'warn',
          summary: 'Cannot Apply',
          detail: 'Application deadline has passed',
          life: 5000
        })
        return
      }
      
      if (!currentResume.value) {
        toast.add({
          severity: 'warn',
          summary: 'Resume Required',
          detail: 'Please upload your resume before applying',
          life: 5000
        })
        return
      }
      
      applyData.value = {
        internship_id: internship.id,
        internship_title: internship.title,
        cover_letter: ''
      }
      showApplyDialog.value = true
    }
    
    const submitApplication = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const response = await axios.post(
          `/api/apply/${applyData.value.internship_id}`,
          { cover_letter: applyData.value.cover_letter },
          { headers }
        )
        
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Application submitted successfully',
          life: 3000
        })
        
        showApplyDialog.value = false
        fetchInternships()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: error.response?.data?.error || 'Failed to submit application',
          life: 5000
        })
      }
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        location: ''
      }
    }
    
    onMounted(fetchInternships)
    
    return {
      internships,
      filters,
      locations,
      filteredInternships,
      showInternshipDialog,
      selectedInternship,
      showApplyDialog,
      applyData,
      currentResume,
      hasApplied,
      isPastDeadline,
      formatDate,
      fetchInternships,
      viewInternship,
      viewApplication,
      applyForInternship,
      submitApplication,
      uploadResume,
      clearFilters
    }
  }
}
</script>

<style scoped>
.internship-list {
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

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: center;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.internship-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.internship-card {
  transition: transform 0.2s;
}

.internship-card:hover {
  transform: translateY(-2px);
}

.internship-details {
  position: relative;
}

.description {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.detail i {
  color: #667eea;
}

.applied-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #4caf50;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.internship-details-dialog {
  padding: 1rem 0;
}

.company-info {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.company-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.section {
  margin-bottom: 1.5rem;
}

.section h4 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.section p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.details-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 2rem;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.detail-item i {
  color: #667eea;
  margin-top: 0.25rem;
}

.detail-item strong {
  display: block;
  color: #2c3e50;
  font-size: 0.9rem;
}

.detail-item p {
  margin: 0.25rem 0 0 0;
  color: #666;
}

.apply-form {
  padding: 1rem 0;
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

.internship-title {
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.resume-upload {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.no-resume {
  color: #999;
  font-style: italic;
  margin: 0;
}
</style>