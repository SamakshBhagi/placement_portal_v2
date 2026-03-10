import {createRouter, createWebHistory} from "vue-router"
import landing from "../src/views/landing.vue"
import auth from "../src/layouts/auth.vue"
import student_register from "../src/views/student_register.vue"
import company_register from "../src/views/company_register.vue"
import admin_login from "../src/views/admin_login.vue"
import student_login from "../src/views/student_login.vue"
import company_login from "../src/views/company_login.vue"
import admin_dashboard from "../src/views/admin_dashboard.vue"
import company_dashboard from "../src/views/company_dashboard.vue"
import create_drive from "../src/views/create_drive.vue"
import update_drive from "../src/views/driveDetails.vue"
import update_application from "../src/views/application_details.vue"
import student_dashboard from "../src/views/student_dashboard.vue"
import student_profile from "../src/views/student_profile.vue"
import company_viewprofile from "../src/views/company_viewprofile.vue"
import student_history from "../src/views/student_history.vue"
import admin_csearch from "../src/views/admin_search_company.vue"
import admin_ssearch from "../src/views/admin_search_student.vue"
import admin_cdrives from "../src/views/admin_get_drives.vue"
const routes = [
    {
        path:"/",
        component:landing,
        meta:{public:true}
    },
    {
        path:"/",
        component:auth,
        children : [
        {
            path:"/admin/login",
            component:admin_login,
            meta:{public:true}
        },
        {
            path:"/admin/search/student",
            component:admin_ssearch
        },
        {
            path:"/admin/search/company",
            component:admin_csearch
        },
        {
            path:"/admin/search/:id/company_drives",
            component:admin_cdrives
        },
        {
            path:"/student/login",
            component:student_login,
            meta:{public:true}
        },
        {
            path:"/company/login",
            component:company_login,
            meta:{public:true}
            
        },
        {
            path:"/company/register",
            component:company_register,
            meta:{public:true}
        },
        {
            path:"/student/register",
            component:student_register,
            meta:{public:true}
        }
        ]
    },
    {
        path:"/admin/dashboard",
        component:admin_dashboard,
    },
    {
        path:"/company/dashboard",
        component:company_dashboard,
    },
    {
        path:"/company/createdrive",
        component:create_drive
    },
    {
        path:"/company/drive/:id",
        component:update_drive
    },
    {
        path:"/company/drive/:id/:s_id",
        component:update_application
    },
    {
        path:"/company/viewprofile/:id",
        component:company_viewprofile,
    },
    {
        path:"/student/dashboard",
        component:student_dashboard
    },
    {
        path:"/student/profile",
        component:student_profile
    },
    {
        path:"/student/history",
        component:student_history
    }
]

const router = createRouter({history:createWebHistory(), routes})
router.beforeEach((to, from , next)=>{
    const token = localStorage.getItem("token")
    if(!token && !to.meta.public){
        next("/")
    }
    next()
})
export default router