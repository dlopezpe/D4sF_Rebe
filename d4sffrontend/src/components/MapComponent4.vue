<template>
    <div>
        <cv-loading
            :small="true"
            :active="true"
            :overlay="false" v-if="true" id="cargando"></cv-loading>
        <vl-map
            :load-tiles-while-animating="false"
            :load-tiles-while-interacting="false"
            data-projection="EPSG:4326"
            style="height: 400px"
            id="map"
            class="mapa"
            ref="map"
            
        >
            <vl-view :zoom.sync="zoom" :center="center"></vl-view> 
            
            
            <!-- manda las solicitudes a https://services.sentinel-hub.com/ogc/wms/ac3c509d-17c1-43b5-8595-45f800ae2e30/?MAXCC= -->
            <vl-layer-tile :id="`wmts_${enterprise.id}`" :opacity="opacitylayer" v-bind:key="`${enterprise.id}_layers_${timestampSentinel}`" v-for="enterprise in arrEmpresas" :z-index="2">
                <vl-source-wms
                    v-if="enterprise.parcels.features.length"
                    :key="`${enterprise.id}_${timestampSentinel}`" 
                    :url="`${urlSentinel}${enterprise.sentinel_instance}/?MAXCC=100&v=${timestampSentinel}&`"
                    :urlProcessingApi="`${urlSentinel}${enterprise.sentinel_instance}/?MAXCC=100&&v=${timestampSentinel}&`"
                    maxcc="100"
                    :minZoom="minZoom"
                    :maxZoom="maxZoom"
                    :preset="preset"
                    :layers="SentinelLayer"
                    :time.sync="time"
                    :serverType="serverType"
                    :opacity="opacitylayer"
                    :transition='transition'
                    :tiled = false
                />
            </vl-layer-tile>
            <!-- marca las lineas de la parcelas -->
            <vl-layer-vector v-for="enterprise in arrEmpresas" v-bind:key="`${enterprise.id}_1_${timestamp}`" :z-index="3">
                <vl-source-vector ref="drawTarget" v-if="enterprise.parcels" :features="enterprise.parcels.features" />
                <vl-style-func :factory="pointsStyleFunc" />
            </vl-layer-vector>
            
            <vl-interaction-select v-if="verCrearParcel" :id="`modify_target_${timestamp}`" ref="selectInteraction" ident="modify-target" @select="selecionaPolygon" :key="timestampSentinel"></vl-interaction-select>
            <vl-interaction-modify v-if="verCrearParcel" source="modify-target" @modifyend="editado"></vl-interaction-modify>
            <!-- posiblemente marca con color a las parcelas guardadas -->
            <vl-layer-vector :z-index="4" v-bind:key="`the_source_indent_${timestampDrawPolygon}`">
                <vl-source-vector ident="the-source" :features.sync="featuresNewPolygon"></vl-source-vector>
                <vl-style-box>
                    <vl-style-stroke color="green"></vl-style-stroke>
                    <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
                </vl-style-box>
            </vl-layer-vector>

            <vl-interaction-draw v-bind:key="`the_source_${timestampDrawPolygon}`" type="Polygon" source="the-source" v-if="!verCrearParcel && !verCrearParcelDraw" @drawend="terminadoNewPolygon"></vl-interaction-draw>

            <vl-feature v-if="!olcultarInconoUbi">
                <vl-geom-point :coordinates.sync="coordenadasPunto"></vl-geom-point>
                <vl-style-box>
                    <vl-style-icon src="https://d4smartfarming.smartbits-es.com/imgMail/icono-mapa.png"></vl-style-icon>
                </vl-style-box>
            </vl-feature>
            <!-- conforma las imagenes del mapa total -->
            <vl-layer-tile id="bingmaps">
                <vl-source-bingmaps :api-key="apiKeyBing" :imagery-set="imagerySetBing" :maxZoom="maxZoomBing"></vl-source-bingmaps>
            </vl-layer-tile>
            
        </vl-map>
        
        <template v-if="flagIndicatingDataHasBeenLoadedInVariables">
            <ControllerPanel
                v-if="!isMobile()"
                :username="name" 
                :arr-enterprises="arrEmpresas4List"
                :arr-cooperativas="arrCooperativas"
                :is_superuser="is_superuser"
                :is_systemadmin="is_systemadmin"
                :is_staff="is_staff"
                :is_enterpriseadmin="is_enterpriseadmin"
                :is_coop_user="is_coop_user"
                :checked-toggle-mostar-texto="checkedToggleMostarTexto"
                :layers-selector="layersSelector"
                :map-component="$refs.map.$map"
                :all-parcels-of-enterprises="allParcelsOfEnterprises"
                :all-parcels-of-enterprises-filter="allParcelsOfEnterprisesFilter"
                :sentinel-layer="SentinelLayer"

                v-on:setToggleAlertSolpamiento="showSolapamientoAlert = $event"

                v-on:setCenter="center = $event"  
                v-on:setflagparcela="zoom=$event"  
                v-on:setCenterLocation="coordenadasPunto = $event"  
                v-on:setToggleMostrarTexto="checkedToggleMostarTexto = $event, getNow()"
                v-on:setEnterprise="arrEmpresas = $event, getNow(), arrEmpresas4List = $event"
                v-on:setSentinelLayer="getNowSentinel(), SentinelLayer = $event"
                v-on:setSentinelClearCache="getNowSentinel()"
                v-on:setSentinelOpacity="opacitylayer = $event"
                v-on:setFechaSentinel="time = $event"
                v-on:setAllParcelsOfEnterprises="allParcelsOfEnterprises = $event, allParcelsOfEnterprisesFilter = $event"
                v-on:setAllParcelsOfEnterprisesFilter="allParcelsOfEnterprisesFilter = $event"
                v-on:setOcultarInconoUbi="olcultarInconoUbi = $event"
            />
            <ControllerPanel4Mobile
                v-if="isMobile()"
                :username="name" 
                :arr-enterprises="arrEmpresas4List"
                :arr-cooperativas="arrCooperativas"
                :is_superuser="is_superuser"
                :is_systemadmin="is_systemadmin"
                :checked-toggle-mostar-texto="checkedToggleMostarTexto"
                :layers-selector="layersSelector"
                :map-component="$refs.map.$map"
                :all-parcels-of-enterprises="allParcelsOfEnterprises"
                :all-parcels-of-enterprises-filter="allParcelsOfEnterprisesFilter"
                :sentinel-layer="SentinelLayer"

                v-on:setflagparcela="zoom=$event"
                v-on:setCenter="center = $event"  
                v-on:setToggleMostrarTexto="checkedToggleMostarTexto = $event, getNow()"

                v-on:setToggleAlertSolpamiento="showSolapamientoAlert = $event"
                
                
                v-on:setEnterprise="arrEmpresas = $event, getNow(), arrEmpresas4List = $event"
                v-on:setSentinelLayer="getNowSentinel(), SentinelLayer = $event"
                v-on:setSentinelClearCache="getNowSentinel()"
                v-on:setSentinelOpacity="opacitylayer = $event"
                v-on:setFechaSentinel="time = $event"
                v-on:setAllParcelsOfEnterprises="allParcelsOfEnterprises = $event, allParcelsOfEnterprisesFilter = $event"
                v-on:setAllParcelsOfEnterprisesFilter="allParcelsOfEnterprisesFilter = $event"
            />
            <ControllerQuickEdit 
                v-if="ifQuickEdit && !is_coop_user && !is_staff"
                :parcel-selected="parcelSelected"
                :error-draw-msg="errorDrawMsg"
                :ver-error-draw="verErrorDraw"
                :coordinates-poly="coordinatesPoly"
                :value-name="valueName"
                :value-desc="valueDesc"
                :arr-enterprises="arrEmpresas"
                :arr-cooperativas="arrCooperativas"
                :area-for-new-polygon="areaForNewPolygon"


                v-on:setClearFeatures="featuresNewPolygon = []"
                v-on:setVerCrearParcel="verCrearParcel = $event"
                v-on:setVerCrearParcelDraw="verCrearParcelDraw = $event"
                
                v-on:setcoordinatesPoly="coordinatesPoly = $event, featuresNewPolygon = []"
                v-on:setifQuickEdit="ifQuickEdit = $event"
                
                v-on:setverErrorDraw="verErrorDraw = $event"
                v-on:setSentinelClearCache="getNowSentinel()"
                v-on:setClearParcels="getNow()"
                v-on:setEnterprise="arrEmpresas = $event, getNow(), arrEmpresas4List = $event"
                v-on:setAllParcelsOfEnterprises="allParcelsOfEnterprises = $event, allParcelsOfEnterprisesFilter = $event"

            />
            <ControllerGoogleSearch
                v-on:setCenter="center = $event, coordenadasPunto = $event"  
            />
            
            <ControllerQuickCreate 
                v-if="!ifQuickEdit && !is_coop_user && !is_staff"
                :ver-crear-parcel="verCrearParcel"
                :error-draw-msg="errorDrawMsg"
                :ver-error-draw="verErrorDraw"
                :coordinates-poly="coordinatesPoly"
                :arr-enterprises="arrEmpresas4List"
                :arr-enterprises-selected="empresaSelForCreateParcel ? empresaSelForCreateParcel : arrEmpresas"
                :arr-cooperativas="arrCooperativas"
                :is_superuser="is_superuser"
                :is_systemadmin="is_systemadmin"
                :area-for-new-polygon="areaForNewPolygon"
                :user="user"

                v-on:setVerCrearParcel="verCrearParcel = $event"
                v-on:setverErrorDraw="verErrorDraw = $event"
                v-on:setEnterpriseSelect="empresaSelForCreateParcel = $event"
                v-on:setClearFeatures="featuresNewPolygon = []"
                v-on:setVerCrearParcelDraw="verCrearParcelDraw = $event"
                v-on:clearCacheDraw="getNowRefreshDrawPolygon()"
                v-on:setSentinelClearCache="getNowSentinel()"
                v-on:setcoordinatesPoly="coordinatesPoly = $event, featuresNewPolygon = []"
                v-on:setEnterprise="arrEmpresas = $event, getNow(), arrEmpresas4List = $event"
                v-on:setAllParcelsOfEnterprises="allParcelsOfEnterprises = $event, allParcelsOfEnterprisesFilter = $event"
            />
        </template>
    </div>
