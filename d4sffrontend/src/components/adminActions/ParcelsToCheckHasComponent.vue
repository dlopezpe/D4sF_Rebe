<template>
    <div class="bx--grid" @mousedown="keepPositionScroll" @mouseup="putPositionScroll">
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <p>Check las has de la parcelas</p>
            </div>
        </div>
        <div class="bx--row">
            <div class="bx--col">
                <cv-select
                    theme=""
                    :label="$t('map.listado_empresas')"
                    :hide-label="false"
                    :inline="false"
                    :disabled="false"
                    @change="seleccionaEmpresa"
                    v-model="selectValueEmpresa"
                >
                    <cv-select-option :value="''" disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                    <cv-select-optgroup label="Todas las Empresas">
                        <cv-select-option :value="`all`">{{$t("map.most_todas_empresas")}}</cv-select-option>
                        <cv-select-option v-for="empresa in arrEmpresasList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                            {{empresa.name}}
                        </cv-select-option>
                    </cv-select-optgroup>
                    <cv-select-optgroup :label="`Cooperativa ${cooperativa.name}`" v-bind:key="cooperativa.id" v-for="cooperativa in arrCooperativas">
                        <cv-select-option :value="`coop_${cooperativa.id}`">{{$t("map.most_todas_empresas")}}</cv-select-option>
                        <cv-select-option v-for="empresa in cooperativa.enterprises" :value="String(empresa.id)"  v-bind:key="empresa.id">
                            {{empresa.name}}
                        </cv-select-option>
                    </cv-select-optgroup>
                </cv-select>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <div id="sentinelLayersList">
                    <p style="font-size: 14px">Selecciona a continuación las parcelas sobre las que quieres realizar la consulta. Puedes utilizar el buscador para encontrar la/s parcela/s que necesitas. Para poder ver el nombre de todas las parcelas, por favor utiliza el selector que encontrarás en la parte inferior de la tabla.</p>
                    <br>
                    <cv-data-table
                        :sortable="false"
                        @pagination="actionOnPagination"
                        :pagination="{ 
                            numberOfItems: allParcelsOfEnterprisesFilter.length, 
                            pageSizes: [
                                {
                                    value: 10,
                                    label: '10'
                                }, 
                                {
                                    value: 15,
                                    label: '15'
                                },
                                {
                                    value: 20,
                                    label: '20'
                                }, 
                                {
                                    value: 25,
                                    label: '25'
                                }, 
                                {
                                    value: allParcelsOfEnterprisesFilter.length,
                                    label: 'Todas'
                                }
                            ] 
                        }"
                        :columns="[
                            {
                                key: 'name',
                                label: this.$t('graficos.nombre'),
                                'sortable': false
                            },
                            {
                                key: 'description',
                                label: this.$t('graficos.descrip'),
                                'sortable': false
                            },
                            {
                                key: 'Puntos',
                                label: this.$t('graficos.puntos'),
                                'sortable': false
                            },
                            {
                                key: 'heactareas en BBDD',
                                label: 'Back',
                                'sortable': false
                            },
                            {
                                key: 'heactareas Recalculadas',
                                label: 'Front',
                                'sortable': false
                            },
                            {
                                key: 'enterprise',
                                label: 'Empresa',
                                'sortable': false
                            },
                        ]"
                        :title="$t('graficos.parcel_list')"
                        v-model="rowSelects"
                        ref="tableLstadoT2MultiCoop"
                        searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
                    >
                        <template v-if="true" slot="actions">
                            <cv-search :placeholder="$t('graficos.buscar_nombre')" @input="onBuscar"></cv-search>
                        </template>
                        <!-- <template v-if="true" slot="batch-actions">
                            <cv-button @click="comprobar">
                                Pruebas
                            </cv-button>  
                        </template> -->
                        <template v-if="true" slot="batch-actions">
                            <cv-button @click="crear_excel">
                                Exportar Excel
                            </cv-button>  
                        </template>
                        <template slot="data">
                            <cv-data-table-row
                                v-for="feature in allParcelsOfEnterprisesFilter.slice(start, start+length)"
                                :key="`${feature.id}`"
                                :value="`${feature.id}`"
                                :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"
                            >
                                <cv-data-table-cell>{{feature.id+' - '}}{{feature.properties.name}}</cv-data-table-cell>
                                <cv-data-table-cell>{{feature.properties.description}}</cv-data-table-cell>
                                <cv-data-table-cell :class="{'errorDraw': getPuntos(feature.id) > 80}" >{{getPuntos(feature.id)}}</cv-data-table-cell>
                                <cv-data-table-cell>{{feature.properties.area.toFixed(2)}}</cv-data-table-cell>
                                <cv-data-table-cell>{{getCalculateHas(feature.id)}} {{getCalculateHas(feature.id) != feature.properties.area.toFixed(2) ? '⚠' : ''}}</cv-data-table-cell>
                                <cv-data-table-cell>{{getNameEnterprise(feature.properties.enterprise_id)}} </cv-data-table-cell>
                            </cv-data-table-row>
                        </template>
                    </cv-data-table>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {getAllEnterprises, getEnterprise} from '@/crudFunctions/crudEnterprise'//getFechasSentinelForInformes
