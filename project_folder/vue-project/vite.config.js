import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
const backendPath = '../django_project';
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    base: '/static/vite/',
    server: {
        watch: {
            ignored: [],
        },
    },
    build: {
        manifest: true,
        emptyOutDir: true,
        outDir: backendPath + '/core/static/vite/',
        rollupOptions: {
            input: {
                vue_reminder_edit: "./src/apps/reminder_edit/reminder_edit.js",
                vue_reminder_create: "./src/apps/reminder_create/reminder_create.js",
            },
        },
    },
});