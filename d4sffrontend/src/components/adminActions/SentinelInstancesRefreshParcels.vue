<template>
    <div class="bx--grid">
        <template id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <p>Procesado de las instancias de Sentinel para volver a cargar todas las parcelas en la instancia de nuevo</p>
            </div>
        </template>
        <template class="bx--row">
            <cv-data-table
                :row-size="rowSize"
                :auto-width="autoWidth"
                :sortable="sortable"
                :title="title"
                :action-bar-aria-label="actionBarAriaLabel"
                :batch-cancel-label="batchCancelLabel"
                :zebra="zebra"
                :columns="columns"
                v-model="rowSelects"
            >
            <template v-if="true" slot="batch-actions">
                <cv-button @click="refrescarInsancia">
                    Refrescar Instancia
                    <Analytics20 class="bx--btn__icon" />
                </cv-button> 
            </template>
            <template slot="data" v-if="listadoParcelas">
                <cv-data-table-row
                    v-for="enterprise in arrEmpresas"
                    :key="`${enterprise.id}`"
                    :value="`${enterprise.id}`"
                >
                    <cv-data-table-cell>{{enterprise.id}}</cv-data-table-cell>
                    <cv-data-table-cell>{{enterprise.name}}</cv-data-table-cell>
                    <cv-data-table-cell>{{enterprise.sentinel_instance}}</cv-data-table-cell>
                </cv-data-table-row>
            </template>
            </cv-data-table>
        </template>
    </div>
</template>
<script>
import {getAllEnterprises, setParcelsForInstance} from '@/crudFunctions/crudEnterprise'//getEnterprise

export default {
    name: 'ParcelsToSentinelComponent',
    components: {
    },
    data(){
        return {
            rowSelects: [],
            listadoParcelas: Array,
            listadoParcelasFilter: Array,
            arrEmpresas: [],
            rowSize: "",
            autoWidth: false,
            sortable: false,
            title: "Listado de Empresas",
            actionBarAriaLabel: "Custom action bar aria label",
            batchCancelLabel: "Cancel",
            zebra: true,
            columns: [
                {
                    key: 'id',
                    label: 'ID',
                },
                {
                    key: 'name',
                    label: 'Nombre de la empresa',
                },
                {
                    key: 'sentinel_instance',
                    label: `Instancia de sentinel`,
                },
            ],
        }
    },
    methods: {
        refrescarInsancia(){
            const result = this.arrEmpresas.filter(empresa => this.rowSelects.includes(empresa.id))
            console.info(result)
            result.map( async enterprise => {
                const allCoordinates = Array();
                enterprise.parcels.features.map(parcel => {
                    allCoordinates.push(parcel.geometry.coordinates)
                })
                console.info(`parcelas de ${enterprise.name}`, allCoordinates)
                await setParcelsForInstance(enterprise.name, allCoordinates, enterprise.sentinel_instance)
                    .then(response => {
                        console.info(`OK refrescado parcelas de ${enterprise.name}`, response.data)
                    })
                    .catch(err => console.info(`ERROR refrescado parcelas de ${enterprise.name}`, err))
            })
            //postParcelsNotSentinelInstance(this.rowSelects)
        }
    },
    mounted: function () {
        //console.info('User Logged')
    },
    beforeCreate(){
        getAllEnterprises()
            .then(async response => {
                this.arrEmpresas = response.data
                this.flagIndicatingDataHasBeenLoadedInVariables = true
            })
    }
}
</script>