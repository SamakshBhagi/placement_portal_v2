<template>
    <Login title = "Student" @login="loginUser"/>
</template>
<script>
    import Login from "../components/login.vue"
    import api from "../services/api.js"
    export default{
        components: {Login},
        methods: {
            async loginUser(data){
                try{
                    const response = await api.post("/api/auth/login",{
                        email:data.email,
                        password:data.password
                    })
                    console.log(response.data)
                    localStorage.setItem("token",response.data.data.token)
                    this.$router.push(`/student/dashboard`)

                }
                catch(error){
                    console.log("Failed...")
                }
            }
        }
    }
</script>