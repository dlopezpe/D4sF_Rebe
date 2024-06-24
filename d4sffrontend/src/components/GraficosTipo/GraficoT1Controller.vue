<template>
    <div class="bx--grid">
        <div class="bx--row">
            <div class="bx--col">
                <h3>{{$t("graficos.gen_grafico_t_one")}}</h3>
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
                v-model="nombreInformeT1"
                :disabled="false"
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
                    :cal-options="calOptions"
                    @change="actionChangeDate"
                    :dateLabel="labelFecha"
                    :value="valueDates"
                    placeholder="mm/dd/yyyy"
                    ref="cambiosFechas"
                    :key="dateUpdate"
                    v-if="false"
                ></cv-date-picker>
                <cv-date-picker
                    kind="range"
                    :dateLabel="$t('graficos.fecha_incio')"
                    :date-end-label="dateEndLabel"
                    :cal-options="calOptions"
                    @change="actionChangeDateRange"
                    :value="valueRange" :key="ketComponentDate">
                </cv-date-picker>
            </div>
        </div>
        <br>
        <div class="bx--row" v-if="empresaSelect !== 'all'">
            <div class="bx--col">
                <cv-search :placeholder="`Buscar`" @input="onBuscar"></cv-search>
            </div>
        </div>
        <div class="bx--row">
            <div class="bx--col" >
                <div id="sentinelLayersList">
                    <cv-structured-list selectable id="parcelList">
                        <template slot="headings">
                            <cv-structured-list-heading>{{$t("graficos.parcels_de")}}</cv-structured-list-heading>
                            <cv-structured-list-heading>{{$t("graficos.descrip")}}</cv-structured-list-heading>
                            <cv-structured-list-heading>{{$t("graficos.hectareas")}}</cv-structured-list-heading>
                        </template>
                        <template slot="items">
                            <cv-structured-list-item 
                            v-for="feature in allParcelsOfEnterprisesFilter" 
                            name="group-1" 
                            :value="String(feature.id)" 
                            v-bind:key="feature.id" 
                            @change="actionChangeParcels"
                            ref="listaDeParcelas" >
                                <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                                <cv-structured-list-data>{{feature.properties.description}}</cv-structured-list-data>
                                <cv-structured-list-data>{{feature.properties.area}}</cv-structured-list-data>
                            </cv-structured-list-item>
                        </template>
                    </cv-structured-list>
                </div>
            </div>
        </div>
        <div class="bx--row">
            <div class="bx--col">
                <p>{{$t("graficos.imagen_por_gen")}} {{numImages}}</p>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <cv-button
                kind="primary"
                size=""
                :disabled="false"
                @click="generaInforme"
                >
                    {{$t("graficos.gen_informe")}}
                </cv-button>
            </div>
        </div>
        <cv-modal @modal-shown="actionShown" @modal-hidden="actionHidden" ref="modal_procesando">
        <template slot="label">{{this.$t('graficos.gen_iformes')}}</template>
        <template slot="title">{{this.$t('graficos.grafico_tipo_uno')}}</template>
        <template slot="content"
            ><p>
                {{this.$t('graficos.grafico_procensandose')}}
            </p></template
            >
            <template slot="primary-button">{{this.$t('graficos.gen_informes_acceptar')}}</template>
        </cv-modal>
    </div>
</template>

<script>
import {getEnterprise, getAllEnterprises} from '@/crudFunctions/crudEnterprise'//getEnterprise
import L from 'leaflet'
import {getCooperative} from '@/crudFunctions/crudCooperativas'
import axios from "axios";
export default {
    name: "GraficoT1Controller",
    components: {
        
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
            listadoEmpresas: this.arrEnterprises,
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            valueDates: [],
            SentinelLayer: 'NDVI',
            nombreInformeT1: '',
            fechasSentinel: Array,
            numImages: 0,
            enterprise_id_sel_parcel: '',
            idParcela: 0,
            bbox: ''
        }
    },
    methods: {
        onBuscar(busqueda){
            console.info(busqueda)
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
        actionChangeDate(valor){
            this.time = "2019-01-01/"+valor;
        },
        actionChangeDateRange(range){
            this.time = `${range.startDate}/${range.endDate}`
            if(range.endDate){
                this.cargaFechasSentinel()
            }
        },
        cargaFechasSentinel(){
            const instanceIns = axios.create({
                baseURL: this.$sentinelURL
            })
            instanceIns.get(`/ogc/wfs/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?REQUEST=GetFeature&TYPENAMES=S2.TILE&OUTPUTFORMAT=application/json&TIME=${this.time}&BBOX=${this.bbox}&SRSNAME=EPSG:4326`).then(resp => {
                if(resp.status != 200){
                    console.warn(resp)
                }else{
                    const respuesta = resp.data.features
                    const fechasArray = Array()
                    const fechasSentinell = Array()
                    respuesta.forEach(feature =>{
                    fechasArray.push(feature.properties.date)
                    })
                    fechasArray.reverse().forEach(fecha =>{
                    fechasSentinell.push(fecha)
                    })
                    let uniqueFechas = [...new Set(fechasSentinell)];
                    this.numImages = uniqueFechas.length
                    this.fechasSentinel = fechasSentinell
                }
            })
        },
        actionChangeParcels(valor){
            let result = []
            this.arrEnterprises.map(enterprise => {
                enterprise.parcels.features.map(feature => {
                    if(feature.id == valor){
                        result.push(feature)
                    }
                })

            })
            const parcela = result[0]
            this.enterprise_id_sel_parcel = parcela.properties.enterprise_id
            this.nombreInformeT1 = parcela.properties.name
            this.idParcela = parcela.id
            const polygon = L.polygon(parcela.geometry.coordinates)
            this.poligonoSelect = parcela.geometry.coordinates
            const bboxP = `${polygon.getBounds()._northEast.lng},${polygon.getBounds()._northEast.lat},${polygon.getBounds()._southWest.lng},${polygon.getBounds()._southWest.lat}`
            this.bbox = bboxP
            this.cargaFechasSentinel()
        },
        generaInforme(){
            this.toProcesar(this.fechasSentinel)
        },
        toProcesar(fechasSentinel){
            setTimeout(() => {
                let uniqueFechas = [...new Set(fechasSentinel)];
                //let uniqueURL = [...new Set(arrURL)];
                //this.isActiveLoading = true
                console.info(uniqueFechas)
                let path = `${this.$apiURL}/procesado/`
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .post(path, {
                    parcela: this.idParcela,
                    urlSentinel: [this.bbox],//uniqueURL,
                    fechas: uniqueFechas,
                    enterprise_id: this.enterprise_id_sel_parcel,
                    capa: this.SentinelLayer,
                    alias: this.nombreInformeT1,
                    polygon: this.poligonoSelect
                })
                .catch(() =>{
                    this.isActiveLoading = false
                    this.mensajeAlerta = this.$t('graficos.informe_gen_error')
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGeneral.verAlerta()
                })
            }, 1000);
            this.$refs.modal_procesando.show()
        }
    },
    
    mounted: function () {
        //console.info('User Logged')
    },
    beforeCreate(){

    }
};
</script>
<style scoped>
#sentinelLayersList{
    overflow: scroll;
    height: 400px;
}
</style>