
<template>
    <div>
        <Board />
        <div class="bx--grid" id="grid-admin">
            <div class="group-list">
                <cv-data-table
                    :sortable="false"
                    :columns="[
                        {
                            key: 'name',
                            label: this.$t('adminEnterprise.nombre')
                        },
                        {
                            key: 'apellido',
                            label: this.$t('empleados.apellido')
                        },
                        {
                            key: 'Empresa',
                            label: this.$t('app.emprise')
                        },
                        {
                            key: 'Login',
                            label: this.$t('login.login')
                        },
                    ]"
                    :title="enterpriseSel.length > 0 ? $t('map.listado_usuarios') + ' - ' +enterpriseSel[0].name : $t('map.listado_usuarios')"
                    ref="table" :helperText='$t("adminEnterprise.info_nav")'
                    :pagination="{ numberOfItems: usersSel.length, pageSizes: [10, 15, 20, 25, usersSel.length] }" @pagination="actionOnPagination"
                >
                <template v-if="true" slot="actions">
                    <cv-search :placeholder="$t('parcelas.place_buscar')" @input="onBuscar"></cv-search>
                    <div id="sentinelLayers">
                        <cv-select
                        theme=""
                        :hide-label="false"
                        :inline="false"
                        :disabled="false"
                        @change="seleccionaEmpresa"
                        label=""
                        >
                            <cv-select-option disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                            <cv-select-option :value="`all`">Todas</cv-select-option>
                            
                            <cv-select-option v-for="empresa in allEnterprises" :value="String(empresa.id)"  v-bind:key="empresa.id">
                                {{empresa.name}}
                            </cv-select-option>
                        </cv-select>
                    </div>
                </template>
                    <template slot="data">
            
                        <cv-data-table-row
                            v-for="user in usersSel.slice(start, start+length)"
                            :key="`${user.id}`"
                            :value="`${user.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${user.id} batch`"
                            
                        >
                            <cv-data-table-cell >{{user.first_name}}</cv-data-table-cell>
                            <cv-data-table-cell >{{user.last_name}}</cv-data-table-cell>
                            <cv-data-table-cell >{{getEmprise(user.enterprise_id)}}</cv-data-table-cell>
                            <cv-data-table-cell >{{getUltAcc(user.user) | formatDate}}</cv-data-table-cell>

                        </cv-data-table-row>
                        
                        
                    </template>
                    
                </cv-data-table>
            </div>
        </div>
        <Footer/>
    </div>
    
</template>


<script>
//v-show="getEmprise(user.id) != 'no encontrado' "
import axios from "axios";
import Board from "@/views/Board.vue";
import Footer from "../views/Footer.vue";

