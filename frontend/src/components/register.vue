<template>
<div class = "card shadow">
    <div class = "card-body">
        <h3 class = "text-center mb-3">{{title}}</h3>
        <form @submit.prevent=handleSubmit>
            <label class = "form-label">Name</label>
            <input v-model = "name" type = "text" class = "form-control" required></input>
            
            <label class= "form-label">Email</label>
            <input v-model = "email" type = "email" class = "form-control" required></input>
            <div v-if="student">
                <label class= "form-label">CGPA</label>
                <input v-model = "cgpa" type = "text" class = "form-control" required></input>
            </div>
            <label class= "form-label">Password</label>
            <input v-model = "password" type = "password" class = "form-control" required></input>
            <a class="btn btn-success m-2" @click="back">back</a>
            <button class = "btn btn-primary mt-3">register</button>
        </form>
    </div>
</div>
</template>

<script>
import { goBack } from '../services/back';
export default{
    props:{
        title:String, 
        student: Boolean
    },
    data(){
        return {name:"",
        email:"",
        password:"",cgpa:""}
    },
    methods: {
        handleSubmit(){
            this.$emit("register", {
                email: this.email,
                name: this.name, 
                password : this.password,
                cgpa:this.cgpa
            })
        },
        back(){goBack()}
    }

}
</script>