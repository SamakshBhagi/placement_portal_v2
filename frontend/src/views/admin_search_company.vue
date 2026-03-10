<template>
<Navbar :midPage="true" @logout = "logout" />
    <div class="container m-2 p-4 bg-light">
        <div class="row fw-bold">
            <div class="col-md-6">Name</div>
            <div class="col-md-6">Drives</div>
        </div>    
        <div class="row mt-4" v-for="c in companies">
            <div class="col-md-6">{{ c.company_name }}</div>
            <div class="col-md-6"><button class="btn p-2 border" @click = "seeDrives(c.id)">Drives</button></div>
        </div>
    </div>

</template>
<script>
import api from '../services/api.js'
import Navbar from '../components/navbar.vue'
export default{
    components:{Navbar},
    data(){
        return{companies:[]}
    },
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        async getCompanies(){
            const value = this.$route.query.search
            const res = await api.get(`/api/admin/companies?search=${value}`)
            this.companies = res.data.data
        },
        seeDrives(id){
            this.$router.push(`/admin/search/${id}/company_drives`)
        }   
    },
    mounted(){
        this.getCompanies()
    }
}
</script>