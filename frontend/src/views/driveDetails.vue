<template>
    <Navbar title = "Update Drives" :mid-page="true" @logout = "logout"/>
    <div class="container m-2 p-2 ">
        <div class="row border p-2">
            <div class="col-md-3">Student ID</div>
            <div class="col-md-3">Name</div>
            <div class="col-md-3">Details</div>
            
            <div class="col-md-3">Action</div>
        </div>
        <div class="row  p-2" v-if="app.length==0">No applications...</div>
        
        <div class="row  p-2 border" v-else v-for="a in app">
            <div class="col-md-3">{{ a.student_id }}</div>
            <div class="col-md-3">{{ a.student_name }}</div>
            <div class="col-md-3"><button class="btn" @click = "studentProfile(a.student_id)">Profile</button></div>
        
            <div class="col-md-3">
            <select :disabled="a.status!='applied'" @change = "updateStatus(a, $event.target.value)">
                <div v-if="a.status!='applied'"><option value="">{{ a.status }}</option></div>
                <div v-else>
                    <option value="pending">Pending</option>    
                    <option value="selected">Select</option>
                    <option value="rejected">Reject</option>
                </div>
                </select>
            </div>
        </div>
    </div>
</template>
<script>
import Navbar from '../components/navbar.vue'
import api from '../services/api.js'
export default {
    components:{Navbar},
    data(){
        return{
            app:[]
        }
    },
    methods:{
        async getApps(){
            const drive_id = this.$route.params.id
            const res = await api.get(`/api/company/drives/${drive_id}/applications`)
            this.app = res.data.data
        },
        logout(){
            localStorage.clear("token")
            this.$router.push("/")
        },
        studentProfile(x){
            this.$router.push(`/company/viewprofile/${x}`)
        },
        async updateStatus(a, status){
            await api.put(`/api/company/applications/${a.application_id}/status`, {status:status})
            a.status = status
            console.log("student updated")

        }

    },
    mounted(){
        this.getApps()
    }
}
</script>