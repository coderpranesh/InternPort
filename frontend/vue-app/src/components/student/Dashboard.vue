<template>
  <div class="student-dashboard">
    <div class="header">
      <h1>Student Dashboard</h1>
      <Button
        label="Browse Internships"
        icon="pi pi-search"
        @click="browseInternships"
        severity="success"
      />
    </div>
    
    <div class="stats-grid">
      <Card class="stat-card">
        <template #title>
          <div class="card-title">
            <i class="pi pi-briefcase"></i>
            <span>Available Internships</span>
          </div>
        </template>
        <template #content>
          <p class="stat-value">{{ stats.availableInternships || 0 }}</p>
          <p class="stat-label">Open positions</p>
        </template>
      </Card>
      
      <Card class="stat-card">
        <template #title>
          <div class="card-title">
            <i class="pi pi-send"></i>
            <span>My Applications</span>
          </div>
        </template>
        <template #content>
          <p class="stat-value">{{ stats.totalApplications || 0 }}</p>
          <p class="stat-label">Total submitted</p>
        </template>
      </Card>
      
      <Card class="stat-card">
        <template #title>
          <div class="card-title">
            <i class="pi pi-clock"></i>
            <span>Pending Review</span>
          </div>
        </template>
        <template #content>
          <p class="stat-value">{{ stats.pendingApplications || 0 }}</p>
          <p class="stat-label">Under consideration</p>
        </template>
      </Card>
      
      <Card class="stat-card">
        <template #title>
          <div class="card-title">
            <i class="pi pi-check-circle"></i>
            <span>Selected</span>
          </div>
        </template>
        <template #content>
          <p class="stat-value">{{ stats.selectedApplications || 0 }}</p>
          <p class="stat-label">Accepted offers</p>
        </template>
      </Card>
    </div>
    
    <div class="recent-section">
      <div class="section-header">
        <h2>Recent Applications</h2>
        <Button
          label="View All"
          icon="pi pi-list"
          @click="viewAllApplications"
          outlined
        />
      </div>
      
      <div v-if="loading" class="loading">
        <ProgressSpinner />
      </div>
      
      <div v-else-if="recentApplications.length === 0" class="no-data">
        <i class="pi pi-inbox" style="font-size: 2rem; color: #ccc;"></i>
        <p>No applications yet</p>
        <Button
          label="Browse Internships"
          icon="pi pi-search"
          @click="browseInternships"
          outlined
        />
      </div>
      
      <div v-else class="applications-list">
        <div v-for="app in recentApplications" :key="app.id" class="application-card">
          <div class="application-header">
            <h3>{{ app.internship_title }}</h3>
            <Tag :value="app.status" :severity="getStatusSeverity(app.status)" />
          </div>
          <p class="company-name">{{ app.company_name }}</p>
          <div class="application-footer">
            <span class="applied-date">
              <i class="pi pi-calendar"></i>
              Applied {{ formatDate(app.applied_at) }}
            </span>
            <Button
              icon="pi pi-eye"
              label="View"
              @click="viewApplication(app)"
              outlined
              size="small"
            />
          </div>
        </div>
      </div>
    </div>
    
    <div class="deadlines-section">
      <div class="section-header">
        <h2>Upcoming Deadlines</h2>
      </div>
      
      <div v-if="loadingInternships" class="loading">
        <ProgressSpinner />
      </div>
      
      <div v-else-if="upcomingInternships.length === 0" class="no-data">
        <i class="pi pi-calendar-times" style="font-size: 2rem; color: #ccc;"></i>
        <p>No upcoming deadlines</p>
      </div>
      
      <div v-else class="deadlines-list">
        <div v-for="internship in upcomingInternships" :key="internship.id" class="deadline-card">
          <div class="deadline-header">
            <h3>{{ internship.title }}</h3>
            <span class="deadline-badge">
              <i class="pi pi-clock"></i>
              {{ getDaysRemaining(internship.last_date) }} days left
            </span>
          </div>
          <p class="company-name">{{ internship.company_name }}</p>
          <div class="deadline-footer">
            <span class="deadline-date">
              <i class="pi pi-calendar"></i>
              Deadline: {{ formatDate(internship.last_date) }}
            </span>
            <Button
              v-if="!hasApplied(internship.id)"
              icon="pi pi-send"
              label="Apply Now"
              @click="applyToInternship(internship)"
              outlined
              size="small"
              severity="success"
            />
            <Button
              v-else
              icon="pi pi-check"
              label="Applied"
              outlined
              size="small"
              disabled
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import ProgressSpinner from 'primevue/progressspinner'
import axios from 'axios'

