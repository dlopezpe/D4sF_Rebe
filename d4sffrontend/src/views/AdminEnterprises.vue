<template>
    <div @mousedown="keepPositionScroll" @mouseup="putPositionScroll">
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
                        key: 'cif',
                        label: this.$t('adminEnterprise.cif')
                    },
                    {
                        key: 'status',
                        label: this.$t('adminEnterprise.estado')
                    },
                    {
                        key: 'hectares',
                        label: this.$t('adminEnterprise.hectareas_disponibles')
                    },
                    {
                        key: 'hectaresUsed',
                        label: this.$t('adminEnterprise.hectareas_usadas')
                    },
                ]" :title="$t('adminEnterprise.listado_empresas') " :helperText='$t("adminEnterprise.info_nav")' ref="table"
                    :pagination="{ numberOfItems: enterprises.length, pageSizes: [10, 15, 20, 25, enterprises.length] }"
                    @pagination="actionOnPagination">
                    <template v-if="true" slot="actions">
                        <p></p>
                        <cv-button small @click="nuevaEmpresa">{{ $t("adminEnterprise.add_empresa") }}</cv-button>
                    </template>
                    <template v-if="use_batchActions" slot="batch-actions">
                        <cv-button @click="eliminarEmpresaModal">
                            {{ $t("adminEnterprise.eliminar") }}
                            <TrashCan32 class="bx--btn__icon" />
                        </cv-button>
                        <cv-button @click="editarEmpresa">
                            {{ $t("adminEnterprise.editar") }}
                            <Edit32 class="bx--btn__icon" />
                        </cv-button>
                        <cv-button @click="cambiarEstadoModal(idEmpresa)">
                            {{ $t("adminEnterprise.editar_estado") }}
                            <Account class="bx--btn__icon" />
                        </cv-button>
                    </template>
                    <template slot="data" >
                        <cv-data-table-row v-for="enterprise in enterprises.slice(start, start + length)"
                            :key="`${enterprise.id}`" :value="`${enterprise.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${enterprise.id} batch`"
                            >
                            <cv-data-table-cell>{{ enterprise.name }}</cv-data-table-cell>
                            <cv-data-table-cell>{{ enterprise.cif }}</cv-data-table-cell>
                            <cv-data-table-cell :style="enterprise.is_active ? 'color: #32a852' : 'color: #cc3939'">
                                {{ enterprise.is_active ? 'Activa' : 'Inactiva' }}
                            </cv-data-table-cell>
                            <cv-data-table-cell>{{ enterprise.hectares_available }}</cv-data-table-cell>
                            <cv-data-table-cell>{{ countParcels(enterprise.parcels) }}</cv-data-table-cell>
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
            <newEnterprise ref="modal" />
            <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
            <cv-modal ref="alerta_eliminar" kind="danger" :visible="visibleAlertaEliminar" @primary-click="eliminarUsuario" :auto-hide-off='autoHideOff'>
                <template slot="label"><div id="targetClose" @mouseenter="cerrarModalEliminar">{{ $t("adminEnterprise.seguro") }}</div></template>
                <template slot="title">{{ $t("adminEnterprise.eliminar") }}</template>
                <template slot="content">
                    <p>{{ $t("adminEnterprise.seguro_enterprise_del") }}</p>
                </template>
                <template slot="secondary-button">{{ $t("adminEnterprise.cancelar") }}</template>
                <template slot="primary-button">{{ $t("adminEnterprise.eliminar") }}</template>
            </cv-modal>
            <!-- MODAL CAMBIAR ESTADO -->
            <cv-modal ref="alerta_estado" :visible="visibleAlertaCambiarEstado" @primary-click="cambiarEstado" :auto-hide-off='autoHideOff'>
                <template slot="label"><div id="targetClose" @mouseenter="cerrarModalEditar">{{ $t("adminEnterprise.seguro") }}</div></template>
                <template slot="title">{{ $t("adminEnterprise.editar") }}</template>
                <template slot="content">
                    <p>{{ $t("adminEnterprise.txt_seguro_enterprise_status") }}</p>
                    <cv-select v-model="estadoSeleccionado" label="Selecciona un Estado">
                        <cv-select-option disabled selected hidden value="placeholder-item" >{{ estadoActual ? 'Activa' : 'Inactiva' }}</cv-select-option>
                        <cv-select-option value="1">{{ $t("adminEnterprise.activo") }}</cv-select-option>
                        <cv-select-option value="0">{{ $t("adminEnterprise.inactivo") }}</cv-select-option>
                    </cv-select>
                </template>
                <template slot="secondary-button">{{ $t("adminEnterprise.cancelar") }}</template>
                <template slot="primary-button" >{{ $t("adminEnterprise.guardar") }}</template>
                <!-- <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" /> -->
            </cv-modal>

        </div>
        <Footer />
    </div>
