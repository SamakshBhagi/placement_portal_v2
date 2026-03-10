<template>
    <Register title = "Company" @register="registerUser"/>
</template>
<script>
    import Register from "../components/register.vue"
    import api from "../services/api.js"
    
    import { goBack } from '../services/back';
    export default{
        components: {Register},
        methods: {
            async registerUser(fData){
                try{
                    const payload ={
                        email:fData.email,
                        company_name: fData.name,
                        password: fData.password
                    }
                    const response = await api.post("/api/auth/register/company",payload) 
                    console.log(response.data)
                    this.$router.push("/")
                    alert("Registered! Pending admin approval")
                }
                catch(error){
                    console.error(error)
                    alert("Failed!")

                }

            },
        }
    }
</script>