<template>
    <div class="bx--grid">
        <template id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <p>Procesado de las parcelas que no tienen una instancia en Sentinel por separado</p>
                <p>En el siguente listado se muestran las parcelas que no tienen una instancia por separado establecida</p>
                <p>Para establecerlas, selecciona las que quieras y pulsa en "Generar Instancia"</p>
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
                @search="onFilter" searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
            >
            <template v-if="true" slot="batch-actions">
                <cv-button @click="generarInstanciaSent">
                    Generar Instancia
                    <Analytics20 class="bx--btn__icon" />
                </cv-button> 
            </template>
            <template slot="data" v-if="listadoParcelas">
                <cv-data-table-row
                    v-for="feature in listadoParcelasFilter"
                    :key="`${feature.id}`"
                    :value="`${feature.id}`"
                >
                    <cv-data-table-cell>{{feature.properties.name}}</cv-data-table-cell>
                    <cv-data-table-cell>{{feature.properties.description}}</cv-data-table-cell>
                    <cv-data-table-cell>{{feature.properties.area}}</cv-data-table-cell>
                    <cv-data-table-cell>{{feature.properties.enterprise}}</cv-data-table-cell>
                </cv-data-table-row>
            </template>
            </cv-data-table>
        </template>
    </div>
</template>
<script>
import {getParcelsNotSentinelInstance, postParcelsNotSentinelInstance} from '@/crudFunctions/crudSentinel.js'

export default {
    name: 'ParcelsToSentinelComponent',
    components: {
    },
    data(){
        return {
            rowSelects: [],
            listadoParcelas: Array,
            listadoParcelasFilter: Array,
            rowSize: "",
            autoWidth: false,
            sortable: false,
            title: "Listado de parcelas sin Instancia en Sentinel",
            actionBarAriaLabel: "Custom action bar aria label",
            batchCancelLabel: "Cancel",
            zebra: true,
            columns: [
                {
                    key: 'name',
                    label: this.$t('graficos.nombre'),
                },
                {
                    key: 'description',
                    label: this.$t('graficos.descrip')
                },
                {
                    key: 'heactareas',
                    label: this.$t('graficos.hectareas'),
                },
                {
                    key: 'enterprise',
                    label: `Empresa`,
                },
            ],
        }
    },
    methods: {
        onFilter(value){
            if(value){
                const result = this.listadoParcelas.filter(feature => feature.properties.enterprise == value)
                this.listadoParcelasFilter = result
            }else{
                this.listadoParcelasFilter = this.listadoParcelas
            }
        },
        generarInstanciaSent(){
            console.info(this.rowSelects)
            postParcelsNotSentinelInstance(this.rowSelects)
        }
    },
    mounted: function () {
        //console.info('User Logged')
    },
    beforeCreate(){
        getParcelsNotSentinelInstance()
        .then(response => {
            this.listadoParcelas = response.data.features
            this.listadoParcelasFilter = response.data.features
        })
    }
}
</script>
