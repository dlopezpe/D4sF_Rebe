<template>
    <div id="layersControlerResponsive" class="layersControler" ref="layersControlersResponsive">
        <div class="bx--row" id="row_box">
            <div class="bx--col-sm-3">
                <div id="sentinelLayers">
                    <cv-dropdown @change="actionChangeLayers" :label="$t('map.sent_layers')" up v-if="!expand">
                            <cv-dropdown-item v-for="layer in layersSelector" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
                    </cv-dropdown>
                    <cv-dropdown @change="actionChangeLayers" :label="$t('map.sent_layers')" v-else>
                            <cv-dropdown-item v-for="layer in layersSelector" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
                    </cv-dropdown>
                </div>
            </div>
            <div class="bx--col-sm-1">
                <ChevronSortUp20 @click="onclickTile" v-if="!expand" style="transform: translate(35px, 0px);"/>
                <ChevronSortDown20  @click="onclickTile" v-if="expand" style="transform: translate(35px, 0px);"/>
            </div>
        </div>
            <div>
                <div class="bx--row">
                    <div class="bx--col">
                        <div id="geolocIcon" style="">
                            <div v-if="mostrarIconErrGeoloc === ''" @click="cargaLocalizacionActual()">
                                <p style="cursor: pointer; font-size: 14px;">Mostrar mi ubicación <img src="../../assets/airport-location.svg" style="width: 14px; height: 14px;"></p>
                            </div>
                            <div v-else-if="mostrarIconErrGeoloc === false" @click="cargaLocalizacionActual()">
                                <p style="cursor: pointer; font-size: 14px;">Para volver a localizar mi ubicación, haz click aquí <Location16 style="stroke: #00abff; width: 14px; height: 14px; fill: #00abff;"/></p>
                            </div>
                            <div v-else-if="mostrarIconErrGeoloc === true" @click="cargaLocalizacionActual()">
                                <p style="cursor: pointer; font-size: 14px;">No temenos acceso a tu ubicación <img src="../../assets/location--hazard.svg" style="width: 14px; height: 14px;"></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <div v-if="expand">
            <div>
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
            <div ref="sentinelLayersListCollapse">
                <cv-search :placeholder="`Buscar`" @input="onBuscar" ></cv-search>
                <cv-structured-list-heading >Listado de Parcelas </cv-structured-list-heading>
                <div id="sentinelLayersList">
                    
                    <cv-structured-list selectable>
                        <template slot="items" v-for="parcel in allParcelsOfEnterprisesFilter">
                            <template>
                                <cv-structured-list-item
                                    v-bind:key="parcel.id" 
                                    name="group-1"
                                    :value="String(parcel.id)"
                                    ref="listaDeParcelas"
                                    @change="actionChangeParcels"
                                >
                                    <cv-structured-list-data>{{parcel.properties.name}} - {{getNameEnterprise(parcel.properties.enterprise_id)}}</cv-structured-list-data>
                                </cv-structured-list-item>
                            </template>
                        </template>
                    </cv-structured-list>  
                </div>
            
                <br>
                <div>
                    <div class="bx--row">
                        <div class="bx--col">
                            <cv-toggle
                                :checked="checkedToggleMostarTexto"
                                label="Desbordamiento de nombres de Parcelas"
                                value="check-1"
                                :small="true"
                                :hide-label="true"
                                @change="actionChangedToggle">
                                <template slot="text-left">Desactivado desbordamiento de nombres de Parcelas</template>
                                <template slot="text-right">Activado desbordamiento de nombres de Parcelas</template>
                            </cv-toggle>
                        </div>
                    </div>
                </div>
            </div>
        
        
        
        
            <div id="sentinelLayers">
                <cv-button
                    :disabled="false"
                    @click="actionClearCacheSentinel"
                    size="small"
                    style="margin-top: 20px"
                >
                Recargar sistema
                </cv-button>
            </div>
            <br>
            <div id="sentinelOpacity">
                <cv-slider
                    :label="$t('map.opacidad')"
                    @change="actionChangeOpacity"></cv-slider>
            </div>
            <br>
            <div id="sentinelDate">
                <div class="bx--row">
                    <div class="bx--col">
                        <cv-date-picker
                            kind="single"
                            :cal-options="calOptions"
                            @change="actionChangeDate"
                            :dateLabel="$t('map.fecha')"
                            :value="valueDates"
                            placeholder="mm/dd/yyyy"
                            ref="cambiosFechas"
                            style="width: 100%!important"
                        ></cv-date-picker>
                    </div>
                    <div class="bx--col">
                        <cv-button
                            :disabled="false"
                            @click="actionClickDateCargaFechasSent"
                            size="small"
                            style="margin-top: 20px"
                            >
                            {{$t("map.fechas_disponibles")}}
                            <cv-loading
                            :small="true"
                            :active="isActiveLoadingFechasSent"
                            :overlay="false" v-if="isVisibleLoadFechasSent"></cv-loading>
                        </cv-button>
                    </div>
                </div>
            </div>
            <br>
            <br>
        </div>
    </div>
