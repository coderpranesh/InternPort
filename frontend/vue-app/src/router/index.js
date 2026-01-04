import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/auth/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../components/auth/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('../components/auth/ForgotPassword.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/terms',
    name: 'Terms',
    component: () => import('../components/auth/Terms.vue')
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: () => import('../components/auth/Privacy.vue')
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../components/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/student',
    name: 'StudentDashboard',
    component: () => import('../components/student/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/company',
    name: 'CompanyDashboard',
    component: () => import('../components/company/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../components/admin/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/internships',
    name: 'InternshipList',
    component: () => import('../components/student/InternshipList.vue'),
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/my-applications',
    name: 'MyApplications',
    component: () => import('../components/student/MyApplications.vue'),
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/company/internships',
    name: 'CompanyInternships',
    component: () => import('../components/company/InternshipList.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/company/applications/:id?',
    name: 'ApplicationList',
    component: () => import('../components/company/ApplicationList.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../components/Profile.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  const userRole = store.getters.userRole

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    if (userRole === 'student') {
      next('/student')
    } else if (userRole === 'company') {
      next('/company')
    } else if (userRole === 'admin') {
      next('/admin')
    } else {
      next('/')
    }
  } else if (to.meta.role && userRole !== to.meta.role) {
    if (userRole === 'student') {
      next('/student')
    } else if (userRole === 'company') {
      next('/company')
    } else if (userRole === 'admin') {
      next('/admin')
    } else {
      next('/')
    }
  } else if (to.name === 'Dashboard' && isAuthenticated) {
    if (userRole === 'student') {
      next('/student')
    } else if (userRole === 'company') {
      next('/company')
    } else if (userRole === 'admin') {
      next('/admin')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router