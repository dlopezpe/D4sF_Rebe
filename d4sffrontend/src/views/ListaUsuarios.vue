<template>
    <div class="employee-list" @mousedown="keepPositionScroll" @mouseup="putPositionScroll">
        <cv-data-table :sortable="sortable" :columns="[
            {
                key: 'first_name',
                label: this.$t('empleados.nombre')
            },
            {
                key: 'last_name',
                label: this.$t('empleados.apellido')
            },
            {
                key: 'phone_number',
                label: this.$t('empleados.telefono')
            },

        ]" @sort="onSort" :title="$t('empleados.empleados_lista')" ref="table"
            :pagination="{ numberOfItems: usuarios.length, pageSizes: [10, 15, 20, 25, usuarios.length] }"
            @pagination="actionOnPagination">
            <template v-if="true" slot="actions">
                <cv-button small @click="nuevoUsuario">{{ $t("empleados.add") }}</cv-button>
            </template>
            <template v-if="use_batchActions" slot="batch-actions">
                <cv-button @click="onBatchAction1">
                    {{ $t("empleados.eliminar") }}
                    <TrashCan32 class="bx--btn__icon" />
                </cv-button>
                <cv-button @click="editarUsuario">
                    {{ $t("empleados.editar") }}
                    <Edit32 class="bx--btn__icon" />
                </cv-button>
                <cv-button @click="onBatchAction3" v-if="false">
                    Descargar
                    <Download16 class="bx--btn__icon" />
                </cv-button>
            </template>
            <template slot="data">
                <cv-data-table-row v-for="usuario in usuarios.slice(start, start + length)" :key="`${usuario.id}`"
                    :value="`${usuario.id}`"
                    :aria-label-for-batch-checkbox="`Custom aria label for row ${usuario.id} batch`">
                    <cv-data-table-cell>{{ usuario.first_name }}</cv-data-table-cell>
                    <cv-data-table-cell>{{ usuario.last_name }}</cv-data-table-cell>
                    <cv-data-table-cell>{{ usuario.phone_number }}</cv-data-table-cell>
                </cv-data-table-row>
            </template>
        </cv-data-table>
        <EditarUser ref="modal" :userSeleccionado="userSeleccionado" />
        <Alertas :tituloAlert="mensajeAlerta" ref="alerta" />
        <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        <cv-modal ref="alerta_eliminar" kind="danger" :visible="visibleAlertaEliminar" @primary-click="eliminarUsuario"
            :auto-hide-off='autoHideOff'>
            <template slot="label">
                <div id="targetClose" @mouseenter="cerrarModal">{{ $t("empleados.seguro") }}</div>
            </template>
            <template slot="title">{{ $t("empleados.eliminar") }}</template>
            <template slot="content">
                <p>{{ $t("empleados.seguro_user_del") }}</p>
            </template>
            <template slot="secondary-button">{{ $t("empleados.cancelar") }}</template>
            <template slot="primary-button">{{ $t("empleados.eliminar") }}</template>
        </cv-modal>
    </div>
</template> 
<script>
import axios from "axios";
//Componentes internos
import Alertas from "../components/Alertas.vue";
import EditarUser from "../components/EditarUser.vue";
import AlertaGeneral from "../components/AlertaGeneral";

