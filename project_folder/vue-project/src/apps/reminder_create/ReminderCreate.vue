<template>
    <div>
        <div v-if="form_error">
            <ul>
                <li v-for="(error, index) in form_error">
                    {{error}}
                </li>
            </ul>
        </div>
        <div v-if="form_updated">
            {{ form_updated }}
        </div><br>
        <form method="post" class="form">
            <input type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrf_token">
            <p>
                <label for="id_name">Reminder Title: </label> &nbsp;
                <input type="text" name="name" v-model="title" maxlength="100"
                required="" id="id_name">
            </p>
            <p>
                <label for="id_homework">Type:</label>&nbsp;
                <select v-model="type" name="homework"  id="id_homework" multiple="" style="display:inline-block;padding:1px;">
                    <!-- <option v-for="type in types" :value="type" selected=""></option> -->
                    <option >Homework</option>
                    <option >Chore</option>
                </select>
            </p>
            <p>
                <label for="id_tags">Tags:</label>
                <select hidden name="tags"  id="id_tags" multiple="">
                    <option v-for="tag in tag_list" :value="tag.id" selected=""></option>
                </select>
                <span v-if="tag in tag_list">
                    <multiselect v-model="tag_list" :options="tag_list_source" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Choose the tags" label="name" track-by="name" :preselect-first="true" style="display:inline-block;width: 300px;padding-bottom:10px;padding-left:10px">
                        <template slot="selection" slot-scope="{ values, search, isOpen }"><span class="multiselect__single" v-if="values.length" v-show="!isOpen">{{ values.length }} options selected</span></template>
                    </multiselect>
                </span>
                <span v-else> No tags. <a href="{% url 'reminders:tag_create' %}">Create tag</a></span>
            </p>
            <p>
                <label for="id_description">Description: </label>&nbsp;
                <input type="hidden" :value="get_description" name="description" value=""
                maxlength="5000" required="" id="id_description" >
                <textarea v-model="description" name="description"> </textarea>
            </p>
            <p>
                <label for="id_date">Date:  </label>&nbsp;
                <input type="hidden" name="date" :value="get_date_string" required=""
                id="id_date">
                <VueDatePicker  v-model="date" format="yyyy-MM-dd HH:mm" value="date" style="width:250px;display: inline-block;" :min="new Date().toISOString().substr(0, 10)"></VueDatePicker>
            </p>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        {{ reminder_dico }}
    </div>
    <br><br>
</template>
<script>
    export default {
        name: 'App',
        components: {
        },
        data: function() {
            return {
            csrf_token: window.ext_csrf_token,
            description: null,
            form: window.ext_form,
            reminder_dico: window.ext_reminder_dict,
            title: this.reminder_dico,
    	    tag_list_source: (window.ext_tag_list != undefined) ? window.ext_tag_list: [],
            homework_tag_source: [],
            chore_tag_source: [],
            date: null,
            submitting_form: false,
            form_error: [],
            types: ['Homework', 'Chore'],
            type: null,
	    	form_updated: "",
            update_bis_url: window.ext_update_bis_url,
            tag_list: (window.ext_reminder_dict != undefined && window.ext_reminder_dict != null) ? window.ext_reminder_dict.tags : [],
            }
        },
        methods: {
        },
    }
</script>