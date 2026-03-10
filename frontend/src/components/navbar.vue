<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-3">
    
    <div class="navbar-brand fw-bold">
      {{ title }} Dashboard
    </div>
    <div class ="navbar-brand">
    </div>

    <div class="ms-auto d-flex align-items-center gap-2">
      
      <button class="btn btn-outline" @click="createDrive" v-if="newDrive"> New Drive </button>
      <div v-if="showSearch" class="d-flex gap-2">
        <select class = "form-select" v-model = "searchType" value="Choose fiter">
          <option disabled>Choose filter</option>
          <option value="student">Student</option>
          <option value="company">Company</option>
        </select>
        <input type="text" class="form-control" placeholder="Search..."  v-model="searchQuery" @keyup.enter="handleSearch" />

        <button class="btn btn-primary" @click="handleSearch">Search</button>
      </div>      
      
      <button v-if="student" class="btn btn-outline" @click="profile"> Profile </button>
      <button v-if="student" class="btn btn-outline" @click="history"> History </button>
      


      <button v-if="midPage" class="btn btn-outline" @click="back"> Back </button>

      <button class="btn btn-outline" @click="logout"> Logout </button>

    </div>

  </nav>
</template>



<script>
import { goBack } from '../services/back';

export default{
    props:{
        title:String, 
        showSearch: Boolean,
        newDrive:Boolean,
        midPage:Boolean,
        student:Boolean,
    },
    data(){
        return{
            searchQuery:"",
            searchType:""
        }
    },
    methods: {
        handleSearch(){
            this.$emit("search", {role:this.searchType, value:this.searchQuery})
        },
        logout(){
            this.$emit("logout")
        },
        createDrive(){
          this.$emit("createDrive")
        },
        back(){
          goBack()
        },
        profile(){this.$emit("profile")},
        history(){this.$emit("history")}
    }
}
</script>