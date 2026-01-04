import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    isAuthenticated: !!localStorage.getItem('token')
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = !!token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    setUser(state, user) {
      state.user = user
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
      }
    },
    clearAuth(state) {
      state.token = null
      state.user = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('setToken', token)
      commit('setUser', user)
    },
    logout({ commit }) {
      commit('clearAuth')
    },
    updateUser({ commit, state }, userData) {
      const updatedUser = { ...state.user, ...userData }
      commit('setUser', updatedUser)
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    userRole: state => state.user?.role,
    userName: state => {
      if (state.user?.role === 'student') {
        return state.user.full_name
      } else if (state.user?.role === 'company') {
        return state.user.company_name
      }
      return state.user?.email
    },
    userEmail: state => state.user?.email
  }
})