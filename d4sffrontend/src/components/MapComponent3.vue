<template>
    <div id="container">
        <div class="mapa" id="map"></div>
        <div id="layersControler" class="layersControler">
            
            <div id="sentinelLayersList">
                    <cv-structured-list selectable id="parcelList">
                        <template slot="headings">
                            <cv-structured-list-heading>Parcelas</cv-structured-list-heading>
                        </template>
                        <template slot="items">
                            <cv-structured-list-item 
                            v-for="feature in allFeatures" name="group-1" :value="feature.properties.pk" 
                            v-bind:key="feature.properties.pk" 
                            :checked="feature.properties.pk == 1"
                            ref="listaDeParcelas"
                            @change="actionChangeParcels"
                            >
                                <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                            </cv-structured-list-item>
                        </template>
                    </cv-structured-list>
            </div>
            <div id="sentinelLayers">
                <cv-dropdown 
                    placeholder="Selecciona un Layer de Sentinel" 
                    @change="actionChangeLayers" :label="labelLayers">
                        <cv-dropdown-item v-for="layer in layersSentinel" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
                </cv-dropdown>
            </div>
            <div v-if="verColoresEsas">
                <label for="text-input-3h9mddk235a" class="bx--label">Colores</label>
                <br>
                <img alt="D4SF" id="logo" src="../assets/muestras-colores.png" style="width: 100%;">
            </div>
            <br>
            <div id="sentinelOpacity">
                <cv-slider
                    :label="labelSliderOpa"
                    @change="actionChangeOpacity" ></cv-slider>
            </div>
            <div id="sentinelClouds" v-if="false">
                <cv-slider
                    :label="labelSliderCloud"
                    @change="actionChangeClouds"></cv-slider>
            </div>
            <div id="sentinelDate">
                <cv-date-picker
                kind="single"
                :cal-options="calOptions"
                @change="actionChangeDate"
                :placeholder="placeholderDate"
                :dateLabel="labelFecha"></cv-date-picker>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
//import Polygon from 'ol/geom/Polygon';
//import proj4 from 'proj4'
import L from 'leaflet'
require('leaflet-bing-layer')
require('leaflet-image-transform')
require('leaflet-boundary-canvas')
require('leaflet-geotiff')

require('leaflet.wms/dist/leaflet.wms.js')


