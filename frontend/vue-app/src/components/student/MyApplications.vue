<template>
  <div class="my-applications">
    <div class="header">
      <h1>My Applications</h1>
      <Button
        label="Browse Internships"
        icon="pi pi-search"
        @click="browseInternships"
      />
    </div>
    
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
        label="Refresh"
        icon="pi pi-refresh"
        @click="fetchApplications"
      />
    </div>
    
    <div v-if="loading" class="loading">
      <ProgressSpinner />
    </div>
    
    <div v-else-if="applications.length === 0" class="no-applications">
      <i class="pi pi-inbox" style="font-size: 3rem; color: #ccc;"></i>
      <h3>No applications yet</h3>
      <p>Start applying to internships to see them here</p>
      <Button
        label="Browse Internships"
        icon="pi pi-search"
        @click="browseInternships"
        severity="success"
      />
    </div>
    
    <DataTable
      v-else
      :value="filteredApplications"
      :paginator="true"
      :rows="10"
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      :rowsPerPageOptions="[5, 10, 20]"
      currentPageReportTemplate="Showing {first} to {last} of {totalRecords} applications"
      class="p-datatable-sm"
    >
      <Column field="internship_title" header="Internship">
        <template #body="slotProps">
          <div class="internship-cell">
            <strong>{{ slotProps.data.internship_title }}</strong>
            <small>{{ slotProps.data.company_name }}</small>
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
      <Column header="Actions">
        <template #body="slotProps">
          <Button
            icon="pi pi-eye"
            @click="viewApplication(slotProps.data)"
            outlined
            size="small"
          />
          <Button
            icon="pi pi-file"
            @click="viewInternship(slotProps.data.internship_id)"
            outlined
            size="small"
          />
        </template>
      </Column>
    </DataTable>
    
    <Dialog
      v-model:visible="showApplicationDialog"
      :header="selectedApplication?.internship_title"
      :style="{ width: '50vw' }"
      :modal="true"
    >
      <div v-if="selectedApplication" class="application-details">
        <div class="status-section">
          <h4>Application Status</h4>
          <Tag :value="selectedApplication.status" :severity="getStatusSeverity(selectedApplication.status)" size="large" />
          <p class="status-info">{{ getStatusInfo(selectedApplication.status) }}</p>
        </div>
        
        <div class="section">
          <h4>Applied On</h4>
          <p>{{ formatDate(selectedApplication.applied_at) }}</p>
        </div>
        
        <div v-if="selectedApplication.cover_letter" class="section">
          <h4>Cover Letter</h4>
          <div class="cover-letter">
            {{ selectedApplication.cover_letter }}
          </div>
        </div>
        
        <div class="section">
          <h4>Company Information</h4>
          <p><strong>Company:</strong> {{ selectedApplication.company_name }}</p>
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
          label="View Internship"
          icon="pi pi-briefcase"
          @click="viewInternship(selectedApplication?.internship_id)"
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
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
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
    Dropdown,
    Tag,
    Dialog,
    ProgressSpinner,
    Toast
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    
    const applications = ref([])
    const loading = ref(true)
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
    
    const fetchApplications = async () => {
      loading.value = true
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const response = await axios.get('/api/my-applications', { headers })
        applications.value = response.data
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
    
    const getStatusInfo = (status) => {
      switch (status) {
        case 'APPLIED': return 'Your application has been submitted and is under review.'
        case 'SHORTLISTED': return 'Your application has been shortlisted! The company may contact you for further steps.'
        case 'SELECTED': return 'Congratulations! You have been selected for this internship.'
        case 'REJECTED': return 'Thank you for applying. Unfortunately, you were not selected for this position.'
        default: return ''
      }
    }
    
    const browseInternships = () => {
      router.push('/internships')
    }
    
    const viewApplication = (application) => {
      selectedApplication.value = application
      showApplicationDialog.value = true
    }
    
    const viewInternship = (internshipId) => {
      router.push(`/internships#${internshipId}`)
    }
    
    onMounted(fetchApplications)
    
    return {
      applications,
      loading,
      selectedStatus,
      statusOptions,
      filteredApplications,
      showApplicationDialog,
      selectedApplication,
      formatDate,
      getStatusSeverity,
      getStatusInfo,
      browseInternships,
      fetchApplications,
      viewApplication,
      viewInternship
    }
  }
}
</script>

<style scoped>
.my-applications {
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

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.no-applications {
  text-align: center;
  padding: 4rem 2rem;
  color: #7f8c8d;
}

.no-applications h3 {
  margin: 1rem 0 0.5rem 0;
  color: #2c3e50;
}

.no-applications p {
  margin-bottom: 2rem;
}

.internship-cell {
  display: flex;
  flex-direction: column;
}

.internship-cell small {
  color: #7f8c8d;
  font-size: 0.85rem;
}

.application-details {
  padding: 1rem 0;
}

.status-section {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.status-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.status-info {
  margin: 1rem 0 0 0;
  color: #666;
  font-style: italic;
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
  margin: 0;
}

.cover-letter {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  white-space: pre-wrap;
  line-height: 1.6;
}
</style>