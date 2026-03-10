<template>
    <Navbar :midPage="true" :student="true" :title ="student.name+`'s`"  @logout = "logout" />
    <div class="container m-2 p-4 bg-light">
        <div class="row p-2 g-3 "><div class="fs-4 fw-bold">Your details:</div></div>
        <div class="row p-2  fs-5">
        Name: {{student.name}}
        </div>
        <div class="row p-2  fs-5">
        CGPA: {{student.cgpa}}
        </div>
        <div class="row p-2  fs-5 align-items-center">
        Resume: <template v-if="student.resume_url"><button class="btn" @click="viewResume(student.student_id)">View</button></template>
        
        <span v-else>Not uploaded yet...</span> 
        </div>
        
    </div>
</template>
<script>
import Navbar from '../components/navbar.vue';
import api from '../services/api.js';
export default{
    components:{Navbar},
    data(){return{app:[], student:{}, field:"",file:null, value:""}},
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        async getStudent(id){
            const res = await api.get(`/api/company/student/${id}`)
            console.log(this.student)
            this.student= res.data.data
        
        },
        uploadResume(e){
            this.file = e.target.files[0]
        },
        async update(){
            if(this.field=='resume'){
                const data = new FormData()
                data.append("resume", this.file)
                await api.post("/api/student/upload-resume", data)
            }
            else{
                await api.put("/api/student/update", {field:this.field, value:this.value})
            }
            console.log("Updating...")
            await this.getStudent()
        },
        async viewResume(x){
            const res = await api.get(`/api/company/student/${x}/resume`, {responseType:"blob"})
            const url = window.URL.createObjectURL(res.data)
            window.open(url)            
        }},  
    mounted(){
        const id = this.$route.params.id
        this.getStudent(id)
        
    }
}
</script>
