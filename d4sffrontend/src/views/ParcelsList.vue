<template>
    <div class="group-list" @mousedown="keepPositionScroll" @mouseup="putPositionScroll">
        <cv-data-table
            :sortable="sortable"
            :columns="[
            {
            key: 'name',
            label: this.$t('parcelas.nombre'),
            sortable: true
            },
            {
            key: 'description',
            label: this.$t('parcelas.descrip')
            },
            {
            key: 'heactareas',
            label: this.$t('parcelas.hectareas'),
            sortable: true
            },
            {
            key: '',
            label: ''
            },
        ]"
            @sort="onSort"
            :title="$t('parcelas.parcel_list')"
            ref="table"
            :pagination="{ numberOfItems: usuarios.length, pageSizes: [10, 15, 20, 25, usuarios.length] }" @pagination="actionOnPagination"
            @search="onFilter" searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
        >
            <template v-if="true" slot="actions">
                <cv-search :placeholder="$t('parcelas.place_buscar')" @input="onBuscar"></cv-search>
                <cv-button small @click="actionNew" :disabled="disabledAddNewParcel" :title="titleDisabledAddNewParcel">{{$t("parcelas.place_nuevo")}}</cv-button>
            </template>
            <template v-if="use_batchActions" slot="batch-actions">
                <cv-button @click="onBatchAction1">
                    {{$t("parcelas.eliminar")}}
                    <TrashCan32 class="bx--btn__icon" />
                </cv-button>
                <cv-button @click="onBatchAction2">
                    {{$t("parcelas.editar")}}
                    <Edit32 class="bx--btn__icon" />
                </cv-button>
                <cv-button @click="onBatchAction3" v-if="false">
                    Descargar
                    <Download16 class="bx--btn__icon" />
                </cv-button>
            </template>
            <template slot="data">
                <cv-data-table-row
                    v-for="usuario in usuarios.slice(start, start+length)"
                    :key="`${usuario.id}`"
                    :value="`${usuario.id}`"
                    :aria-label-for-batch-checkbox="`Custom aria label for row ${usuario.id} batch`"
                >
                    <cv-data-table-cell>{{usuario.properties.name}}</cv-data-table-cell>
                    <cv-data-table-cell>{{usuario.properties.description}}</cv-data-table-cell>
                    <cv-data-table-cell>{{formateaHectareas(usuario.properties.area)}}</cv-data-table-cell>
                    <cv-data-table-cell>
                        <cv-overflow-menu flip-menu style="margin: 0 auto;">
                            <cv-overflow-menu-item @click="editarRow(usuario.id)">{{$t("parcelas.editar")}}</cv-overflow-menu-item>
                            <cv-overflow-menu-item @click="eliminaRow(usuario.id)">{{$t("parcelas.eliminar")}}</cv-overflow-menu-item>
                        </cv-overflow-menu>
                    </cv-data-table-cell>
                </cv-data-table-row>
            </template>
        </cv-data-table>
        

        <EditarParcel2 ref="modal" :userSeleccionado="userSeleccionado" :key="componentKey" />
        <Alertas :tituloAlert="mensajeAlerta" ref="alerta" />
        <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        <cv-modal
        ref="alerta_eliminar"
        kind="danger"
        :visible="visibleAlertaEliminar"
        @primary-click="actionPrimary">
            <template slot="label">{{$t("parcelas.seguro")}}</template>
            <template slot="title">{{$t("parcelas.eliminar")}}</template>
            <template slot="content">
            <p>{{$t("parcelas.seguro_parcel_del")}}</p>
            </template>
            <template slot="secondary-button">{{$t("parcelas.cancelar")}}</template>
            <template slot="primary-button">{{$t("parcelas.eliminar")}}</template>
        </cv-modal>
    </div>
