<template>
    <div v-if="!loading">
        <Navbar :student="true" :title ="student.name+`'s`"  @logout = "logout" @history="history" @profile = "profile"/>
        <div class="container m-2 p-4 bg-light">
            <div class="row p-2 g-3 "><div class="fs-4 fw-bold">Ongoing Drives</div></div>
            <div class="row p-2  fs-5">
                <div class="col-md-3">Company</div>
                <div class="col-md-3">Role</div>
                <div class="col-md-3">Package</div>
                <div class="col-md-3">Action</div>
            </div>
            <div v-for="d in drives.data" class="row g-3 m-2 border">
                <div class="col-md-3 ">{{ d.company }}</div>
                <div class="col-md-3">{{ d.job_role }}</div>
                <div class="col-md-3">{{ d.ctc }}</div>
                
                <div class="col-md-3"><button class="btn m-2 border" @click="apply(d)" :disabled="d.applied">Apply</button></div>
            </div>
            <div class="row mt-3">
                <div class="col">
                    <button class="btn m-2" @click="prevPage" :disabled="!drivePagination.hasPrev">Prev</button>
                    <button class="btn m-2" @click ="nextPage" :disabled = "!drivePagination.hasNext">Next</button>
                </div>
            </div>
        </div>
        </div>
        <div v-else>Loading...</div>
</template>

<script>
import Navbar from '../components/navbar.vue'
import api from "../services/api.js"


export default{
    name:"student_dashboard",
    components:{Navbar},
    data(){return{loading:true, drives:{data:[],meta:{}},drivePagination:{page:1,hasNext:false,hasPrev:false},app:[], student:{}}},
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        profile(){
            this.$router.push("/student/profile")
            console.log("Profile")
        },
        history(){
            // need to send student to a view that allows him to view all past applications hes applied to and also export csv. 
            this.$router.push("/student/history")
            console.log("Placement history of the student")
        },
        async getStudent(){
            try{
                const res = await api.get(`/api/student/dashboard`)        
                this.student= res.data.data
            }catch(err){
                console.log(err)
            }finally{
                this.loading = false
            }
        
        },
        async getDrives(){
            const res = await api.get(`/api/student/drives?page=${this.drivePagination.page}`)
            console.log(res)
            console.log(this)
            this.drives.data = res.data.data
            this.drives.meta = res.data.meta
            
            this.drivePagination.hasNext = res.data.meta.has_next
            this.drivePagination.hasPrev = res.data.meta.has_prev
        },
        async nextPage(){
            this.drivePagination.page++
            this.getDrives()
        },
        
        async prevPage(){
            this.drivePagination.page--
            this.getDrives()
        },
        async apply(d){
            try{
                const res = await api.post(`/api/student/drives/${d.drive_id}/apply`)
                alert("Application sent! Check history for updates.")
                await this.getDrives()
            }
            catch(error){
                alert("Failed..")
            }
        }

    },  
    mounted(){
        this.getStudent()
        this.getDrives()
    }
}
</script>