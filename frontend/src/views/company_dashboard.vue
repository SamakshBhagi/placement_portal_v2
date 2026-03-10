<template>
    <Navbar title = "Company" @logout = "logout" :newDrive="true" @createDrive = "createDrive"/>
    <div class="container mt-4 border">
        <div class="row border-bottom p-2">
            <div class="col-md-3">Drive ID</div>
            <div class="col-md-3">Role</div>
            <div class="col-md-3">Deadline</div>
        </div>
        <div v-for="d in drives" :key="d.drive_id" class="row border-bottom" >
            <div class="col-md-3">{{ d.drive_id }}</div>
            <div class="col-md-3">{{ d.role }}</div>
            <div class="col-md-3">{{ d.deadline }}</div>
            <div class="col"><button class="btn border m-2" @click="updateDrive(d)">Details</button></div>
        </div>
        <div class="row border-bottom p-2" v-if="drives.length==0">No drives...</div>
    </div>
</template>

<script>
import Navbar from '../components/navbar.vue'
import api from '../services/api.js'

export default{
    components:{
        Navbar
    },
    data(){
        return{drives:[],}
    },
    methods: {
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        async getDrives(){
            const res  = await api.get("/api/company/dashboard")
            this.drives = res.data.data

        }, 
        createDrive(){
            this.$router.push("/company/createdrive")
            console.log("lets create a new drive")
        },
        async updateDrive(d){
            // go to view applicants page, from where i can go to applicant page and select/reject applicant and also view resume
            this.$router.push(`/company/drive/${d.drive_id}`)
        }
    },
    mounted(){
        this.getDrives()
    }
}

</script>