</template>
<script>
import axios from "axios";
import Alertas from "../components/Alertas.vue";
import EditarParcel2 from "../components/EditarParcel2.vue";
import AlertaGeneral from "../components/AlertaGeneral";
export default {
    name: "ParcelsList",
    props: {},
    components: {
        Alertas,
        EditarParcel2,
        AlertaGeneral
    },
    data() {
        return {
        sortable: false,
        start: 0,
        length: 10,
        columns3: [
            {
            key: "name",
            label: this.$t('parcelas.nombre'),
            sortable: true
            },
            {
            key: "description",
            label: this.$t('parcelas.descrip')
            },
            {
            key: "heactareas",
            label: this.$t('parcelas.hectareas'),
            sortable: true
            },
            {
            key: "",
            label: ""
            },
        ],
        usuarios: [],
        basicPagination: false,
        use_batchActions: true,
        hasExpandingRows: false,
        use_slottedData: true,
        mensajeAlerta: "", 
        userSeleccionado: '',
        visibleAlertaEliminar: false,
        componentKey: 0,
        busqueda: ``,
        columa: ``,
        ordena: ``,
        total_hectares_enterprise: 0,
        disabledAddNewParcel: false,
        titleDisabledAddNewParcel: ``,
        scrollPosition: 0,
        };
    },
    methods: {
        keepPositionScroll(){
            this.scrollPosition = window.scrollY;
        },
        putPositionScroll(){
            setTimeout(() => {
                window.scrollTo(0, this.scrollPosition);
            }, 0);
        },
        formateaHectareas(area){
            if(this.enterprise.type_metric == "Acre"){
                return area
            } else {
            return Math.round((area + Number.EPSILON) * 100) / 100
            }

        },
        metricaparcela(area){

            if(this.enterprise.type_metric == "Acre"){
                const onehecttoAcre = 2.4710538146717
                const acre = onehecttoAcre * area
                this.metric = "Acre"
                     console.log(acre.toFixed(4));
                return  acre.toFixed(4)
            }
            return area
        
        },
        editarRow(row){
            this.$refs.table.selectedRows.forEach(()=>{
                this.$refs.table.selectedRows.pop()
            })
            this.$refs.table.selectedRows.push(row)
            this.onBatchAction2()
        },
        eliminaRow(row){
            this.$refs.table.selectedRows.forEach(()=>{
                this.$refs.table.selectedRows.pop()
            })
            this.$refs.table.selectedRows.push(row)
            this.onBatchAction1()
        },
        showAlert(){
            this.mensajeAlerta = this.$t('parcelas.desarrollo')
            this.tipoAlerta = 'info'
            this.$refs.alertaGeneral.verAlerta()
        },
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        getUsers() {
            if(typeof this.idEmpresaEd == "undefined"){
                this.idEmpresaEd = localStorage.getItem("enterprise") || sessionStorage.getItem("enterprise");
            }


            if(this.idEmpresaEd){
                if (this.$route.query.enterprise) {
                    this.idEmpresaEd = this.$route.query.enterprise;
                    localStorage.setItem("enterprise", this.idEmpresaEd);
                    sessionStorage.setItem("enterprise", localStorage.getItem("enterprise"));
                } else {
                    this.idEmpresaEd = this.idEmpresaEd || localStorage.getItem("enterprise") || sessionStorage.getItem("enterprise");
                }
                console.log("Id Empresa desde dentro",this.idEmpresaEd)
                const path = `${this.$apiURL}/enterprises/${this.idEmpresaEd}/?size=1000000000&page=1`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                    .get(path)
                    .then(response => {
                        this.enterprise = response.data
                        console.log(response.data);
                        console.log(this.enterprise.type_metric);
                        this.metric = this.enterprise.type_metric
                        this.usuarios = response.data.parcels.features;
                        this.usuarios.forEach(parcel =>{
                            this.total_hectares_enterprise += parcel.properties.area
                            parcel.properties.area = this.metricaparcela(parcel.properties.area)
                        })
                        
                        const porcentaje = (parseFloat(this.total_hectares_enterprise) / parseFloat(response.data.hectares_available)  * 100)
                        if(porcentaje >= 100.00){
                            this.disabledAddNewParcel = true
                            this.titleDisabledAddNewParcel = this.$t('parcelas.parcel_limit')
                        }
                    })
                    .catch(error => {
                        console.warn(error);
                    });
            }else{
                const path = `${this.$apiURL}/parcels/`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                    .get(path)
                    .then(response => {
                        this.usuarios = response.data.features;
                    })
                    .catch(error => {
                        console.error(error);
                    });
            }
            this.total_hectares_enterprise
        },
        
        onBatchAction2() {
        const rowSeleccionado = this.$refs.table.selectedRows;
        if (rowSeleccionado.length > 1) {
            this.mensajeAlerta = this.$t('parcelas.parcel_sel_alert');
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
            const path = `${this.$apiURL}/parcels/${element}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
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
            this.mensajeAlerta = this.$t('parcelas.parcel_del_error');
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
        },
        onBuscar(search){
            if(typeof this.idEmpresaEd == "undefined"){
                this.idEmpresaEd = localStorage.getItem("enterprise") || sessionStorage.getItem("enterprise");
            }
            if (this.$route.query.enterprise) {
                    this.idEmpresaEd = this.$route.query.enterprise;
                    localStorage.setItem("enterprise", this.idEmpresaEd);
                    sessionStorage.setItem("enterprise", localStorage.getItem("enterprise"));
                } else {
                    this.idEmpresaEd = this.idEmpresaEd || localStorage.getItem("enterprise") || sessionStorage.getItem("enterprise");
            }
            this.busqueda = search
            const path = `${this.$apiURL}/enterprises/${this.idEmpresaEd}/?size=1000000000&page=1&parcel_mame=${search}&colum_name=${this.columa}&order=${this.ordena}`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                this.usuarios = response.data.parcels.features;
            })
            .catch(error => {
                console.warn(error)
            })
        },
        onSort(order) {
            const index = order.index
            let column = ``
            const orden = order.order
            
            switch (index) {
                case '0':
                    column = `name`
                    break
                case '2':
                    column = 'area'
                    break
                default:
                    column = `name`
            }
            this.columa = column
            this.ordena = orden
            const path = `${this.$apiURL}/enterprises/${localStorage.getItem("enterprise")}/?size=1000000000&page=1&parcel_mame=${this.busqueda}&colum_name=${column}&order=${orden}`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.usuarios = response.data.parcels.features;
            })
            .catch(error => {
                console.warn(error);
            });
            
        },
    },
    created() {
        this.getUsers();
    }
};
</script>
<style scoped>
</style>