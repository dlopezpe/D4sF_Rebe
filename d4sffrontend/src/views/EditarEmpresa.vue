<template>
    <div>
        <Board />
        <div class="bx--grid" id="grid-admin">
            <br>
            <h2>{{$t("newEnterprise.editar_enterprise")}}</h2>
            <br><br>
            <EditarEmpresaComponent :idEmpresa="enterprise" ref="datosempresa" />
            <br><br>
            <ListaUsuarios  ref="listausuarios" />
            <br><br>
            <ParcelsList/>
            <br><br>
            
        </div>
        <Footer/>
    </div>
</template>
<script>
import EditarEmpresaComponent from "../components/EditarEmpresaComponent.vue";
import ListaUsuarios from "../views/ListaUsuarios.vue";
import ParcelsList from "../views/ParcelsList.vue";
import Footer from "../views/Footer.vue";
import Board from "@/views/Board.vue";
import axios from "axios";
export default {
    name: "EditarEmpresa",
    props: {},
    components: {
        EditarEmpresaComponent,
        ListaUsuarios,
        ParcelsList,
        Footer,
        Board
    },
    data() {
        return {
            enterprise: ''
        }
    },
    methods: {
        getDatosUser(){
            if(sessionStorage.getItem("apiAccess")){
                const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .get(path_lang)
                .then(response =>{
                    this.$root.$i18n.locale = response.data.language
                })
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
                this.$parent.is_enterpriseadmin = response.data.is_enterpriseadmin,
                this.$parent.customLinkEnterprise = 'edit-enterprise?enterprise='+this.$session.get('enterprise')
                this.$parent.$parent.is_coop_user = this.$session.get('is_coop_user')
                this.$parent.$parent.customLinkCoop = 'edit-cooperative?cooperative='+this.$session.get('enterprise')
                //---------------------------------------------------------------
                this.montarMapa()
            })
        },
    },
    mounted() {
        const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path_lang)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
        this.enterprise = this.$route.query.enterprise
        this.$refs.datosempresa.getDatosEmpresa(this.enterprise)
        this.$refs.listausuarios.getUsuariosEmpresa(this.enterprise)
    },
    created() {
        const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path_lang)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
        this.getDatosUser()
    }
}
</script>
<style scoped>
#grid-admin{
        margin-bottom: 50px;
    }
</style>