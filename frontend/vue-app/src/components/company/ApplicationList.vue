<template>
  <div class="application-list">
    <div class="header">
      <h1>Internship Applications</h1>
      <Dropdown
        v-model="selectedInternshipId"
        :options="internshipOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Select Internship"
        class="internship-dropdown"
      />
    </div>
    
    <div v-if="selectedInternship" class="internship-info">
      <h3>{{ selectedInternship.title }}</h3>
      <div class="internship-meta">
        <span><i class="pi pi-map-marker"></i> {{ selectedInternship.location || 'Remote' }}</span>
        <span><i class="pi pi-money-bill"></i> {{ selectedInternship.stipend ? `₹${selectedInternship.stipend}/month` : 'Unpaid' }}</span>
        <span><i class="pi pi-calendar"></i> Deadline: {{ formatDate(selectedInternship.last_date) }}</span>
      </div>
    </div>
    
    <div v-if="!selectedInternshipId" class="no-selection">
      <i class="pi pi-briefcase" style="font-size: 3rem; color: #ccc;"></i>
      <h3>Select an Internship</h3>
      <p>Choose an internship from the dropdown above to view applications</p>
    </div>
    
    <div v-else-if="loading" class="loading">
      <ProgressSpinner />
    </div>
    
    <div v-else-if="applications.length === 0" class="no-applications">
      <i class="pi pi-inbox" style="font-size: 3rem; color: #ccc;"></i>
      <h3>No applications yet</h3>
      <p>No students have applied to this internship yet</p>
    </div>
    
    <div v-else class="applications-container">
      <div class="filters">
        <Dropdown
          v-model="selectedStatus"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Filter by status"
          showClear
        />
        <Button
          label="Export CSV"
          icon="pi pi-download"
          @click="exportCSV"
          outlined
        />
      </div>
      
      <DataTable
        :value="filteredApplications"
        :paginator="true"
        :rows="10"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5, 10, 20]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} applications"
        class="p-datatable-sm"
      >
        <Column field="student_name" header="Student">
          <template #body="slotProps">
            <div class="student-cell">
              <strong>{{ slotProps.data.student_name }}</strong>
              <small>{{ slotProps.data.student_university }}</small>
              <small>{{ slotProps.data.student_major }}</small>
            </div>
          </template>
        </Column>
        <Column field="applied_at" header="Applied On">
          <template #body="slotProps">
            {{ formatDate(slotProps.data.applied_at) }}
          </template>
        </Column>
        <Column field="status" header="Status">
          <template #body="slotProps">
            <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
          </template>
        </Column>
        <Column header="Resume">
          <template #body="slotProps">
            <Button
              v-if="slotProps.data.resume_path"
              icon="pi pi-download"
              @click="downloadResume(slotProps.data.resume_path)"
              outlined
              size="small"
            />
          </template>
        </Column>
        <Column header="Actions">
          <template #body="slotProps">
            <Button
              icon="pi pi-eye"
              @click="viewApplication(slotProps.data)"
              outlined
              size="small"
            />
            <SplitButton
              :model="statusActions"
              @click="updateStatus(slotProps.data, 'SHORTLISTED')"
              size="small"
              :disabled="slotProps.data.status === 'SELECTED' || slotProps.data.status === 'REJECTED'"
            >
              Update Status
            </SplitButton>
          </template>
        </Column>
      </DataTable>
    </div>
    
    <Dialog
      v-model:visible="showApplicationDialog"
      :header="selectedApplication?.student_name"
      :style="{ width: '50vw' }"
      :modal="true"
    >
      <div v-if="selectedApplication" class="application-details">
        <div class="student-info">
          <h4>Student Information</h4>
          <div class="info-grid">
            <div class="info-item">
              <strong>Name:</strong>
              <span>{{ selectedApplication.student_name }}</span>
            </div>
            <div class="info-item">
              <strong>University:</strong>
              <span>{{ selectedApplication.student_university || 'Not specified' }}</span>
            </div>
            <div class="info-item">
              <strong>Major:</strong>
              <span>{{ selectedApplication.student_major || 'Not specified' }}</span>
            </div>
            <div class="info-item">
              <strong>Applied On:</strong>
              <span>{{ formatDate(selectedApplication.applied_at) }}</span>
            </div>
          </div>
        </div>
        
        <div v-if="selectedApplication.cover_letter" class="section">
          <h4>Cover Letter</h4>
          <div class="cover-letter">
            {{ selectedApplication.cover_letter }}
          </div>
        </div>
        
        <div class="section">
          <h4>Current Status</h4>
          <Tag :value="selectedApplication.status" :severity="getStatusSeverity(selectedApplication.status)" size="large" />
        </div>
        
        <div class="section">
          <h4>Update Status</h4>
          <div class="status-buttons">
            <Button
              v-for="status in updateableStatuses"
              :key="status.value"
              :label="status.label"
              :severity="getStatusSeverity(status.value)"
              @click="updateApplicationStatus(selectedApplication.id, status.value)"
              :disabled="selectedApplication.status === status.value || selectedApplication.status === 'SELECTED' || selectedApplication.status === 'REJECTED'"
              outlined
            />
          </div>
        </div>
      </div>
      <template #footer>
        <Button
          label="Close"
          icon="pi pi-times"
          @click="showApplicationDialog = false"
          text
        />
        <Button
          v-if="selectedApplication?.resume_path"
          label="Download Resume"
          icon="pi pi-download"
          @click="downloadResume(selectedApplication.resume_path)"
        />
      </template>
    </Dialog>
    
    <Toast />
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import SplitButton from 'primevue/splitbutton'
import Dropdown from 'primevue/dropdown'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import ProgressSpinner from 'primevue/progressspinner'
import Toast from 'primevue/toast'
import axios from 'axios'

