<template>
  <div class="admin-dashboard">
    <div class="header">
      <h1>Admin Dashboard</h1>
      <div class="header-actions">
        <Button
          label="Refresh"
          icon="pi pi-refresh"
          @click="fetchAllData"
        />
      </div>
    </div>
    
    <TabView v-model:activeIndex="activeTab">
      <TabPanel header="Users">
        <DataTable
          :value="users"
          :paginator="true"
          :rows="10"
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
          :rowsPerPageOptions="[5, 10, 20]"
          currentPageReportTemplate="Showing {first} to {last} of {totalRecords} users"
          class="p-datatable-sm"
        >
          <Column field="id" header="ID" sortable></Column>
          <Column field="email" header="Email" sortable></Column>
          <Column field="role" header="Role" sortable>
            <template #body="slotProps">
              <Tag :value="slotProps.data.role" :severity="getRoleSeverity(slotProps.data.role)" />
            </template>
          </Column>
          <Column field="full_name" header="Name">
            <template #body="slotProps">
              {{ slotProps.data.full_name || slotProps.data.company_name || '-' }}
            </template>
          </Column>
          <Column field="created_at" header="Joined" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.created_at) }}
            </template>
          </Column>
          <Column field="is_active" header="Status" sortable>
            <template #body="slotProps">
              <Tag
                :value="slotProps.data.is_active ? 'Active' : 'Inactive'"
                :severity="slotProps.data.is_active ? 'success' : 'danger'"
              />
            </template>
          </Column>
        </DataTable>
      </TabPanel>
      
      <TabPanel header="Internships">
        <DataTable
          :value="internships"
          :paginator="true"
          :rows="10"
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
          :rowsPerPageOptions="[5, 10, 20]"
          currentPageReportTemplate="Showing {first} to {last} of {totalRecords} internships"
          class="p-datatable-sm"
        >
          <Column field="id" header="ID" sortable></Column>
          <Column field="title" header="Title" sortable></Column>
          <Column field="company_name" header="Company" sortable></Column>
          <Column field="location" header="Location" sortable></Column>
          <Column field="stipend" header="Stipend" sortable>
            <template #body="slotProps">
              {{ slotProps.data.stipend ? `₹${slotProps.data.stipend}` : 'Unpaid' }}
            </template>
          </Column>
          <Column field="application_count" header="Applications" sortable>
            <template #body="slotProps">
              <Badge :value="slotProps.data.application_count" severity="info" />
            </template>
          </Column>
          <Column field="last_date" header="Deadline" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.last_date) }}
            </template>
          </Column>
          <Column field="is_active" header="Status" sortable>
            <template #body="slotProps">
              <Tag
                :value="slotProps.data.is_active ? 'Active' : 'Closed'"
                :severity="slotProps.data.is_active ? 'success' : 'secondary'"
              />
            </template>
          </Column>
        </DataTable>
      </TabPanel>
      
      <TabPanel header="Applications">
        <DataTable
          :value="applications"
          :paginator="true"
          :rows="10"
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
          :rowsPerPageOptions="[5, 10, 20]"
          currentPageReportTemplate="Showing {first} to {last} of {totalRecords} applications"
          class="p-datatable-sm"
        >
          <Column field="id" header="ID" sortable></Column>
          <Column field="internship_title" header="Internship" sortable></Column>
          <Column field="company_name" header="Company" sortable></Column>
          <Column field="student_name" header="Student" sortable></Column>
          <Column field="status" header="Status" sortable>
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
            </template>
          </Column>
          <Column field="applied_at" header="Applied On" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.applied_at) }}
            </template>
          </Column>
        </DataTable>
      </TabPanel>
    </TabView>
    
    <div class="statistics">
      <h2>Statistics</h2>
      <div class="stats-grid">
        <Card class="stat-card">
          <template #title>Total Users</template>
          <template #content>
            <p class="stat-value">{{ statistics.totalUsers }}</p>
            <div class="stat-breakdown">
              <span>{{ statistics.studentCount }} Students</span>
              <span>{{ statistics.companyCount }} Companies</span>
              <span>{{ statistics.adminCount }} Admins</span>
            </div>
          </template>
        </Card>
        
        <Card class="stat-card">
          <template #title>Total Internships</template>
          <template #content>
            <p class="stat-value">{{ statistics.totalInternships }}</p>
            <div class="stat-breakdown">
              <span>{{ statistics.activeInternships }} Active</span>
              <span>{{ statistics.closedInternships }} Closed</span>
            </div>
          </template>
        </Card>
        
        <Card class="stat-card">
          <template #title>Total Applications</template>
          <template #content>
            <p class="stat-value">{{ statistics.totalApplications }}</p>
            <div class="stat-breakdown">
              <span>{{ statistics.appliedCount }} Applied</span>
              <span>{{ statistics.shortlistedCount }} Shortlisted</span>
              <span>{{ statistics.selectedCount }} Selected</span>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Badge from 'primevue/badge'
import Card from 'primevue/card'
import axios from 'axios'

export default {
  components: {
    TabView,
    TabPanel,
    DataTable,
    Column,
    Button,
    Tag,
    Badge,
    Card
  },
  setup() {
    const store = useStore()
    const toast = useToast()
    
    const activeTab = ref(0)
    const users = ref([])
    const internships = ref([])
    const applications = ref([])
    
    const fetchAllData = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const [usersRes, internshipsRes, applicationsRes] = await Promise.all([
          axios.get('/api/admin/users', { headers }),
          axios.get('/api/admin/internships', { headers }),
          axios.get('/api/admin/applications', { headers })
        ])
        
        users.value = usersRes.data
        internships.value = internshipsRes.data
        applications.value = applicationsRes.data
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load admin data',
          life: 5000
        })
      }
    }
    
    const statistics = computed(() => {
      return {
        totalUsers: users.value.length,
        studentCount: users.value.filter(u => u.role === 'student').length,
        companyCount: users.value.filter(u => u.role === 'company').length,
        adminCount: users.value.filter(u => u.role === 'admin').length,
        totalInternships: internships.value.length,
        activeInternships: internships.value.filter(i => i.is_active).length,
        closedInternships: internships.value.filter(i => !i.is_active).length,
        totalApplications: applications.value.length,
        appliedCount: applications.value.filter(a => a.status === 'APPLIED').length,
        shortlistedCount: applications.value.filter(a => a.status === 'SHORTLISTED').length,
        selectedCount: applications.value.filter(a => a.status === 'SELECTED').length
      }
    })
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const getRoleSeverity = (role) => {
      switch (role) {
        case 'admin': return 'danger'
        case 'company': return 'warning'
        case 'student': return 'info'
        default: return 'info'
      }
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
    
    onMounted(fetchAllData)
    
    return {
      activeTab,
      users,
      internships,
      applications,
      statistics,
      formatDate,
      getRoleSeverity,
      getStatusSeverity,
      fetchAllData
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  max-width: 1400px;
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

.statistics {
  margin-top: 3rem;
}

.statistics h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  height: 100%;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0 0 1rem 0;
  text-align: center;
}

.stat-breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: #7f8c8d;
}

.stat-breakdown span {
  display: block;
}

:deep(.p-tabview) {
  margin-top: 1rem;
}
</style>