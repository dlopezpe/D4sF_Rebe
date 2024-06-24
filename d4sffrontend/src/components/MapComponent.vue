<template>
    <div>
        <div id="map" class="map"></div>
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
    </div>
</template>
<script>
import axios from "axios";
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
//import OSM from "ol/source/OSM";
import GeoJSON from "ol/format/GeoJSON";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import { fromLonLat } from "ol/proj";
import {defaults as defaultInteractions, Modify, Select} from 'ol/interaction';
import Style from 'ol/style/Style';
import Stroke from 'ol/style/Stroke';
import Fill from 'ol/style/Fill';
import TileWMS from 'ol/source/TileWMS';
import BingMaps from 'ol/source/BingMaps';

import SourceVector from 'ol/source/Vector';
//import Feature from 'ol/Feature';
//import {transformExtent} from 'ol/proj';
import Polygon from 'ol/geom/Polygon';
import { transform } from 'ol/proj';

export default {
    name: "",
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
            //map options
            map: Object,
            vectorLayer: Object,
            wmsLayer: Object,
            allFeatures: Array(),
            view: Object,
            jsondata: Object,
            vectorSource: Object,
            vectorLayerParcels: new VectorLayer({
                source: new SourceVector({}),
            })
        }
    },
    methods: {
        initMap() {
            var select = new Select({
                wrapX: false
            });
            var modify = new Modify({
                features: select.getFeatures()
            });
            const styles = [
                new Style({
                    stroke: new Stroke({
                    color: 'blue',
                    width: 3
                    }),
                    fill: new Fill({
                    color: 'transparent'
                    })
                }),
            ];
            this.wmsLayer = new TileLayer({
                source: new TileWMS({
                    url: `https://services.sentinel-hub.com/ogc/wms/98c6d822-edb7-4a78-b7da-96b1a2bdefb4`,
                    params: {
                        "urlProcessingApi":`https://services.sentinel-hub.com/ogc/wms/98c6d822-edb7-4a78-b7da-96b1a2bdefb4`,
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
                opacity: 0.5
            });
            
            this.vectorSource = new VectorSource({
                format: new GeoJSON()
            })
            
            this.vectorLayer = new VectorLayer({
                source: new VectorSource({
                    format: new GeoJSON(),
                    url: `${this.$apiURL}/parcels/`,
                    wrapX: false
                }),
                style: styles
            });

            this.view = new View({
                //center: fromLonLat(this.geometry.geometry.coordinates[0][0]),
                center: fromLonLat(this.geometry.geometry.coordinates[0][0]),
                zoom: 16
            })
            
            this.map = new Map({
                target: 'map',
                interactions: defaultInteractions().extend([select, modify]),
                layers: [
                    new TileLayer({
                        source: new BingMaps({
                            key: 'Ajf7rbOuQ1cg5-D5vOeqPxZ7PR1k5Uc_3XMYEZSRGqqx0-LdXnYfflWQfQfIHD5-',
                            imagerySet: 'AerialWithLabels',
                            maxZoom: 20
                        })
                    }),
                    this.wmsLayer,
                    this.vectorLayer,
                    this.vectorLayerParcels
                ],
                view: this.view 
            });
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
            console.info(valor/100)
            this.wmsLayer.setOpacity(valor/100);
        },
        actionChangeClouds(valor){
            this.wmsLayer.getSource().updateParams({"maxcc": valor});
        },
        actionChangeDate(valor){
            console.info(valor)
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
    created() {
            const path = `${this.$apiURL}/parcels/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                    this.jsondata = response;
                    this.geometry = response.data.features[0];
                    var allCoordinates = Array();
                    response.data.features.forEach(element => {
                        allCoordinates.push(element.geometry.coordinates)
                        this.allFeatures.push(element)
                        
                    });
                    console.info(response.data.features)
                    console.info(response.data.features[0].geometry)
                    const polygon = new Polygon([response.data.features[0].geometry.coordinates])
                    console.info(polygon)
                    

                    const instanceIns = axios.create({
                        baseURL: "https://services.sentinel-hub.com"
                    })
                    const configIns = {
                        headers: {
                            'Content-Type': 'application/json;charset=utf-8',
                            'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
                        }
                    }
                    const bodyIns = JSON.stringify({
                        'name': 'Fermin',
                        "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                        'areaOfInterest': {
                            'type': "MultiPolygon",
                            'coordinates': allCoordinates
                            ,"crs": {
                                "type": "name",
                                "properties": {
                                    "name": "urn:ogc:def:crs:EPSG::4326"
                                }
                            }
                        }
                    })
                    instanceIns.put("/configuration/v1/wms/instances/98c6d822-edb7-4a78-b7da-96b1a2bdefb4", bodyIns, configIns).then(resp => {
                        if(resp.status != 200){
                            console.warn(resp)
                        }
                    })
                    instanceIns.get("/configuration/v1/wms/instances/98c6d822-edb7-4a78-b7da-96b1a2bdefb4/layers", configIns).then(resp =>{
                        if(resp.status != 200){
                            console.warn(resp)
                        }
                        this.layersSentinel = resp.data
                    })
                    this.initMap();
                    
                })
                .catch( () => {
                    
                });
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