export default {
    name: "ListaUsuarios",
    props: {},
    components: { Alertas, EditarUser, AlertaGeneral },
    data() {
        return {
            sortable: false,
            start: 0,
            length: 10,
            columns3: [
                {
                    key: "first_name",
                    label: this.$t('empleados.nombre')
                },
                {
                    key: "last_name",
                    label: this.$t('empleados.apellido')
                },
                {
                    key: "phone_number",
                    label: this.$t('empleados.telefono')
                },

            ],
            usuarios: [],
            basicPagination: false,
            use_batchActions: true,
            hasExpandingRows: false,
            use_slottedData: true,
            visibleAlertaEliminar: false,
            autoHideOff: true,
        };
    },
    methods: {
        keepPositionScroll(){
            this.scrollPosition = window.scrollY;
        },
        putPositionScroll(){
            setTimeout(() => {
                window.scrollTo(0, this.scrollPosition);
                console.log(this.scrollPosition);
            }, 0);
        },
        cerrarModal() {
            const titulo = document.getElementById('targetClose');
            const header_entero = titulo.parentElement.parentElement;
            header_entero.addEventListener('mouseenter', () => {
                this.autoHideOff = false;
            });
            header_entero.addEventListener('mouseleave', () => {
                this.autoHideOff = true;
            });

        },
        showAlert() {
            this.mensajeAlerta = this.$t('empleados.desarrollo')
            this.tipoAlerta = 'info'
            this.$refs.alertaGeneral.verAlerta()
        },
        actionOnPagination(ev) {
            this.start = ev.start - 1
            this.length = ev.length
        },
        getUsuariosEmpresa(idEmpresa) {
            this.idEmpresaEd = idEmpresa

            if (idEmpresa) {
                this.idEmpresaEd = idEmpresa;
                localStorage.setItem("enterprise", idEmpresa);
                sessionStorage.setItem("enterprise", localStorage.getItem("enterprise"));
            } else {
                this.idEmpresaEd = this.idEmpresaEd || localStorage.getItem("enterprise") || sessionStorage.getItem("enterprise");
            }   
            const path = `${this.$apiURL}/profiles_enterprises/${this.idEmpresaEd}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer " + sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                    this.usuarios = response.data
                })
        },
        editarUsuario() {
            const rowSeleccionado = this.$refs.table.selectedRows;
            if (rowSeleccionado.length > 1) {
                this.mensajeAlerta = `${this.$t('empleados.un_user_selec')}`;
                this.$refs.alerta.verAlerta()
            } else {
                this.userSeleccionado = rowSeleccionado[0]
                this.$refs.modal.openModal(this.userSeleccionado)
            }
        },
        nuevoUsuario() {
            this.$refs.modal.openModal()
        },
        onBatchAction1() {
            this.$refs.alerta_eliminar.dataVisible = true
            console.warn(this.$refs.alerta_eliminar.dataVisible)
        },
        eliminarUsuario() {
            const rowSeleccionado = this.$refs.table.selectedRows
            let flag = false
            rowSeleccionado.forEach(element => {

                /*
                    1. Buscamos por el usuario y sacamos el campo `user`
                    2. Eliminamos el perfil
                    3. Desabilitamos el usuario 
                    
                */

                const path = `${this.$apiURL}/profiles/${element}/`
                axios
                    .get(path)
                    .then(response => {
                        const user = response.data.user;
                        axios
                            .delete(`${this.$apiURL}/profiles/${element}/`)
                            .then(() => {
                                axios
                                    .delete(`${this.$apiURL}/permisos/${user}/`)
                                    .then(() => {
                                        const enterprise_id_ = (this.$route.query.enterprise) ? this.$route.query.enterprise : (this.$route.query.cooperative) ? this.$route.query.cooperative : ''
                                        this.getUsuariosEmpresa(enterprise_id_);
                                    })
                            })
                    })
                    .catch(response => {
                        flag = true
                        console.log(response.error)
                    });
            });
            if (flag) {
                console.error('error')
                this.mensajeAlerta = `${this.$t('empleados.user_error')}`;
                this.$refs.alerta.verAlerta()
            } else {
                this.$refs.alerta_eliminar.hide()
            }
        },
    },
    mounted() {
        const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer " + sessionStorage.getItem("apiAccess")
        axios
            .get(path_lang)
            .then(response => {
                this.$root.$i18n.locale = response.data.language
            })
    },
    created() {
        const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer " + sessionStorage.getItem("apiAccess")
        axios
            .get(path_lang)
            .then(response => {
                this.$root.$i18n.locale = response.data.language
            })
    }
};
</script> 
<style scoped>
.bx--modal-content {
    width: 100%;
    height: 100% !important;
    overflow: initial !important;
    overflow-y: initial;
}
</style>