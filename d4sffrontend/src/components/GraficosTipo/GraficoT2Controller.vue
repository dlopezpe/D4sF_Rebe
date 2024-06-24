<template>
    <div class="bx--grid">
        <div class="bx--row">
            <div class="bx--col">
                <h3>{{$t("graficos.gen_grafico_t_two")}}</h3>
            </div>
        </div>
        <br>
        <div class="bx--row" v-if="is_superuser || is_systemadmin || is_coop_user">
            <div class="bx--col">
                <cv-select
                    theme=""
                    :label="$t('map.listado_empresas')"
                    :hide-label="false"
                    :inline="false"
                    :disabled="false"
                    @change="seleccionaEmpresa"
                >
                    <cv-select-option disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                    <cv-select-optgroup label="Todas las Empresas" v-if="is_superuser || is_systemadmin">
                        <cv-select-option :value="`all`" v-if="is_superuser || is_systemadmin">{{$t("map.most_todas_empresas")}}</cv-select-option>
                        <cv-select-option v-for="empresa in listadoEmpresas" :value="String(empresa.id)"  v-bind:key="empresa.id">
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
                <cv-text-input
                :label="$t('graficos.nombre_informe')"
                v-model="nombreInformeT2"
                :disabled="false"
                :value="$t('graficos.grafico_tipo_dos')"
                ></cv-text-input>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col-lg-3">
                <cv-select :label="$t('graficos.sel_layer_sen')" @change="chageCapas">
                    <cv-select-option selected value="NDVI">{{$t("graficos.NDVI")}}</cv-select-option>
                    <cv-select-option value="MOISTURE_INDEX">{{$t("graficos.mostisture_index")}}</cv-select-option>
                </cv-select>
            </div>
            <div id="sentinelDate" class="bx--col-lg-3">
                <cv-date-picker
                    kind="single"
                    :date-label="$t('graficos.fecha')"
                    @change="chageFecha" :cal-options="calOptions">
                </cv-date-picker>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col" >
                <div id="sentinelLayersList">
                    <cv-data-table
                        :sortable="false"
                        :pagination="{ numberOfItems: allParcelsOfEnterprisesFilter.length, pageSizes: [10, 15, 20, 25, allParcelsOfEnterprisesFilter.length] }" @pagination="actionOnPagination"
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
                                key: 'heactareas',
                                label: this.$t('graficos.hectareas'),
                                'sortable': false
                            },
                            {
                                key: 'enterprise',
                                label: 'Empresa',
                                'sortable': false
                            },
                        ]"
                        @sort="onSort"
                        v-model="rowSelects"
                        :title="$t('graficos.parcel_list')"
                        ref="tableLstadoT2MultiCoop"
                        searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
                    >
                        <template v-if="true" slot="actions">
                            <cv-search :placeholder="$t('graficos.buscar_nombre')" @input="onBuscar"></cv-search>
                        </template>
                        <template v-if="true" slot="batch-actions">
                            <cv-button @click="generarInforme">
                                {{$t("graficos.generar")}}
                                <Analytics20 class="bx--btn__icon" />
                            </cv-button>  
                        </template>
                        <template slot="data">
                            <cv-data-table-row
                                v-for="feature in allParcelsOfEnterprisesFilter.slice(start, start+length)"
                                :key="`${feature.id}`"
                                :value="`${feature.id}`"
                                :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"
                            >
                                <cv-data-table-cell>{{feature.properties.name}}</cv-data-table-cell>
                                <cv-data-table-cell>{{feature.properties.description}}</cv-data-table-cell>
                                <cv-data-table-cell>{{feature.properties.area}}</cv-data-table-cell>
                                <cv-data-table-cell>{{getNameEnterprise(feature.properties.enterprise_id)}}</cv-data-table-cell>
                            </cv-data-table-row>
                        </template>
                    </cv-data-table>
                </div>
            </div>
        </div>
        <cv-modal @modal-shown="actionShown" @modal-hidden="actionHidden" ref="modal_procesando">
        <template slot="label">{{this.$t('graficos.gen_iformes')}}</template>
        <template slot="title">{{this.$t('graficos.grafico_tipo_dos')}}</template>
        <template slot="content"
            ><p>
                {{this.$t('graficos.grafico_procensandose')}}
            </p></template
            >
            <template slot="primary-button">{{this.$t('graficos.gen_informes_acceptar')}}</template>
        </cv-modal>
        <AlertaGeneral ref="alertaGenerall" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
    </div>
