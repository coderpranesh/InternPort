<template>
  <div class="terms-container">
    <div class="terms-header">
      <Button
        icon="pi pi-arrow-left"
        label="Back"
        @click="goBack"
        text
      />
      <h1>Terms of Service</h1>
    </div>
    
    <Card class="terms-card">
      <template #content>
        <div class="terms-content">
          <h2>InternPort Terms of Service</h2>
          <p class="effective-date">Last Updated: {{ new Date().toLocaleDateString() }}</p>
          
          <div class="section">
            <h3>1. Acceptance of Terms</h3>
            <p>By accessing and using InternPort, you accept and agree to be bound by the terms and provision of this agreement.</p>
          </div>
          
          <div class="section">
            <h3>2. User Accounts</h3>
            <p>You are responsible for maintaining the confidentiality of your account and password. You agree to accept responsibility for all activities that occur under your account.</p>
          </div>
          
          <div class="section">
            <h3>3. Student Responsibilities</h3>
            <p>As a student user, you agree to:</p>
            <ul>
              <li>Provide accurate and truthful information in your profile and applications</li>
              <li>Apply only to internships for which you are qualified</li>
              <li>Not submit false or misleading information</li>
              <li>Respect application deadlines</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>3. Company Responsibilities</h3>
            <p>As a company user, you agree to:</p>
            <ul>
              <li>Post accurate internship descriptions</li>
              <li>Process applications in a timely manner</li>
              <li>Provide clear internship requirements and expectations</li>
              <li>Respect applicant privacy and data protection</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>4. Prohibited Activities</h3>
            <p>Users may not:</p>
            <ul>
              <li>Post false or misleading information</li>
              <li>Harass or discriminate against other users</li>
              <li>Use the platform for illegal purposes</li>
              <li>Attempt to gain unauthorized access to other accounts</li>
              <li>Share login credentials with others</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>5. Intellectual Property</h3>
            <p>All content on InternPort, including text, graphics, logos, and software, is the property of InternPort and is protected by intellectual property laws.</p>
          </div>
          
          <div class="section">
            <h3>6. Limitation of Liability</h3>
            <p>InternPort shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of the platform.</p>
          </div>
          
          <div class="section">
            <h3>7. Changes to Terms</h3>
            <p>We reserve the right to modify these terms at any time. We will notify users of any significant changes via email or platform notifications.</p>
          </div>
          
          <div class="section">
            <h3>8. Contact Information</h3>
            <p>For questions about these Terms of Service, please contact us at: support@internport.com</p>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import Card from 'primevue/card'
import Button from 'primevue/button'

export default {
  components: {
    Card,
    Button
  },
  setup() {
    const router = useRouter()
    
    const goBack = () => {
      router.back()
    }
    
    return {
      goBack
    }
  }
}
</script>

<style scoped>
.terms-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.terms-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.terms-header h1 {
  color: #2c3e50;
  margin: 0;
  flex: 1;
}

.terms-card {
  margin-bottom: 2rem;
}

.terms-content {
  padding: 1rem;
}

.terms-content h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.effective-date {
  color: #7f8c8d;
  margin-bottom: 2rem;
  font-style: italic;
}

.section {
  margin-bottom: 2rem;
}

.section h3 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.section p {
  color: #5a6c7d;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.section ul {
  color: #5a6c7d;
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

.section li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}
</style>