<!--
@modal-shown="actionShown"
@modal-hidden="actionHidden"
@modal-hide-request="actionHideRequest"
-->
<template>
  <cv-modal
    :close-aria-label="closeAriaLabel"
    :size="size"
    :primary-button-disabled="primaryButtonDisabled"
    :auto-hide-off="false"
    @primary-click="actionPrimary"
    ref="editarRolForm" id="parcelModal"
  >
    <template v-if="use_label" slot="label">{{title_card}}</template>
    <template v-if="use_title" slot="title">{{subtitle_card}} {{userSeleccionado}}</template>
    <template v-if="use_content" slot="content">
      <cv-text-input
        :label="labelName"
        :value="valueName"
        :disabled="disabledName"
        :type="inputTypeName"
        :placeholder="placeholderName"
        :invalid-message="invalidMessageName"
        ref="inputName"
        id="input-MIRLwtCq"
      ></cv-text-input>

      <br />

      <cv-text-input
        :label="labelDesc"
        :value="valueDesc"
        :disabled="disabledDesc"
        :type="inputTypeDesc"
        :placeholder="placeholderDesc"
        :invalid-message="invalidMessageDesc"
        ref="inputDesc"
        id="input-3zcRveTf"
      ></cv-text-input>

      <br />
      <div id="map" class="map"></div>
    </template>
    <template v-if="use_primaryButton" slot="primary-button">Guardar</template>
  </cv-modal>
</template>
<script>
import axios from "axios";
//import qs from "qs"
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
//import OSM from "ol/source/OSM";
import BingMaps from 'ol/source/BingMaps';
import GeoJSON from "ol/format/GeoJSON";
//import Feature from 'ol/Feature';
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import { fromLonLat } from "ol/proj";
import {defaults as defaultInteractions, Modify, Select} from 'ol/interaction';
import Style from 'ol/style/Style';
import Stroke from 'ol/style/Stroke';
import Fill from 'ol/style/Fill';


export default {
    name: "EditarParcel",
    props: {
        userSeleccionado: String
    },
    components: {},
    data() {
        return {
            title_card: "",
            subtitle_card: "",
            closeAriaLabel: true,
            use_label: true,
            use_title: true,
            use_content: true,
            size: "",
            use_primaryButton: true,
            primaryButtonDisabled: false,
            autoHideOff: true,
            //input-name
            labelName: 'Nombre de la parcela',
            valueName: '',
            disabledName: false,
            inputTypeName: 'text',
            placeholderName: 'Nombre...',
            invalidMessageName: '',
            //input-email
            labelDesc: 'Descripción de la Parcela',
            valueDesc: '',
            disabledDesc: false,
            inputTypeDesc: 'text',
            placeholderDesc: 'Descripción...',
            invalidMessageDesc: '',
            //OPEN LAYERS
            geometry: Object,
            vectorLayer: Object,
            vectorLayer2: Object,
            map: Object,
            styles: Object,
        };
    },
    methods: {
        initMap(user) {
            console.info(user)
            var select = new Select({
                wrapX: false
            });
            var modify = new Modify({
                features: select.getFeatures()
            });
            this.styles = [
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
            this.vectorLayer = new VectorLayer({
                source: new VectorSource({
                    format: new GeoJSON(),
                    url: `${this.$apiURL}/parcels/${this.userSeleccionado}/`,
                    wrapX: false
                }),
                style: this.styles
            });
            
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
                    this.vectorLayer,
                ],
                view: new View({
                    center: fromLonLat(this.geometry.geometry.coordinates[0][0]),
                    zoom: 15
                })
            });
        },
        openModal(userSelec) {
            this.$refs.editarRolForm.show();
            
            this.showPassword = false
            this.title_card = 'Editar Parcela',
            this.subtitle_card = 'Editar Parcela:'
            this.userSeleccionado = userSelec;
            const path = `${this.$apiURL}/parcels/${this.userSeleccionado}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                    this.valueName = response.data.properties.name;
                    this.valueDesc = response.data.properties.description;
                    this.geometry = response.data;
                    document.getElementById('map').innerHTML = "";
                    this.initMap()
                })
                .catch( () => {
                    this.showPassword = true
                    this.title_card = 'Nueva Parcela'
                    this.subtitle_card = 'Crear Nueva Parcela'
                    this.valueName = '';
                    this.valueDesc = '';
                    document.getElementById('map').innerHTML = "";
                });
        },
        actionPrimary() {
            let path = '';
            if(this.userSeleccionado){
                path = `${this.$apiURL}/parcels/${this.userSeleccionado}/`;
                axios
                .put(path, {
                    name: this.$refs.inputName.$refs.input.value,
                    description: this.$refs.inputDesc.$refs.input.value,
                })
                .then(response => {
                    this.valueName = response.data.properties.name;
                    this.valueDesc = response.data.properties.description;
                    this.$parent.getUsers();
                    this.$refs.editarRolForm.hide();
                    this.invalidMessageName = "";
                    this.invalidMessageDesc = "";
                })
                .catch(error => {
                    //console.info(error);
                    if (error.response.data.name)
                        this.invalidMessageName = error.response.data.name[0];
                    if (error.response.data.description)
                        this.invalidMessageDesc = error.response.data.description[0];
                });
            }else{
                path = `${this.$apiURL}/parcels/`;
                axios
                .post(path, {
                    name: this.$refs.inputName.$refs.input.value,
                    description: this.$refs.inputDesc.$refs.input.value,
                })
                .then(response => {
                    this.valueName = response.data.properties.name;
                    this.valueDesc = response.data.properties.description;
                    this.$parent.getUsers();
                    this.$refs.editarRolForm.hide();
                    this.invalidMessageName = "";
                    this.invalidMessageDesc = "";
                })
                .catch(error => {
                    //console.info(error);
                    if (error.response.data.name)
                        this.invalidMessageName = error.response.data.name[0];
                    if (error.response.data.description)
                        this.invalidMessageDesc = error.response.data.description[0];
                });
            }
            
            
        }
    }
    
};
</script>
<style scoped>
.bx--modal-container {
    width: 90% !important;
}
#map {
    width: 100%;
    height: 500px;
}
</style>