<template>
    <a :href="this.reminder_list_url">Reminders list</a><br/>
    <a :href="this.reminder_update_url">Update Reminder</a><br/>
    <a :href="this.reminder_delete_url">Delete Reminder</a><br/>
    <h1>{{ this.reminder.name }}</h1>
    Tags:<br/>
    <span v-for="tag in this.reminder.tags">
    {{tag.name}}<br/></span>
    <br/>
    Description: {{this.reminder.description}}<br/>
    Date: {{this.convert_date_to_string(this.reminder.date)}}<br/>
</template>
<script>
export default {
    name: 'App',
    components: {
    },
    data: function() {
        return {
            reminder_error: [],
            reminder_id: window.ext_reminder_id,
            reminder_detail_js_url: window.ext_reminder_detail_js_url,
            reminder_list_url: window.ext_reminder_list_url,
            reminder_update_url: window.ext_reminder_update_url,
            reminder_delete_url: window.ext_reminder_delete_url,
            reminder: {},
        }
    },
    methods: {
        get_reminder_info(){
            fetch(this.reminder_detail_js_url,
                {
                    method: "get",
                    credentials: 'same-origin'
                }
            ).then(function(response) {
                console.log('response', response)
                return response.json()}).then(this.assign_reminder).catch(
                    (error) => { 
                    console.log('error', error)
                    this.reminder_error=["error when loading reminder information"]
        })
        },
        assign_reminder(reminder_json) {
            console.log('json', reminder_json)
            this.reminder = reminder_json['reminder']
            // this.reminder.running_time = this.convert_string_to_time(
            //     this.reminder.running_time)
            this.reminder.date = this.init_date(
                this.reminder.date
            )
        },
        // convert_string_to_time(time_string) {
        //     return new Date("1970-01-01T" + time_string)
        // },
        init_date(date_string){
            let dato = new Date(date_string)
            const offset = dato.getTimezoneOffset()
            dato = new Date(dato.getTime())
            return dato
        },
        convert_date_to_string(dato){
            if (dato) {
                const offset = dato.getTimezoneOffset()
                dato = new Date(dato.getTime() - (offset*60*1000))
                console.log('date', dato, dato.toISOString())
                return dato.toISOString().split('T')[0]
            }
        },
        // convert_time_to_string(timo){
        //     if (timo) {
        //         return `${timo.getHours()} hours ${timo.getMinutes()} minutes`
        //     }
        // }
    },
    computed: {
    },
    beforeMount() {
        this.get_reminder_info()
    },
}
</script>