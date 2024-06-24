<template>
    <div>
        <Board />
        <div class="bx--grid" id="grid-admin">
            <br>
            <h2>{{$t("editCoop.title")}}</h2>
            <br><br>
            <EditarCooperativeComponent :cooperativeId="cooperative" ref="datoscooperative" />
            <br><br>
            <EditCooperativeComponentEnterpriseList :cooperativeId="cooperative" ref="cooperativeEnterprise" />
            <br><br>
            <ListaUsuarios  ref="listausuarios" />
        </div>
    </div>
</template>
<script>
import axios from "axios";
import EditarCooperativeComponent from "../components/EditCooperativeComponent.vue"
import EditCooperativeComponentEnterpriseList from "../components/EditCooperativeComponentEnterpriseList.vue"
import ListaUsuarios from "../views/ListaUsuarios.vue";
import Board from "@/views/Board.vue";
export default {
    name: "EditarCooperative",
    props: {},
    components: {
        EditarCooperativeComponent,
        EditCooperativeComponentEnterpriseList,
        ListaUsuarios,
        Board
    },
    data() {
        return{
            cooperative: ``,
            mensajeAlerta: ``,
            tipoAlerta: ``,
            
        }
    },
    methods: {
        getDatosUser(){
            if(sessionStorage.getItem("apiAccess")){
                const path = `${this.$apiURL}/profile/`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .get(path)
                .then(response => {
                    this.$session.start()
                    //---------------------------------------------------------------
                    this.$session.set('is_coop_user', response.data[0].cooperative_user)
                    this.$session.set('enterprise', response.data[0].enterprise_id)
                    this.$session.set('user', response.data[0].user)
                    sessionStorage.setItem('enterprise', response.data[0].enterprise_id)
                    sessionStorage.setItem('user', response.data[0].user)
                    let pathEnterpriseInstance = `${this.$apiURL}/enterprises/${response.data[0].enterprise_id}/`;
                    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                    axios.get(pathEnterpriseInstance)
                    .then(response =>{
                        sessionStorage.setItem('sI', response.data.sentinel_instance)
                        
                    })
                    //---------------------------------------------------------------
                    this.getPermisosUser(response.data[0].user)
                }).catch(error =>{
                    console.warn(error)
                })
            }
        },
        getPermisosUser(id){
            const pathRol = `${this.$apiURL}/permisos/${id}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(pathRol)
            .then(response => {
                //---------------------------------------------------------------
                this.$session.set('is_enterpriseadmin', response.data.is_enterpriseadmin)
                this.$session.set('is_staff', response.data.is_staff)
                this.$session.set('is_superuser', response.data.is_superuser)
                this.$session.set('is_systemadmin', response.data.is_systemadmin)
                sessionStorage.setItem('is_enterpriseadmin', response.data.is_enterpriseadmin)
                sessionStorage.setItem('is_staff', response.data.is_staff)
                sessionStorage.setItem('is_superuser', response.data.is_superuser)
                sessionStorage.setItem('is_systemadmin', response.data.is_systemadmin)
                this.$parent.is_superuser = response.data.is_superuser
                this.$parent.is_staff = response.data.is_staff,
                this.$parent.is_systemadmin = response.data.is_systemadmin,
                this.$parent.is_enterpriseadmin = response.data.is_enterpriseadmin
                this.$parent.customLinkEnterprise = 'edit-enterprise?enterprise='+this.$session.get('enterprise')
                this.$parent.$parent.is_coop_user = this.$session.get('is_coop_user')
                this.$parent.$parent.customLinkCoop = 'edit-cooperative?cooperative='+this.$session.get('enterprise')
            })
        },
    },
    mounted(){
        this.cooperative = this.$route.query.cooperative
        this.$refs.listausuarios.getUsuariosEmpresa(this.$route.query.cooperative)
        this.getDatosUser()
    },
    created(){}
}
</script>
<style scoped>

</style>