export default {
    name: "AdminUsers",
    props: {},
    components: {
        Footer,
        Board
    },
    data() {
        return {
            basicPagination: false,
            use_batchActions: true,
            hasExpandingRows: false,
            use_content: true,
            use_slottedData: true,
            visibleAlertaEliminar: false,
        
            start: 0,
            length: 10,
            columns3: [
                {
                    key: "user",
                    label: this.$t('adminEnterprise.nombre')
                },
                {
                    key: "lastlogin",
                    label: this.$t('adminEnterprise.cif')
                },
            ],
            users: [],
            userList:[],
            usersName: [],
            enterprises: [],
            userSeleccionado : "",
            //Fermin
            allEnterprises: Array(),
            allUsers: Array(),
            enterpriseSel: Array(),
            usersSel: Array(),
            ultimosAcc: Array(),
        }
    },
    methods: {
        getUltAcc(userID){
            const result = this.ultimosAcc.filter(user => user.id === userID)
            if(result.length > 0){
                return result[0].last_login
            }
            return 'No login'
        },
        onBuscar(search){
            let result = Array()
            if(this.enterpriseSel.length > 0){
                result = this.allUsers.filter(user => {
                    if(user.first_name.includes(search) && this.enterpriseSel[0].id === user.enterprise_id){
                        return user
                    }
                })
                this.usersSel = result
            }else{
                result = this.allUsers.filter(user => {
                    if(user.first_name.includes(search)){
                        return user
                    }
                })
                this.usersSel = result
            }
        },
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        seleccionaEmpresa(empresa){
            if(empresa === 'all'){
                this.usersSel = this.allUsers
                this.enterpriseSel = Array()
            }else{
                this.usersSel = this.allUsers.filter( x=> x.enterprise_id == empresa )
                this.enterpriseSel = this.allEnterprises.filter(enterprise => enterprise.id === empresa)
            }
        },
        obtenerListaEmpresas(){
            const path = `${this.$apiURL}/profiledata/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                const data = response.data
                this.users = data.filter( x=> x.last_login != null) 
                //console.info(this.users)
            })   
            //esta funcion hace lo mismo
            
            const path2 = `${this.$apiURL}/profiles/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path2)
            .then(response =>{
                this.usersName = response.data
            })
            
            this.getEnterprise()
        },
        getEnterprise(){
            /*
            const path3 = `${this.$apiURL}/enterprises/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path3)
            .then(response => {
                this.enterprises = response.data
                this.allEnterprises = response.data
            }).catch(error =>{
                console.info(error)
            })
        
            const idSmartbits = '178e5240-1a64-4631-a95d-a9a8f70f3305'
            if(this.$session.get('enterprise') != idSmartbits ){
                this.enterprises = this.enterprises.filter( x=> x.name != 'Smartbits') 
                this.allEnterprises = this.enterprises.filter( x=> x.name != 'Smartbits')
            } 
            */
        },
        getName(userid){
            let name = "no encontrado"
            this.usersName.forEach((value) => {
                if (value.user == userid ){
                        name= value.first_name
                    }  
                });
                return name
        },
        getlastame(userid){
            let name = "no encontrado"
            this.usersName.forEach((value) => {
                if (value.user == userid ){
                    name= value.last_name
                }  
            });
            return name
        },
        getEmprise(userid){
            let name = "no encontrado"
            /*
            this.usersName.forEach((value) => {
                if (value.user == userid ){
                    this.enterprises.forEach((valueEm) => {
                        if (value.enterprise_id == valueEm.id ){
                            name= valueEm.name
                        }  
                    });
                }  
            });
            */
            const result = this.allEnterprises.filter(enterpise => enterpise.id === userid)
            if(result.length > 0){
                return result[0].name
            }
            return name
        },
        //Fermin
        obtenerListadoEmpresas(){
            const path3 = `${this.$apiURL}/enterprises/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path3)
            .then(response => {
                this.allEnterprises = response.data

                const idSmartbits = '178e5240-1a64-4631-a95d-a9a8f70f3305'
                if(this.$session.get('enterprise') != idSmartbits ){
                    this.allEnterprises = this.allEnterprises.filter( x=> x.name != 'Smartbits')
                }
                //this.enterpriseSel = this.allEnterprises.filter( x=> x.id == this.$session.get('enterprise'))
                //this.enterpriseSel[0].push({name: 'Todas las empresas'})
                this.getAllUsers()
            }).catch(error =>{
                console.info(error)
            })
        
        },
        getAllUsers(){
            const arrUsuarios = Array()
            let path = ``
            this.allEnterprises.forEach(enterprise => {
                path = `${this.$apiURL}/profiles_enterprises/${enterprise.id}/`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .get(path)
                .then(response => {
                    response.data.forEach(usuario => {
                        arrUsuarios.push(usuario)
                    })
                })
            })
            this.allUsers = arrUsuarios
            this.usersSel =  arrUsuarios
        },
        getUltimosAccesos(){
            const path = `${this.$apiURL}/profiledata/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                this.ultimosAcc = response.data
                /*
                const data = response.data
                this.users = data.filter( x=> x.last_login != null) 
                //console.info(this.users)
                */
            })  
        },

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
                //---------------------------------------------------------------
                this.obtenerListadoEmpresas()
                this.getUltimosAccesos()
            })
        },
    },
    created(){
        this.getDatosUser()
    },
    mounted(){
        this.getDatosUser()
    }
}
</script>
<style scoped>
    #grid-admin{
        margin-bottom: 50px;
    }
</style>