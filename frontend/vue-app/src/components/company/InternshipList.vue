<template>
  <div class="company-internships">
    <div class="header">
      <h1>My Internships</h1>
      <Button
        label="Post New Internship"
        icon="pi pi-plus"
        @click="showNewInternshipDialog = true"
        severity="success"
      />
    </div>
    
    <div class="filters">
      <ToggleButton
        v-model="showActiveOnly"
        onLabel="Active"
        offLabel="All"
        onIcon="pi pi-check"
        offIcon="pi pi-list"
      />
      <InputText
        v-model="searchQuery"
        placeholder="Search internships..."
        class="search-input"
      />
      <Button
        label="Refresh"
        icon="pi pi-refresh"
        @click="fetchInternships"
      />
    </div>
    
    <div v-if="loading" class="loading">
      <ProgressSpinner />
    </div>
    
    <div v-else-if="internships.length === 0" class="no-internships">
      <i class="pi pi-briefcase" style="font-size: 3rem; color: #ccc;"></i>
      <h3>No internships posted yet</h3>
      <p>Start posting internships to attract talented students</p>
      <Button
        label="Post Your First Internship"
        icon="pi pi-plus"
        @click="showNewInternshipDialog = true"
        severity="success"
      />
    </div>
    
    <DataTable
      v-else
      :value="filteredInternships"
      :paginator="true"
      :rows="10"
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      :rowsPerPageOptions="[5, 10, 20]"
      currentPageReportTemplate="Showing {first} to {last} of {totalRecords} internships"
      class="p-datatable-sm"
    >
      <Column field="title" header="Title"></Column>
      <Column field="location" header="Location"></Column>
      <Column field="stipend" header="Stipend">
        <template #body="slotProps">
          {{ slotProps.data.stipend ? `₹${slotProps.data.stipend}/month` : 'Unpaid' }}
        </template>
      </Column>
      <Column field="last_date" header="Deadline">
        <template #body="slotProps">
          {{ formatDate(slotProps.data.last_date) }}
        </template>
      </Column>
      <Column field="application_count" header="Applications">
        <template #body="slotProps">
          <Badge :value="slotProps.data.application_count" severity="info" />
        </template>
      </Column>
      <Column field="is_active" header="Status">
        <template #body="slotProps">
          <Tag
            :value="slotProps.data.is_active ? 'Active' : 'Closed'"
            :severity="slotProps.data.is_active ? 'success' : 'secondary'"
          />
        </template>
      </Column>
      <Column header="Actions">
        <template #body="slotProps">
          <Button
            icon="pi pi-eye"
            @click="viewInternship(slotProps.data)"
            outlined
            size="small"
          />
          <Button
            icon="pi pi-users"
            @click="viewApplications(slotProps.data)"
            outlined
            size="small"
          />
          <Button
            icon="pi pi-pencil"
            @click="editInternship(slotProps.data)"
            outlined
            size="small"
          />
          <Button
            v-if="slotProps.data.is_active"
            icon="pi pi-trash"
            @click="confirmDelete(slotProps.data)"
            outlined
            size="small"
            severity="danger"
          />
        </template>
      </Column>
    </DataTable>
    
    <Dialog
      v-model:visible="showNewInternshipDialog"
      header="Post New Internship"
      :style="{ width: '50vw' }"
      :modal="true"
    >
      <div class="internship-form">
        <div class="field">
          <label for="title">Title *</label>
          <InputText
            id="title"
            v-model="newInternship.title"
            placeholder="e.g., Software Development Intern"
            class="w-full"
            :class="{ 'p-invalid': errors.title }"
          />
          <small v-if="errors.title" class="p-error">{{ errors.title }}</small>
        </div>
        
        <div class="field">
          <label for="description">Description *</label>
          <Textarea
            id="description"
            v-model="newInternship.description"
            :rows="5"
            placeholder="Describe the internship role, responsibilities, and what the intern will learn"
            class="w-full"
            :class="{ 'p-invalid': errors.description }"
          />
          <small v-if="errors.description" class="p-error">{{ errors.description }}</small>
        </div>
        
        <div class="field">
          <label for="requirements">Requirements</label>
          <Textarea
            id="requirements"
            v-model="newInternship.requirements"
            :rows="3"
            placeholder="List any specific requirements or skills needed"
            class="w-full"
          />
        </div>
        
        <div class="grid-2">
          <div class="field">
            <label for="location">Location</label>
            <InputText
              id="location"
              v-model="newInternship.location"
              placeholder="e.g., Remote, Mumbai, Bangalore"
              class="w-full"
            />
          </div>
          
          <div class="field">
            <label for="stipend">Stipend (₹/month)</label>
            <InputNumber
              id="stipend"
              v-model="newInternship.stipend"
              placeholder="Enter stipend amount"
              class="w-full"
              :min="0"
            />
          </div>
        </div>
        
        <div class="field">
          <label for="last_date">Application Deadline *</label>
          <Calendar
            id="last_date"
            v-model="newInternship.last_date"
            :minDate="minDate"
            dateFormat="yy-mm-dd"
            showIcon
            class="w-full"
            :class="{ 'p-invalid': errors.last_date }"
          />
          <small v-if="errors.last_date" class="p-error">{{ errors.last_date }}</small>
        </div>
      </div>
      <template #footer>
        <Button
          label="Cancel"
          icon="pi pi-times"
          @click="closeNewInternshipDialog"
          text
        />
        <Button
          label="Post Internship"
          icon="pi pi-check"
          @click="createInternship"
          :loading="creating"
          severity="success"
        />
      </template>
    </Dialog>
    
    <Dialog
      v-model:visible="showEditDialog"
      header="Edit Internship"
      :style="{ width: '50vw' }"
      :modal="true"
    >
      <div v-if="editingInternship" class="internship-form">
        <div class="field">
          <label for="edit-title">Title *</label>
          <InputText
            id="edit-title"
            v-model="editingInternship.title"
            class="w-full"
            :class="{ 'p-invalid': editErrors.title }"
          />
          <small v-if="editErrors.title" class="p-error">{{ editErrors.title }}</small>
        </div>
        
        <div class="field">
          <label for="edit-description">Description *</label>
          <Textarea
            id="edit-description"
            v-model="editingInternship.description"
            :rows="5"
            class="w-full"
            :class="{ 'p-invalid': editErrors.description }"
          />
          <small v-if="editErrors.description" class="p-error">{{ editErrors.description }}</small>
        </div>
        
        <div class="field">
          <label for="edit-requirements">Requirements</label>
          <Textarea
            id="edit-requirements"
            v-model="editingInternship.requirements"
            :rows="3"
            class="w-full"
          />
        </div>
        
        <div class="grid-2">
          <div class="field">
            <label for="edit-location">Location</label>
            <InputText
              id="edit-location"
              v-model="editingInternship.location"
              class="w-full"
            />
          </div>
          
          <div class="field">
            <label for="edit-stipend">Stipend (₹/month)</label>
            <InputNumber
              id="edit-stipend"
              v-model="editingInternship.stipend"
              class="w-full"
              :min="0"
            />
          </div>
        </div>
        
        <div class="field">
          <label for="edit-last_date">Application Deadline *</label>
          <Calendar
            id="edit-last_date"
            v-model="editingInternship.last_date"
            :minDate="minDate"
            dateFormat="yy-mm-dd"
            showIcon
            class="w-full"
            :class="{ 'p-invalid': editErrors.last_date }"
          />
          <small v-if="editErrors.last_date" class="p-error">{{ editErrors.last_date }}</small>
        </div>
      </div>
      <template #footer>
        <Button
          label="Cancel"
          icon="pi pi-times"
          @click="showEditDialog = false"
          text
        />
        <Button
          label="Save Changes"
          icon="pi pi-check"
          @click="updateInternship"
          :loading="updating"
          severity="success"
        />
      </template>
    </Dialog>
    
    <ConfirmDialog />
    <Toast />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Calendar from 'primevue/calendar'
