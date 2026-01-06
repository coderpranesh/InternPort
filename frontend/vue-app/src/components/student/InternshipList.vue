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
    
    <div v-if="loading" class="loading-container">
      <ProgressSpinner />
    </div>
    
    <div v-else-if="filteredInternships.length === 0" class="no-data">
      <i class="pi pi-inbox" style="font-size: 3rem; color: var(--surface-400);"></i>
      <p>No internships found</p>
    </div>
    
    <div v-else class="internship-grid">
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
                <span>{{ internship.stipend || 'Unpaid' }}</span>
              </div>
              <div class="detail">
                <i class="pi pi-calendar"></i>
                <span>Apply by {{ formatDate(internship.last_date) }}</span>
              </div>
              <div class="detail">
                <i class="pi pi-clock"></i>
                <span>
                  <Tag :severity="internship.is_active ? 'success' : 'danger'">
                    {{ internship.is_active ? 'Open' : 'Closed' }}
                  </Tag>
                </span>
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
              @click="viewInternship(internship)"
              outlined
            />
            <Button
              v-if="!hasApplied(internship.id)"
              label="Apply Now"
              icon="pi pi-send"
              @click="applyForInternship(internship)"
              :disabled="!internship.is_active"
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
          <p class="company-description">{{ selectedInternship.company_description || 'No description available' }}</p>
        </div>
        
        <div class="section">
          <h4>Description</h4>
          <p>{{ selectedInternship.description }}</p>
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
              <p>{{ selectedInternship.stipend || 'Unpaid' }}</p>
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
          <div class="detail-item">
            <i class="pi pi-info-circle"></i>
            <div>
              <strong>Status</strong>
              <p>
                <Tag :severity="selectedInternship.is_active ? 'success' : 'danger'">
                  {{ selectedInternship.is_active ? 'Open' : 'Closed' }}
                </Tag>
              </p>
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
          :disabled="!selectedInternship?.is_active"
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
          <label for="coverLetter">Cover Letter</label>
          <Textarea
            v-model="applyData.cover_letter"
            id="coverLetter"
            :rows="5"
            placeholder="Write your cover letter here..."
            class="w-full"
          />
        </div>
        
        <div class="field">
          <label for="resume">Resume (Required)</label>
          <div class="resume-upload">
            <FileUpload
              id="resume"
              mode="basic"
              accept=".pdf,.doc,.docx"
              :maxFileSize="16000000"
              :auto="false"
              chooseLabel="Select Resume"
              customUpload
              @select="onFileSelect"
              :class="{ 'p-invalid': fileError }"
            />
            <div v-if="selectedFile" class="file-info">
              <i class="pi pi-file"></i>
              <span>{{ selectedFile.name }}</span>
              <span class="file-size">({{ formatFileSize(selectedFile.size) }})</span>
              <Button
                icon="pi pi-times"
                severity="secondary"
                text
                rounded
                @click="clearFile"
              />
            </div>
            <small v-if="fileError" class="p-error">{{ fileError }}</small>
            <small class="p-text-secondary">Maximum file size: 16MB. Allowed types: PDF, DOC, DOCX</small>
          </div>
        </div>
        
        <div v-if="applyError" class="field">
          <Message severity="error">{{ applyError }}</Message>
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
          :disabled="!selectedFile || applying"
          severity="success"
        >
          <template #loadingicon v-if="applying">
            <ProgressSpinner style="width: 20px; height: 20px" />
          </template>
        </Button>
      </template>
    </Dialog>
    
    <Toast />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Dialog from 'primevue/dialog'
import Textarea from 'primevue/textarea'
import Toast from 'primevue/toast'
import Tag from 'primevue/tag'
import ProgressSpinner from 'primevue/progressspinner'
import FileUpload from 'primevue/fileupload'
import Message from 'primevue/message'
import axios from 'axios'

