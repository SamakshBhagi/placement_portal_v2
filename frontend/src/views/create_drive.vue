<template>
<Navbar title = "Company drive creation" @logout = "logout" :midPage="true"/>
<div class="container mt-4">
    <h4>Create Drive</h4>
    <form @submit.prevent = "createDrive">
        <!-- get job_role, job_desc, ctc, cgpa_criteria, deadline -->
         <div class="mb-2">
            <label for="">Job Role</label>
            <input type="text" v-model= "job_role" class = "form_control">
         </div>

         <div class="mb-2">
            <label for="">Job description</label>
            <textarea name="" v-model="job_desc"></textarea>
         </div>
         <div class="mb-2">
            <label for="">GPA cutoff</label>
            <input type="text" v-model= "cgpa_criteria" class = "form_control">
         </div>
         
         <div class="mb-2">
            <label for="">CTC</label>
            <input type="text" v-model= "ctc" class = "form_control">
         </div>
         
         <div class="mb-2">
            <label for="">Deadline</label>
            <input type="date" v-model= "deadline" class = "form_control">
         </div>
         <button type="submit" class="btn p-2">Create Drive</button>
    </form>
</div>

</template>
<script>
import Navbar from '../components/navbar.vue'
import api from '../services/api.js'
import { goBack } from '../services/back.js';
export default{
    components:
    {Navbar},
    data(){
        return{job_role:"",job_desc:"", cgpa_criteria:"",deadline:"", ctc:""}
    },
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        back(){
            goBack()
        },
        async createDrive(){
            const payload = {"job_role":this.job_role, "job_desc":this.job_desc, "ctc":this.ctc, "cgpa_criteria":this.cgpa_criteria, "deadline":this.deadline}
            const res = await api.post("/api/company/drives",payload)
            alert("Drive created!")
            console.log(res)
            this.$router.back()
        }
    }
}


</script>