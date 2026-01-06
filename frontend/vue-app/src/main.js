import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import axios from 'axios'


import 'primevue/resources/themes/lara-light-blue/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.headers.common['Content-Type'] = 'application/json'

const app = createApp(App)

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'


app.component('Button', Button)
app.component('InputText', InputText)
app.component('Password', Password)
app.component('Toast', Toast)
app.component('ConfirmDialog', ConfirmDialog)

app.use(router)
app.use(store)
app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService)

app.mount('#app')