export default {
  components: {
    Card,
    Button,
    Tag,
    ProgressSpinner
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    
    const stats = ref({})
    const recentApplications = ref([])
    const upcomingInternships = ref([])
    const loading = ref(true)
    const loadingInternships = ref(true)
    
    const fetchDashboardData = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const [internshipsRes, applicationsRes] = await Promise.all([
          axios.get('/api/internships', { headers }),
          axios.get('/api/my-applications', { headers })
        ])
        
        const applications = applicationsRes.data
        const internships = internshipsRes.data
        
        stats.value = {
          availableInternships: internships.length,
          totalApplications: applications.length,
          pendingApplications: applications.filter(a => a.status === 'APPLIED').length,
          selectedApplications: applications.filter(a => a.status === 'SELECTED').length
        }
        
        recentApplications.value = applications
          .sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at))
          .slice(0, 5)
        
        const now = new Date()
        const twoWeeksFromNow = new Date(now.getTime() + 14 * 24 * 60 * 60 * 1000)
        
        upcomingInternships.value = internships
          .filter(internship => {
            const deadline = new Date(internship.last_date)
            return deadline > now && deadline <= twoWeeksFromNow
          })
          .sort((a, b) => new Date(a.last_date) - new Date(b.last_date))
          .slice(0, 5)
        
        loading.value = false
        loadingInternships.value = false
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load dashboard data',
          life: 5000
        })
        loading.value = false
        loadingInternships.value = false
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
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const getDaysRemaining = (dateString) => {
      const deadline = new Date(dateString)
      const now = new Date()
      const diffTime = deadline - now
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    }
    
    const hasApplied = (internshipId) => {
      return recentApplications.value.some(app => app.internship_id === internshipId)
    }
    
    const browseInternships = () => {
      router.push('/internships')
    }
    
    const viewAllApplications = () => {
      router.push('/my-applications')
    }
    
    const viewApplication = (application) => {
      router.push('/my-applications')
    }
    
    const applyToInternship = (internship) => {
      router.push(`/internships#${internship.id}`)
    }
    
    onMounted(fetchDashboardData)
    
    return {
      stats,
      recentApplications,
      upcomingInternships,
      loading,
      loadingInternships,
      getStatusSeverity,
      formatDate,
      getDaysRemaining,
      hasApplied,
      browseInternships,
      viewAllApplications,
      viewApplication,
      applyToInternship
    }
  }
}
</script>

<style scoped>
.student-dashboard {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  height: 100%;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #2c3e50;
}

.card-title i {
  font-size: 1.25rem;
  color: #667eea;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0.5rem 0 0.25rem 0;
  text-align: center;
}

.stat-label {
  color: #7f8c8d;
  text-align: center;
  margin: 0;
}

.recent-section,
.deadlines-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: #2c3e50;
  margin: 0;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.no-data {
  text-align: center;
  padding: 3rem 2rem;
  color: #7f8c8d;
}

.no-data i {
  margin-bottom: 1rem;
}

.applications-list,
.deadlines-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.application-card,
.deadline-card {
  background: #f8f9fa;
  padding: 1.25rem;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
}

.application-header,
.deadline-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.application-header h3,
.deadline-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  flex: 1;
}

.deadline-badge {
  background: #ff9800;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.company-name {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

.application-footer,
.deadline-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.applied-date,
.deadline-date {
  color: #7f8c8d;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.applied-date i,
.deadline-date i {
  color: #667eea;
}
</style>