<template>
    <Login title = "Company" @login="loginUser"/>
    
</template>
<script>
    import Login from "../components/login.vue"
    import api from "../services/api.js"
    import { goBack } from "../services/back.js";
    export default{
        components: {Login},
        methods: {
            async loginUser(data){
                const res =await api.post(`/api/auth/login`,{
                    email:data.email,
                    password:data.password
                })
                console.log(res)
                localStorage.setItem("token",res.data.data.token)
                this.$router.push('/company/dashboard')
                console.log('logged in as company')
            },
        }
    }
</script>