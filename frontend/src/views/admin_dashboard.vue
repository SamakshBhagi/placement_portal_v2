<template>
        <Navbar title ="Admin" :showSearch="true" @search="handleSearch" @logout = "logout"/>
        <div class="container m-2 p-4 bg-light">
            <div class="row g-3">
                <div class="col-10"><b>Total Students: {{students.meta.total_items  }}</b></div>
                
                <div class="col-10"><b>Total Companies: {{ companies.meta.total_items }}</b></div>
                
                <div class="col-10"><b>Total Ongoing Drives: {{ drives.meta.total_items }}</b></div>
            </div>
        </div>
        <div class="container mt-4">
            <div class="row g-4">
                <!-- registerations, drives, applications  -->
                <!-- if company is approved, ddrives are auto approved. --> 
                <div class="col-12">
                    <div class="card shadow-sm">
                        <div class="card-header">
                            Companies
                        </div>
                        <div class="card-body">
                            <div class="row fs-4 py-2 border-bottom">
                                <div class="col-md-3">NAME</div>
                                <div class="col-md-3">STATUS</div>
                                <div class="col-md-3">ACTION</div>
                                <div class="col-md-3">DEBAR</div>
                            </div>
                            <div v-for = "c in companies.data" :key="c.id" class = "row align-items-center border-bottom py-2">
                                <div class="col-md-3">{{ c.company_name }}</div>
                                <div class="col-md-3">{{ c.approval }}</div>
                                <div class="col-md-3"><button class="btn m-2" @click = "toggleCompanyApproval(c)">{{ c.approval=="approved"?"Reject":"Approve"}}</button></div>
                                <div class="col-md-3"><button class = "btn ms-4" :class="c.is_blacklisted? 'btn-primary':'btn-success'" @click="toggleCompanyBlacklist(c)">{{ c.is_blacklisted? "Unblacklist":"Blacklist" }}</button></div>
                            </div>
                            
                        <button class="btn m-2" @click = "prevCompanyPage" :disabled="!companyPagination.hasPrev">Prev</button>
                        <button class="btn m-2" @click="nextCompanyPage" :disabled="!companyPagination.hasNext">Next</button>
                        </div>
                    </div>
                </div>
                <div class="col-12">
                    <div class="card shadow-sm">
                        <div class="card-header">
                            Students
                        </div>
                        <div class="card-body">
                            <div class="row fs-4 py-2 border-bottom">
                                <div class="col-md-2">ID</div>
                                <div class="col-md-2">NAME</div>
                                <div class="col-md-3">STATUS</div>
                                <div class="col-md-2">ACTION</div>
                                <div class="col-md-3">DEBAR</div>
                            </div>
                            <div v-for = "s in students.data" :key="s.student_id" class = "row align-items-center border-bottom py-2">
                                <div class="col-md-2">{{ s.student_id}}</div>
                                <div class="col-md-2">{{ s.full_name }}</div>
                                
                                <div class="col-md-3">{{ s.approval }}</div>
                                <div class="col-md-2"><button class="btn m-2" @click = "toggleStudentsApproval(s)">{{ s.approval=="approved"?"Reject":"Approve"}}</button></div>
                                <div class="col-md-3 "><button class = "btn " :class="s.is_blacklisted ? 'btn-primary': 'btn-success'" @click="toggleStudentBlacklist(s)">{{ s.is_blacklisted? "Unblacklist": "Blacklist" }}</button></div>
                            </div>
                            <button class="btn m-2" @click = "prevStudentPage" :disabled="!studentPagination.hasPrev">Prev</button>
                            <button class="btn m-2" @click="nextStudentPage" :disabled="!studentPagination.hasNext">Next</button>
                        </div>
                    </div>
                </div>
                <div class="col-12">
                    <div class="card shadow-sm">
                        <div class="card-header">
                            Ongoing drives
                        </div>
                        <div class="card-body">
                            <div class="row fs-4 py-2 border-bottom">
                                <div class="col-md-1">ID</div>
                                <div class="col-md-2">COMPANY</div>
                                <div class="col-md-2">ROLE</div>
                                <div class="col-md-3">DEADLINE</div>
                                <div class="col-md-2">APPLICATIONS</div>
                                <div class="col-md-2">STATUS</div>
                            </div>
                            <div v-for = "d in drives.data" :key="d.drive_id" class = "d-flex justify-content-center align-items-center rounded p-2 mb-2">
                                <div class="col-md-1">{{d.drive_id}}</div>
                                <div class="col-md-2">{{d.company}}</div>
                                <div class="col-md-2">{{ d.job_role }}</div>
                                <div class="col-md-3">{{ d.deadline }}</div>
                                <div class="col-md-2">{{ d.app_count }}</div>
                                <div class="col-md-2"><button class="btn m-2" @click = "toggleDriveStatus(d)">{{ d.approval }}</button></div>
                                
                            </div>
                        <button class="btn m-2" @click = "prevDrivePage" :disabled="!drivePagination.hasPrev">Prev</button>
                        <button class="btn m-2" @click="nextDrivePage" :disabled="!drivePagination.hasNext">Next</button>
                        </div>
                        
                    </div>
                </div>
                <div class="col-12">
                    <div class="card shadow-sm">
                        <div class="card-header">
                            Applications
                        </div>
                        <div class="card-body">
                            <div class="row fs-4 py-2 border-bottom">
                                <div class="col-md-2">ID</div>
                                <div class="col-md-3">Student </div>
                                <div class="col-md-2">Company</div>
                                <div class="col-md-3">Date of application</div>
                                <div class="col-md-2">Status</div>
                            </div>
                            <div v-for = "a in applications.data"  class = "d-flex justify-content-center align-items-center rounded p-2 mb-2">
                                <div class="col-md-2">{{ a.application_id }}</div>
                                <div class="col-md-3">{{ a.student_name  }}</div>
                                <div class="col-md-2">{{ a.company_name }}</div>
                                <div class="col-md-3">{{ a.applied_at }}</div>
                                <div class="col-md-2">{{ a.status }}</div>
                            </div>
                        <button class="btn m-2" @click = "prevAppPage" :disabled="!applicationPagination.hasPrev">Prev</button>
                        <button class="btn m-2" @click="nextAppPage" :disabled="!applicationPagination.hasNext">Next</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
