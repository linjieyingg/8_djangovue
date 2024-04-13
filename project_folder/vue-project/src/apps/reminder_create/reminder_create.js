import 'vite/modulepreload-polyfill';
import { createApp } from 'vue';
import AppCreate from './ReminderCreate.vue'

createApp(AppCreate).mount("#appcreate")