</template>
<script>
import axios from "axios";
import newEnterprise from "../components/newEnterprise.vue";
import Board from "@/views/Board.vue";
import Footer from "../views/Footer.vue";

import AlertaGeneral from "../components/AlertaGeneral";
export default {
    name: "AdminEnterprises",
    props: {},
    components: {
        newEnterprise,
        Footer,
        AlertaGeneral,
        Board
    },
    data() {
        return {
            autoHideOff: true,
            basicPagination: false,
            use_batchActions: true,
            hasExpandingRows: false,
            use_slottedData: true,
            visibleAlertaEliminar: false,
            visibleAlertaCambiarEstado: false,
            visibleAlertaConfirmacion: false,
            start: 0,
            length: 10,
            idEmpresaSeleccionada: null,
            nuevoEstadoSeleccionado: null,
            estadoActual: null,
            filaSeleccionada: null,
            columns3: [
                {
                    key: "name",
                    label: this.$t('adminEnterprise.nombre')
                },
                {
                    key: "cif",
                    label: this.$t('adminEnterprise.cif')
                },
                {
                    key: "status",
                    label: this.$t('adminEnterprise.estado')
                },
                {
                    key: "hectares",
                    label: this.$t('adminEnterprise.hectareas_disponibles')
                },
                {
                    key: "hectaresUsed",
                    label: this.$t('adminEnterprise.hectareas_usadas')
                },
            ],
            enterprises: [],
            userId: null,
            userMail: null,
            enterpriseId: null,
            scrollPosition: 0,
            // 
        }
    },
    methods: {

        /* Hago estas dos funciones por el reset de posición que hace la pagina sin ello.
        Cuando se elige una opcion de las checkboxes, se va directamente para arriba, pero con esta funcion, no lo hace */

        keepPositionScroll(){
            this.scrollPosition = window.scrollY;
            setTimeout(() => {
                document.body.style.overflow = "hidden";
                document.body.style.overflow = "auto";
            }, 0);
        },
        putPositionScroll(){
            setTimeout(() => {
                window.scrollTo(0, this.scrollPosition);
                document.body.style.overflow = "hidden";
                document.body.style.overflow = "auto";
            }, 0);
        },
        cerrarModal(){
            const titulo = document.getElementById('targetClose');
            const header_entero = titulo.parentElement.parentElement;
            header_entero.addEventListener('mouseenter', () => {
                this.autoHideOff = false;
            });
            header_entero.addEventListener('mouseleave', () => {
                this.autoHideOff = true;
            });
        },
        cerrarModalEliminar(){
            const titulo = document.querySelectorAll('[aria-label="Eliminar"]');
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
        cerrarModalEditar(){
            const titulo = document.querySelectorAll('[aria-label="Editar"]');
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
        countParcels(parcels) {
            //const regx = '/Ha/g;'
            let hectareas_disponibles = 0
            parcels.features.forEach(parcel => {
                hectareas_disponibles = (hectareas_disponibles + parcel.properties.area)
            })
            const total = Math.round((hectareas_disponibles + Number.EPSILON) * 100) / 100
            return total.toString().replace('.', ',')

        },
        // showAlert() {
        //     this.mensajeAlerta = "En desarrollo"
        //     this.tipoAlerta = 'info'
        //     this.$refs.alertaGeneral.verAlerta()
        // },
        showAlertSuccess(){
            this.mensajeAlerta = `${this.$t('newEnterprise.save_status')}`
            this.tipoAlerta = 'success'
            this.$refs.alertaGeneral.verAlerta()
        },

        
        actionOnPagination(ev) {
            this.start = ev.start - 1
            this.length = ev.length
        },
        obtenerListaEmpresas() {
            const path = `${this.$apiURL}/enterprises/`;
            axios.defaults.headers.common['Authorization'] = "Bearer " + sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                //this.enterprises = response.data
                // Ordena el arreglo 'enterprises' por el campo 'name'
                this.enterprises = response.data.slice().sort((a, b) => {
                    return a.name.localeCompare(b.name);
                });
                 
            }).catch(error =>{
                    console.log(error)
            })
        },

        editarEmpresa() {
            const rowSeleccionado = this.$refs.table.selectedRows
            this.$router.push(`/edit-enterprise?enterprise=${rowSeleccionado}`);
        },
        nuevaEmpresa(){
            const rowSeleccionado = this.$refs.table.selectedRows;
            if (rowSeleccionado.length > 1) {
                this.mensajeAlerta = `${this.$t('adminEnterprise.solo_una_empresa')}`;
                this.$refs.alerta.verAlerta()
            } else {
                this.userSeleccionado = rowSeleccionado[0]
                this.$refs.modal.openModal()
            }
            
        },
        cambiarEstado() {
            const rowSeleccionado = this.$refs.table.selectedRows;
            let flag = false;
            const nuevoEstado = this.estadoSeleccionado; //almaceno el nuevo estado
            this.showAlertSuccess();
            this.showAlertSuccess();
            rowSeleccionado.forEach(element => {
                console.log(element);
                this.enterpriseId = element;
                const path = `${this.$apiURL}/enterprises/${element}/`;
                axios
                .patch(path, { is_active: nuevoEstado }) //mando el estado a la bb.dd
                .then(() => {
                    this.showAlertSuccess();
                    this.showAlertSuccess();
                    this.obtenerListaEmpresas();
                    this.$refs.alerta_estado.dataVisible = false;
                    this.userId = sessionStorage.getItem("user");
                    console.log("Estado: ", this.estadoSeleccionado);
                    
                    if (typeof this.estadoSeleccionado != 'undefined') {
                        this.insertTraza();
                    }

                })
                .catch(response => {
                    flag = true;
                    console.error('Error:', response.error);
                });
            });

            if (flag) {
                this.$refs.alerta.verAlerta();
            } else {
                this.$refs.alerta_eliminar.hide();
            }
        },
        insertTraza(){
            axios.post(`${this.$apiURL}/insert_trazas/`,
            {
                id_user: this.userId,
                enterprise_code: this.enterpriseId,
                old_status: this.estadoActual,
                status: this.estadoSeleccionado,
                crud: "Nuevo estado: " + this.estadoSeleccionado + " de la empresa: " + this.enterpriseId + " por el usuario: " + this.userId
            }).catch(error => {
                console.error('Error al insertar en la base de datos:', error);
            });
        },
        cambiarEstadoModal() {
            this.filaSeleccionada = this.$refs.table.selectedRows;
            console.log(this.filaSeleccionada[0]);

            const url = `${this.$apiURL}/enterprises/${this.filaSeleccionada[0]}/`;

            axios.get(url)
                .then(response => {
                    this.estadoActual = response.data.is_active;
                    console.log("Estado activo:", this.estadoActual);
                })
                .catch(error => {
                    console.error("Error al obtener el estado de la empresa:", error);
                });
            this.$refs.alerta_estado.dataVisible = true;
        },
        eliminarEmpresaModal() {
            this.$refs.alerta_eliminar.dataVisible = true
        },
        eliminarUsuario() {
            const rowSeleccionado = this.$refs.table.selectedRows
            let flag = false
            rowSeleccionado.forEach(element => {
                console.log(element)
                const path = `${this.$apiURL}/enterprises/${element}/`
                axios
                    .delete(path)
                    .then(() => {
                        this.obtenerListaEmpresas();
                    })
                    .catch(response => {
                        flag = true
                        console.log(response.error)
                    });
            });
            if (flag) {
                console.error('error')
                this.mensajeAlerta = `${this.$t('adminEnterprise.del_empresa_error')}`;
                this.$refs.alerta.verAlerta()
            } else {
                this.$refs.alerta_eliminar.hide()
            }
        }
    },
    created() {
        this.obtenerListaEmpresas()
    },
    mounted() {
        this.cerrarModal();
        this.cerrarModalEliminar();
        this.cerrarModalEditar();
    }
}
</script>
<style scoped>
#grid-admin {
    margin-bottom: 70px;
}


</style>