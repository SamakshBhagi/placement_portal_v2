<template>
<Navbar :student = "true" @profile = "profile" @logout = "logout" :midPage="true"/>
    <div class="container m-2 p-4 bg-light">
            <div class="row p-2 g-3 "><div class="fs-4 fw-bold">Ongoing Drives</div></div>
            <div class="row p-2  fs-5">
                <div class="col-md-3">Company</div>
                <div class="col-md-3">Role</div>
                <div class="col-md-3">Applied</div>
                <div class="col-md-3">Action</div>
            </div>
            <div class="row p-2  fs-5" v-for="a in applications">
                <div class="col-md-3">{{ a.company_name }}</div>
                <div class="col-md-3">{{a.role}}</div>
                <div class="col-md-3">{{ a.applied_at }}</div>
                <div class="col-md-3">{{ a.status }}</div>
            </div>
            
            <div class="row mt-3">
                <div class="col">
                    <button class="btn m-2" @click="prevPage" :disabled="!historyPagination.hasPrev">Prev</button>
                    <button class="btn m-2" @click ="nextPage" :disabled = "!historyPagination.hasNext">Next</button>
                </div>
            </div>
    </div>
    <div class="container"><button class="btn btn-success border p-2 m-2" @click = "exportApp">Export Applications</button></div>
</template>
<script>
import Navbar from '../components/navbar.vue';

import api from '../services/api.js'
export default{
    components:{Navbar},
    data(){return{historyPagination:{page:1, hasNext:false, hasPrev:false}, applications:[]}},
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        profile(){
            this.$router.push("/student/profile")
            
        },
        async getHistory(){
            const res = await api.get(`/api/student/view_applications?page=${this.historyPagination.page}`) // get data
            this.historyPagination.hasNext= res.data.meta.has_next
            this.historyPagination.hasPrev =  res.data.meta.has_prev
            console.log(res)
            this.applications = res.data.data

        },
        async nextPage(){
            this.historyPagination.page++
            this.getHistory()
        },
        
        async prevPage(){
            this.historyPagination.page--
            this.getHistory()
        },
        async exportApp(){
            try{
                const res = await api.post("/api/student/export_appn")
                console.log(res)
                alert("Started the export, your download will be ready soon!")

                const id = res.data.data.task_id
                this.checkExportStatus(id)

            }catch(error){console.log(error)}
        },
        async checkExportStatus(task_id){
            const interval = setInterval(async ()=>{
                const res = await api.get(`/api/student/export_appn_status/${task_id}`)
                if(res.data.message=="done!"){
                    clearInterval(interval)
                    const file= res.data.data.file
                    window.open(`http://localhost:5000/api/student/download_file/${file}`)
                }
            },2000)
        },
        },
    mounted(){
        this.getHistory()
    }
}
</script>