import {getCooperative} from '@/crudFunctions/crudCooperativas'
import { getArea } from 'ol/sphere';
import Feature from 'ol/Feature';
import Polygon from 'ol/geom/Polygon';
import * as XLSX from 'xlsx';
export default {
    name: 'ParcelsToSentinelComponent',
    components: {
    },
    data(){
        return {
            selectValueEmpresa: '',
            //Empresas sel
            arrEmpresas: [],
            arrEmpresasList: [],
            arrCooperativas: [],
            allParcelsOfEnterprises: [],
            allParcelsOfEnterprisesFilter: [],
            start: 0,
            length: 10,

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
        keepPositionScroll(){
            this.scrollPosition = window.scrollY;
        },
        putPositionScroll(){
            setTimeout(() => {
                window.scrollTo(0, this.scrollPosition);
            }, 0);
        },
        crear_excel() {
            var data=[]
            const result = this.allParcelsOfEnterprises.filter(parcel => this.rowSelects.includes(String(parcel.id)))
            result.forEach((x)=>{
                data.push({"Nombre de la parcela":x.properties.name,"Numero de puntos":this.getPuntos(x.id),"Back":x.properties.area.toFixed(2),"Front":this.getCalculateHas(x.id),"Empresa":this.getNameEnterprise(x.properties.enterprise_id)})
            })
            const ws = XLSX.utils.json_to_sheet(data);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, 'Hectareas por empresa');
            XLSX.writeFile(wb, 'data.xlsx');
        },
        comprobar(){
            console.info(this.rowSelects)
            const result = this.allParcelsOfEnterprises.filter(parcel => this.rowSelects.includes(String(parcel.id)))
            console.info(result)
            console.info(result[0].geometry)
            const feature = new Feature({
                geometry: new Polygon(result[0].geometry.coordinates)
            })
            feature.getGeometry().transform('EPSG:4326', 'EPSG:3857')
            console.info(feature.getGeometry())
            const areaForNewPolygon = (Math.round((getArea(feature.getGeometry())/ 10000) * 10000) / 10000)
            console.info(areaForNewPolygon)
        },
        getCalculateHas(idParcel){
            const result = this.allParcelsOfEnterprises.filter(parcel => idParcel == parcel.id)
            const feature = new Feature({
                geometry: new Polygon(result[0].geometry.coordinates)
            })
            feature.getGeometry().transform('EPSG:4326', 'EPSG:3857')
            return (Math.round((getArea(feature.getGeometry())/ 10000) * 10000) / 10000).toFixed(2)
        }
        ,
        getPuntos(idParcel){
            const result = this.allParcelsOfEnterprises.filter(parcel => idParcel == parcel.id)
            const feature = new Feature({
                geometry: new Polygon(result[0].geometry.coordinates)
            })
            feature.getGeometry().transform('EPSG:4326', 'EPSG:3857')
            const poligono = feature.getGeometry();
            //Dividimos entre 2 porque cada punto son 2 coordenadas
            return poligono.flatCoordinates.length / 2 
        },
        getNameEnterprise(value){
            const result = this.arrEmpresas.filter(enterprise => enterprise.id == value)
            return result[0].name
        },
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        onBuscar(busqueda){
            if(busqueda){
                const result = this.allParcelsOfEnterprises.filter(parcel => parcel.properties.name.toUpperCase().includes(busqueda.toUpperCase()))
                this.allParcelsOfEnterprisesFilter = result
            }else{
                this.allParcelsOfEnterprisesFilter = this.allParcelsOfEnterprises
            }
        },
        seleccionaEmpresa(empresa){
            const arrParcels = []
            if(empresa == 'all'){
                getAllEnterprises()
                    .then(async response => {
                        response.data.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        this.arrEmpresas = response.data
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                    })
            }else{
                const result = empresa.split('_')
                if(result[0] == 'coop'){
                    getCooperative(result[1])
                    .then(response => {
                        response.data.enterprises.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        this.arrEmpresas = response.data.enterprises
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                    })
                }else{
                    getEnterprise(empresa)
                    .then(async response => {
                        response.data.parcels.features.map(parcel => {
                            arrParcels.push(parcel)
                        })
                        this.arrEmpresas = [response.data]
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                    })
                }
            }
        },
    },
    mounted: function () {
        //console.info('User Logged')
    },
    beforeCreate(){
        getAllEnterprises()
        .then(async response => {
            this.arrEmpresas = response.data
            this.arrEmpresasList = response.data
            const arrParcels = []
            response.data.map(enterprise => {
                enterprise.parcels.features.map(parcel => {
                    arrParcels.push(parcel)
                })
            })
            this.allParcelsOfEnterprises = arrParcels
            this.allParcelsOfEnterprisesFilter = arrParcels
            this.flagIndicatingDataHasBeenLoadedInVariables = true
        })
    }
}
</script>
<style scoped>
    .errorDraw{
        color: #da1e28;
        font-weight: 400;
    }
</style>