<template>
    <div>
        <div id="map" class="map"></div>

        <!--
        <div id="layersControler" class="layerControler">
            <cv-structured-list selectable @change="actionChange" id="parcelList">
                <template slot="headings">
                    <cv-structured-list-heading>Parcelas</cv-structured-list-heading>
                </template>
                <template slot="items">
                    <cv-structured-list-item 
                    v-for="feature in allFeatures" 
                    name="group-1" 
                    :value="feature.id" 
                    v-bind:key="feature.id" 
                    :checked="feature.id == 1"
                    @change="actionChangeParcels">
                        <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                    </cv-structured-list-item>
                </template>
            </cv-structured-list>
            <div id="sentinelLayers">
                <cv-dropdown 
                    :placeholder="placeholderLayers" 
                    @change="actionChangeLayers" :label="labelLayers">
                        <cv-dropdown-item v-for="layer in layersSentinel" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.id}}</cv-dropdown-item>
                </cv-dropdown>
            </div>
            <div id="sentinelOpacity">
                <cv-slider
                    :label="labelSliderOpa"
                    @change="actionChangeOpacity" ></cv-slider>
            </div>
            <div id="sentinelClouds">
                <cv-slider
                    :label="labelSliderCloud"
                    @change="actionChangeClouds"></cv-slider>
            </div>
            <div id="sentinelDate">
                <cv-date-picker
                kind="single"
                :cal-options="calOptions"
                @change="actionChangeDate"
                v-model="modelValue"
                :placeholder="placeholderDate"
                :dateLabel="labelFecha"></cv-date-picker>
            </div>
        </div>
        -->
    </div>
</template>
<script>
//import axios from "axios";

//import OSM from "ol/source/OSM";
//import GeoJSON from "ol/format/GeoJSON";
//import VectorLayer from "ol/layer/Vector";
//import VectorSource from "ol/source/Vector";
//import { fromLonLat } from "ol/proj";
//import {defaults as defaultInteractions, Modify, Select} from 'ol/interaction';
//import Style from 'ol/style/Style';
//import Stroke from 'ol/style/Stroke';
//import Fill from 'ol/style/Fill';
//import TileWMS from 'ol/source/TileWMS';
//import Feature from 'ol/Feature';
//import {transformExtent} from 'ol/proj';
//import Polygon from 'ol/geom/Polygon';


import axios from "axios";
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import { defaults as defaultInteractions } from 'ol/interaction';
import { transform } from 'ol/proj';
//import BingMaps from 'ol/source/BingMaps';
import SourceVector from 'ol/source/Vector';
import VectorLayer from "ol/layer/Vector";
import { fromLonLat } from "ol/proj";
import Collection from 'ol/Collection';
import Select from 'ol/interaction/Select';
//import L from 'leaflet'
import Feature from 'ol/Feature';
import Polygon from 'ol/geom/Polygon';
//import TileWMS from 'ol/source/TileWMS';
import OSM from "ol/source/OSM";

