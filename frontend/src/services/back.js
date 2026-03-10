import router from "../../router"
export function goBack(){
    const roles = router.currentRoute.value.path.split("/")
    if(roles[1]=="dashboard") pass
    else if(window.history.length>1) router.back()
    else router.push(`/${roles[0]}`)
    console.log(roles)

}