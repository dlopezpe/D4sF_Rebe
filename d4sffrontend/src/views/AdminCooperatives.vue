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
                            label: this.$t('adminCoop.nombre')
                        },
                        {
                            key: 'cif',
                            label: this.$t('adminCoop.cif')
                        },
                        {
                            key: 'direction',
                            label: this.$t('adminCoop.direction')
                        },
                    ]"
                    :title="$t('adminCoop.listado_coop')"
                    :helperText='$t("adminEnterprise.info_nav")'
                    ref="table"
                    @row-select-changes="checkCoops"
                >
                    <template slot="actions">
                        <!-- Esta Opción solo tiene que estar disponible para admins -->
                        <cv-button small @click="nuevaCoop">{{$t("adminCoop.add_coop")}}</cv-button>
                    </template>
                    <template v-if="true" slot="batch-actions">
                        <cv-button @click="editarCoop" v-if="verEditarCoop">
                            {{$t("adminCoop.editar_coop")}}
                            <Edit32 class="bx--btn__icon" />
                        </cv-button>
                        <cv-button @click="eliminarCoopModal">
                            {{$t("adminCoop.delete_coop")}}
                            <TrashCan32 class="bx--btn__icon" />
                        </cv-button>
                    </template>
                    <template slot="data">
                        <cv-data-table-row
                            v-for="cooperative in cooperatives"
                            :key="`${cooperative.id}`"
                            :value="`${cooperative.id}`"
                        >
                            <cv-data-table-cell>{{cooperative.name}}</cv-data-table-cell>
                            <cv-data-table-cell>{{cooperative.cif}}</cv-data-table-cell>
                            <cv-data-table-cell>{{cooperative.direction}}</cv-data-table-cell>
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
            <newCooperative ref="modal" />
            <cv-modal
            ref="alerta_eliminar"
            kind="danger"
            :visible="false"
            @primary-click="eliminarCoop"
            :auto-hide-off='autoHideOff'
            >
                <template slot="label"><div id="targetClose" @mouseenter="cerrarModalEliminar">{{$t("adminCoop.seguro")}}</div></template>
                <template slot="title">{{$t("adminCoop.delete_coop")}}</template>
                <template slot="content">
                <p>{{$t("adminCoop.seguro_coop_del")}}</p>
                </template>
                <template slot="secondary-button">{{$t("adminCoop.cancelar")}}</template>
                <template slot="primary-button">{{$t("adminCoop.eliminar")}}</template>
            </cv-modal>
            <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        </div>
        <Footer/>
    </div>
</template>
<script>
import axios from "axios";
import Footer from "../views/Footer.vue";
import newCooperative from "../components/NewCooperative.vue"
import AlertaGeneral from "@/components/AlertaGeneral";
import Board from "@/views/Board.vue";
export default {
    name: "AdminCooperatives",
    props: {},
    components: {
        Footer,
        newCooperative,
        AlertaGeneral,
        Board
    },
    data() {
        return {
            cooperatives: Array(),
            mensajeAlerta: ``,
            tipoAlerta: ``,
            verEditarCoop: true,
            autoHideOff: true,
        }
    },
    methods: {
        cerrarModalEliminar(){
            const titulo = document.querySelectorAll('[aria-label="Eliminar Cooperativa"]');
            // const header_entero = titulo.parentElement.parentElement;
            // alert(titulo.parentElement.parentElement.classList[0])
            // console.log(header_entero)
            titulo[0].addEventListener('mouseenter', () => {
                console.log("Acabo de entrar");
                this.autoHideOff = false;
            });
            titulo[0].addEventListener('mouseleave', () => {
                // alert("Acabo de salir");
                this.autoHideOff = true;
            });
        },
        obtenerCooperativas(){
            const path = `${this.$apiURL}/cooperatives/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.cooperatives = response.data
            })
            .catch(error =>{
                console.warn(error)
            })
        },
        checkCoops(arrSel){
            if(arrSel.length === 1){
                this.verEditarCoop = true
            }else{
                this.verEditarCoop = false
            }
        },
        nuevaCoop(){
            this.$refs.modal.openModal()
        },
        editarCoop(){
            const rowSeleccionado = this.$refs.table.selectedRows
            if(rowSeleccionado.length === 1)
                this.$router.push(`/edit-cooperative?cooperative=${rowSeleccionado}`)
        },
        eliminarCoopModal(){
            this.$refs.alerta_eliminar.dataVisible = true
        },
        eliminarCoop(){
            let path = ''
            const rowSeleccionados = this.$refs.table.selectedRows
            for (const row in rowSeleccionados){
                path = `${this.$apiURL}/cooperatives/${rowSeleccionados[row]}/`
                axios
                .delete(path)
                .then(() => {
                    this.obtenerCooperativas();
                    this.mensajeAlerta = this.$t('adminCoop.del_coop_ok')
                    this.tipoAlerta = 'success'
                    this.$refs.alertaGeneral.verAlerta()
                })
                .catch(() =>{
                    this.obtenerCooperativas();
                    this.mensajeAlerta = this.$t('adminCoop.del_coop_ko')
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGeneral.verAlerta()
                });
                this.$refs.table.selectedRows = ''
                this.$refs.alerta_eliminar.hide()
            }
        },
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
    created(){
        this.getDatosUser()
        this.obtenerCooperativas()
        this.cerrarModalEliminar()
    },
    mounted(){
        this.cerrarModalEliminar()
    }
}
</script>
<style scoped>

</style>