</template>

<script>
import Navbar from '../components/navbar.vue'
import api from "../services/api.js"


export default{
    name:"admin_dashboard",
    components:
    {Navbar},
    data(){
        return {
        students:{data:[],meta:{}},
        companies:{data:[],meta:{}},
        applications:{data:[],meta:{}},
        drives:{data:[],meta:{}},
        studentPagination:{
            page:1,
            hasNext:false,
            hasPrev:false
        },
        companyPagination:{
            page:1,
            hasNext:false,
            hasPrev:false
        },
        drivePagination:{
            page:1,
            hasNext:false,
            hasPrev:false
        },
        applicationPagination:{
            page:1,
            hasNext:false,
            hasPrev:false
        }
    }
    },
    methods:{
        handleSearch(payload){
            console.log(payload.role,payload.value)
            if(payload.role=="student"){
                this.$router.push( {path:`/admin/search/student`, query: {search: payload.value}})
            }else if(payload.role=="company"){
                this.$router.push({path:"/admin/search/company",query:{ search:payload.value}} )
            }
            
        },
        
        
        logout(){
            localStorage.removeItem("token")
            this.$router.push("/")
        },
        async getStudents(){
            const res = await api.get(`/api/admin/students?page=${this.studentPagination.page}`)
            this.students.data = res.data.data
            this.students.meta = res.data.meta
            this.studentPagination.hasNext = res.data.meta.has_next
            
            this.studentPagination.hasPrev = res.data.meta.has_prev
        },
        nextStudentPage(){
            this.studentPagination.page++
            this.getStudents()
        },
        prevStudentPage(){
            this.studentPagination.page--
            this.getStudents()
        },
        async toggleStudentBlacklist(student){
            console.log(student)
            if(student.is_blacklisted){
                const res = await api.post(`/api/admin/students/${student.student_id}/unblacklist`)
            }else{
                const res = await api.post(`/api/admin/students/${student.student_id}/blacklist`)

            }
            await this.getStudents()
        },
        async toggleStudentsApproval(s){
            if(s.approval=="approved"){
                await api.put(`/api/admin/students/${s.student_id}/reject`)
            }else await api.put(`/api/admin/students/${s.student_id}/approve`)
            await this.getStudents()
        },
        async getCompanies(){
            
            const res = await api.get(`/api/admin/companies?page=${this.companyPagination.page}`)
            console.log(res.data.data)
            this.companies = res.data
            this.companyPagination.hasNext = res.data.meta.has_next
            this.companyPagination.hasPrev = res.data.meta.has_prev
        },
        nextCompanyPage(){
            this.companyPagination.page++
            this.getCompanies()
        },
        prevCompanyPage(){
            this.companyPagination.page--
            this.getCompanies()
        },
        async toggleCompanyBlacklist(company){
            console.log(company)
            if(company.is_blacklisted){
                const res = await api.post(`/api/admin/companies/${company.id}/unblacklist`)
            }else{
                const res = await api.post(`/api/admin/companies/${company.id}/blacklist`)

            }
            await this.getCompanies()
        },
        async toggleCompanyApproval(c){
            if(c.approval=="approved"){
                await api.put(`/api/admin/companies/${c.id}/reject`)
            }else await api.put(`/api/admin/companies/${c.id}/approve`)
            console.log(c)
            await this.getCompanies()
        },
        async getDrives(){
            const res= await api.get(`/api/admin/drives?page=${this.drivePagination.page}`)
            
            this.drives.data = res.data.data
            this.drives.meta = res.data.meta
            this.drivePagination.hasNext = res.data.meta.has_next
            this.drivePagination.hasPrev = res.data.meta.has_prev
            console.log(this.drives)
        },
        nextDrivePage(){
            this.drivePagination.page++
            this.getDrives()
        },
        
        prevDrivePage(){
            this.drivePagination.page--
            this.getDrives()
        },
        async toggleDriveStatus(d){
            if (d.approval!="approved") await api.put(`/api/admin/drives/${d.drive_id}/approve`)
            else await api.put(`/api/admin/drives/${d.drive_id}/reject`)
            console.log("approval changed")
            await this.getDrives()
        },

        async getApplications(){
            const res = await api.get(`/api/admin/applications?page=${this.applicationPagination.page}`)
            this.applications = res.data
            this.applicationPagination.hasNext = res.data.meta.has_next
            this.applicationPagination.hasPrev = res.data.meta.has_prev 
            console.log(res)
            console.log("applications fetched")
        },
        prevAppPage(){
            this.applicationPagination.page--
            this.getApplications()
        },
        nextAppPage(){
            this.applicationPagination.page++;
            this.getApplications()
        }
        

    },
    mounted(){
        this.getStudents()
        this.getApplications()
        this.getCompanies()
        this.getDrives()
    }
}

</script>