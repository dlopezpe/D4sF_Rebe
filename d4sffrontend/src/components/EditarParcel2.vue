<template>
    <div>
    <!-- desactivar AutoHide = ponerlo a false
        activar Autohide = ponerlo a true -->
        <cv-modal
            :close-aria-label="closeAriaLabel"
            size='large'
            :primary-button-disabled="primaryButtonDisabled"
            :auto-hide-off='autoHideOff'
            @modal-shown="actionShownMap"
            ref="editarRolForm" id="parcelModal" class="parcelModalClass"
        >
            <!-- <div slot="content" @mouseover="deactivateAutoHide" @mouseout="activateAutoHide"> -->
        <!--auto-hide-off: para evitar que se cierre el modal de ninguna forma
            @modal-hidden: para que haga una acción justo cuando se sale del modal-->

            <template v-if="use_label" slot="label"><div id="targetClose" @mouseenter="cerrarModal">{{ title_card }}</div></template>
            <template v-if="use_title" slot="title">{{ subtitle_card }} {{ userSeleccionado }}</template>
            <template v-if="use_content" slot="content" id="contenido" v-modal="">
                <div class="bx--row" id="row_box">
                    <div class="bx--col-lg-3 bx--col-md-3 bx--col-sm-3">
                        <cv-text-input
                        :label="$t('parcelas.parcel_name')"
                        :value="valueName"
                        :disabled="disabledName"
                        :type="inputTypeName"
                        :placeholder="$t('parcelas.place_name')"
                        :invalid-message="invalidMessageName"
                        ref="inputName"
                        id="input-MIRLwtCq"
                        v-model="valueName"></cv-text-input>
                        <br/>
                        <cv-text-input
                            :label="$t('parcelas.parcel_descrip')"
                            :value="valueDesc"
                            :disabled="disabledDesc"
                            :type="inputTypeDesc"
                            :placeholder="$t('parcelas.place_descrip')"
                            :invalid-message="invalidMessageDesc"
                            ref="inputDesc"
                            id="input-3zcRveTf"
                            v-model="valueDesc"
                        ></cv-text-input>
                        <br />
                        <div class="errorDraw" v-if="verErrorDraw">{{errorDraw}}</div>
                        <br />
                            <cv-button
                                :kind="kindSave"
                                :size="sizeSave"
                                :disabled="disabledSave"
                                @click="actionPrimary"
                                :icon="icon"
                            >
                            {{$t("parcelas.guardar")}}
                            </cv-button>
                        <br/>
                        <br>
                        <div id="geolocIcon" style="">
                            <div v-if="mostrarIconErrGeoloc === ''" @click="cargaLocalizacionActual()">
                                <p style="cursor: pointer; font-size: 14px;">Mostrar mi ubicación <img src="../assets/airport-location.svg" style="width: 14px; height: 14px;"></p>
                            </div>
                            <div v-else-if="mostrarIconErrGeoloc === false" @click="cargaLocalizacionActual()">
                                <p style="cursor: pointer; font-size: 14px;">Para volver a localizar mi ubicación, haz click aquí <Location16 style="stroke: #00abff; width: 14px; height: 14px; fill: #00abff;"/></p>
                            </div>
                            <div v-else-if="mostrarIconErrGeoloc === true" @click="cargaLocalizacionActual()">
                                <p style="cursor: pointer; font-size: 14px;">No temenos acceso a tu ubicación <img src="../assets/location--hazard.svg" style="width: 14px; height: 14px;"></p>
                            </div>
                        </div>
                        <br>
                        <div id="sentinelLayersList">
                            <cv-tabs
                            :container="false"
                            aria-label="navigation tab label">
                                <cv-tab id="tab-1" :label="$t('parcelas.parcel_list')">
                                    <cv-structured-list selectable id="parcelList">
                                        <template slot="items">
                                            <cv-structured-list-item 
                                            v-for="feature in allParcels" 
                                            name="group-1" 
                                            :value="feature.id" 
                                            v-bind:key="feature.id" 
                                            :checked="feature.id == selectedParcelList"
                                            @change="actionChangeParcels"
                                            ref="listaDeParcelas">
                                                <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                                            </cv-structured-list-item>
                                        </template>
                                    </cv-structured-list>
                                </cv-tab>
                                <cv-tab id="tab-2" :label="$t('parcelas.sigpac_pro')" :selected="selected">
                                    <br>
                                    <cv-dropdown 
                                        :placeholder.sync="placeholderComunidad" 
                                        @change="actionChangeComunidades" :label="labelComunidad" ref="comunidadesSelect">
                                            <cv-dropdown-item v-for="comunidad in comunidades" :value="comunidad.properties.codigo" v-bind:key="comunidad.properties.codigo">{{comunidad.properties.nombre}}</cv-dropdown-item>
                                    </cv-dropdown>
                                    <br>
                                    <cv-dropdown 
                                        :placeholder="placeholderProv" 
                                        @change="actionChangeProv" :label="labelProv" :disabled="!visibleProv" ref="provinciasSelect">
                                            <cv-dropdown-item v-for="provincia in provincias" :value="provincia.properties.codigo" v-bind:key="provincia.properties.codigo">{{provincia.properties.nombre}}</cv-dropdown-item>
                                    </cv-dropdown>
                                    <br>
                                    <cv-dropdown 
                                        :placeholder="placeholderMun" 
                                        @change="actionChangeMun" :label="labelMun" :disabled="!visibleMun" ref="munSelect">
                                            <cv-dropdown-item v-for="municipio in municipios" :value="municipio.properties.codigo" v-bind:key="municipio.properties.codigo">{{municipio.properties.nombre}}</cv-dropdown-item>
                                    </cv-dropdown>

                                    <br>
                                    <cv-dropdown 
                                        :placeholder="placeholderAgre" 
                                        @change="actionChangeAgre" :label="labelAgre" :disabled="!visibleAgre" ref="agreSelect">
                                            <cv-dropdown-item v-for="agregado in agregados" :value="agregado" v-bind:key="agregado">{{agregado}}</cv-dropdown-item>
                                    </cv-dropdown>
                                    <br>
                                    <cv-dropdown 
                                        :placeholder="placeholderZona" 
                                        @change="actionChangeZona" :label="labelZona" :disabled="!visibleZona" ref="zonaSelect">
                                            <cv-dropdown-item v-for="zona in zonas" :value="zona" v-bind:key="zona">{{zona}}</cv-dropdown-item>
                                    </cv-dropdown>

                                    <br>
                                    <cv-dropdown 
                                        :placeholder="placeholderPol" 
                                        @change="actionChangePol" :label="labelPol" :disabled="!visiblePol" ref="polSelect">
                                            <cv-dropdown-item v-for="poligono in poligonos" :value="poligono.properties.codigo" v-bind:key="poligono.properties.codigo">{{poligono.properties.nombre}}</cv-dropdown-item>
                                    </cv-dropdown>
                                    <br>
                                    <cv-dropdown 
                                        :placeholder="placeholderPar" 
                                        @change="actionChangePar" :label="labelPar" :disabled="!visiblePar" ref="parSelect">
                                            <cv-dropdown-item v-for="parcela in parcelas" :value="parcela.properties.dn_pk" v-bind:key="parcela.properties.dn_pk">{{parcela.properties.nombre}}</cv-dropdown-item>
                                    </cv-dropdown>
                                    <br>
                                    <cv-dropdown 
                                        :placeholder="placeholderRec" 
                                        @change="actionChangeRec" :label="labelRec" :disabled="!visibleRec" ref="recSelect">
                                            <cv-dropdown-item v-for="recinto in recintos" :value="recinto.properties.dn_pk" v-bind:key="recinto.properties.dn_pk">{{recinto.properties.nombre}}</cv-dropdown-item>
                                    </cv-dropdown>
                                </cv-tab>
                                <cv-tab id="tab-3" :label="$t('parcelas.sigpac_direc')">
                                    <div class="errorDraw" v-if="verErrorBusq">{{$t("parcelas.sigpac_error")}}</div>
                                    <cv-number-input
                                    :label="placeholderProv" v-model="vProv">
                                    </cv-number-input>
                                    <cv-number-input
                                    :label="placeholderMun" v-model="vMun">
                                    </cv-number-input>
                                    <cv-number-input
                                    :label="placeholderAgre" v-model="vAgre">
                                    </cv-number-input>
                                    <cv-number-input
                                    :label="placeholderZona" v-model="vZona">
                                    </cv-number-input>
                                    <cv-number-input
                                    :label="placeholderPol" v-model="vPol">
                                    </cv-number-input>
                                    <cv-number-input
                                    :label="placeholderPar" v-model="vPar">
                                    </cv-number-input>
                                    <cv-number-input
                                    :label="placeholderRec" v-model="vRec">
                                    </cv-number-input>
                                    <cv-button kind="primary" @click="bucardorSigpacDirect">
                                    {{$t("parcelas.buscar")}}
                                    </cv-button>
                                </cv-tab>
                            </cv-tabs>
                                
                        </div>
                    </div>
                    <div class="bx--col-lg  bx--col-md bx--col-sm">
                        
                        <div id="div_map">
                            <vl-map
                                :load-tiles-while-animating="true"
                                :load-tiles-while-interacting="true"
                                data-projection="EPSG:4326"
                                :id="parcel.id"
                                class="mapa"
                                ref="map"
                            >
                                <vl-view :zoom.sync="zoom" :center="center"></vl-view>      
                                <!--Bing MAP -->    
                        <!--Bing MAP -->    
                                <!--Bing MAP -->    
                                <vl-layer-tile id="bingmaps">
                                    <vl-source-bingmaps :api-key="apiKeyBing" :imagery-set="imagerySetBing" :maxZoom="maxZoomBing"></vl-source-bingmaps>
                                </vl-layer-tile>
                                <!--todas las parcelas-->
                                <vl-layer-vector>
                                    <vl-source-vector>
                                        <vl-feature v-for="parcel in allParcels" :value="parcel.id" v-bind:key="parcel.id">
                                            <vl-geom-polygon :coordinates="parcel.geometry.coordinates" :indent="parcel.id" :ref="parcel.id+'parcela'"></vl-geom-polygon>
                                            <vl-style-box>
                                                <vl-style-stroke color="rgba(0, 0, 255, 1)" :width="2"></vl-style-stroke>
                                                <vl-style-fill color="rgba(255,255,255,0.0)"></vl-style-fill>
                                                <vl-style-text :text="parcel.properties.name+'\n'+parcel.properties.area.toFixed(2)+'Ha' +'/'+metricaparcela(parcel.properties.area)+'Acre'" font="14px IBM Plex Sans">
                                                    <vl-style-fill color="white"></vl-style-fill>
                                                    <vl-style-stroke color="black" :width="3"></vl-style-stroke>
                                                </vl-style-text>
                                            </vl-style-box>
                                        </vl-feature>
                                    </vl-source-vector>
                                </vl-layer-vector>
                                <!-- Parcela -->
                                <vl-layer-vector>
                                    <vl-source-vector ident="drawTarget" :features.sync="featuress">
                                        <vl-feature>
                                            <vl-geom-polygon :coordinates="coordenadasParcel" indent="poligono" ref="parcela"></vl-geom-polygon>
                                            <vl-style-box>
                                                <vl-style-stroke :color="colorParcela" :width="3"></vl-style-stroke>
                                                <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
                                                <vl-style-text :text="valueName+'\n'+metric + metricName"></vl-style-text>
                                            </vl-style-box>
                                        </vl-feature>
                                    </vl-source-vector>
                                </vl-layer-vector>
                                <vl-interaction-draw source="drawTarget" type="Polygon" v-if="dibujaPoligono" @drawend="terminado" :key.sync="refreshDibujo" >
                                    
                                </vl-interaction-draw>
                                <vl-interaction-modify source="drawTarget" v-if="ModificaPoligono" @modifyend="editado">
                                    
                                </vl-interaction-modify>
                                <!--<vl-interaction-snap source="drawTarget" :priority="10"></vl-interaction-snap>-->
                                <vl-feature>
                                    <vl-geom-point :coordinates.sync="coordenadasPunto"></vl-geom-point>
                                    <vl-style-box>
                                        <vl-style-icon src="https://d4smartfarming.smartbits-es.com/imgMail/icono-mapa.png"></vl-style-icon>
                                    </vl-style-box>
                                </vl-feature>

                                
                            </vl-map>
                            <div id="div_buscador">
                                <gmap-autocomplete @place_changed="setPlace"  class="form-control bx--text-input" :placeholder="$t('parcelas.ubicacion')" style="width: 100%">
                                </gmap-autocomplete>
                            </div>
                        </div>
                        
                    </div>
                </div>

            </template>

            <template v-if="false" slot="primary-button" v-bind:disabled="true">{{$t("parcelas.guardar")}}</template>

        </cv-modal>
    </div>
