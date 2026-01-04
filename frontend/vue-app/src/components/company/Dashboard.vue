<template>
  <div class="company-dashboard">
    <div class="header">
      <h1>Company Dashboard</h1>
      <Button
        label="Post New Internship"
        icon="pi pi-plus"
        @click="postNewInternship"
        severity="success"
      />
    </div>
    
    <div class="stats-grid">
      <Card class="stat-card">
        <template #title>
          <div class="card-title">
            <i class="pi pi-briefcase"></i>
            <span>Active Internships</span>
          </div>
        </template>
        <template #content>
          <p class="stat-value">{{ stats.activeInternships || 0 }}</p>
          <p class="stat-label">Currently posted</p>
        </template>
      </Card>
      
      <Card class="stat-card">
        <template #title>
          <div class="card-title">
            <i class="pi pi-users"></i>
            <span>Total Applications</span>
          </div>
        </template>
        <template #content>
          <p class="stat-value">{{ stats.totalApplications || 0 }}</p>
          <p class="stat-label">Received applications</p>
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
          <p class="stat-value">{{ stats.pendingReview || 0 }}</p>
          <p class="stat-label">Awaiting action</p>
        </template>
      </Card>
      
      <Card class="stat-card">
        <template #title>
          <div class="card-title">
            <i class="pi pi-check-circle"></i>
            <span>Selected Candidates</span>
          </div>
        </template>
        <template #content>
          <p class="stat-value">{{ stats.selectedCandidates || 0 }}</p>
          <p class="stat-label">Successfully placed</p>
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
        <p>No applications received yet</p>
        <Button
          label="Post Internship"
          icon="pi pi-plus"
          @click="postNewInternship"
          outlined
        />
      </div>
      
      <div v-else class="applications-list">
        <div v-for="app in recentApplications" :key="app.id" class="application-card">
          <div class="application-header">
            <div>
              <h3>{{ app.student_name }}</h3>
              <p class="internship-title">{{ app.internship_title }}</p>
            </div>
            <Tag :value="app.status" :severity="getStatusSeverity(app.status)" />
          </div>
          <div class="application-details">
            <span class="detail">
              <i class="pi pi-building"></i>
              {{ app.student_university || 'University not specified' }}
            </span>
            <span class="detail">
              <i class="pi pi-calendar"></i>
              Applied {{ formatDate(app.applied_at) }}
            </span>
          </div>
          <div class="application-actions">
            <Button
              icon="pi pi-eye"
              label="View"
              @click="viewApplication(app)"
              outlined
              size="small"
            />
            <Button
              v-if="app.status === 'APPLIED'"
              icon="pi pi-check"
              label="Review"
              @click="reviewApplication(app)"
              severity="success"
              size="small"
            />
          </div>
        </div>
      </div>
    </div>
    
    <div class="internships-section">
      <div class="section-header">
        <h2>Active Internships</h2>
        <Button
          label="Manage Internships"
          icon="pi pi-cog"
          @click="manageInternships"
          outlined
        />
      </div>
      
      <div v-if="loadingInternships" class="loading">
        <ProgressSpinner />
      </div>
      
      <div v-else-if="activeInternships.length === 0" class="no-data">
        <i class="pi pi-briefcase" style="font-size: 2rem; color: #ccc;"></i>
        <p>No active internships</p>
        <Button
          label="Post Your First Internship"
          icon="pi pi-plus"
          @click="postNewInternship"
          severity="success"
        />
      </div>
      
      <div v-else class="internships-list">
        <div v-for="internship in activeInternships" :key="internship.id" class="internship-card">
          <div class="internship-header">
            <h3>{{ internship.title }}</h3>
            <Badge :value="internship.application_count" severity="info" />
          </div>
          <div class="internship-details">
            <span class="detail">
              <i class="pi pi-map-marker"></i>
              {{ internship.location || 'Remote' }}
            </span>
            <span class="detail">
              <i class="pi pi-money-bill"></i>
              {{ internship.stipend ? `₹${internship.stipend}/month` : 'Unpaid' }}
            </span>
            <span class="detail">
              <i class="pi pi-calendar"></i>
              Deadline: {{ formatDate(internship.last_date) }}
            </span>
          </div>
          <div class="internship-actions">
            <Button
              icon="pi pi-eye"
              label="View"
              @click="viewInternship(internship)"
              outlined
              size="small"
            />
            <Button
              icon="pi pi-users"
              label="Applications"
              @click="viewApplications(internship)"
              severity="info"
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
      
      <div v-if="loadingDeadlines" class="loading">
        <ProgressSpinner />
      </div>
      
      <div v-else-if="upcomingDeadlines.length === 0" class="no-data">
        <i class="pi pi-calendar-times" style="font-size: 2rem; color: #ccc;"></i>
        <p>No upcoming deadlines</p>
      </div>
      
      <div v-else class="deadlines-list">
        <div v-for="internship in upcomingDeadlines" :key="internship.id" class="deadline-card">
          <div class="deadline-header">
            <h3>{{ internship.title }}</h3>
            <span class="deadline-badge">
              <i class="pi pi-clock"></i>
              {{ getDaysRemaining(internship.last_date) }} days left
            </span>
          </div>
          <div class="deadline-details">
            <span class="detail">
              <i class="pi pi-users"></i>
              {{ internship.application_count }} applications
            </span>
            <span class="detail">
              <i class="pi pi-calendar"></i>
              Closes {{ formatDate(internship.last_date) }}
            </span>
          </div>
          <div class="deadline-actions">
            <Button
              icon="pi pi-eye"
              label="View Details"
              @click="viewInternship(internship)"
              outlined
              size="small"
            />
            <Button
              icon="pi pi-users"
              label="Review Applications"
              @click="viewApplications(internship)"
              severity="success"
              size="small"
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
import Badge from 'primevue/badge'
import ProgressSpinner from 'primevue/progressspinner'
import axios from 'axios'