export default {
  components: {
    Card,
    Button,
    InputText,
    Dropdown,
    Dialog,
    Textarea,
    Toast,
    Tag,
    ProgressSpinner,
    FileUpload,
    Message
  },
  setup() {
    const router = useRouter()
    const toast = useToast()
    
    const internships = ref([])
    const myApplications = ref([])
    const loading = ref(true)
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
    const selectedFile = ref(null)
    const fileError = ref('')
    const applyError = ref('')
    const applying = ref(false)
    
    const fetchInternships = async () => {
      loading.value = true
      try {
        const token = localStorage.getItem('token')
        const headers = { Authorization: `Bearer ${token}` }
        
        const [internshipsRes, applicationsRes] = await Promise.all([
          axios.get('http://localhost:5000/api/internships', { headers }),
          axios.get('http://localhost:5000/api/my-applications', { headers })
        ])
        
        internships.value = internshipsRes.data
        myApplications.value = applicationsRes.data
        
        const uniqueLocations = [...new Set(internships.value
          .map(i => i.location)
          .filter(Boolean)
        )]
        locations.value = uniqueLocations.map(loc => ({ label: loc, value: loc }))
        
      } catch (error) {
        console.error('Error fetching internships:', error)
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load internships',
          life: 5000
        })
      } finally {
        loading.value = false
      }
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
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const viewInternship = (internship) => {
      selectedInternship.value = internship
      showInternshipDialog.value = true
    }
    
    const viewApplication = (internshipId) => {
      router.push('/my-applications')
    }
    
    const applyForInternship = (internship) => {
      if (!internship.is_active) {
        toast.add({
          severity: 'warn',
          summary: 'Cannot Apply',
          detail: 'Application deadline has passed',
          life: 5000
        })
        return
      }
      
      if (hasApplied(internship.id)) {
        toast.add({
          severity: 'info',
          summary: 'Already Applied',
          detail: 'You have already applied for this internship',
          life: 5000
        })
        return
      }
      
      applyData.value = {
        internship_id: internship.id,
        internship_title: internship.title,
        cover_letter: ''
      }
      selectedFile.value = null
      fileError.value = ''
      applyError.value = ''
      showApplyDialog.value = true
    }
    
    const onFileSelect = (event) => {
      const file = event.files[0]
      console.log("Selected file:", file)
      selectedFile.value = file
      
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/msword', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
      if (!allowedTypes.includes(file.type) && 
          !file.name.match(/\.(pdf|doc|docx)$/i)) {
        fileError.value = 'Invalid file type. Please upload PDF, DOC, or DOCX files only.'
        return
      }
      
      // Validate file size (16MB max)
      if (file.size > 16 * 1024 * 1024) {
        fileError.value = 'File size too large. Maximum size is 16MB.'
        return
      }
      
      selectedFile.value = file
      fileError.value = ''
    }
    
    const clearFile = () => {
      selectedFile.value = null
      fileError.value = ''
    }
    
    const submitApplication = async () => {
      if (!selectedFile.value) {
        fileError.value = 'Please select a resume file'
        return
      }
      
      applying.value = true
      applyError.value = ''
      
      try {
        const token = localStorage.getItem('token')
        const formData = new FormData()
        formData.append('resume', selectedFile.value)
        formData.append('cover_letter', applyData.value.cover_letter)
        console.log("Sending file:", selectedFile.value)

        
        const response = await axios.post(
          `http://localhost:5000/api/apply/${applyData.value.internship_id}`,
          formData,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Application submitted successfully!',
          life: 3000
        })
        
        showApplyDialog.value = false
        fetchInternships()
      } catch (error) {
        console.error('Application error:', error)
        applyError.value = error.response?.data?.error || 'Failed to submit application. Please try again.'
      } finally {
        applying.value = false
      }
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        location: ''
      }
    }
    
    onMounted(() => {
      fetchInternships()
    })
    
    return {
      internships,
      filters,
      locations,
      filteredInternships,
      showInternshipDialog,
      selectedInternship,
      showApplyDialog,
      applyData,
      selectedFile,
      fileError,
      applyError,
      applying,
      loading,
      hasApplied,
      formatDate,
      formatFileSize,
      fetchInternships,
      viewInternship,
      viewApplication,
      applyForInternship,
      submitApplication,
      onFileSelect,
      clearFile,
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
  color: var(--surface-900);
  margin: 0;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 250px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}

.no-data {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 300px;
  color: var(--surface-400);
}

.no-data p {
  margin-top: 1rem;
  font-size: 1.2rem;
}

.internship-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.internship-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.internship-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.internship-details {
  position: relative;
  min-height: 180px;
}

.description {
  color: var(--surface-700);
  margin-bottom: 1rem;
  line-height: 1.5;
  display: -webkit-box;
  /* -webkit-line-clamp: 3; */
  -webkit-box-orient: vertical;
  overflow: hidden;
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
  color: var(--surface-600);
  font-size: 0.9rem;
}

.detail i {
  color: var(--primary-color);
}

.applied-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: var(--green-500);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
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
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--surface-200);
}

.company-info h3 {
  margin: 0 0 0.5rem 0;
  color: var(--surface-900);
}

.company-description {
  color: var(--surface-600);
  line-height: 1.6;
  margin: 0;
}

.section {
  margin-bottom: 1.5rem;
}

.section h4 {
  color: var(--surface-900);
  margin: 0 0 0.5rem 0;
}

.section p {
  color: var(--surface-700);
  line-height: 1.6;
  margin: 0;
}

.details-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-top: 2rem;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.detail-item i {
  color: var(--primary-color);
  margin-top: 0.25rem;
}

.detail-item strong {
  display: block;
  color: var(--surface-900);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.detail-item p {
  margin: 0;
  color: var(--surface-700);
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
  color: var(--surface-900);
  font-weight: 500;
}

.internship-title {
  font-weight: bold;
  color: var(--surface-900);
  margin: 0;
  padding: 0.75rem;
  background: var(--surface-50);
  border-radius: 6px;
  border: 1px solid var(--surface-200);
}

.resume-upload {
  margin-top: 0.5rem;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem;
  background: var(--surface-50);
  border-radius: 6px;
  border: 1px solid var(--surface-200);
}

.file-info i {
  color: var(--primary-color);
}

.file-size {
  color: var(--surface-500);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .internship-list {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    min-width: auto;
  }
  
  .internship-grid {
    grid-template-columns: 1fr;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .details-summary {
    grid-template-columns: 1fr;
  }
}
</style>