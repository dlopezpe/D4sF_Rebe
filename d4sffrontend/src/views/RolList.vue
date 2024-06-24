<template>
    <div class="bx--grid">
        <div class="group-list">
            <cv-data-table
                :sortable="sortable"
                :columns="columns3"
                @sort="onSort"
                title="Lista de Roles"
                ref="table"
            >
                <template v-if="true" slot="actions">
                    <cv-button small @click="actionNew">Añadir nuevo</cv-button>
                </template>
                <template v-if="use_batchActions" slot="batch-actions">
                    <cv-button @click="onBatchAction1">
                        Eliminar
                        <TrashCan32 class="bx--btn__icon" />
                    </cv-button>
                    <cv-button @click="onBatchAction2">
                        Editar
                        <Edit32 class="bx--btn__icon" />
                    </cv-button>
                    <cv-button @click="onBatchAction3" v-if="false">
                        Descargar
                        <Download16 class="bx--btn__icon" />
                    </cv-button>
                </template>
                <template slot="data">
                    <cv-data-table-row
                        v-for="usuario in usuarios"
                        :key="`${usuario.id}`"
                        :value="`${usuario.id}`"
                        :aria-label-for-batch-checkbox="`Custom aria label for row ${usuario.id} batch`"
                    >
                        <cv-data-table-cell>{{usuario.id}}</cv-data-table-cell>
                        <cv-data-table-cell>{{usuario.name}}</cv-data-table-cell>
                        <cv-data-table-cell>{{usuario.description}}</cv-data-table-cell>
                    </cv-data-table-row>
                </template>
            </cv-data-table>
            <EditarRol ref="modal" :userSeleccionado="userSeleccionado" />
            <Alertas :tituloAlert="mensajeAlerta" ref="alerta" />
            <cv-modal
            ref="alerta_eliminar"
            kind="danger"
            :visible="visibleAlertaEliminar"
            @primary-click="actionPrimary">
                <template slot="label">¿Estás seguro?</template>
                <template slot="title">Eliminar</template>
                <template slot="content">
                <p>Seguro que quieres eliminar el/los rol/es?</p>
                </template>
                <template slot="secondary-button">Cancelar</template>
                <template slot="primary-button">Eliminar</template>
            </cv-modal>
        </div>
    </div>
</template>
<script>
import axios from "axios";
import Alertas from "../components/Alertas.vue";
import EditarRol from "../components/EditarRol.vue";

export default {
    name: "RolList",
    props: {},
    components: {
        Alertas,
        EditarRol
    },
    data() {
        return {
        sortable: false,
        columns3: [
            {
            key: "id",
            label: "ID"
            },
            {
            key: "name",
            label: "Nombre"
            },
            {
            key: "description",
            label: "Descripción"
            },
        ],
        usuarios: [],
        basicPagination: false,
        use_batchActions: true,
        hasExpandingRows: false,
        use_slottedData: true,
        mensajeAlerta: "", 
        userSeleccionado: '',
        visibleAlertaEliminar: false
        };
    },
    methods: {
        getUsers() {
        const path = "${this.$apiURL}/roles/";
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
            .get(path)
            .then(response => {
            this.usuarios = response.data;
            })
            .catch(error => {
            console.error(error);
            });
        },
        onSort(order) {
        console.log(order.order);
        },
        onBatchAction2() {
        const rowSeleccionado = this.$refs.table.selectedRows;
        if (rowSeleccionado.length > 1) {
            this.mensajeAlerta =
            "Solo tienes que seleccionar un usuario para esta acción";
            this.$refs.alerta.verAlerta()
        } else {
            this.userSeleccionado = rowSeleccionado[0]
            this.$refs.modal.openModal(this.userSeleccionado)
        }
        },
        onBatchAction1(){
        
        this.$refs.alerta_eliminar.dataVisible = true
        console.warn(this.$refs.alerta_eliminar.dataVisible)
        
        },
        actionPrimary(){
        
        const rowSeleccionado = this.$refs.table.selectedRows
        let flag = false
        rowSeleccionado.forEach(element => {
            console.log(element)
            const path = `${this.$apiURL}/roles/${element}/`
            axios
            .delete(path)
            .then(() => {
                this.getUsers();
            })
            .catch(response =>{
                flag = true
                console.log(response.error)
            });
        });
        if(flag){
            console.error('error')
            this.mensajeAlerta = "Ha ocurrido un error con la eliminación de los roles";
            this.$refs.alerta.verAlerta()
        }else{
            this.$refs.alerta_eliminar.hide()
        }
        
        },
        doClose() {
        this.visibleAlerta = false;
        },
        actionNew(){
        this.$refs.modal.openModal()
        }
    },
    created() {
        this.getUsers();
    }
};
</script>
<style scoped>
</style>