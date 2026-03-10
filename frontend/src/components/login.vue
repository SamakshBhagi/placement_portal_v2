<template>
    <div class = "card shadow w-100">
        <div class = "card-body">
            <h3 class = "text-center mb-3">{{title}}</h3>
            <form @submit.prevent = "handleSubmit">
                <div class = "mb-3">
                    <label class = "form-label"> Email</label>
                    <input v-model = "email" class = "form-control" type = "email" placeholder ="yourID@iitm.com" required>
                </div> 
                <div class = "mb-3">
                    <label class = "form-label"> Password</label>
                    <input v-model = "password" class = "form-control" type = "password" placeholder ="" required>
                </div>
                <a class="btn btn-success m-2" @click="back">back</a>
                <button class = "btn btn-primary">login</button>
            </form>
        </div>
    </div>
</template>

<script>
import { goBack } from '../services/back';

export default{
    props:["title"],
    data(){
        return {email:"",
        password:""}
    },
    methods:{
        handleSubmit(){
            this.$emit("login", {
                email:this.email,
                password: this.password
            })
        },
        back(){goBack()}
    }
}
</script>