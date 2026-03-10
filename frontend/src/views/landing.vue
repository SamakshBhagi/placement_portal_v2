<template>
<div class = "container mt-3 text-center ">
    <h1 class = "mb-5"> Placement Portal </h1>
    <div class = "row justify-content-center">
        <div class = "col-md-4">
            <div class = "card p-3">
                <h3> Admin? Login here</h3>
                <router-link to = "/admin/login" class = "btn btn-primary mt-2">
                Login</router-link>
            </div>
        </div>
        <div class = "col-md-4">
            <div class = "card p-3">
                <h3> Students </h3>
                <router-link to = "/student/login" class = "btn btn-primary mt-2">
                Login
                </router-link>
                <router-link to = "/student/register" class = "btn btn-success mt-2">
                Register
                </router-link>
            </div>
        </div>
        <div class = "col-md-4">
            <div class = "card p-3">
            <h3> Company </h3>
                <router-link to = "/company/login" class = "btn btn-primary mt-2">
                Login
                </router-link>
                <router-link to = "/company/register" class = "btn btn-success mt-2">    
                Register
                </router-link>
            </div>
        </div>
    </div>
</div>
</template>