export default {
  components: {
    DataTable,
    Column,
    Button,
    SplitButton,
    Dropdown,
    Tag,
    Dialog,
    ProgressSpinner,
    Toast
  },
  setup() {
    const route = useRoute()
    const store = useStore()
    const toast = useToast()
    
    const internships = ref([])
    const selectedInternshipId = ref(null)
    const selectedInternship = ref(null)
    const applications = ref([])
    const loading = ref(false)
    const selectedStatus = ref(null)
    const showApplicationDialog = ref(false)
    const selectedApplication = ref(null)
    
    const statusOptions = [
      { label: 'All', value: null },
      { label: 'Applied', value: 'APPLIED' },
      { label: 'Shortlisted', value: 'SHORTLISTED' },
      { label: 'Selected', value: 'SELECTED' },
      { label: 'Rejected', value: 'REJECTED' }
    ]
    
    const updateableStatuses = [
      { label: 'Shortlist', value: 'SHORTLISTED' },
      { label: 'Select', value: 'SELECTED' },
      { label: 'Reject', value: 'REJECTED' }
    ]
    
    const statusActions = computed(() => {
      return updateableStatuses.map(status => ({
        label: status.label,
        command: () => updateApplicationStatus(selectedApplication.value?.id, status.value)
      }))
    })
    
    const fetchInternships = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const response = await axios.get('/api/internships', { headers })
        internships.value = response.data
        
        const internshipId = route.params.id
        if (internshipId) {
          selectedInternshipId.value = parseInt(internshipId)
        }
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load internships',
          life: 5000
        })
      }
    }
    
    const fetchApplications = async () => {
      if (!selectedInternshipId.value) return
      
      loading.value = true
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const response = await axios.get(`/api/applications/${selectedInternshipId.value}`, { headers })
        applications.value = response.data
        
        selectedInternship.value = internships.value.find(i => i.id === selectedInternshipId.value)
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load applications',
          life: 5000
        })
      } finally {
        loading.value = false
      }
    }
    
    const filteredApplications = computed(() => {
      if (!selectedStatus.value) {
        return applications.value
      }
      return applications.value.filter(app => app.status === selectedStatus.value)
    })
    
    const internshipOptions = computed(() => {
      return internships.value.map(internship => ({
        label: internship.title,
        value: internship.id
      }))
    })
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const getStatusSeverity = (status) => {
      switch (status) {
        case 'APPLIED': return 'info'
        case 'SHORTLISTED': return 'warning'
        case 'SELECTED': return 'success'
        case 'REJECTED': return 'danger'
        default: return 'info'
      }
    }
    
    const viewApplication = (application) => {
      selectedApplication.value = application
      showApplicationDialog.value = true
    }
    
    const updateApplicationStatus = async (applicationId, status) => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        await axios.put(
          `/api/application/${applicationId}/status`,
          { status },
          { headers }
        )
        
        toast.add({
          severity: 'success',
          summary: 'Status Updated',
          detail: `Application status changed to ${status}`,
          life: 3000
        })
        
        fetchApplications()
        showApplicationDialog.value = false
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: error.response?.data?.error || 'Failed to update status',
          life: 5000
        })
      }
    }
    
    const updateStatus = (application, status) => {
      updateApplicationStatus(application.id, status)
    }
    
    const downloadResume = (resumePath) => {
      window.open(`/uploads/${resumePath}`, '_blank')
    }
    
    const exportCSV = () => {
      const csvContent = [
        ['Student Name', 'University', 'Major', 'Applied On', 'Status', 'Cover Letter'],
        ...applications.value.map(app => [
          app.student_name,
          app.student_university,
          app.student_major,
          formatDate(app.applied_at),
          app.status,
          app.cover_letter?.replace(/,/g, ';')
        ])
      ].map(row => row.join(',')).join('\n')
      
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `applications_${selectedInternshipId.value}.csv`
      a.click()
    }
    
    watch(selectedInternshipId, (newVal) => {
      if (newVal) {
        fetchApplications()
      }
    })
    
    onMounted(fetchInternships)
    
    return {
      internships,
      selectedInternshipId,
      selectedInternship,
      applications,
      loading,
      selectedStatus,
      statusOptions,
      updateableStatuses,
      statusActions,
      filteredApplications,
      internshipOptions,
      showApplicationDialog,
      selectedApplication,
      formatDate,
      getStatusSeverity,
      viewApplication,
      updateApplicationStatus,
      updateStatus,
      downloadResume,
      exportCSV
    }
  }
}
</script>

<style scoped>
.application-list {
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

.internship-dropdown {
  min-width: 300px;
}

.internship-info {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.internship-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.internship-meta {
  display: flex;
  gap: 2rem;
  color: #7f8c8d;
}

.internship-meta i {
  margin-right: 0.5rem;
}

.no-selection,
.no-applications {
  text-align: center;
  padding: 4rem 2rem;
  color: #7f8c8d;
}

.no-selection h3,
.no-applications h3 {
  margin: 1rem 0 0.5rem 0;
  color: #2c3e50;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.applications-container {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.student-cell {
  display: flex;
  flex-direction: column;
}

.student-cell small {
  color: #7f8c8d;
  font-size: 0.85rem;
}

.application-details {
  padding: 1rem 0;
}

.student-info {
  margin-bottom: 2rem;
}

.student-info h4 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item strong {
  color: #2c3e50;
  font-size: 0.9rem;
}

.info-item span {
  color: #666;
}

.section {
  margin-bottom: 1.5rem;
}

.section h4 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.cover-letter {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  white-space: pre-wrap;
  line-height: 1.6;
}

.status-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.p-button.p-button-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>