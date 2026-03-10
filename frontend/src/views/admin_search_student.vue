<template>
<Navbar :midPage="true" @logout = "logout" />
    <div class="container m-2 p-4 bg-light">
        <div class="row fw-bold" v-if="students.length==0">No students found...</div>
        <div class="row fw-bold" v-else>
            <div class="col-md-3">Name</div>
            <div class="col-md-3">CGPA</div>
            <div class="col-md-3">Approval</div>
            <div class="col-md-3">Profile</div>
        </div>    
        <div class="row p-2" v-for="s in students"  :key="s.student_id">
            <div class="col-md-3">{{ s.full_name }}</div>
            <div class="col-md-3">{{ s.cgpa }}</div>
            <div class="col-md-3">{{ s.approval }}</div>
            <div class="col-md-3" ><button class = "btn p-2 border" v-if="s.resume_path" @click="viewResume(s.resume_path)" >View Resume</button>
            <span v-else>Not uploaded</span>
            </div>
        </div>    
        
    </div>

</template>
<script>
import api from '../services/api.js'
import Navbar from '../components/navbar.vue'
export default{
    components:{Navbar},
    data(){
        return{students:[]}
    },
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        async getStudents(){
            const search = this.$route.query.search
            const res = await api.get(`/api/admin/students?search=${search}`)
            this.students = res.data.data
        },
        viewResume(path){
            console.log(path)
            window.open(`http://localhost:5000/api/admin/${path}`)
        }
    },
    mounted(){
        this.getStudents()
    }
}
</script>