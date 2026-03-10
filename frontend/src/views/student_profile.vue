<template>
    <Navbar :midPage="true" :student="true" :title ="student.name+`'s`"  @profile = "profile" @history = "history" @logout = "logout" />
    <div class="container m-2 p-4 bg-light">
        <div class="row p-2 g-3 "><div class="fs-4 fw-bold">Your details:</div></div>
        <div class="row p-2  fs-5">
        Name: {{student.name}}
        </div>
        <div class="row p-2  fs-5">
        CGPA: {{student.cgpa}}
        </div>
        <div class="row p-2  fs-5 align-items-center">
        Resume: <template v-if="student.resume_path"><button class="btn" @click="viewResume">View</button></template>
        <span v-else>Not uploaded yet...</span> 
        </div>

    </div>
    <div class="container m-2 p-4 bg-light">
        <div class="row p-2 g-3 "><div class="fs-4 fw-bold">EDIT:</div></div>
        <div class="row p-2  fs-5">
            <select v-model = "field">
                <option value="name">Name</option>
                <option value="cgpa">CGPA</option>
                <option value="resume">Resume</option>
            </select>
        </div>
        <div class="row p-2" v-if="field!='resume'">
            <input type="text" v-model = "value" >
        </div>

        <div class="row p-2" v-if="field=='resume'">
            <input class="form-control" accept=".pdf" type="file" @change="uploadResume" >
        </div>
        <div class="row p-2"><button class="btn" @click="update">Change</button></div>
        
    </div>
</template>
<script>
import Navbar from '../components/navbar.vue';
import api from '../services/api.js';
export default{
    name:"student_dashboard",
    components:{Navbar},
    data(){return{app:[], student:{}, field:"",file:null, value:""}},
    methods:{
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        history(){
            this.$router.push("/student/history")
            console.log("History")
        },
        profile(){
            this.$router.push("/student/profile")
            console.log("Profile")
        },
        async getStudent(){
            const res = await api.get(`/api/student/dashboard`)
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
        async viewResume(){
        
            const res =await  api.get(`/api/student/resume/${this.student.student_id}`, {responseType:"blob"})
            console.log(res)
            const url = window.URL.createObjectURL(new Blob([res.data],{ type : "application/pdf"}))
            window.open(url)
            
        }},  
    mounted(){
        this.getStudent()
        
    }
}
</script>