import InputNumber from 'primevue/inputnumber'
import ToggleButton from 'primevue/togglebutton'
import Tag from 'primevue/tag'
import Badge from 'primevue/badge'
import Dialog from 'primevue/dialog'
import ProgressSpinner from 'primevue/progressspinner'
import ConfirmDialog from 'primevue/confirmdialog'
import Toast from 'primevue/toast'
import axios from 'axios'

export default {
  components: {
    DataTable,
    Column,
    Button,
    InputText,
    Textarea,
    Calendar,
    InputNumber,
    ToggleButton,
    Tag,
    Badge,
    Dialog,
    ProgressSpinner,
    ConfirmDialog,
    Toast
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    const confirm = useConfirm()
    
    const internships = ref([])
    const loading = ref(true)
    const showActiveOnly = ref(true)
    const searchQuery = ref('')
    const showNewInternshipDialog = ref(false)
    const showEditDialog = ref(false)
    const creating = ref(false)
    const updating = ref(false)
    
    const newInternship = ref({
      title: '',
      description: '',
      requirements: '',
      location: '',
      stipend: null,
      last_date: null
    })
    
    const editingInternship = ref(null)
    
    const errors = ref({})
    const editErrors = ref({})
    
    const minDate = new Date()
    
    const fetchInternships = async () => {
      loading.value = true
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const response = await axios.get('/api/internships', { headers })
        internships.value = response.data.map(internship => ({
          ...internship,
          application_count: internship.applications?.length || 0
        }))
      } catch (error) {
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
      let filtered = internships.value
      
      if (showActiveOnly.value) {
        filtered = filtered.filter(i => i.is_active)
      }
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(i =>
          i.title.toLowerCase().includes(query) ||
          i.description.toLowerCase().includes(query) ||
          i.location?.toLowerCase().includes(query)
        )
      }
      
      return filtered
    })
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const validateInternship = (internship, isEdit = false) => {
      const validationErrors = {}
      
      if (!internship.title?.trim()) {
        validationErrors.title = 'Title is required'
      }
      
      if (!internship.description?.trim()) {
        validationErrors.description = 'Description is required'
      }
      
      if (!internship.last_date) {
        validationErrors.last_date = 'Deadline is required'
      } else if (new Date(internship.last_date) < minDate) {
        validationErrors.last_date = 'Deadline must be in the future'
      }
      
      return validationErrors
    }
    
    const createInternship = async () => {
      errors.value = validateInternship(newInternship.value)
      
      if (Object.keys(errors.value).length > 0) {
        return
      }
      
      creating.value = true
      
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const data = {
          ...newInternship.value,
          last_date: newInternship.value.last_date.toISOString()
        }
        
        const response = await axios.post('/api/internships', data, { headers })
        
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Internship posted successfully',
          life: 3000
        })
        
        closeNewInternshipDialog()
        fetchInternships()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: error.response?.data?.error || 'Failed to post internship',
          life: 5000
        })
      } finally {
        creating.value = false
      }
    }
    
    const updateInternship = async () => {
      editErrors.value = validateInternship(editingInternship.value, true)
      
      if (Object.keys(editErrors.value).length > 0) {
        return
      }
      
      updating.value = true
      
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const data = {
          ...editingInternship.value,
          last_date: editingInternship.value.last_date.toISOString()
        }
        
        await axios.put(`/api/internships/${editingInternship.value.id}`, data, { headers })
        
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Internship updated successfully',
          life: 3000
        })
        
        showEditDialog.value = false
        fetchInternships()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: error.response?.data?.error || 'Failed to update internship',
          life: 5000
        })
      } finally {
        updating.value = false
      }
    }
    
    const closeNewInternshipDialog = () => {
      showNewInternshipDialog.value = false
      newInternship.value = {
        title: '',
        description: '',
        requirements: '',
        location: '',
        stipend: null,
        last_date: null
      }
      errors.value = {}
    }
    
    const viewInternship = (internship) => {
      router.push(`/internships#${internship.id}`)
    }
    
    const viewApplications = (internship) => {
      router.push(`/company/applications/${internship.id}`)
    }
    
    const editInternship = (internship) => {
      editingInternship.value = {
        ...internship,
        last_date: new Date(internship.last_date)
      }
      showEditDialog.value = true
    }
    
    const confirmDelete = (internship) => {
      confirm.require({
        message: `Are you sure you want to delete "${internship.title}"?`,
        header: 'Delete Confirmation',
        icon: 'pi pi-exclamation-triangle',
        acceptClass: 'p-button-danger',
        accept: () => deleteInternship(internship.id)
      })
    }
    
    const deleteInternship = async (internshipId) => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        await axios.delete(`/api/internships/${internshipId}`, { headers })
        
        toast.add({
          severity: 'success',
          summary: 'Deleted',
          detail: 'Internship deleted successfully',
          life: 3000
        })
        
        fetchInternships()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: error.response?.data?.error || 'Failed to delete internship',
          life: 5000
        })
      }
    }
    
    onMounted(fetchInternships)
    
    return {
      internships,
      loading,
      showActiveOnly,
      searchQuery,
      filteredInternships,
      showNewInternshipDialog,
      showEditDialog,
      creating,
      updating,
      newInternship,
      editingInternship,
      errors,
      editErrors,
      minDate,
      formatDate,
      fetchInternships,
      createInternship,
      updateInternship,
      closeNewInternshipDialog,
      viewInternship,
      viewApplications,
      editInternship,
      confirmDelete
    }
  }
}
</script>

<style scoped>
.company-internships {
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

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.no-internships {
  text-align: center;
  padding: 4rem 2rem;
  color: #7f8c8d;
}

.no-internships h3 {
  margin: 1rem 0 0.5rem 0;
  color: #2c3e50;
}

.no-internships p {
  margin-bottom: 2rem;
}

.internship-form {
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

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.p-button.p-button-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>