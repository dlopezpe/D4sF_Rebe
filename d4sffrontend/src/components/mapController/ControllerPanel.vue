<template>
    <div id="layersControler" class="layersControler" ref="layersController">
        <div>
            <div class="bx--row">
                <div class="bx--col">
                    <span><ChevronSortDown20  @click="onclickTile2" v-if="expand2"/></span><span><ChevronSortUp20 @click="onclickTile2" v-if="!expand2" style="transform: translate(0px, 10px)"/></span>
                </div>
                <div class="bx--col">
                    <div id="geolocIcon" style="text-align: right;">
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
        
        <div v-if="is_superuser || is_systemadmin || is_coop_user">
            <cv-select
                theme=""
                :label="$t('map.listado_empresas')"
                :hide-label="false"
                :inline="false"
                :disabled="false"
                @change="seleccionaEmpresa"
                id="selectEmp"
                >
                <cv-select-option disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                <cv-select-optgroup label="Todas las Empresas" v-if="is_superuser || is_systemadmin">
                    <cv-select-option :value="`all`" v-if="is_superuser || is_systemadmin">{{$t("map.most_todas_empresas")}}</cv-select-option>
                    <cv-select-option v-for="empresa in sortedListadoEmpresas" :value="String(empresa.id)"  v-bind:key="empresa.id">
                        {{empresa.name}}
                    </cv-select-option>
                </cv-select-optgroup>
                <cv-select-optgroup :label="`Cooperativa ${cooperativa.name}`" v-bind:key="cooperativa.id" v-for="cooperativa in arrCooperativas">
                    <cv-select-option :value="`coop_${cooperativa.id}`">{{$t("map.most_todas_empresas")}}</cv-select-option>
                    <cv-select-option v-for="empresa in getSortedCooperativa(cooperativa).enterprises" :value="String(empresa.id)"  v-bind:key="empresa.id">
                        {{empresa.name}}
                    </cv-select-option>
                </cv-select-optgroup>
            </cv-select>
            <p>Actualmente mostrando las parcelas de: <strong><u><span id="empresa"></span></u></strong></p>
        </div>
        <!--
        <div id="sentinelLayersList" ref="sentinelLayersListCollapse">
            <cv-structured-list selectable>
                <template slot="headings">
                    <cv-structured-list-heading>{{$t("map.parcelas_de")}}</cv-structured-list-heading>
                </template>
                <template slot="items" v-for="enterprise in arrEnterprises">
                        {{`${enterprise.name}`}}
                    <template v-if="enterprise.parcels">
                        <cv-structured-list-item
                            v-for="feature in enterprise.parcels.features"
                            v-bind:key="feature.id" 
                            name="group-1"
                            :value="String(feature.id)"
                            ref="listaDeParcelas"
                            @change="actionChangeParcels"
                        >
                            <cv-structured-list-data>{{feature.properties.name}} - {{enterprise.name}}</cv-structured-list-data>
                        </cv-structured-list-item>
                    </template>
                </template>
            </cv-structured-list>  
        </div>
        -->
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
                                <cv-structured-list-data>{{is_superuser ? parcel.id+' - ' : ''}}{{parcel.properties.name}} - {{getNameEnterprise(parcel.properties.enterprise_id)}}</cv-structured-list-data>
                            </cv-structured-list-item>
                        </template>
                    </template>
                </cv-structured-list>  
            </div>
        
            <br>

            <div v-if="this.is_superuser">
                <div class="bx--row">
                    <div class="bx--col">
                        <cv-toggle
                            :checked="true"
                            label="Desbordamiento de Alerta  de Parcelas"
                            value="check-2"
                            :small="true"
                            :hide-label="true"
                            @change="actionChangedAlertSolpamientoToggle">
                            <template slot="text-left">Desactivado alerta de solapamiento de Parcelas</template>
                            <template slot="text-right">Activado alerta de solapamiento de Parcelas</template>
                        </cv-toggle>
                    </div>
                </div>
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
            <br>
            <div>
                <div class="bx--row">
                    <div class="bx--col">
                        <cv-toggle
                            :checked="false"
                            label="Ocultar icono de mi ubicación"
                            value="check-1"
                            :small="true"
                            :hide-label="false"
                            @change="actionChangedToggleIconoUbi">
                            <template slot="text-left">No</template>
                            <template slot="text-right">Sí</template>
                        </cv-toggle>
                    </div>
                </div>
            </div>
        </div>
        <br>
        <div id="sentinelLayers">
            <cv-dropdown 
                @change="actionChangeLayers" 
                :label="$t('map.sent_layers')">
                    <cv-dropdown-item v-for="layer in layersSelector" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
            </cv-dropdown>
        </div>
        <div v-if="SentinelLayer == 'NDVI'">
            <label for="text-input-3h9mddk235a" class="bx--label">{{$t("map.colors")}}</label>
            <br>
            <img alt="D4SF" id="logo" src="../../assets/NDVI-colores.png" style="width: 100%;">
        </div>
        <div v-if="SentinelLayer == 'MOISTURE_INDEX'">
            <label for="text-input-3h9mddk235a" class="bx--label">{{$t("map.colors")}}</label>
            <br>
            <img alt="D4SF" id="logo" src="../../assets/Moisture-index-valores.png" style="width: 100%;">
        </div>
        <br>
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
</template>
<script>
//import proj4 from 'proj4'
//import {polygonCenter} from '@/crudFunctions/crudEnterprise'
import {getEnterprise, getAllEnterprises, /*getAllActiveEnterprises,*/ getFechasSentinel, setParcelsForInstance} from '@/crudFunctions/crudEnterprise'//getEnterprise
import {getCooperative} from '@/crudFunctions/crudCooperativas'
export default {
    name: 'ControllerPanel',
    props: {
        username: String,
        arrEnterprises: Array,
        arrCooperativas: Array,
        centro: [],
        layersSelector: Array,
        checkedToggleMostarTexto: Boolean,
        is_superuser: Boolean,
        is_systemadmin: Boolean,
        is_staff: Boolean,
        is_enterpriseadmin: Boolean,
        is_coop_user: Boolean,
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
            expand: true,
            expand2: true,
            erorCompaGeoloc: '',
            mostrarIconErrGeoloc: '',
            empresa_selec:Object()
        }
    },
    components: {
        
    },
    methods: {
        // para ordenar las empresas de la cooperativa alfabéticamente
        getSortedCooperativa(cooperativa) {
            return {
                ...cooperativa,
                enterprises: cooperativa.enterprises.slice().sort((a, b) => {
                return a.name.localeCompare(b.name);
                }),
            };
        },
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
                this.$emit('setCenterLocation', [pos.coords.longitude, pos.coords.latitude])
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
            this.empresa_selec = empresa;
            const nombre = document.getElementById("selectEmp");
            document.getElementById("empresa").innerHTML = nombre.options[nombre.selectedIndex].text;
            const arrParcels = [];
            console.log("Empresa selecccionada ", empresa);

            if (empresa == 'all') {
                getAllEnterprises()
                    .then(async response => {
                        response.data.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel);
                            });
                        });
                        this.$emit('setEnterprise', response.data);
                        this.$emit('setAllParcelsOfEnterprises', arrParcels);
                    })
                    .catch(error => {
                        console.error('Error al obtener empresas activas:', error);
                    });
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
                        console.log('parada')
                        this.$emit('setEnterprise', [response.data])   
                        this.$emit('setAllParcelsOfEnterprises', arrParcels)                     

                        const allCoordinates = Array();
                        arrParcels.map(parcel => {
                            allCoordinates.push(parcel.geometry.coordinates)
                        })
                        await setParcelsForInstance(response.data.name, allCoordinates, response.data.sentinel_instance)
                        .then(response1 => {
                            console.info(`OK refrescado parcelas de ${response.data.name}`, response1.data)
                            
                            console.log(response.data)
                        })
                        .catch(err => console.info(`ERROR refrescado parcelas de ${response.data.name}`, err))
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
            const arrAllParcelsFilter = this.allParcelsOfEnterprisesFilter
            this.$emit('setCenter', [newCenter[0], newCenter[1]])
            this.$emit('setflagparcela', 16.5)
            this.$emit('setAllParcelsOfEnterprisesFilter', arrAllParcelsFilter)
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

        actionChangedAlertSolpamientoToggle(value){
            console.warn('actionChangedAlertSolpamientoToggle', value)
            //this.checkedToggleMostarTexto = value
            this.$emit('setToggleAlertSolpamiento', value)
        },

        actionChangedToggleIconoUbi(value){
            this.$emit('setOcultarInconoUbi', value)
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
        this.$nextTick(function(){
            this.seleccionaEmpresa('all');
        }
 
        )
        //console.info('User Logged')
    },
    beforeCreate(){
        
    },
    computed: {
    // para ordenar las empresas alfabéticamente
    sortedListadoEmpresas() {
      return this.listadoEmpresas.slice().sort((a, b) => {
        return a.name.localeCompare(b.name);
      });
    },
  },
}
</script>
<style scoped>
    #layersControler{
        position: fixed;
        width: 450px;
        padding: 10px;
        background-color: #f4f4f4;
        margin-top: 10px;
        margin-left: 10px;
        max-width: 480.6px;
        overflow: scroll;
        height: auto;
        max-height: 850px;
        overflow-x: hidden;
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

    @media (max-height: 700px) {
        #sentinelLayersList{
            overflow: scroll;
            height: 280px;
        }
        #layersControler{
            height: 600px;
            overflow-x: hidden;
        }
    }
    /*
    @media (max-height: 800px) {
        #layersControler{
            height: 600px;
            overflow-x: hidden;
        }
    */
</style>