</template>
<script>
//import proj4 from 'proj4'
//import {polygonCenter} from '@/crudFunctions/crudEnterprise'
import {getEnterprise, getAllEnterprises, getFechasSentinel} from '@/crudFunctions/crudEnterprise'//getEnterprise
import {getCooperative} from '@/crudFunctions/crudCooperativas'
export default {
    name: 'ControllerPanel4Mobile',
    props: {
        username: String,
        arrEnterprises: Array,
        arrCooperativas: Array,
        centro: [],
        layersSelector: Array,
        checkedToggleMostarTexto: Boolean,
        is_superuser: Boolean,
        is_systemadmin: Boolean,
        mapComponent: Object,
        allParcelsOfEnterprises: Array,
        allParcelsOfEnterprisesFilter: Array,
        SentinelLayer: String,
    },
    data() {
        return {
            listadoEmpresas: this.arrEnterprises,
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            valueDates: [],
            isActiveLoadingFechasSent: false,
            isVisibleLoadFechasSent: false,
            expand: false,
            expand2: true,
            erorCompaGeoloc: '',
            mostrarIconErrGeoloc: '',
        }
    },
    components: {
        
    },
    methods: {
        cargaLocalizacionActual(){
            if(!("geolocation" in navigator)) {
                this.erorCompaGeoloc =  this.$t('map.loc_no_disponible')
                this.mostrarIconErrGeoloc = true
                return;
            }
            
            // get position
            navigator.geolocation.getCurrentPosition(pos => {
                console.info('Localizacion autorizada', pos)
                this.mostrarIconErrGeoloc = false;
                this.$emit('setCenter', [pos.coords.longitude, pos.coords.latitude])
            }, err => {
                this.mostrarIconErrGeoloc = true
                console.info('Localización no autorizada', err)
            })
        },
        onclickTile(){
            if(this.expand){
                this.expand = false
                this.$refs.layersControlersResponsive.style['max-height'] = ''
                this.$refs.layersControlersResponsive.style['overflow-y'] = ''
                this.componentDrop +=1
            }else{
                this.expand = true
                this.$refs.layersControlersResponsive.style['max-height'] = '90%'
                this.$refs.layersControlersResponsive.style['overflow-y'] = 'auto'
            }
        },
        onclickTile2(){
            if(this.expand2){
                this.expand2 = false
                this.$refs.sentinelLayersListCollapse.style.display = "none"
                this.$refs.sentinelLayersListCollapseP.$el.style.display = "none"
                this.classfechaR = ``
                this.classfechab1 = ``
                this.classfechab2 = ``

            }else{
                this.expand2 = true
                this.$refs.sentinelLayersListCollapse.style.display = "block"
                this.$refs.sentinelLayersListCollapseP.$el.style.display = ""
                this.classfechaR = `bx--row`,
                this.classfechab1 = `bx--col-lg-7 bx--col-md-10 bx--col-sm-8`
                this.classfechab2 = `bx--col-lg-1 bx--col-md-1 bx--col-sm-1`
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
        actionChangeParcels(valor){
            let result = []
            this.arrEnterprises.map(enterprise => {
                enterprise.parcels.features.map(feature => {
                    if(feature.id == valor){
                        result.push(feature)
                    }
                })

            })
            const coordenadasGeometricas = result[0].geometry.coordinates[0]
            const newCenter = this.getCenter(coordenadasGeometricas)
            this.$emit('setCenter', [newCenter[0], newCenter[1]])
            
        },
        actionChangeDate(valor){
            const arrFechas = valor.split(', ')
            if(arrFechas.length == 1){
                this.time = "2019-01-01/"+valor
                this.$emit('setFechaSentinel', valor)
            }
        },
        actionClickDateCargaFechasSent(){
            this.isActiveLoadingFechasSent = true
            this.isActiveLoadingFechasSent = true
            getFechasSentinel(this.mapComponent.previousExtent_)
            .then(response => {
                const respuesta = response.data.features
                const fechasArray = Array()
                respuesta.forEach(feature =>{
                    fechasArray.push(feature.properties.date)
                })
                this.valueDates = fechasArray.reverse()
                this.isActiveLoadingFechasSent = false
                this.isActiveLoadingFechasSent = false
            })
        },
        getCenter(coordenadasGeometricas){
            var minX, maxX, minY, maxY;
            for (var i = 0; i < coordenadasGeometricas.length; i++){
                minX = (coordenadasGeometricas[i][0] < minX || minX == null) ? coordenadasGeometricas[i][0] : minX;
                maxX = (coordenadasGeometricas[i][0] > maxX || maxX == null) ? coordenadasGeometricas[i][0] : maxX;
                minY = (coordenadasGeometricas[i][1] < minY || minY == null) ? coordenadasGeometricas[i][1] : minY;
                maxY = (coordenadasGeometricas[i][1] > maxY || maxY == null) ? coordenadasGeometricas[i][1] : maxY;
            }
            return [(minX + maxX) / 2, (minY + maxY) / 2];
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
        actionChangedToggle(value){
            //this.checkedToggleMostarTexto = value
            this.$emit('setToggleMostrarTexto', value)
        },
        actionChangeLayers(value){
            this.$emit('setSentinelLayer', value)
        },
        actionClearCacheSentinel(){
            this.$emit('setSentinelClearCache')
        },
        actionChangeOpacity(value){
            this.$emit('setSentinelOpacity', value/100)
        }
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
    beforeCreate(){
        
    }
}
</script>
<style scoped>
    #layersControler{
        position: fixed;
        width: auto;
        padding: 10px;
        background-color: #f4f4f4;
        margin-top: 10px;
        margin-left: 10px;
        max-width: 480.6px;
    }
    #layersControlerResponsive{
        bottom: 0;
        position: fixed;
        width: 100%;
        background-color: #f4f4f4;
        /*
        overflow-y: auto;
        */
    }
    #div_buscador{
        position: fixed;
        width: 40vw;
        padding: 10px;
        margin-top: 0px;
        margin-left: 500px;
    }
    #parcelList{
        margin-bottom: 1em;
    }
    #sentinelLayers, #sentinelOpacity, #sentinelClouds, #sentinelDate{
        margin-bottom: 1em;
    }
    footer{
        display: none;
    }
    #sentinelLayersList{
        overflow-y: auto;
        height: 250px;
    }
    @media (max-height: 700px) {
        #sentinelLayersList{
            overflow: scroll;
            height: 280px;
        }
    }
    #paginacionResp{
        font-weight: 411;
        line-height: 1.125rem;
        letter-spacing: 0.16px;
        width: 10px;
        background-color: #f4f4f4;
        display: inline-grid;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #e0e0e0;
        height: 3rem;
    }
    .errorDraw{
        color: #da1e28;
        font-weight: 400;
        font-size: 12px;
    }
    #control_der{
        margin-top: 58px;
        padding: 10px;
        background-color: #f4f4f4;
        position: fixed;
        top: 0px;
        right: 8px;
    }
    @media (max-height: 900px) {
        #layersControler{
            max-height: 90%;
            overflow-y: auto;
        }
    }
</style>
