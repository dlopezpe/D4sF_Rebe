<template>
    <cv-modal
        @primary-click="actionPrimary"
        ref="newCooperativeForm"
        :auto-hide-off='autoHideOff'
    >
        <template v-if="true" slot="label">{{$t("editCoop.title")}}</template>
        <template v-if="true" slot="title">{{$t("editCoop.title")}}</template>
        <template v-if="true" slot="content" class="formcontent" ref="content_form">
            <div class="bx--row">
                <div class="bx--col-lg-12 bx--col-md-12 bx--col-sm-12">
                    <cv-data-table
                        :sortable="false"
                        :columns="[
                            {
                                key: 'name',
                                label: this.$t('adminEnterprise.nombre')
                            },
                            {
                                key: 'cif',
                                label: this.$t('adminEnterprise.cif')
                            },
                        ]"
                        :title="$t('adminEnterprise.listado_empresas')"
                        ref="tableEmpresas"
                        :rows-selected="enterprisesInCoop"
                        :key="componentKey"
                    >
                        <template v-if="true" slot="batch-actions">
                            <cv-button>
                                {{''}}
                            </cv-button>
                        </template>

                        <template slot="data">
                            <cv-data-table-row
                                v-for="enterprise in enterprises"
                                :key="`${enterprise.id}`"
                                :value="`${enterprise.id}`"
                                
                            >
                                <cv-data-table-cell>{{enterprise.name}}</cv-data-table-cell>
                                <cv-data-table-cell>{{enterprise.cif}}</cv-data-table-cell>
                            </cv-data-table-row>
                        </template>
                    </cv-data-table>
                </div>
            </div>
        </template>
        <template v-if="true" slot="primary-button">{{$t("newEnterprise.guardar")}}</template>
    </cv-modal>
</template>
<script>
import axios from "axios";
export default {
    name: "NewCooperative",
    props: {
        cooperative_id: String
    },
    components: {},
    data() {
        return {
            invalidMessageNombre: ``,
            invalidMessageDirection: ``,
            invalidMessagePhone: ``,
            invalidMessageCif: ``,
            enterprises: Array(),
            start: 0,
            length: 10,
            mensajeAlerta: ``,
            tipoAlerta: ``,
            parent: Object,
            cooperative: ``,
            enterprisesInCoop: [],
            componentKey: 0,
            autoHideOff: true,
        }
    },
    methods: {
        cerrarModalEditarCooperativa(){
            const titulo = document.querySelectorAll('[aria-label="Editar Cooperativa"]');
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
        cerrarModalEditarUser(){
            const titulo = document.querySelectorAll('[aria-label="Editar usuario"]');
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
        openModal() {
            this.cooperative = this.cooperative_id
            this.$refs.newCooperativeForm.show()
            this.parent = this.$refs.newCooperativeForm.$parent.$parent
            this.obtenerEmpresas()
        },
        obtenerEmpresas(){
            const path = `${this.$apiURL}/enterprises/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.enterprises = response.data
                this.getListaSeleccionados()
            }).catch(error =>{
                console.info(error)
            })
        },
        getListaSeleccionados(){
            const path = `${this.$apiURL}/cooperatives/${this.cooperative}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                //this.enterprisesInCoop = response.data.enterprises
                response.data.enterprises.forEach(element => {
                    this.enterprisesInCoop.push(element.id)
                });
            }).catch(error =>{
                console.info(error)
            })
            console.info(this.enterprisesInCoop)
        },
        actionPrimary(){
            const rowSeleccionados = this.$refs.tableEmpresas.selectedRows
            if(rowSeleccionados.length == 0){
                return false
            }
            let path = `${this.$apiURL}/cooperativesr/${this.cooperative}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .put(path, {
                id_empresas: rowSeleccionados,
                enterprises: rowSeleccionados
            })
            .then(() => {
                this.parent.mensajeAlerta = this.$t('newCoop.create_coop_success')
                this.parent.tipoAlerta = 'success'
            
                this.parent.$refs.alertaGeneral.verAlerta()
                this.parent.getDatosCoop()
                this.$refs.newCooperativeForm.hide()
                
            })
            .catch(error => {
                if(error.response.data.name[0].includes('not be blank')){
                    this.invalidMessageNombre = `${this.$t('newCoop.invalido_blank')}`
                }
            })
        }
    },
    created(){
    },
    mounted(){
        this.cerrarModalEditarCooperativa();
        this.cerrarModalEditarUser();
    }

}
</script>
<style scoped>

</style>