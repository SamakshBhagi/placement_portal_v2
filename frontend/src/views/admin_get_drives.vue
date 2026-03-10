<template>
    <Navbar title ="Admin" :midPage="true" @logout = "logout"/>
    <div class="container m-2 p-4 bg-light">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-header">
                    Ongoing drives
                </div>
                <div class="card-body">
                    <div class="row fs-4 py-2 border-bottom">
                        <div class="col-md-2">ID</div>
                        <div class="col-md-2">ROLE</div>
                        <div class="col-md-4">DEADLINE</div>
                        <div class="col-md-4">STATUS</div>
                    </div>
                    <div v-for = "d in drives" :key="d.drive_id" class = "row align-items-center">
                        <div class="col-md-2">{{d.drive_id}}</div>
                        <div class="col-md-2">{{ d.job_role }}</div>
                        <div class="col-md-4">{{ d.deadline }}</div>
                       <div class="col-md-4"><button class="btn m-2" @click = "toggleDriveStatus(d)">{{ d.approval }}</button></div>
                        
                    </div>
                <button class="btn m-2" @click = "prevDrivePage" :disabled="!drivePagination.hasPrev">Prev</button>
                <button class="btn m-2" @click="nextDrivePage" :disabled="!drivePagination.hasNext">Next</button>
                </div>
                
            </div>
        </div>
    </div>

</template>

<script>
import Navbar from '../components/navbar.vue';
import api from '../services/api.js';
export default{
    components:{Navbar},
    data(){
        return{drivePagination:{page:1, hasNext:false, hasPrev:false}, drives:[]
        }
    },
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        async getDrives(){
            const id = this.$route.params.id
            const res = await api.get(`/api/admin/companies/${id}/drives?page=${this.drivePagination.page}`)
            console.log(res)
            this.drives= res.data.data
            this.drivePagination.hasNext = res.data.meta.has_next
            this.drivePagination.hasPrev = res.data.meta.has_prev

        },
        prevDrivePage(){
            this.drivePagination.page--
            this.getDrives()
        },
        nextDrivePage(){
            this.drivePagination.page++
            this.getDrives()
        },
        async toggleDriveStatus(d){
            const newStatus = d.approval == "approved"?"rejected":"approved"
            d.approval = newStatus
            if (newStatus!="approved") await api.put(`/api/admin/drives/${d.drive_id}/reject`)
            else await api.put(`/api/admin/drives/${d.drive_id}/approve`)
            console.log("approval changed")
            await this.getDrives()
        },


    }, 
    mounted(){
        this.getDrives()
    }
}
</script>