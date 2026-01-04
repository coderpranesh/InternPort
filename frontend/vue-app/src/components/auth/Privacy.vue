
<template>
  <div class="privacy-container">
    <div class="privacy-header">
      <Button
        icon="pi pi-arrow-left"
        label="Back"
        @click="goBack"
        text
      />
      <h1>Privacy Policy</h1>
    </div>
    
    <Card class="privacy-card">
      <template #content>
        <div class="privacy-content">
          <h2>InternPort Privacy Policy</h2>
          <p class="effective-date">Last Updated: {{ new Date().toLocaleDateString() }}</p>
          
          <div class="section">
            <h3>1. Information We Collect</h3>
            <p>We collect the following types of information:</p>
            <ul>
              <li><strong>Account Information:</strong> Name, email, password, role</li>
              <li><strong>Profile Information:</strong> For students: university, major, resume. For companies: company details, description</li>
              <li><strong>Application Data:</strong> Internship applications, cover letters, status updates</li>
              <li><strong>Usage Data:</strong> How you interact with our platform</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>2. How We Use Your Information</h3>
            <p>We use your information to:</p>
            <ul>
              <li>Provide and maintain the InternPort service</li>
              <li>Process internship applications</li>
              <li>Connect students with companies</li>
              <li>Send important notifications about your account</li>
              <li>Improve and optimize our platform</li>
              <li>Comply with legal obligations</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>3. Data Sharing</h3>
            <p>We share information in the following circumstances:</p>
            <ul>
              <li><strong>Between Users:</strong> Student profiles are shared with companies they apply to. Company information is shared with applicants.</li>
              <li><strong>Service Providers:</strong> With third-party services that help us operate our platform (hosting, analytics, etc.)</li>
              <li><strong>Legal Requirements:</strong> When required by law or to protect our rights</li>
              <li><strong>Business Transfers:</strong> In connection with a merger or acquisition</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>4. Data Security</h3>
            <p>We implement appropriate security measures to protect your personal information:</p>
            <ul>
              <li>Encryption of sensitive data</li>
              <li>Secure server infrastructure</li>
              <li>Regular security audits</li>
              <li>Access controls and authentication</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>5. Your Rights</h3>
            <p>You have the right to:</p>
            <ul>
              <li>Access your personal data</li>
              <li>Correct inaccurate data</li>
              <li>Request deletion of your data</li>
              <li>Export your data</li>
              <li>Opt-out of marketing communications</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>6. Data Retention</h3>
            <p>We retain your data for as long as your account is active or as needed to provide services. You can request account deletion at any time.</p>
          </div>
          
          <div class="section">
            <h3>7. Cookies and Tracking</h3>
            <p>We use cookies and similar technologies to:</p>
            <ul>
              <li>Remember your preferences</li>
              <li>Analyze site usage</li>
              <li>Improve user experience</li>
              <li>Provide personalized content</li>
            </ul>
          </div>
          
          <div class="section">
            <h3>8. Children's Privacy</h3>
            <p>Our service is not intended for users under 16 years of age. We do not knowingly collect data from children under 16.</p>
          </div>
          
          <div class="section">
            <h3>9. International Transfers</h3>
            <p>Your information may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place.</p>
          </div>
          
          <div class="section">
            <h3>10. Changes to Privacy Policy</h3>
            <p>We may update this policy periodically. We will notify you of significant changes via email or platform notifications.</p>
          </div>
          
          <div class="section">
            <h3>11. Contact Us</h3>
            <p>For privacy-related questions or concerns, please contact us at: privacy@internport.com</p>
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
.privacy-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.privacy-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.privacy-header h1 {
  color: #2c3e50;
  margin: 0;
  flex: 1;
}

.privacy-card {
  margin-bottom: 2rem;
}

.privacy-content {
  padding: 1rem;
}

.privacy-content h2 {
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

.section strong {
  color: #2c3e50;
}
</style>