export default {
  components: {
    Card,
    Button,
    Tag,
    Badge,
    ProgressSpinner
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const toast = useToast()
    
    const stats = ref({})
    const recentApplications = ref([])
    const activeInternships = ref([])
    const upcomingDeadlines = ref([])
    const loading = ref(true)
    const loadingInternships = ref(true)
    const loadingDeadlines = ref(true)
    
    const fetchDashboardData = async () => {
      try {
        const token = store.state.token
        const headers = { Authorization: `Bearer ${token}` }
        
        const [internshipsRes, applicationsRes] = await Promise.all([
          axios.get('/api/internships', { headers }),
          axios.get('/api/applications/all', { headers }).catch(() => ({ data: [] }))
        ])
        
        const internships = internshipsRes.data.filter(i => i.is_active)
        const applications = applicationsRes.data
        
        stats.value = {
          activeInternships: internships.length,
          totalApplications: applications.length,
          pendingReview: applications.filter(a => a.status === 'APPLIED').length,
          selectedCandidates: applications.filter(a => a.status === 'SELECTED').length
        }
        
        recentApplications.value = applications
          .sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at))
          .slice(0, 5)
        
        activeInternships.value = internships
          .map(internship => ({
            ...internship,
            application_count: applications.filter(app => app.internship_id === internship.id).length
          }))
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        
        const now = new Date()
        const twoWeeksFromNow = new Date(now.getTime() + 14 * 24 * 60 * 60 * 1000)
        
        upcomingDeadlines.value = internships
          .filter(internship => {
            const deadline = new Date(internship.last_date)
            return deadline > now && deadline <= twoWeeksFromNow
          })
          .sort((a, b) => new Date(a.last_date) - new Date(b.last_date))
          .slice(0, 5)
        
        loading.value = false
        loadingInternships.value = false
        loadingDeadlines.value = false
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load dashboard data',
          life: 5000
        })
        loading.value = false
        loadingInternships.value = false
        loadingDeadlines.value = false
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
    
    const postNewInternship = () => {
      router.push('/company/internships?new=true')
    }
    
    const viewAllApplications = () => {
      router.push('/company/applications')
    }
    
    const viewApplication = (application) => {
      router.push(`/company/applications/${application.internship_id}`)
    }
    
    const reviewApplication = (application) => {
      router.push(`/company/applications/${application.internship_id}`)
    }
    
    const manageInternships = () => {
      router.push('/company/internships')
    }
    
    const viewInternship = (internship) => {
      router.push(`/company/internships`)
    }
    
    const viewApplications = (internship) => {
      router.push(`/company/applications/${internship.id}`)
    }
    
    onMounted(fetchDashboardData)
    
    return {
      stats,
      recentApplications,
      activeInternships,
      upcomingDeadlines,
      loading,
      loadingInternships,
      loadingDeadlines,
      getStatusSeverity,
      formatDate,
      getDaysRemaining,
      postNewInternship,
      viewAllApplications,
      viewApplication,
      reviewApplication,
      manageInternships,
      viewInternship,
      viewApplications
    }
  }
}
</script>

<style scoped>
.company-dashboard {
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
.internships-section,
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
.internships-list,
.deadlines-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.application-card,
.internship-card,
.deadline-card {
  background: #f8f9fa;
  padding: 1.25rem;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  transition: transform 0.2s;
}

.application-card:hover,
.internship-card:hover,
.deadline-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.application-header,
.internship-header,
.deadline-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.application-header h3,
.internship-header h3,
.deadline-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  flex: 1;
}

.internship-title {
  color: #666;
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
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

.application-details,
.internship-details,
.deadline-details {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.detail {
  color: #7f8c8d;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.detail i {
  color: #667eea;
}

.application-actions,
.internship-actions,
.deadline-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.p-button.p-button-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>