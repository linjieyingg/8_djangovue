<template>
    <div>
        This is the page where we are going to edit reminder in vuejs, this is cool
        This is the form coming from django, displayed in vue
    </div><br>
    <div>
        <br>
        With fetch this time
        <br>
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
        <!-- <form method="post" class="form"> -->
            <input type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrf_token">
            <p>
                <label for="id_name">Reminder Name: </label>
                <input type="text" name="name" value="" maxlength="100"
                required="" id="id_name">
            </p>
            <!-- <p>
                <label for="id_running_time">Running time: </label>
                <input type="hidden" name="running_time" :value="get_time_string" required=""
                id="id_running_time">
                <VueDatePicker style="display:inline-block;width:
                250px;padding-bottom:10px;padding-left:10px" v-model="time"
                :time-picker="true"  enable-seconds></VueDatePicker>
            </p> -->
            <p>
                <label for="id_tags">Tags:</label>
                <select hidden name="tags"  id="id_tags" multiple="">
                    <option v-for="tag in tag_list" :value="tag.id" selected=""></option>
                </select>
                <multiselect v-model="tag_list" :options="tag_list_source" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Choose the tags" label="name" track-by="name" :preselect-first="true" style="display:inline-block;width: 300px;padding-bottom:10px;padding-left:10px">
                    <template slot="selection" slot-scope="{ values, search, isOpen }"><span class="multiselect__single" v-if="values.length" v-show="!isOpen">{{ values.length }} options selected</span></template>
                </multiselect>
            </p>
            <!-- <p>
                <label for="id_director">Director: </label>
                <input type="text" name="director" value="The Wachowskis"
                maxlength="200" required="" id="id_director">
            </p> -->
            <p>
                <label for="id_date">Date:  </label>
                <input type="hidden" name="date" :value="get_date_string" required=""
                id="id_date">
                <VueDatePicker  v-model="date" format="yyyy-MM-dd" value="date" style="width:250px;display: inline-block;" :enable-time-picker="false"></VueDatePicker>
            </p>
            <button type="submit" class="btn btn-primary"
            @click.prevent="submit_form_fetch"
            :disabled="submitting_form">
                Submit
            </button>
        <!-- </form> -->
    </div>
    <br><br>
</template>
<script>
import VueDatePicker from '@vuepic/vue-datepicker'; 
import '@vuepic/vue-datepicker/dist/main.css'
import { resolveTransitionHooks } from 'vue';
import Multiselect from 'vue-multiselect'
export default {
    name: 'App',
    components: {
        VueDatePicker,
        Multiselect,
    },
    data: function() {
        return {
            csrf_token: window.ext_csrf_token,
            form: window.ext_form,
            reminder_dico: window.ext_reminder_dict,
    	    tag_list_source: (window.ext_tag_list != undefined) ? window.ext_tag_list: [],
            date: this.proceed('date'),
            submitting_form: false,
            form_error: [],
	    	form_updated: "",
            update_bis_url: (window.ext_update_bis_url != undefined) ? window.ext_update_bis_url : null,
            tag_list: (window.ext_reminder_dict != undefined) ? window.ext_reminder_dict.tags : [],
        }
    },
    methods: {
        submit_form_fetch(){
        	this.form_error = []
        	this.form_updated = ""
        	let formData = new FormData();
        	let form_data = {
	            	'name': this.tag_dico.name,
	            	'running_time': this.get_time_string,
	            	'director': this.movie_dico.director,
	            	'release_date': this.get_date_string,
        	}
        	for (var key in form_data) {
            		formData.append(key, form_data[key])
        	}
        	this.tag_list.map(dic => formData.append('tags', dic.id))
        	fetch(this.update_bis_url,
            	{
                	method: "post",
                	body: formData,
                	headers: {'X-CSRFToken': this.csrf_token},
                	credentials: 'same-origin'
            	}
        	).then(function(response) {
            	console.log('response', response)
            	return response.json()}).then(
	            	this.handleResponse).catch(
	                	(error) => {
	                	console.log('error', String(error))
	                	this.form_error=["error"]
    			})
    	},
    	handleResponse(response) {
        	console.log('json response', response)
        	if ('success' in response){
	            	if (response['success'] == true) {
	                	this.form_updated = "Reminder has been updated"
	            	} else {
	                	if ('errors' in response){
		                    	for (const [key, value] of Object.entries(response['errors'])) {
		                        	for (const error of value) {
		                            		this.form_error.push(`${key}: ${error}`)
		                        	}
	                    		}
	                	} else {
	                    		this.form_error=["Update failed - An error occurred but do not have more information about it"]
	                	}
	            	}
		} else {
	            	this.form_error=["Update failed - It has been an error on the form request"]
		}
            console.log(this.form_error)
    	},
        submit_form(){
            if (this.submitting_form === true) {
            return;
            }
            this.submitting_form = true
            var form = document.createElement('form');
            form.setAttribute('method', 'post');
            let form_data = {
                'csrfmiddlewaretoken': this.csrf_token,
                'name': this.reminder_dico.name,
                'description': this.reminder_dico.description,
                'date': this.get_date_string,
            }
            console.log('tag_list', this.tag_list)
            console.log("form_data", form_data)
            for (var key in form_data) {
                var html_field = document.createElement('input')
                html_field.setAttribute('type', 'hidden')
                html_field.setAttribute('name', key)
                html_field.setAttribute('value', form_data[key])
                form.appendChild(html_field)
            }
            var tag_field = document.createElement('select')
            tag_field.setAttribute('name', 'tag')
            tag_field.setAttribute('id', 'id_tag')
            tag_field.setAttribute('multiple', '')
            for (var tag of this.tag_list) {
                console.log('tag', tag)
                var option_field = document.createElement('option')
                option_field.setAttribute('value', tag.id)
                option_field.setAttribute('selected', '')
                tag_field.appendChild(option_field)
            }
            form.appendChild(tag_field)
            document.body.appendChild(form);
            form.submit()
        },
        convert_date_to_string(dato){
            const offset = dato.getTimezoneOffset()
            dato = new Date(dato.getTime() - (offset*60*1000))
            console.log('date', dato, dato.toISOString())
            return dato.toISOString().split('T')[0]
        },
        proceed(dot){
            if (window.ext_movie_dict != undefined  ){
                if(dot == 'date'){
                    console.log(this.datify(window.ext_movie_dict.release_date))
                    return this.datify(window.ext_movie_dict.release_date)
                }
                else if (dot == 'time'){
                    console.log(this.timify(window.ext_movie_dict.running_time))
                    return this.timify(window.ext_movie_dict.running_time)
                }
            }
            else{
                return null
            }
        },
        // timify(string){
        //     let split = string.split(':')
        //     return {
        //         'hours': split[0],
        //         'minutes': split[1],
        //         'seconds': split[2]
        //     }
        // },
        datify(string){
            let dat = new Date(string)
            const offset = dat.getTimezoneOffset()
            dat = new Date(dat.getTime() + (offset*60*1000))
            console.log(dat)
            return dat
        },
    },
    computed: {
        get_date_string() {
            if (this.date == null) {
                return ""
            } else {
                return this.convert_date_to_string(this.date)
            }
        },
        // get_time_string(){
        //     if (this.time == null){
        //         return ""
        //     }
        //     else {
        //         // console.log(this.convert_time(this.time))
        //         return `${this.time.hours}:${this.time.minutes}:${this.time.seconds}`            }
        // },
    },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
