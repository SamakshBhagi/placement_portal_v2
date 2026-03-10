<template>
    <Register :student = "true" title = "Student" @register="registerUser"/>
</template>
<script>
    import Register from "../components/register.vue"
    import api from "../services/api.js"
    export default{
        components: {Register},
        methods: {
            async registerUser(fData){
                try{    
                    const payload = {
                        email:fData.email,
                        full_name: fData.name, 
                        password: fData.password,
                        cgpa: fData.cgpa
                    }
                    const response = await api.post("/api/auth/register/student", payload)
                    this.$router.push("/")
                    alert("Registered, kindly wait for admin's approval")
                    console.log(response)
                }
                catch(error){
                    alert(error, " has occured")
                }
            }
        }
    }
</script>