export default {
    name: "MapComponent",
    props: {
    },
    components: {},
    data() {
        return {
            geometry: Object,
            allCoordinatesMultipolygon: Array,
            valueLayersControler: '0',
            placeholderLayers: 'Selecciona un Layer de Sentinel',
            layersSentinel: Array,
            SentinelLayer: 'AGRICULTURE',
            labelSliderOpa: 'Opacidad',
            labelSliderCloud: 'Nubes',
            labelLayers: 'Sentinel Layers',
            labelFecha: 'Fecha',
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            placeholderDate: "yyyy/mm/dd",
            map: Object,
            vectorLayer: Object,
            wmsLayer: Object,
            allFeatures: Array(),
            view: Object,
            jsondata: Object,
            vectorSource: Object,
            parcelsLayer: new VectorLayer({
                source: new SourceVector({}),
            }),
            selectInteraction: new Select,
            parcelIndexSelected: ''
        }
    },
    methods: {
        initMap() {
            this.map = new Map({
                target: 'map',
                
                layers: [
                    new TileLayer({
                        source: new OSM()
                    }),
                    /*
                    new TileLayer({
                        source: new BingMaps({
                            key: 'Ajf7rbOuQ1cg5-D5vOeqPxZ7PR1k5Uc_3XMYEZSRGqqx0-LdXnYfflWQfQfIHD5-',
                            imagerySet: 'AerialWithLabels',
                        })
                    }),
                    */
                    this.parcelsLayer,
                ],
                view: new View({
                    center: [0, 0],
                    //center: fromLonLat(this.geometry.geometry.coordinates[0][0]),
                    constrainRotation: true,
                    zoom: 13
                }),
                interactions: defaultInteractions(),
                overlays: new Collection(),
                controls: new Collection(),
            });
        },
        getGeometryFromParcel(parcel) {
            const coordinates = parcel.geometry.coordinates;
            const olCoordinates = coordinates.map(coord => {
                const transCoord = this.transformClientToMapCoordinates(coord);
                return [transCoord[0], transCoord[1]];
            });
            return new Polygon([olCoordinates]);
        },
        createParcelsWithSentinelLayer(){
            let path = `${this.$apiURL}/parcels_json/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                response.data.features.map((parcel, index) =>{
                    const feature = new Feature({
                        id: 'parcel_' + parcel.properties.pk,
                        geometry: new Polygon(parcel.geometry)
                    })
                    feature.setId('parcel_' + parcel.properties.pk)
                    this.parcelsLayer.getSource().addFeature(feature);
                    /*
                    const sentinelLayer = new TileLayer({
                        source: new TileWMS({
                            url: `https://services.sentinel-hub.com/ogc/wms/2440dd85-0720-4c4c-bea2-7982fa8aa9b1`,
                            params: {
                                "urlProcessingApi":`https://services.sentinel-hub.com/ogc/wms/2440dd85-0720-4c4c-bea2-7982fa8aa9b1`,
                                "maxcc":50,
                                "minZoom":6,
                                "maxZoom":16,
                                "preset":this.SentinelLayer,
                                "layers":this.SentinelLayer,
                                "time":"2019-01-01/2020-06-04",
                                "BBOX": ""
                                },
                            serverType: 'geoserver',
                            transition: 0,
                        }),
                        opacity: 0.5,
                        zIndex: 9000 + index,
                    })
                    console.info(sentinelLayer)
                    */
                    
                    //parcel.sentinelTileIndex = this.map.getLayers().getLength();
                    //this.map.getLayers().insertAt(parcel.sentinelTileIndex, sentinelLayer);
                            
                })
            })
            .catch(error => {
                console.warn(error)
            })
        },


        actionChangeLayers(valor){
            this.SentinelLayer = valor
            this.wmsLayer.getSource().updateParams({"layers": valor});
        },
        actionChangeParcels(valor){
            const parcelSelect = this.allFeatures.find(x => x.id === valor).geometry
            const DURATION_BETWEEN_FITS = 1000;
            this.view.animate({center: fromLonLat(parcelSelect.coordinates[0][0]), duration: DURATION_BETWEEN_FITS, Zoom: 20});
        },
        actionChangeOpacity(valor){
            this.wmsLayer.setOpacity(valor/100);
        },
        actionChangeClouds(valor){
            this.wmsLayer.getSource().updateParams({"maxcc": valor});
        },
        actionChangeDate(valor){
            this.wmsLayer.getSource().updateParams({"time": "2019-01-01/"+valor});
        },
        transformClientToMapCoordinates([c1, c2]){
            let [a, b] = [c1, c2];
            if (this.referenceSystem === 'EPSG:4326') {
                [a, b] = this.transformToEpsg4326([a, b]);
            }
            return [a, b];
        },
        transformToEpsg4326([a, b]){
            return transform([a, b], 'EPSG:3857', 'EPSG:4326');
        }
        
    },
    mounted() {
        this.initMap() 
        this.createParcelsWithSentinelLayer()       
    }

}

</script>
<style scoped>
    #nav{
        padding: 17px!important;
    }
    #map {
        width: 100%; height: 100%; position:fixed
    }
    #layersControler{
        position: fixed;
        width: auto;
        padding: 10px;
        background-color: #f4f4f4;
        margin-top: 10px;
        margin-left: 10px;
    }
    #parcelList{
        margin-bottom: 1em;
    }
    #sentinelLayers, #sentinelOpacity, #sentinelClouds, #sentinelDate{
        margin-bottom: 1em;
    }

</style>