</template>
<script>
import axios from "axios";
import proj4 from 'proj4'
import { getArea } from 'ol/sphere';
import {getComunidades,getProvincias,getMunicipios,getAgregados,getZonas,getPoligonos,getParcelas,getRecintos,getDirect} from '@/crudFunctions/crudSigpac'
export default {
    name: "EditarParcel2",
    props: {
        userSeleccionado: String
    },
    data () {
        return{
            erorCompaGeoloc: '',
            mostrarIconErrGeoloc: '',
            metricName: 'Ha',
            //SIGPAC DIRECTO
            vProv: '',
            vMun: '',
            vAgre: '',
            vZona: '',
            vPol: '',
            vPar: '',
            vRec: '',
            verErrorBusq: false,
            //SIGPPAC CONFIGURATION
            placeholderComunidad: this.$t('parcelas.comunidad'),
            labelComunidad: this.$t('parcelas.comunidad_sel'),
            comunidades: Array,
            
            visibleProv: false,
            placeholderProv: this.$t('parcelas.provincia'),
            labelProv: this.$t('parcelas.provincia_sel'),
            provincias: Array,
            provinciaSel: 0,

            visibleMun: false,
            placeholderMun: this.$t('parcelas.municipio'),
            labelMun: this.$t('parcelas.municipio_sel'),
            municipios: Array,
            municipioSel: 0,

            visibleAgre: false,
            placeholderAgre: this.$t('parcelas.agregado'),
            labelAgre: this.$t('parcelas.agregado_sel'),
            agregados: Array,
            agregadoSel: 0,

            visibleZona: false,
            placeholderZona: this.$t('parcelas.zona'),
            labelZona: this.$t('parcelas.zona_sel'),
            zonas: Array,
            zonaSel: 0,

            visiblePol: false,
            placeholderPol: this.$t('parcelas.poligono'),
            labelPol: this.$t('parcelas.poligono_sel'),
            poligonos: Array,
            poligonoSel: 0,

            visiblePar: false,
            placeholderPar: this.$t('parcelas.parcela'),
            labelPar: this.$t('parcelas.parcela_sel'),
            parcelas: Array,
            parcelaSel: 0,

            visibleRec: false,
            placeholderRec: this.$t('parcelas.recinto'),
            labelRec: this.$t('parcelas.recinto_sel'),
            recintos: Array,
            recintoSel: 0,

            //
            selectedParcelList: 0,
            colorParcela: 'green',
            //BTN GUARDADO
            kindSave: "primary",
            sizeSave: "",
            disabledSave: false,    
            featuress: [],
            title_card: "",
            subtitle_card: "",
            closeAriaLabel: "Close",
            use_label: true,
            use_title: true,
            use_content: true,
            size: 'lg',
            use_primaryButton: true,
            primaryButtonDisabled: false,
            autoHideOff: true,
            //input-name
            labelName: this.$t('parcelas.parcel_name'),
            valueName: '',
            disabledName: false,
            inputTypeName: 'text',
            placeholderName: this.$t('parcelas.place_name'),
            invalidMessageName: '',
            
            //input-email
            labelDesc: this.$t('parcelas.parcel_descrip'),
            valueDesc: '',
            disabledDesc: false,
            inputTypeDesc: 'text',
            placeholderDesc: this.$t('parcelas.place_descrip'),
            invalidMessageDesc: '',
            //BingMap Config
            apiKeyBing: this.$apiKeyBing,
            imagerySetBing: `AerialWithLabels`,
            maxZoomBing: 20,
            zoom: 15,
            center:  [0 , 0],
            coordinates: [0 , 0],
            coordenadasParcel: [ [ [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ] ] ],
            parcel: Array(),
            dibujaPoligono: false,
            //GUARDADO DE DATOS
            area: 0,
            poligonObjecto: '',
            verErrorDraw: false,
            coordinatesPoligono: [],
            allFeatures: Array(),
            allParcels: Array(),
            refreshDibujo: 0,
            ModificaPoligono: true,
            ErrorDraw: '',
            coordenadasPunto: [0, 0],
        }
    },
    methods: {
        cerrarModal(){
            const titulo = document.querySelectorAll('[aria-label="Editar Parcela "]');
            titulo[0].addEventListener('mouseenter', () => {
                console.log("Acabo de entrar");
                this.autoHideOff = false;
            });
            titulo[0].addEventListener('mouseleave', () => {
                console.log("Acabo de salir");
                this.autoHideOff = true;
            });

        },
        metricaparcela(area){
            const onehecttoAcre = 2.4710538146717
            const acre = onehecttoAcre * area
            this.metric = "Acre"
            return  acre.toFixed(2)
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
                this.center = [pos.coords.longitude, pos.coords.latitude]
            }, err => {
                this.mostrarIconErrGeoloc = true
                console.info('Localización no autorizada', err)
            })
        },
        getEnterprise(){
            if(this.$route.query.enterprise){
                    const path = `${this.$apiURL}/enterprises/${this.$route.query.enterprise}/?size=1000000000&page=1`;
                    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                    axios
                        .get(path)
                        .then(response => {
                            this.enterprise = response.data
                            this.metric = this.enterprise.type_metric;
                            this.actionShownMap();
                        })
                        .catch(error => {
                            console.warn(error);
                        });
            }
        },
        bucardorSigpacDirect(){
            const arrSel = [this.vProv, this.vMun, this.vAgre, this.vZona, this.vPol, this.vPar, this.vRec]
            const arrURI = ['provinciabox', 'municipiobox', 'agregadobox', 'zonabox', 'poligonobox', 'parcelabox', 'recintobox']
            let cont = -1
            console.info(arrSel)
            let uriParams = ``
            arrSel.map(value=>{
                if(value){
                    cont ++
                    uriParams += `/${value}`
                }
            })
            if(uriParams == '')
                return false
            let dato=arrURI[cont]+uriParams
            getDirect(dato)
            .then(response => {
                const lat = (response.data.data.features[0].properties.x1 + response.data.data.features[0].properties.x2) / 2
                const long = (response.data.data.features[0].properties.y1 + response.data.data.features[0].properties.y2) / 2
                this.coordenadasPunto = [lat, long] 
                this.center = [lat, long]
                this.zoom = 18
                this.verErrorBusq = false
            })
            .catch(() => {
                this.verErrorBusq = true
            })
        },
        cargarComunidades(){
            console.log('Cargando comunidades')
            getComunidades()
            .then(response=>{
                this.comunidades=response.data.data.features
            })
            .catch(error => {
                console.warn(error.response)
            })
        },
        actionChangeComunidades(comunidad){
            getProvincias(comunidad)
            .then(response=>{
                this.placeholderComunidad = comunidad
                const comunidadSelec = comunidad
                this.comunidades.forEach(comunidad => {
                    if(comunidad.properties.codigo == comunidadSelec){
                        this.placeholderComunidad = comunidad.properties.nombre
                    }
                })
                this.provincias = response.data.data.features
                this.visibleProv = true
            })
            .catch(error => {
                console.warn(error.response)
            })

        },
        actionChangeProv(provincia){
            getMunicipios(provincia)
            .then(response => {
                this.provinciaSel = provincia
                
                this.placeholderProv = provincia
                this.provincias.forEach(provincia => {
                    if(provincia.properties.codigo == this.provinciaSel){
                        this.placeholderProv = provincia.properties.nombre
                    }
                })
                this.municipios = response.data.data.features
                this.visibleMun = true
            })
            .catch(error => {
                console.warn(error.response)
            })

        },
        actionChangeMun(municipio){
            getAgregados(this.provinciaSel,municipio)
            .then(response => {
                this.placeholderMun = municipio
                let unique = [...new Set(response.data.data.features.map(x => x.properties.codigo))]; 
                this.agregados = unique
                this.visibleAgre = true
                this.municipioSel = municipio
                this.placeholderMun = municipio
                this.municipios.forEach(municipio => {
                    if(municipio.properties.codigo == this.municipioSel){
                        this.placeholderMun = municipio.properties.nombre
                    }
                })
                if(this.agregados.length == 1){
                    this.actionChangeAgre(this.agregados[0])
                    this.placeholderAgre = this.agregados[0]
                }
            })
            .catch(error => {
                console.warn(error)
            })

        },
        actionChangeAgre(agregado){
            getZonas(this.provinciaSel,this.municipioSel,agregado)
            .then(response => {
                this.placeholderAgre = agregado
                let unique = [...new Set(response.data.data.features.map(x => x.properties.codigo))]; 
                this.zonas = unique
                this.visibleZona = true
                this.agregadoSel = agregado 
                if(this.agregados.length == 1){
                    this.actionChangeZona(this.agregados[0])
                    this.placeholderAgre = this.agregados[0]
                }
                
            })
            .catch(error => {
                console.warn(error)
            })

        },
        actionChangeZona(zona){
            getPoligonos(this.provinciaSel,this.municipioSel,this.agregadoSel,zona)
            .then(response => {
                this.zonaSel = zona
                this.placeholderZona = zona
                this.poligonos = response.data.data.features
                this.visiblePol = true
            })
            .catch(error => {
                console.warn(error.response)
            })

        },
        actionChangePol(poligono){
            getParcelas(this.provinciaSel,this.municipioSel,this.agregadoSel,this.zonaSel,poligono)
            .then(response => {
                this.poligonoSel = poligono
                this.placeholderPol = poligono
                this.parcelas = response.data.data.features
                this.visiblePar = true
            })
            .catch(error => {
                console.warn(error.response)
            })

        },
        actionChangePar(parcela){
            let parcelaCOD = 0
            this.parcelas.forEach(parcelaMap =>{
                if(parcelaMap.properties.dn_pk == parcela){
                    parcelaCOD = parcelaMap.properties.codigo
                }
            })
            getRecintos(this.provinciaSel,this.municipioSel,this.agregadoSel,this.zonaSel,this.poligonoSel,parcelaCOD)
            .then(response => {
                this.parcelaSel = parcela
                this.placeholderPar = parcelaCOD
                this.recintos = response.data.data.features
                this.visibleRec = true
            })
            .catch(error => {
                console.warn(error.response)
            })

        },

        actionChangeRec(recintoSell){
            this.recintos.forEach(recinto => {
                if(recinto.properties.dn_pk == recintoSell){
                    const lat = (recinto.properties.x1 + recinto.properties.x2) / 2
                    const long = (recinto.properties.y1 + recinto.properties.y2) / 2
                    this.coordenadasPunto = [lat, long] 
                    this.center = [lat, long]
                    this.zoom = 18
                }
            })
        },
        setPlace(place){
            this.center = [place.geometry.location.lng(), place.geometry.location.lat()]
            this.zoom = 15
        },
        openModal(userSelec) {
            this.$refs.editarRolForm.show();
            this.verErrorDraw = false
            this.invalidMessageName = ""
            this.showPassword = false
            this.title_card = this.$t('parcelas.parcel_edit')
            this.subtitle_card = this.$t('parcelas.parcel_edit')
            this.userSeleccionado = userSelec;
            this.getEnterprise();
            this.actionShownMap();
                
        },
        terminado(p){
            this.dibujaPoligono = false
            this.area = (Math.round((getArea(p.feature.getGeometry())/ 10000) * 10000) / 10000)
            this.coordinatesBuenas(p.feature.getGeometry().getCoordinates())
            this.verErrorDraw = false
        },
        editado(p){
            this.coordinatesEditadas = p.features.array_[0].getGeometry().getCoordinates()
            this.area = (Math.round((getArea(p.features.array_[0].getGeometry()) / 10000) * 10000) / 10000)
            if(this.userSeleccionado){
                this.coordinatesBuenas(this.coordinatesEditadas)
            }
            
            this.verErrorDraw = false
        },
        coordinatesBuenas(ArrayCoor){
            if(this.userSeleccionado){
                this.ModificaPoligono = true
            }else{
                this.ModificaPoligono = false
            }
            
            var source = new proj4.Proj('EPSG:3785'); 
            var dest = new proj4.Proj('EPSG:4326'); 
            let newCenter = Array;
            let polygonObject= 'POLYGON(('
            for (var i = 0; i < ArrayCoor[0].length; i++) {
                newCenter = proj4(source, dest, [ArrayCoor[0][i][0], ArrayCoor[0][i][1]])
                this.coordinatesPoligono.push([newCenter[0] , newCenter[1]])
                polygonObject += newCenter[0]+' '+newCenter[1]
                if(i != (ArrayCoor[0].length-1)){
                    polygonObject += ', '
                }
            }
            polygonObject += '))';
            this.poligonObjecto = polygonObject
            
            let path = `${this.$apiURL}/parcel_filter/?enterprise_id=${this.$route.query.enterprise}&polygon=${polygonObject}`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                if(response.data.features.length){
                    this.errorDraw = ''
                    this.verErrorDraw = false
                    response.data.features.forEach(parcela =>{
                        if(this.userSeleccionado != parcela.id){
                            this.errorDraw += `"${parcela.properties.name}"  `
                            if(!this.userSeleccionado){
                                this.featuress = []
                                this.dibujaPoligono = true
                            }
                        }
                    })
                    if(this.errorDraw){
                        this.verErrorDraw = true
                        this.disabledSave = true
                        this.errorDraw = `${this.$t('parcelas.parcela_solapada_con')}   ${this.errorDraw}`
                        this.colorParcela = 'red'
                    }else{
                        this.compruebaParcelaSimple(polygonObject)
                    }
                }else{
                    this.compruebaParcelaSimple(polygonObject)
                }
            })
            .catch(error =>{ 
                console.info(error.data)
            })
        },
        compruebaParcelaSimple(polygonObject){
            let path = `${this.$apiURL}/parcel_valid/?polygon=${polygonObject}`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response=>{
                if(response.data == "False"){
                    this.verErrorDraw = true
                    this.disabledSave = true
                    this.errorDraw = `${this.$t('parcelas.parcela_solapada_si')}`
                    this.colorParcela = 'red'
                    if(!this.userSeleccionado){
                        this.featuress = []
                        this.dibujaPoligono = true
                    }
                }else{
                    this.verErrorDraw = false
                    this.disabledSave = false
                    this.colorParcela = 'green'
                    this.disabledSave = false
                    this.compruebaLimites()
                }
            })
            .catch(error => {
                console.warn(error)
            })
        },
        compruebaLimites(){
            let path = `${this.$apiURL}/enterprises_except/${this.$route.query.enterprise}/?parcel=${this.userSeleccionado}`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                const porcentaje_ant = (parseFloat(this.$parent.total_hectares_enterprise) / parseFloat(response.data.hectares_available)  * 100)
                const porcentaje_now = ((parseFloat(response.data.parcels.area__sum)+parseFloat(this.area)) / parseFloat(response.data.hectares_available) * 100)
                if(parseFloat(porcentaje_ant) < parseFloat(porcentaje_now)){
                    if(porcentaje_now > 100.00){
                        this.verErrorDraw = true
                        this.disabledSave = true
                        this.errorDraw = `${this.$t('parcelas.parcela_limite_area')}`
                        this.colorParcela = 'red'
                        if(!this.userSeleccionado){
                            this.featuress = []
                            this.dibujaPoligono = true
                        }
                    }else{
                        this.verErrorDraw = false
                        this.disabledSave = false
                        this.colorParcela = 'green'
                        this.disabledSave = false
                    }
                }else{
                    this.verErrorDraw = false
                    this.disabledSave = false
                    this.colorParcela = 'green'
                    this.disabledSave = false
                }
            })
        },
        actionPrimary(){
            if(!this.verErrorDraw){
                let path = ''
                
                if(this.userSeleccionado){
                    if(!this.poligonObjecto){
                        this.coordinatesBuenas(this.$refs['parcela'].$geometry.getCoordinates())
                    }
                    path = `${this.$apiURL}/parcels/${this.userSeleccionado}/`;
                    axios
                    .put(path, {
                        name: this.$refs.inputName.$refs.input.value,
                        description: this.$refs.inputDesc.$refs.input.value,
                        polygon: this.poligonObjecto,
                        area: this.area,
                        enterprise: (this.$route.query.enterprise) ? this.$route.query.enterprise : sessionStorage.getItem('enterprise'),
                        user_updated: sessionStorage.getItem('user')
                    })
                    .then(response => {
                        this.compruebaParcelas(response.data.id);
                    })
                    .catch(error => {
                        console.info(error);
                    
                    });
                }else{
                    path = `${this.$apiURL}/parcels/`;
                    axios
                    .post(path, {
                        name: this.$refs.inputName.$refs.input.value,
                        description: this.$refs.inputDesc.$refs.input.value,
                        polygon: this.poligonObjecto,
                        area: this.area,
                        enterprise: (this.$route.query.enterprise) ? this.$route.query.enterprise : sessionStorage.getItem('enterprise'),
                        user_created: sessionStorage.getItem('user')
                    })
                    .then(response => {
                        this.compruebaParcelas(response.data.id);
                    })
                    .catch(error => {
                        if (error.response.data.name)
                            this.invalidMessageName = error.response.data.name[0];
                        if (error.response.data.polygon)
                            this.verErrorDraw = true
                            this.errorDraw = this.$t('parcelas.parcela_limite')
                        
                    });   
                }
            }
            
        },
        compruebaParcelas(parcelaid){    
            let path = `${this.$apiURL}/enterprises/${this.$route.query.enterprise}/`;
            var allCoordinates = Array();
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                
                response.data.parcels.features.forEach(element => {
                    allCoordinates.push(element.geometry.coordinates)
                });
            
                console.info(this.coordinatesPoligono, parcelaid)      
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
                        'name': `${this.$route.query.enterprise}`,
                        "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                        "additionalData": {
                            "showLogo": false,
                            "showWarnings": false,
                            "imageQuality": 90,
                            "disabled": false
                        },
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
                instanceIns.put("/configuration/v1/wms/instances/"+sessionStorage.getItem('sI'), bodyIns, configIns).then((resp) => {
                    console.info(`respuesta sentinel`, resp)
                    if(resp.status == 200 || resp.statusText == 'OK'){
                        this.$parent.getUsers();
                        this.$refs.editarRolForm.hide();
                        this.$parent.componentKey += 1;
                        this.coordenadasParcel = ''
                        this.$parent.mensajeAlerta = this.$t('parcelas.parcela_guardada')
                        this.$parent.tipoAlerta = 'success'
                        this.$parent.$refs.alertaGeneral.verAlerta()
                    }else{
                        this.$parent.getUsers();
                        this.$refs.editarRolForm.hide();
                        this.$parent.componentKey += 1;
                        this.coordenadasParcel = ''
                        this.$parent.mensajeAlerta = this.$t('parcelas.parcel_guardada_error_sent')
                        this.$parent.tipoAlerta = 'error'
                        this.$parent.$refs.alertaGeneral.verAlerta()
                    }
                    
                }).catch(error => {
                    console.info(`error`, error)
                    this.$parent.getUsers();
                    this.$refs.editarRolForm.hide();
                    this.$parent.componentKey += 1;
                    this.coordenadasParcel = ''
                    this.$parent.mensajeAlerta = this.$t('parcelas.parcel_guardada_error_sent')
                    this.$parent.tipoAlerta = 'error'
                    this.$parent.$refs.alertaGeneral.verAlerta()
                })
                
                
            })
        },
        actionShown(){
            this.coordenadasParcel = ''
            this.$parent.componentKey += 1;
        },        
        actionShownMap(){
            //Si el usuario seleccionado esta vacio 
            let path = `${this.$apiURL}/parcels/${this.userSeleccionado}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                    
                    this.parcel = response.data
                    this.valueName = response.data.properties.name;
                    this.valueDesc = response.data.properties.description;
                    this.geometry = response.data;
                    this.area = response.data.properties.area;
                    this.coordenadasParcel = this.geometry.geometry.coordinates
                    let coordenadasGeometricas = ''
                    coordenadasGeometricas = this.$refs['parcela'].$geometry.extent_
                    const ex = coordenadasGeometricas[0] + (coordenadasGeometricas[2]-coordenadasGeometricas[0])/2;
                    const ye = coordenadasGeometricas[1] + (coordenadasGeometricas[3]-coordenadasGeometricas[1])/2;
                    var source = new proj4.Proj('EPSG:3785'); 
                    var dest = new proj4.Proj('EPSG:4326');  
                    const newCenter = proj4(source, dest, [ex, ye])
                    this.center = [newCenter[0], newCenter[1]]
                    this.zoom = 15
                    this.dibujaPoligono = false
                    console.info(response.data)
                    
                    //this.metric= this.metricaparcela(response.data.properties);
                })
                .catch( error => {
                    console.info('entra')
                    this.cargarComunidades()
                    console.warn(error)
                    this.disabledSave = true
                    this.showPassword = true
                    this.title_card = this.$t('parcelas.parcel_nueva')
                    this.subtitle_card = this.$t('parcelas.parcel_nueva')
                    this.valueName = '';
                    this.valueDesc = '';
                    this.coordenadasParcel = [0,0]
                    this.center = [0, 0]
                    this.zoom = 4
                    this.dibujaPoligono = true
                });
                
            path = `${this.$apiURL}/parcel_enterprise/${this.$route.query.enterprise}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.allParcels=response.data.features
                if(!this.userSeleccionado){
                    const lastItem = this.allParcels[this.allParcels.length - 1]
                    this.selectedParcelList = lastItem.id
                    setTimeout(() => {
                        this.actionChangeParcels(this.selectedParcelList)
                    }, 1000);
                    
                }else{
                    this.selectedParcelList = this.userSeleccionado
                }
            })
        
        
        },
        actionChangeParcels(valor){
            const coordenadasGeometricas = this.$refs[valor+'parcela'][0].$geometry.extent_
            const ex = coordenadasGeometricas[0] + (coordenadasGeometricas[2]-coordenadasGeometricas[0])/2;
            const ye = coordenadasGeometricas[1] + (coordenadasGeometricas[3]-coordenadasGeometricas[1])/2;
            var source = new proj4.Proj('EPSG:3785'); 
            var dest = new proj4.Proj('EPSG:4326');  
            const newCenter = proj4(source, dest, [ex, ye])
            this.center = [newCenter[0], newCenter[1]]
            this.zoom = 16
        },
        
        
    },
    mounted(){
        console.log('MOUNTED')
        const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path_lang)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
        this.$refs.comunidadesSelect.$el.firstChild.style.display = 'flex'
        this.$refs.provinciasSelect.$el.firstChild.style.display = 'flex'
        this.$refs.munSelect.$el.firstChild.style.display = 'flex'
        this.$refs.agreSelect.$el.firstChild.style.display = 'flex'
        this.$refs.zonaSelect.$el.firstChild.style.display = 'flex'
        this.$refs.polSelect.$el.firstChild.style.display = 'flex'
        this.$refs.parSelect.$el.firstChild.style.display = 'flex'
        this.$refs.recSelect.$el.firstChild.style.display = 'flex'

        this.$refs.editarRolForm.$el.firstChild.style.width = '98%'
        this.$refs.editarRolForm.$el.firstChild.style.height = '95%'
        this.$refs.editarRolForm.$el.firstChild.style["max-width"] = '100%'
        this.$refs.editarRolForm.$el.firstChild.style["max-height"] = '100%'

        this.$refs.editarRolForm.$el.firstChild.childNodes[2].style["padding-right"] = '1%'
        this.$refs.editarRolForm.$el.firstChild.childNodes[2].style["margin-bottom"] = '1%'
        this.$refs.editarRolForm.$el.firstChild.childNodes[2].style["height"] = '95%'
        this.cargarComunidades()
    },
    created(){
        var estilo = document.createElement('style');
        document.head.appendChild(estilo);
        var hojaEstilo = estilo.sheet;
        hojaEstilo.insertRule('.bx--modal-container--lg { width: 96% !important; height:95% !important; max-height: 100%; max-width: 100% }', 0);
    },
    beforeCreate(){
        this.cerrarModal()
    }
    
}
</script>
<style scoped>
    #div_buscador{
        width: 50vw;
        position: fixed;
        padding: 10px;
        margin-top: 4px;
        margin-left: 40px;
        top: 79px;

    }
    .bx--modal-container{
        width: 98%;
        height: 95%;
        max-height: 100%;
    }
    .errorDraw{
        color: #da1e28;
        font-weight: 400;
        font-size: 12px;
    }
    #row_box, #row_box >div{
        height: 100%;
    }
    #div_map{
        height: 100%;
        
    }
    .mapa{
        height: 100% !important;
        color: white;
    }
    #sentinelLayersList{
        overflow: scroll;
        height: 540px;
    }
    .pac-container{
        z-index: 10000!important;
    }
    @media (min-width: 42rem){
        .bx--modal-container--lg {
    width: 96% !important;
}
    }

</style>
