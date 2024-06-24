<template>
    <cv-modal
        @primary-click="actionPrimary"
        ref="newCooperativeForm"
        :auto-hide-off='autoHideOff'
    >
        <template v-if="true" slot="label"><div @mouseenter="cerrarModalNuevaCoop">{{$t("newCoop.nueva")}}</div></template>
        <template v-if="true" slot="title">{{$t("newCoop.nueva")}}</template>
        <template v-if="true" slot="content" class="formcontent" ref="content_form">
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="$t('newCoop.nombre')"
                        value=""
                        :disabled="false"
                        :type="`text`"
                        :placeholder="$t('newCoop.nombrePlace')"
                        :invalid-message="invalidMessageNombre"
                        ref="inputNameCoop"
                    ></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="$t('newCoop.direction')"
                        value=""
                        :disabled="false"
                        :type="`text`"
                        :placeholder="$t('newCoop.directionPlace')"
                        :invalid-message="invalidMessageDirection"
                        ref="inputDirectionCoop"
                    ></cv-text-input>
                </div>
            </div>
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="$t('newCoop.phone')"
                        value=""
                        :disabled="false"
                        :type="`text`"
                        :placeholder="$t('newCoop.phonePlace')"
                        :invalid-message="invalidMessagePhone"
                        ref="inputPhoneCoop"
                    ></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="$t('newCoop.cif')"
                        value=""
                        :disabled="false"
                        :type="`text`"
                        :placeholder="$t('newCoop.cifPlace')"
                        :invalid-message="invalidMessageCif"
                        ref="inputCifCoop"
                    ></cv-text-input>
                </div>
            </div>
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
                        :pagination="{ numberOfItems: enterprises.length, pageSizes: [10, 15, 20, 25, enterprises.length] }" @pagination="actionOnPagination"
                    >
                        <template v-if="true" slot="batch-actions">
                            <cv-button>
                                {{''}}
                            </cv-button>
                        </template>

                        <template slot="data">
                            <cv-data-table-row
                                v-for="enterprise in enterprises.slice(start, start+length)"
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
    props: {},
    components: {},
    data() {
        return {
            autoHideOff: true,
            invalidMessageNombre: ``,
            invalidMessageDirection: ``,
            invalidMessagePhone: ``,
            invalidMessageCif: ``,
            enterprises: Array(),
            start: 0,
            length: 10,
            mensajeAlerta: ``,
            tipoAlerta: ``,
            parent: Object
        }
    },
    methods: {
        cerrarModalNuevaCoop(){
            const titulo = document.querySelectorAll('[aria-label="Nueva Cooperativa"]');
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
            }).catch(error =>{
                console.info(error)
            })
        },
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        actionPrimary(){
            const rowSeleccionados = this.$refs.tableEmpresas.selectedRows
            if(rowSeleccionados.length == 0){
                return false
            }
            let path = `${this.$apiURL}/cooperativess/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .post(path, {
                name: this.$refs.inputNameCoop.$refs.input.value,
                direction: this.$refs.inputDirectionCoop.$refs.input.value,
                phone_number: this.$refs.inputPhoneCoop.$refs.input.value,
                cif: this.$refs.inputCifCoop.$refs.input.value,
                id_empresas: rowSeleccionados,
                //enterprises: rowSeleccionados
            })
            .then(() => {
                this.parent.mensajeAlerta = this.$t('newCoop.create_coop_success')
                this.parent.tipoAlerta = 'success'
                this.parent.$refs.alertaGeneral.verAlerta()
                this.parent.obtenerCooperativas()
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
    mounted() {
        this.cerrarModalNuevaCoop();
    },
}
</script>
<style scoped>

</style>