</template>

<script>
import {getProfile, getPermisos} from '@/auth/index'
import {getAllEnterprises, getLayersFromSentinel, getEnterprise} from '@/crudFunctions/crudEnterprise'//getEnterprise
import {getAllCooperatives, getCooperative} from '@/crudFunctions/crudCooperativas'
import ControllerPanel from '@/components/mapController/ControllerPanel.vue'
import ControllerPanel4Mobile from '@/components/mapController/ControllerPanel4Mobile.vue'
import ControllerQuickEdit from '@/components/mapController/ControllerQuickEdit.vue'
import ControllerGoogleSearch from '@/components/mapController/ControllerGoogleSearch.vue'
import ControllerQuickCreate from '@/components/mapController/ControllerQuickCreate.vue'
import {checkValidPolygon} from '@/crudFunctions/crudEnterprise'
import proj4 from 'proj4'
import Style from 'ol/style/Style'
import Text from 'ol/style/Text'
import Fill from 'ol/style/Fill'
import Stroke from 'ol/style/Stroke'
import L from 'leaflet'
import { getArea } from 'ol/sphere';
import axios from 'axios'
//import Polygon from 'ol/geom/Polygon'
export default {
    name: 'MapComponent4',
    components: {ControllerPanel, ControllerQuickEdit, ControllerGoogleSearch,ControllerPanel4Mobile, ControllerQuickCreate
    },
    data() {
        return {
            flagparcela:false,
            zoomParcela:16.5,
            flagIndicatingDataHasBeenLoadedInVariables: false,
            //Usuario
            is_superuser: false,
            is_staff: false,
            is_systemadmin: false,
            is_enterpriseadmin: false,
            is_coop_user: false,
            //BingMap
            apiKeyBing: this.$apiKeyBing,
            imagerySetBing: `AerialWithLabels`,
            zoom: 15,
            center: [-3.8225970954841486, 40.28385074244977 ],
            maxZoomBing: 20,
            isActiveLoading: false,
            isVisibleLoad: false,
            name: 'pruebas',
            //Parcelas
            parcelas: {},
            //Empresas sel
            arrEmpresas: [],
            arrCooperativas: [],
            arrEmpresas4List: [],
            //Sentinel layer tile controller
            urlSentinel: `${this.$sentinelURL}/ogc/wms/`,
            minZoom:6,
            maxZoom:16,
            preset:'AGRICULTURE',
            layers:'AGRICULTURE',
            time:`2019-01-01/${this.getNow()}`,
            serverType: 'geoserver',
            opacitylayer: 0.5,
            transition: 0,
            SentinelLayer: 'AGRICULTURE',
            timestamp: 0,
            timestampSentinel: 0,
            timestampDrawPolygon: 0,
            checkedToggleMostarTexto: false,
            layersSelector: [],
            //ModificarParcela
            keyModificar: 0,
            allParcelsOfEnterprises: [],
            allParcelsOfEnterprisesFilter: [],
            ifQuickEdit: false,
            showSolapamientoAlert: true,
            
            parcelSelected: Object,
            verErrorDraw: false,
            errorDrawMsg: '',
            guardadoOKMsg: '',
            coordinatesPoly: '',
            //Crear Parcela
            featuresNewPolygon: [],
            verCrearParcel: true,
            verCrearParcelDraw: false,
            empresaSelForCreateParcel: '',
            refreshDibujo: 0,
            //editarParcel
            valueDesc: '',
            valueName: '',
            areaForNewPolygon: 0,
            //
            user: '',
            coordenadasPunto: [0, 0],
            olcultarInconoUbi: false
        }
    },
    methods: {
        isMobile() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return true
            } else {
                return false
            }
        },
        getNowSentinel() {
            const today = new Date();
            const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            const dateTime = date +' '+ time;
            this.timestampSentinel = dateTime;
        },
        getNowRefreshDrawPolygon() {
            const today = new Date();
            const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            const dateTime = date +' '+ time;
            this.timestampDrawPolygon = dateTime;
        },
        getNow() {
            const today = new Date();
            const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            const dateTime = date +' '+ time;
            this.timestamp = dateTime;
        },
        pointsStyleFunc(){
            return feature => {
                let baseStyle = new Style({
                    fill: new Fill({
                        color: "rgba(255,255,255,0.0)",
                    }),
                    stroke: new Stroke({
                        color: "rgba(0, 0, 255, 1)",
                        with: 5
                    }),
                    text: new Text({
                        overflow: this.checkedToggleMostarTexto,
                        text: `${feature.get('name')} \n ${feature.get('description') ? feature.get('description') : ''} \n ${feature.get('area') ? feature.get('area').toFixed(2)+'Ha' : '' } / ${feature.get('area') ? this.metricaparcela(feature.get('area'))+'Acre' : '' }`,
                        font: "14px IBM Plex Sans",
                        fill: new Fill({
                            //color: "#161616",
                            color: "#FFFFFF",
                        }),
                        stroke: new Stroke({
                            color: "#161616",
                            width: 4.5
                        }),
                    }),
                })
                return [
                    baseStyle,
                ]
            }
        },
        metricaparcela(area){
            const onehecttoAcre = 2.4710538146717
            const acre = onehecttoAcre * area
            this.metric = "Acre"
            return  acre.toFixed(2)
        
        },

        selecionaPolygon(po){
            this.ifQuickEdit = true
            this.coordinatesPoly = ''
            this.verErrorDraw = true
            this.verErrorDraw = true
            const result = this.allParcelsOfEnterprises.filter(parcel => parcel.id == po.id_)
            this.parcelSelected = result[0]
            const coordenadasGeometricas = po.getGeometry().getExtent()
            const ex = coordenadasGeometricas[0] + (coordenadasGeometricas[2]-coordenadasGeometricas[0])/2;
            const ye = coordenadasGeometricas[1] + (coordenadasGeometricas[3]-coordenadasGeometricas[1])/2;
            var source = new proj4.Proj('EPSG:3785'); 
            var dest = new proj4.Proj('EPSG:4326');  
            const newCenter = proj4(source, dest, [ex, ye])
            this.center = [newCenter[0], newCenter[1]]
            const enterprise_id = po.values_.enterprise_id
            this.valueName = po.values_.name
            this.valueDesc = po.values_.description
            this.comprobarCoordenadas(po.getGeometry().getCoordinates(), enterprise_id, po.id_)
        },
        terminadoNewPolygon(p){
            console.info(p)
            this.verCrearParcelDraw = true
            this.areaForNewPolygon = (Math.round((getArea(p.feature.getGeometry())/ 10000) * 10000) / 10000)
            const coordinatesEditadas = p.feature.getGeometry().getCoordinates()
            this.comprobarCoordenadas(coordinatesEditadas, (this.empresaSelForCreateParcel ? this.empresaSelForCreateParcel[0].id : this.arrEmpresas[0].id), 0)
        },
        editado(p){
            console.warn("editado..")
            

            const enterprise_id = p.features.array_[0].values_.enterprise_id
            const coordinatesEditadas = p.features.array_[0].getGeometry().getCoordinates()
            console.warn(coordinatesEditadas)
            this.areaForNewPolygon = (Math.round((getArea(p.features.array_[0].getGeometry())/ 10000) * 10000) / 10000)
            
            //const area = (Math.round((getArea(p.features.array_[0].getGeometry()) / 10000) * 10000) / 10000)
            this.comprobarCoordenadas(coordinatesEditadas, enterprise_id, p.features.array_[0].id_)
            //if(this.parcelaSeleccionada){
                //this.coordinatesBuenas(this.coordinatesEditadas)
            //}
            
            //this.verErrorDraw = false
        },
        getBBOX(parcel){
            const polygon = L.polygon(parcel.geometry.coordinates)

            const bboxP = `${polygon.getBounds()._northEast.lng},${polygon.getBounds()._northEast.lat},${polygon.getBounds()._southWest.lng},${polygon.getBounds()._southWest.lat}`
            return bboxP
        },
        getBBOX2(parcel){
            const polygon = L.polygon(parcel.geometry.coordinates)

            const bboxP = [polygon.getBounds()._northEast.lng,polygon.getBounds()._northEast.lat,polygon.getBounds()._southWest.lng,polygon.getBounds()._southWest.lat]
            return bboxP
        },
        comprobarCoordenadas(coords, enterprise, idParcela){
            var source = new proj4.Proj('EPSG:3785'); 
            var dest = new proj4.Proj('EPSG:4326'); 
            let newCenter = Array;
            let polygonObject= 'POLYGON(('
            for (var i = 0; i < coords[0].length; i++) {
                newCenter = proj4(source, dest, [coords[0][i][0], coords[0][i][1]])
                polygonObject += newCenter[0]+' '+newCenter[1]
                if(i != (coords[0].length-1)){
                    polygonObject += ', '
                }
            }
            polygonObject += '))';

            checkValidPolygon(polygonObject, enterprise)
            .then(response => {
                if(response.data.features.length){
                    const result = response.data.features.filter(feature => {
                        console.info(feature.id, idParcela)
                        if(feature.id != idParcela){
                            return feature
                        }
                    })
                    
                    console.warn("result.length",result.length)
                    console.warn("result.ifQuickEdit",this.ifQuickEdit)
                    console.warn("result.showSolapamientoAlert",this.showSolapamientoAlert)

                    if(result.length && this.showSolapamientoAlert){ 
                        if(this.ifQuickEdit){
                        let parcelsName = ''
                        result.map(resultado => {
                            parcelsName += resultado.properties.name + ' '
                        })
                            
                            this.errorDrawMsg = this.$t('map.parcela_solapada_con') + ' ' + parcelsName
                        this.verErrorDraw = true
                        this.coordinatesPoly = ''
                        }
                        
                    }else{
                        this.verErrorDraw = false
                        this.errorDrawMsg = ''
                        this.coordinatesPoly = polygonObject
                        this.compruebaParcelaSimple(polygonObject)
                    }
                }else{
                    this.verErrorDraw = false
                    this.errorDrawMsg = ''
                    this.coordinatesPoly = polygonObject
                    this.compruebaParcelaSimple(polygonObject)
                }
            })
        },
        compruebaParcelaSimple(polygonObject){
            let path = `${this.$apiURL}/parcel_valid/?polygon=${polygonObject}`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response=>{
                if(response.data == "False"){ // todo: quitar el ! para que funcione
                    this.errorDrawMsg = this.$t('map.parcela_solapada_misma')
                    this.verErrorDraw = true
                }else{
                    this.verErrorDraw = false
                    this.errorDrawMsg = ''
                }
            })
            .catch(error => {
                console.warn(error)
            })
        },
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
    beforeCreate(){
        this.isActiveLoading = false
        this.isVisibleLoad = false
        //* 1 - Obtenemos la info del usuario, a que empresa pertenece y si es administrador
        getProfile()
        .then(response => {
            const user = response.data[0]
            
            this.user = user
            getPermisos(response.data[0].user)
            .then(response => {
                this.is_superuser = response.data.is_superuser
                this.is_staff = response.data.is_staff
                this.is_systemadmin = response.data.is_systemadmin
                this.is_enterpriseadmin = response.data.is_enterpriseadmin
                this.is_coop_user = user.cooperative_user
                
                
                if(this.is_superuser || this.is_systemadmin){
                    getAllEnterprises()
                    .then(async response => {
                        this.arrEmpresas = [response.data[0]]
                        this.arrEmpresas4List = response.data
                        const arrParcels = []
                        //carga de la primera empresa
                        const empresaFirst = [response.data[0]]
                        //response.data[0].map(enterprise => {
                        empresaFirst.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                    })
                }else if((this.is_enterpriseadmin || this.is_staff) && !this.is_coop_user){ 
                    getEnterprise(user.enterprise_id)
                    .then(async response => {
                        this.arrEmpresas = [response.data]
                        this.arrEmpresas4List = [response.data]
                        const arrParcels = []
                        response.data.parcels.features.map(parcel => {
                            arrParcels.push(parcel)
                        })
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                    })
                }else if(this.is_coop_user){
                    getCooperative(user.enterprise_id)
                    .then(response => {
                        this.arrCooperativas = [response.data]
                        //this.arrEmpresas = response.data.enterprises
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                    })
                }

                if(this.is_superuser || this.is_systemadmin){
                    getAllCooperatives()
                    .then(async response => {
                        this.arrCooperativas = response.data
                    })
                }
                this.isActiveLoading = false
                this.isVisibleLoad = false
            })
        })
        getLayersFromSentinel().then(response => {
            this.layersSelector = response.data
        })
    }
}
</script>
<style scoped>
    #map{
        width: 100%; height: 100%; position:fixed
    }
    
    .mapa{
        width: 100%; height: 100%!important; position: fixed
    }
    #cargando{
        position:fixed
    }
</style>