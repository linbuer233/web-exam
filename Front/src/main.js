import './assets/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import { zhCn } from 'element-plus/es/locale/index'


const app = createApp(App)
app.component('QuillEditor', QuillEditor)
app.use(router)
app.use(ElementPlus, { locale: zhCn })
app.mount('#app')