export default {
    data () {
        return{
            labelLayers: 'Sentinel Layers',
            layersSentinel: Array,
            verColoresEsas: false,
            labelSliderOpa:'Opacidad',

            geojson: [],
            allFeatures: Array(),
            map: Object,
            allCoordinates: Array(),
            SentinelLayer: 'AGRICULTURE',
            opacitylayer: 0,
            geoJsonLayer: Object,
        }
    },
    methods: {
        initMap() {
            var map = L.map('map', {
                center: [0, 0],
                zoom: 13,
            });
            L.tileLayer.bing(this.$apiKeyBing).addTo(map)
            let path = `${this.$apiURL}/parcels_json/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                this.geojson = response.data
                this.allFeatures = response.data.features
                
                L.geoJSON(this.geojson, {
                    onEachFeature: function (feature, layer) {
                        layer.bindTooltip(`${layer.feature.properties.name}`, {permanent: true, direction: 'center', opacity: 0.7}).openTooltip();
                        /*
                        var imageUrl = `https://services.sentinel-hub.com/ogc/wms/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?service=WMS&request=GetMap&layers=AGRICULTURE&styles=&format=image%2Fpng&transparent=true&version=1.1.1&width=256&height=256&srs=EPSG%3A4326&bbox=${layer.getBounds()._northEast.lng},${layer.getBounds()._northEast.lat},${layer.getBounds()._southWest.lng},${layer.getBounds()._southWest.lat}`
                        //var imageBounds = [[layer.getBounds()._northEast.lat, layer.getBounds()._northEast.lng], [layer.getBounds()._southWest.lat, layer.getBounds()._southWest.lng]];
                        var ImageTrans = L.imageOverlay(imageUrl, layer.getBounds()).bringToBack()
                        ImageTrans.addTo(map)
                        */
                        
                    },
                    style: function () {
                        return {color: 'blue', fillOpacity: 0.0, fillColor:'transparent', zIndex:2, className: 'layerpol'};
                    }
                })
                .bindPopup(function (layer) {
                    map.fitBounds(layer.getBounds());
                    
                    //return `${layer.feature.properties.name} \n ${layer.feature.properties.description} \n ${layer.feature.properties.area}`;
                })
                .addTo(map);
                map.on('moveend', function(layer) { 
                    console.info(layer)
                })

                this.actionChangeParcels(this.allFeatures[0].properties.pk)

                this.allFeatures.forEach(element => {
                    this.allCoordinates.push(element.geometry.coordinates)
                    
                });
                
                const instanceIns = axios.create({
                    baseURL: this.$sentinelURL
                })
                const configIns = {
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8',
                        'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
                    }
                }

                const bodyIns = JSON.stringify({
                    'name': `${sessionStorage.getItem('enterprise')}`,
                    "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                    "additionalData": {
                        "showLogo": false,
                        "showWarnings": false,
                        "imageQuality": 90,
                        "disabled": false
                    },
                    'areaOfInterest': {
                        'type': "MultiPolygon",
                        'coordinates': this.allCoordinates
                        ,"crs": {
                            "type": "name",
                            "properties": {
                                "name": "urn:ogc:def:crs:EPSG::4326"
                            }
                        }
                    }
                })

                instanceIns.put("/configuration/v1/wms/instances/"+sessionStorage.getItem('sI'), bodyIns, configIns).then(resp => {
                    if(resp.status != 200){
                        console.warn(resp)
                    }else{
                        /*
                        L.tileLayer.wms(`${this.$sentinelURL}/ogc/wms/${sessionStorage.getItem('sI')}`, {
                            layers: 'AGRICULTURE',
                            transparent: true,
                            format: 'image/png'
                        }).addTo(this.map);
                        */
                    }
                })
                instanceIns.get("/configuration/v1/wms/instances/"+sessionStorage.getItem('sI')+"/layers", configIns).then(resp =>{
                    if(resp.status != 200){
                        console.warn(resp)
                    }
                    this.layersSentinel = resp.data
                })
            })
            .catch(error => {
                console.warn(error)
            })
            this.map = map
        },
        actionChangeParcels(parcelSelect){
            const featureSel = this.allFeatures.filter(feature =>{
                return feature.properties.pk == parcelSelect
            })
            const polygon = L.polygon(featureSel[0].geometry.coordinates)
            var bounds = polygon.getBounds();
            var latLng = bounds.getCenter();
            this.map.panTo(new L.LatLng(latLng.lng, latLng.lat));
        },

        actionChangeLayers(valor){
            console.info(valor)
            if(valor == "INTERPRETACIN-MULTIFACTOR" || valor == "ESAS-SCENE"){
                this.verColoresEsas = true
            }else{
                this.verColoresEsas = false
            }
            this.SentinelLayer = valor
            //const geoJsonLayer = this.geoJsonLayer.getLayers()

            L.tileLayer.wms(`${this.$sentinelURL}/ogc/wms/2440dd85-0720-4c4c-bea2-7982fa8aa9b1`, {
                layers: valor,
                transparent: true,
                format: 'image/png'
            }).addTo(this.map)
                    
                
            /*
            L.tileLayer.wms(`${this.$sentinelURL}/ogc/wms/${sessionStorage.getItem('sI')}`, {
                layers: valor,
                format: 'image/png',
                transparent: true,
            }).addTo(this.map);
                */

            
            //this.wmsLayer.getSource().updateParams({"layers": valor});
        },
        actionChangeOpacity(valor){
            console.info(valor)
            this.opacitylayer = valor/100;
            const opacityLy = L.tileLayer.wms(`${this.$sentinelURL}/ogc/wms/${sessionStorage.getItem('sI')}`, {
                layers: this.SentinelLayer,
                format: 'image/png',
                transparent: true,
                opacity: this.opacitylayer
            }).addTo(this.map);
            console.info(opacityLy)
        },
        getDatosUser(){
            if(sessionStorage.getItem("apiAccess")){
                const path = `${this.$apiURL}/profile/`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .get(path)
                .then(response => {
                    this.$session.start()
                    //---------------------------------------------------------------
                    this.$session.set('is_coop_user', response.data[0].cooperative_user)
                    this.$session.set('enterprise', response.data[0].enterprise_id)
                    this.$session.set('user', response.data[0].user)
                    sessionStorage.setItem('enterprise', response.data[0].enterprise_id)
                    sessionStorage.setItem('user', response.data[0].user)

                    let pathEnterpriseInstance = `${this.$apiURL}/enterprises/${response.data[0].enterprise_id}/`;
                    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                    axios.get(pathEnterpriseInstance)
                    .then(response =>{
                        sessionStorage.setItem('sI', response.data.sentinel_instance)
                        
                    })
                    //---------------------------------------------------------------
                    this.getPermisosUser(response.data[0].user)
                }).catch(error =>{
                    console.warn(error)
                })
            }
        },
        getPermisosUser(id){
            const pathRol = `${this.$apiURL}/permisos/${id}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(pathRol)
            .then(response => {
                //---------------------------------------------------------------
                this.$session.set('is_enterpriseadmin', response.data.is_enterpriseadmin)
                this.$session.set('is_staff', response.data.is_staff)
                this.$session.set('is_superuser', response.data.is_superuser)
                this.$session.set('is_systemadmin', response.data.is_systemadmin)
                sessionStorage.setItem('is_enterpriseadmin', response.data.is_enterpriseadmin)
                sessionStorage.setItem('is_staff', response.data.is_staff)
                sessionStorage.setItem('is_superuser', response.data.is_superuser)
                sessionStorage.setItem('is_systemadmin', response.data.is_systemadmin)
                this.$parent.$parent.is_superuser = response.data.is_superuser
                this.$parent.$parent.is_staff = response.data.is_staff,
                this.$parent.$parent.is_systemadmin = response.data.is_systemadmin,
                this.$parent.$parent.is_enterpriseadmin = response.data.is_enterpriseadmin
                this.$parent.$parent.customLinkEnterprise = 'edit-enterprise?enterprise='+this.$session.get('enterprise')
                //---------------------------------------------------------------
                this.initMap();
            })
        },
    },
    
    created() {
        
    },
    mounted(){
        this.getDatosUser()
        /*
        this.getDatosUser()
        console.info(this.$parent)
        this.$parent.$parent.is_superuser = true
        this.$parent.$parent.is_superuser = false,
        this.$parent.$parent.is_staff = false,
        this.$parent.$parent.is_systemadmin = false,
        this.$parent.$parent.is_enterpriseadmin = false
        */
    }
}
</script>
<style scoped>
    #container{
        display:flex;
        height:100%;
    }
    .mapa{
        flex-grow:1;
        z-index:10;
        height: 100vh;
    }
    #layersControler{
        position:absolute;
        width: auto;
        z-index:20;
        margin-top: 10px;
        margin-left: 10px;
        background-color: #f4f4f4;
        max-width: 366.6px;
        padding: 8px;
    }
    #sentinelLayersList{
        overflow: scroll;
        height: 400px;
    }
    @media (max-height: 700px) {
        #sentinelLayersList{
            overflow: scroll;
            height: 280px;
        }
    }
    .layerpol{
        background-color: black;
    }
</style>