</template>

<script>
import {getEnterprise, getAllEnterprises} from '@/crudFunctions/crudEnterprise'//getEnterprise
import {getCooperative} from '@/crudFunctions/crudCooperativas'
import axios from "axios";
import L from 'leaflet'
import AlertaGeneral from "@/components/AlertaGeneral";
export default {
    name: "GraficoT1Controller",
    components: {
        AlertaGeneral
    },
    props: {
        arrEnterprises: Array,
        arrCooperativas: Array,
        is_superuser: Boolean,
        is_systemadmin: Boolean,
        is_staff: Boolean,
        is_enterpriseadmin: Boolean,
        is_coop_user: Boolean,
        allParcelsOfEnterprises: Array,
        allParcelsOfEnterprisesFilter: Array
    },
    data() {
        return {
            tipoAlerta: `error`,
            mensajeAlerta: '',
            rowSelects: [],
            listadoEmpresas: this.arrEnterprises,
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            valueDates: [],
            SentinelLayer: 'NDVI',
            nombreInformeT2: '',
            fechasSentinel: Array,
            numImages: 0,
            enterprise_id_sel_parcel: '',
            idParcela: 0,
            bbox: '',
            poligonoSelect: Array(),
            polygonsSelecc: Array(),
            start: 0,
            length: 10,
            nombreParcels: Array()
        }
    },
    methods: {
        onSort(order) {
            const index = order.index
            let column = ``
            const orden = order.order
            
            switch (index) {
                case '0':
                    column = `name`
                    break
                case '1':
                    column = `name`
                    break
                case '2':
                    column = 'area'
                    break
                case '3':
                    column = 'enterprise'
                    break
                default:
                    column = `name`
            }
            if(orden == 'ascending'){
                console.info('enter')
                this.allParcelsOfEnterprisesFilter.sort((a, b) => parseFloat(a.name) - parseFloat(b.name));
            }
            console.info(column, orden)
        },
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        onBuscar(busqueda){
            console.info(busqueda)
            if(busqueda){
                const result = this.allParcelsOfEnterprises.filter(parcel => parcel.properties.name.toUpperCase().includes(busqueda.toUpperCase()))
                this.allParcelsOfEnterprisesFilter = result
            }else{
                this.allParcelsOfEnterprisesFilter = this.allParcelsOfEnterprises
            }
        },
        getNameEnterprise(value){
            const result = this.arrEnterprises.filter(enterprise => enterprise.id == value)
            return result[0].name
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
                        this.$emit('setEnterprise', response.data)
                        this.$emit('setAllParcelsOfEnterprises', arrParcels)
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
                        this.$emit('setEnterprise', response.data.enterprises)
                        this.$emit('setAllParcelsOfEnterprises', arrParcels)
                    })
                }else{
                    getEnterprise(empresa)
                    .then(async response => {
                        response.data.parcels.features.map(parcel => {
                            arrParcels.push(parcel)
                        })
                        this.$emit('setEnterprise', [response.data])
                        this.$emit('setAllParcelsOfEnterprises', arrParcels)
                    })
                }
            }
        },
        chageCapas(capa){
            this.SentinelLayer = capa
            this.cargaFechasSentinel()
        },
        chageFecha(date){
            this.fechaGenerar = date
        },
        
        generarInforme(){
            console.info(this.rowSelects)
            const results = this.allParcelsOfEnterprisesFilter.filter(parcel => this.rowSelects.includes(String(parcel.id)))
            console.info(results)
            const enterprisesInResults = []
            results.map(result => {
                enterprisesInResults.push(result.properties.enterprise_id)
            })
            console.info(enterprisesInResults)
            const uniqueEmpresas = [...new Set(enterprisesInResults)];
            console.info(uniqueEmpresas)
            this.urlSentinel = Array()
            this.nombreParcels = Array()
            if(uniqueEmpresas.length > 1){
                console.info('Seleccion Multiempresa')
                //*Es multiempresa
                /**
                 * Vamos a saber si es copperativa
                 */
                const enterprisesInResultsCoop = []
                console.info(this.arrCooperativas)
                this.arrCooperativas.map(cooperative => {
                    cooperative.enterprises.map(enterprise => {
                        if(uniqueEmpresas.includes(enterprise.id)){
                            enterprisesInResultsCoop.push(cooperative.id)
                        }
                    })
                })
                console.info(enterprisesInResultsCoop)
                if(enterprisesInResultsCoop.length == uniqueEmpresas.length){
                    console.info('Todas las empresas Pertenecen a cooperativas')
                    const uniqueCoops = [...new Set(enterprisesInResultsCoop)];
                    if(uniqueCoops.length > 1){
                        console.info('MultiCoop')
                        console.info('Cooperativas', uniqueCoops)
                            this.mensajeAlerta = this.$t('No se puede generar el informe ya que se ha seleccionado parcelas de distintas empresas que pertenecen a distintas cooperativas')
                            this.tipoAlerta = 'error'
                            this.$refs.alertaGenerall.verAlerta()
                    }else{
                        console.info('UniCoop')
                        console.info('Cooperativas', uniqueCoops)
                        results.map(parcel => {
                            this.actionChangeParcels(parcel)
                        })
                        this.parcelasSeleccionadasId = this.rowSelects
                        this.toProcesarUniCoop(this.urlSentinel, this.rowSelects, true, uniqueCoops[0])
                    }
                }else{
                    console.info('No se puede generar el informe')
                    this.mensajeAlerta = this.$t('No se puede generar el informe con las parcelas seleccionadas')
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                }
                
            }else{
                console.info('Seleccion Uniempresa')
                results.map(parcel => {
                    this.actionChangeParcels(parcel)
                })
                this.parcelasSeleccionadasId = this.rowSelects
                this.toProcesarUniEmpresa(this.urlSentinel, this.nombreParcels, uniqueEmpresas[0])
            }
            //this.toProcesar(this.fechasSentinel)
        },
        toProcesarUniEmpresa(arrURL, fechasSentinel, empresa_id){
            setTimeout(() => {
                let path = `${this.$apiURL}/procesadot2/`
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .post(path, {
                    parcela: this.nombreInformeT2 ? this.nombreInformeT2 : '0',
                    urlSentinel: arrURL, //arr url
                    fechas: fechasSentinel, //Arr parcelas
                    polygon: this.polygonsSelecc,
                    enterprise_id: empresa_id,
                    capa: this.SentinelLayer,
                    fechaElegida: this.fechaGenerar,
                    id_parcelas: this.parcelasSeleccionadasId,
                    esCooperative: false
                })
                .catch(() =>{
                })
            }, 1000);
            this.$refs.modal_procesando.show()
        },
        toProcesarUniCoop(arrURL, fechasSentinel, esCooperative, empresa_id){
            setTimeout(() => {
                //this.isActiveLoading = true
                let path = `${this.$apiURL}/procesadot2/`
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .post(path, {
                    parcela: this.nombreInformeT2 ? this.nombreInformeT2 : '0',
                    urlSentinel: arrURL, //arr url
                    fechas: fechasSentinel, //Arr parcelas
                    polygon: this.polygonsSelecc,
                    enterprise_id: empresa_id,
                    capa: this.SentinelLayer,
                    fechaElegida: this.fechaGenerar,
                    id_parcelas: this.parcelasSeleccionadasId,
                    esCooperative: esCooperative
                })
                .catch(() =>{
                })
            }, 1000);
            this.$refs.modal_procesando.show()
        },
        actionChangeParcels(valor){{ //GEneramos el poligono
            const result = [valor]
            const polygon = L.polygon(result[0].geometry.coordinates)
            this.poligonoSelect = result[0].geometry.coordinates
            const bboxP = `${polygon.getBounds()._northEast.lng},${polygon.getBounds()._northEast.lat},${polygon.getBounds()._southWest.lng},${polygon.getBounds()._southWest.lat}`
            this.bbox = bboxP
            this.urlSentinel.push(bboxP)
            this.polygonsSelecc.push(this.poligonoSelect)
            this.nombreParcels.push(result[0].properties.name)
        //this.cargaFechasSentinel()
        }
    },
    },
    
    mounted: function () {
        //console.info('User Logged')
    },
    beforeCreate(){

    }
};
</script>
<style scoped>
</style>