<template>
    <div>
        <vl-map
            :load-tiles-while-animating="false"
            :load-tiles-while-interacting="false"
            data-projection="EPSG:4326"
            style="height: 400px"
            id="map"
            class="mapa"
            ref="map"
            :key="keyComponentMap"
        >
            <vl-view :zoom.sync="zoom" :center.sync="center"></vl-view>    
            <!--Bing MAP @moveend="moveend"-->    
            <vl-layer-tile id="bingmaps">
                <vl-source-bingmaps :api-key="apiKeyBing" :imagery-set="imagerySetBing" :maxZoom="maxZoomBing"></vl-source-bingmaps>
            </vl-layer-tile>
            <!--Sentinel Layers -->
            
            <!-- parcelas
            <div v-for="parcel in allParcels" :value="parcel.id" v-bind:key="parcel.id">
                <vl-layer-vector >
                    <vl-source-vector :ident="parcel.id" >
                        <vl-feature>
                            <vl-geom-polygon :coordinates="parcel.geometry.coordinates" :indent="parcel.id" :ref="parcel.id+'parcela'">
                                
                            </vl-geom-polygon>
                            <vl-style-box>

                                <vl-style-stroke color="rgba(0, 0, 255, 1)" :width="2"></vl-style-stroke>
                                <vl-style-fill color="rgba(255,255,255,0.0)"></vl-style-fill>
                                <vl-style-text :text="parcel.properties.name+'\n'+parcel.properties.area" font="14px IBM Plex Sans">
                                    <vl-style-fill color="white"></vl-style-fill>
                                    <vl-style-stroke color="black" :width="3"></vl-style-stroke>
                                </vl-style-text>
                            </vl-style-box>
                        </vl-feature>
                    </vl-source-vector>
                </vl-layer-vector>
                
                <vl-interaction-select :source="parcel.id" @select="selecionaPolygon"></vl-interaction-select>
                
            </div>
            -->
            <!--
            <vl-layer-image id="wmts" :opacity="opacitylayer" :key="componentKey" >
                <vl-source-image-wms
                :url.sync="urlSent"
                :urlProcessingApi.sync="urlSent"
                :maxcc="maxcc"
                :minZoom="minZoom"
                :maxZoom="maxZoom"
                :preset="preset"
                :layers="SentinelLayer"
                :time="time"
                :serverType="serverType"
                :opacity="opacitylayer"
                :transition='transition'
                RESOLUTION=1
                QUALITY=1
                PRIORITY="mostRecent"
                >
                </vl-source-image-wms>
            </vl-layer-image>
            -->
            
            <vl-layer-tile id="wmts" :opacity="opacitylayer" :key="componentKey" v-if="verLayerTile && empresaSelect !== 'all' && mostarListaParcelsCoops == false">
                <vl-source-wms
                    :url="urlSent+'/?MAXCC=100&'"
                    :urlProcessingApi="urlSent"
                    :MAXCC="maxcc"
                    :minZoom="minZoom"
                    :maxZoom="maxZoom"
                    :preset="preset"
                    :layers="SentinelLayer"
                    :time.sync="time"
                    :serverType="serverType"
                    :opacity="opacitylayer"
                    :transition='transition'
                    RESOLUTION=1
                    QUALITY=1
                    ref="wmsSource"
                    v-if="verLayerTile"
                >
                </vl-source-wms>
            </vl-layer-tile>
            <vl-layer-tile :id="'wmts_'+enterprisee.id" :opacity="opacitylayer" v-bind:key="enterprisee.id" v-for="enterprisee in enterprisesList" v-else-if="empresaSelect == 'all' && mostarListaParcelsCoops == false">
                <vl-source-wms
                    :url="'https://services.sentinel-hub.com/ogc/wms/'+enterprisee.sentinel_instance+'/?MAXCC=100&'"
                    :urlProcessingApi="'https://services.sentinel-hub.com/ogc/wms/'+enterprisee.sentinel_instance+'/?MAXCC=100&'"
                    :maxcc="maxcc"
                    :minZoom="minZoom"
                    :maxZoom="maxZoom"
                    :preset="preset"
                    :layers="SentinelLayer"
                    :time.sync="time"
                    :serverType="serverType"
                    :opacity="opacitylayer"
                    :transition='transition'
                    RESOLUTION=1
                    QUALITY=1
                    :ref="'wmsSource_'+enterprisee.id"
                >
                </vl-source-wms>
            </vl-layer-tile>

            <vl-layer-tile :id="'wmts_'+enterprisee.id" :opacity="opacitylayer" v-bind:key="enterprisee.id" v-for="enterprisee in cooperativeSelectObj.enterprises" v-else-if="mostarListaParcelsCoops == true">
                <vl-source-wms
                    :url="'https://services.sentinel-hub.com/ogc/wms/'+enterprisee.sentinel_instance+'/?MAXCC=100&'"
                    :urlProcessingApi="'https://services.sentinel-hub.com/ogc/wms/'+enterprisee.sentinel_instance+'/?MAXCC=100&'"
                    :maxcc="maxcc"
                    :minZoom="minZoom"
                    :maxZoom="maxZoom"
                    :preset="preset"
                    :layers="SentinelLayer"
                    :time.sync="time"
                    :serverType="serverType"
                    :opacity="opacitylayer"
                    :transition='transition'
                    RESOLUTION=1
                    QUALITY=1
                    :ref="'wmsSource_'+enterprisee.id"
                >
                </vl-source-wms>
            </vl-layer-tile>
            
            
            <!--
            <vl-layer-vector>
                <vl-source-vector>
                    <vl-feature v-for="parcel in allParcels" :value="parcel.id" v-bind:key="parcel.id">
                        <vl-geom-polygon :coordinates="parcel.geometry.coordinates" :indent="parcel.id" :ref="parcel.id+'parcela'"></vl-geom-polygon>
                        <vl-style-box>
                            <vl-style-stroke color="rgba(0, 0, 255, 1)" :width="2"></vl-style-stroke>
                            <vl-style-fill color="rgba(255,255,255,0.0)"></vl-style-fill>
                            <vl-style-text :text="parcel.properties.name+'\n'+parcel.properties.area + ' hm2'" font="14px IBM Plex Sans">
                                <vl-style-fill color="white"></vl-style-fill>
                                <vl-style-stroke color="black" :width="3"></vl-style-stroke>
                            </vl-style-text>
                        </vl-style-box>
                    </vl-feature>
                </vl-source-vector>
            </vl-layer-vector>
            <vl-interaction-select @select="selecionaPolygon"></vl-interaction-select>
            -->
            <vl-layer-vector :key="componentKey" v-if="empresaSelect != 'all' && mostarListaParcelsCoops == false" :declutter="false">
                <vl-source-vector ident="drawTarget" >
                    <vl-feature v-for="parcel in enterprise.parcels.features" :value="parcel.id" v-bind:key="parcel.id">
                        <vl-geom-polygon :coordinates="parcel.geometry.coordinates" :indent="parcel.id" :name="parcel.properties.name" :id="parcel.id" :ref="parcel.id+'parcela'"></vl-geom-polygon>
                        <vl-style-box>
                            <vl-style-stroke color="rgba(0, 0, 255, 1)"></vl-style-stroke>
                            <vl-style-fill color="rgba(255,255,255,0.0)"></vl-style-fill>
                            <vl-style-text :overflow="checkedToggleMostarTexto" textAlign="center" :text="parcel.properties.name +(parcel.properties.description ? '\n'+parcel.properties.description: '')+'\n'+ ( parcel.properties.area.toFixed(2) ? parcel.properties.area.toFixed(2) : '') + ' ' +metric" font="14px IBM Plex Sans">
                                <vl-style-fill color="white"></vl-style-fill>
                                <vl-style-stroke color="black" :width="3"></vl-style-stroke>
                            </vl-style-text>
                        </vl-style-box>
                    </vl-feature>
                </vl-source-vector>
            </vl-layer-vector>

            <vl-layer-vector :id="enterprisee.id" :key="enterprisee.id" v-else-if="empresaSelect == 'all' && mostarListaParcelsCoops == false" v-for="enterprisee in enterprisesList">
                <vl-source-vector>
                    <vl-feature v-for="parcel in enterprisee.parcels.features" v-bind:key="parcel.id" :id="parcel.id" :properties="parcel.properties" :ref="parcel.id+'parcela'">
                        <vl-geom-polygon :coordinates="parcel.geometry.coordinates"></vl-geom-polygon>
                        <vl-style-box>
                            <vl-style-stroke color="rgba(0, 0, 255, 1)" :width="2"></vl-style-stroke>
                            <vl-style-fill color="rgba(255,255,255,0.0)"></vl-style-fill>
                            <vl-style-text :overflow="checkedToggleMostarTexto" :text="parcel.properties.name +(parcel.properties.description ? '\n'+parcel.properties.description: '')+'\n'+ parcel.properties.area.toFixed(2) + ' ' +metric" font="14px IBM Plex Sans">
                                <vl-style-fill color="white"></vl-style-fill>
                                <vl-style-stroke color="black" :width="3"></vl-style-stroke>
                            </vl-style-text>
                        </vl-style-box>
                    </vl-feature>
                </vl-source-vector>
            </vl-layer-vector>

            <vl-layer-vector :id="enterprisee.id" :key="enterprisee.id" v-else-if="mostarListaParcelsCoops == true" v-for="enterprisee in cooperativeSelectObj.enterprises">
                <vl-source-vector>
                    <vl-feature v-for="parcel in enterprisee.parcels.features" v-bind:key="parcel.id" :id="parcel.id" :properties="parcel.properties" :ref="parcel.id+'parcela'">
                        <vl-geom-polygon :coordinates="parcel.geometry.coordinates"></vl-geom-polygon>
                        <vl-style-box>
                            <vl-style-stroke color="rgba(0, 0, 255, 1)" :width="2"></vl-style-stroke>
                            <vl-style-fill color="rgba(255,255,255,0.0)"></vl-style-fill>
                            <vl-style-text :overflow="checkedToggleMostarTexto" :text="parcel.properties.name +(parcel.properties.description ? '\n'+parcel.properties.description: '')+'\n'+ parcel.properties.area.toFixed(2) + ' ' +metric" font="14px IBM Plex Sans">
                                <vl-style-fill color="white"></vl-style-fill>
                                <vl-style-stroke color="black" :width="3"></vl-style-stroke>
                            </vl-style-text>
                        </vl-style-box>
                    </vl-feature>
                </vl-source-vector>
            </vl-layer-vector>

            <vl-interaction-select @select="selecionaPolygon" v-if="verSeleccionaPolygon && empresaSelect != 'all' && mostarListaParcelsCoops == false" ident="modify-target" :key="keyModificar"></vl-interaction-select>
            <vl-interaction-modify v-if="$parent.$parent.is_superuser || $parent.$parent.is_systemadmin || $parent.$parent.is_enterpriseadmin && empresaSelect != 'all'" source="modify-target" @modifyend="editado" :key="keyModificar"></vl-interaction-modify>
            <!--Parcela-->
            
            <vl-layer-vector z-index="1">
            <vl-source-vector :features.sync="featuresss" ident="the-source"></vl-source-vector>
                <vl-style-box>
                    <vl-style-stroke color="green"></vl-style-stroke>
                    <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
                </vl-style-box>
            </vl-layer-vector>

            <vl-interaction-draw type="Polygon" source="the-source" v-if="dibujaPoligono && !isMobile()" @drawend="terminado" :key.sync="refreshDibujo"></vl-interaction-draw>

        </vl-map>
        <div id="layersControler" class="layersControler" v-if="!isMobile()">
            <cv-loading
            :small="true"
            :active="isActiveLoading"
            :overlay="true" v-if="isVisibleLoad"></cv-loading>
            <!--
            <div id="geolocIcon" style="text-align: right;">
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
            -->
            <div v-if="mostrarListaCooperativas" id="sentinelLayers">
                <cv-select
                    theme=""
                    label="Listado de Cooperativas"
                    :hide-label="false"
                    :inline="false"
                    :disabled="false"
                    @change="seleccionaCoop">
                    <cv-select-option disabled selected hidden>Selecciona una Cooperativa</cv-select-option>
                    <cv-select-option v-for="empresa in cooperativesList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                        {{empresa.name}}
                    </cv-select-option>
                </cv-select>
            </div>
            <div v-if="mostrarListaEmpresas" id="sentinelLayers">
                <cv-select
                    theme=""
                    :label="$t('map.listado_empresas')"
                    :hide-label="false"
                    :inline="false"
                    :disabled="false"
                    @change="seleccionaEmpresa">
                    <cv-select-option disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                    <cv-select-option v-for="empresa in enterprisesList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                        {{empresa.name}}
                    </cv-select-option>
                </cv-select>
            </div>
            <div v-if="mostrarListaEmpresasCoop" id="sentinelLayers">
                <cv-select
                    theme=""
                    :label="$t('map.listado_empresas')"
                    :hide-label="false"
                    :inline="false"
                    :disabled="false"
                    @change="seleccionaEmpresa">
                    <cv-select-option disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                    <cv-select-option :value="String('all')">{{$t("map.most_todas_empresas")}}</cv-select-option>
                    <cv-select-option v-for="empresa in enterprisesList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                        {{empresa.name}}
                    </cv-select-option>
                </cv-select>
            </div>
            <div>
                <p>{{$t("map.listado_parcelas")}} <span><ChevronSortDown20  @click="onclickTile2" v-if="expand2"/></span><span><ChevronSortUp20 @click="onclickTile2" v-if="!expand2" style="transform: translate(0px, 10px)"/></span></p>
            </div>
            <div id="sentinelLayersList" ref="sentinelLayersListCollapse" v-if="empresaSelect !== 'all' && mostarListaParcelsCoops == false">
                <cv-search :placeholder="`Buscar`" @input="onBuscar"></cv-search>
                <cv-structured-list selectable id="parcelList" >
                    <template slot="headings">
                        <cv-structured-list-heading>{{$t("map.parcelas_de")}} {{enterprise.name}}</cv-structured-list-heading>
                    </template>
                    <template slot="items">
                        <cv-structured-list-item 
                        v-for="feature in enterprise.parcels.features" 
                        name="group-1" 
                        :value="String(feature.id)" 
                        v-bind:key="feature.id" 
                        :checked="feature.id == parcelaSeleccionada"
                        @change="actionChangeParcels"
                        ref="listaDeParcelas" >
                            <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                        </cv-structured-list-item>
                    </template>
                </cv-structured-list>
            </div>
            <div id="sentinelLayersList" ref="sentinelLayersListCollapse" v-else-if="empresaSelect === 'all' && mostarListaParcelsCoops == false">
                <cv-structured-list selectable id="parcelList" >
                    <template slot="headings">
                        <cv-structured-list-heading>{{$t("map.parcelas_de")}}</cv-structured-list-heading>
                    </template>
                    <template slot="items" v-for="enterprisee in enterprisesList">
                            <cv-structured-list-item 
                            v-for="feature in enterprisee.parcels.features" 
                            name="group-1" 
                            :value="String(feature.id)" 
                            v-bind:key="feature.id" 
                            :checked="feature.id == parcelaSeleccionada"
                            @change="actionChangeParcels"
                            ref="listaDeParcelas" >
                                <cv-structured-list-data>{{feature.properties.name}} - {{enterprisee.name}}</cv-structured-list-data>
                            </cv-structured-list-item>
                    </template>
                </cv-structured-list>
            </div>
            <div id="sentinelLayersList" ref="sentinelLayersListCollapse" v-else-if="empresaSelect != 'all' && mostarListaParcelsCoops == true">
                <cv-structured-list selectable id="parcelList" >
                    <template slot="headings">
                        <cv-structured-list-heading>{{$t("map.parcelas_de")}} - {{cooperativeSelectObj.name}}</cv-structured-list-heading>
                    </template>
                    <template slot="items" v-for="enterprise in cooperativeSelectObj.enterprises">
                            <cv-structured-list-item 
                            v-for="feature in enterprise.parcels.features" 
                            name="group-1" 
                            :value="String(feature.id)" 
                            v-bind:key="feature.id" 
                            :checked="feature.id == parcelaSeleccionada"
                            @change="actionChangeParcels"
                            ref="listaDeParcelas" >
                                <cv-structured-list-data>{{feature.properties.name}} - {{enterprise.name}}</cv-structured-list-data>
                            </cv-structured-list-item>
                    </template>
                </cv-structured-list>
            </div>
            <cv-pagination
                    v-if="empresaSelect !== 'all'"
                    backwards-text="Previous page"
                    forwards-text="Next page"
                    page-sizes-label="Por Página"
                    :page-sizes="[60, 90, 120, 150, 180, {label: `total(${totalParcelas})`, value: totalParcelas}]"
                    :isLastPage="true"
                    :forwards-button-disabled="false" @change="changePaginacion" ref="sentinelLayersListCollapseP">
            </cv-pagination>
            <cv-pagination
                    v-else-if="empresaSelect === 'all'"
                    backwards-text="Previous page"
                    forwards-text="Next page"
                    page-sizes-label="Por Página"
                    :page-sizes="[60, 90, 120, 150, 180, {label: `total(${totalParcelasCoops})`, value: totalParcelasCoops}]"
                    :isLastPage="true"
                    :forwards-button-disabled="false" @change="changePaginacion" ref="sentinelLayersListCollapseP">
            </cv-pagination>
            <br>
            <div>
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
            <br>
            <div id="sentinelLayers">
                <cv-dropdown 
                    :placeholder="placeholderLayers" 
                    @change="actionChangeLayers" :label="labelLayers">
                        <cv-dropdown-item v-for="layer in layersSentinel" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
                </cv-dropdown>
            </div>
            <div v-if="verColoresEsas">
                <label for="text-input-3h9mddk235a" class="bx--label">{{$t("map.colors")}}</label>
                <br>
                <img alt="D4SF" id="logo" src="../assets/muestras-colores.png" style="">
            </div>
            <div v-if="verColorNDVI">
                <label for="text-input-3h9mddk235a" class="bx--label">{{$t("map.colors")}}</label>
                <br>
                <img alt="D4SF" id="logo" src="../assets/NDVI-colores.png" style="">
            </div>
            <div v-if="verColorMoisture">
                <label for="text-input-3h9mddk235a" class="bx--label">{{$t("map.colors")}}</label>
                <br>
                <img alt="D4SF" id="logo" src="../assets/Moisture-index-valores.png" style="">
            </div>
            <br>
            <div id="sentinelOpacity">
                <cv-slider
                    :label="$t('map.opacidad')"
                    @change="actionChangeOpacity"></cv-slider>
            </div>
            <div id="sentinelClouds" v-if="false">
                <cv-slider
                    :label="labelSliderCloud"
                    @change="actionChangeClouds"></cv-slider>
            </div>
            <div :class="classfechaR">
                <div id="sentinelDate" :class="classfechab1">
                    <cv-date-picker
                    kind="single"
                    :cal-options="calOptions"
                    @change="actionChangeDate"
                    :dateLabel="$t('map.fecha')"
                    :value="valueDates"
                    placeholder="mm/dd/yyyy"
                    ref="cambiosFechas"
                    :key="dateUpdate"
                    style=""
                    ></cv-date-picker>
                </div>
                <div :class="classfechab2">
                    <cv-button
                    :disabled="false"
                    @click="actionClickDate"
                    size="small"
                    style="margin-top: 20px"
                    >
                    {{$t("map.fechas_disponibles")}}
                    <cv-loading
                    :small="true"
                    :active="isActiveLoading2"
                    :overlay="false" v-if="isVisibleLoad2"></cv-loading>
                    </cv-button>
                </div>
            </div>
        </div>
        <div id="layersControlerResponsive" class="layersControler" ref="layersControlersResponsive" :key="componentDrop" v-if="isMobile()">
            <cv-tile
            kind=""
            :theme="theme"
            :expanded="true">

            <cv-loading
            :small="true"
            :active="isActiveLoading"
            :overlay="true" v-if="isVisibleLoad"></cv-loading>
                <div class="bx--row" id="row_box">
                    <div class="bx--col-sm-3">
                    <div id="sentinelLayers">
                        <cv-dropdown :placeholder="placeholderLayers" @change="actionChangeLayers" :label="labelLayers" up ref="dropDownLayersResp" v-if="!expand" >
                            <cv-dropdown-item v-for="layer in layersSentinel" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
                        </cv-dropdown>
                        <cv-dropdown :placeholder="placeholderLayers" @change="actionChangeLayers" :label="labelLayers" ref="dropDownLayersResp" v-else>
                            <cv-dropdown-item v-for="layer in layersSentinel" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
                        </cv-dropdown>
                    </div>
                    </div>
                    <div class="bx--col-sm-1">
                        <ChevronSortUp20 @click="onclickTile" v-if="!expand" style="transform: translate(35px, 0px);"/>
                        <ChevronSortDown20  @click="onclickTile" v-if="expand" style="transform: translate(35px, 0px);"/>
                    </div>
                </div>
                <div v-if="expand">
                    <div v-if="mostrarListaEmpresas" id="sentinelLayers">
                        <cv-select
                            theme=""
                            :label="$t('map.listado_empresas')"
                            :hide-label="false"
                            :inline="false"
                            :disabled="false"
                            @change="seleccionaEmpresa">
                            <cv-select-option disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                            <cv-select-option v-for="empresa in enterprisesList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                                {{empresa.name}}
                            </cv-select-option>
                        </cv-select>
                    </div>
                    <div id="sentinelLayersList">
                        <cv-structured-list selectable id="parcelList">
                            <template slot="headings">
                                <cv-structured-list-heading>{{$t("map.parcelas_de")}} {{enterprise.name}}</cv-structured-list-heading>
                            </template>
                            <template slot="items">
                                <cv-structured-list-item 
                                v-for="feature in enterprise.parcels.features" 
                                name="group-1" 
                                :value="String(feature.id)" 
                                v-bind:key="feature.id" 
                                :checked="feature.id == parcelaSeleccionada"
                                @change="actionChangeParcels"
                                ref="listaDeParcelas" >
                                    <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                                </cv-structured-list-item>
                            </template>
                        </cv-structured-list>
                    </div>
                    <div style="overflow-x: auto;">
                        <cv-pagination
                        id=""
                        backwards-text="Previous page"
                        forwards-text="Next page"
                        page-sizes-label="Por Página"
                        :page-sizes="[60, 90, 120, 150, 180, {label: `total(${totalParcelas})`, value: totalParcelas}]"
                        :isLastPage="true"
                        :forwards-button-disabled="false" @change="changePaginacion" :key="keyPagination"></cv-pagination>
                    </div>
                    <div id="sentinelOpacity">
                        <cv-slider
                            :label="$t('map.opacidad')"
                            @change="actionChangeOpacity"></cv-slider>
                    </div>
                </div>
            </cv-tile>
        </div>
        <div id="div_buscador" v-if="!isMobile()">
            <gmap-autocomplete @place_changed="setPlace"  class="form-control bx--text-input" :placeholder="$t('map.intro_ubica')" style="with: 100%">
            </gmap-autocomplete>
        </div>
        <div id="control_der"  v-if="!isMobile() && $parent.$parent.is_superuser || $parent.$parent.is_systemadmin || $parent.$parent.is_enterpriseadmin">
            <div id="edicionParcela" v-if="verEdicionRapida" :key="keyModificar">
                <p>{{$t("map.edit_rapido")}} {{$parent.$parent.is_staff}}</p>
                <div class="errorDraw" v-if="verErrorDraw"><br>{{errorDraw}}</div>
                <br>
                <cv-button
                kind="primary"
                size="small"
                :disabled="disabledSave"
                @click="guardadoPoligono"
                >
                {{$t("map.guardar")}}
                </cv-button>
                <cv-button
                kind="danger"
                size="small"
                :disabled="false"
                @click="cancelarEdicion"
                >
                {{$t("map.cancelar")}}
                </cv-button>
                <br>
                <br>
                <br>
                <p>{{$t("map.elimina_parcela")}}</p>
                <br>
                <cv-button
                kind="danger"
                size="small"
                :disabled="false"
                @click="eliminarPoligono"
                >
                {{$t("map.eliminar")}}
                </cv-button>
            </div>
        <div id="edicionParcela" v-if="verCrearRapida" :key="keyModificar">
                <p>{{$t("map.parcela_nueva")}}</p>
                <cv-text-input
                    :label="labelName"
                    :value="valueName"
                    :disabled="disabledName"
                    :type="inputTypeName"
                    :placeholder="placeholderName"
                    :invalid-message="invalidMessageName"
                    ref="inputName"
                    id="input-MIRLwtCq"
                    v-model="valueName"></cv-text-input>
                <br>
                <cv-text-input
                    :label="labelDesc"
                    :value="valueDesc"
                    :disabled="disabledDesc"
                    :type="inputTypeDesc"
                    :placeholder="placeholderDesc"
                    :invalid-message="invalidMessageDesc"
                    ref="inputDesc"
                    id="input-3zcRveTf"
                    v-model="valueDesc"
                    ></cv-text-input>
                    <br>
                <div class="errorDraw" v-if="verErrorDraw"><br>{{errorDraw}}</div>
                <br>
                <cv-button
                kind="primary"
                size="small"
                :disabled="disabledSave"
                @click="guardadoPoligono"
                >
                {{$t("map.guardar")}}
                </cv-button>
                <cv-button
                kind="danger"
                size="small"
                :disabled="false"
                @click="cancelarEdicion"
                >
                {{$t("map.cancelar")}}
                </cv-button>
            </div>
            <div id="btnCrearParcela" v-if="verBtnCrearPar && empresaSelect != 'all'">
                <cv-button
                kind="primary"
                size="small"
                :disabled="disabledAddNewParcela"
                @click="crearParcela"
                >
                {{$t("map.crear_parcela")}}
                </cv-button>  
            </div>
        </div>
        <cv-modal
        ref="alerta_eliminar"
        kind="danger"
        :visible="visibleAlertaEliminar"
        @primary-click="confirmaElimar">
            <template slot="label">{{$t("map.seguro")}}</template>
            <template slot="title">{{$t("map.eliminar")}}</template>
            <template slot="content">
            <p>{{$t("map.seguro_parcel_del")}} {{nombreParcelaEliminar}}?</p>
            </template>
            <template slot="secondary-button">{{$t("map.cancelar")}}</template>
            <template slot="primary-button">{{$t("map.eliminar")}}</template>
        </cv-modal>
    </div>
</template>
<script>
import axios from "axios";
//import Polygon from 'ol/geom/Polygon';
import proj4 from 'proj4'
import L from 'leaflet'
import { getArea } from 'ol/sphere';
//import {crearInstanciaTempMapaCoop} from '../sentinelFunctions/sentinelFunc'
import {getAllCooperatives} from '../crudFunctions/crudCooperativas'
export default {
    data () {
        return{
            checkedToggleMostarTexto: false,
            disabledAddNewParcela: false,
            verLayerTile: true,
            esUp: true,
            //resposive
            classfechaR: `bx--row`,
            classfechab1: `bx--col-lg-7 bx--col-md-10 bx--col-sm-8`,
            classfechab2: `bx--col-lg-1 bx--col-md-1 bx--col-sm-1`,
            use_slotBelow: true,
            theme: "",
            expanded: false,
            label: "Icon button",
            tipPosition: "rigth",
            tipAlignment: "center",
            expand: false,
            expand2: true,
            //
            valueDates: [],
            verColorMoisture:false,
            verColorNDVI:false,
            verColoresEsas: false,
            //BingMap Config
            apiKeyBing: this.$apiKeyBing,
            imagerySetBing: `AerialWithLabels`,
            maxZoomBing: 20,
            //Sentinel 
            urlSent: `${this.$sentinelURL}/ogc/wms/${sessionStorage.getItem('sI')}`,
            urlProcessingApi:`${this.$sentinelURL}/ogc/wms/${sessionStorage.getItem('sI')}`,
            maxcc:0,
            minZoom:6,
            maxZoom:16,
            preset:'AGRICULTURE',
            layers:'AGRICULTURE',
            time:"2019-01-01/2020-06-04",
            serverType: 'geoserver',
            opacitylayer: 0.5,
            transition: 0,
            //GENERAL
            zoom: 15,
            center: [-3.8225970954841486, 40.28385074244977 ],
            coordinates: Object,
            //Herencia
            geometry: Object,
            allCoordinatesMultipolygon: Array,
            valueLayersControler: '0',
            placeholderLayers: `${this.$t('map.sent_layers_sel')}`,
            layersSentinel: Array,
            SentinelLayer: 'AGRICULTURE',
            labelSliderOpa: `${this.$t('map.opacidad')}`,
            labelSliderCloud: 'Nubes',
            labelLayers: this.$t('map.sent_layers'),
            labelFecha: this.$t('map.fecha'),
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            placeholderDate: "yyyy/mm/dd",
            allFeatures: Array(),
            allParcels: Array(),
            sentinelInstaceEnterprise: '',
            jsondata: Object,
            //Nuevo map
            enterprise: Object(),
            pageSize: 60,
            pagePar: 1,
            enterprisesList: Array(),
            empresaSelect: '',
            componentKey: 0,
            mostrarListaEmpresas: false,
            mostrarListaEmpresasCoop: false,
            totalParcelas: 0,
            isActiveLoading: false,
            isVisibleLoad: true,
            dateUpdate: 0,
            fechasArr:Array(),
            isActiveLoading2: false,
            isVisibleLoad2: false,
            //modificacion de parcelas
            parcelaSeleccionada: 0,
            parcelaSeleccionadaName: ``,
            modifyingFeatures: {},
            modifiedFeatures: [],
            verErrorDraw: false,
            verguardadoOK: false,
            area: 0,
            errorDraw: ``,
            guardadoOKMsg = ``,
            coordinatesPoligono: [],
            disabledSave: true,
            verEdicionRapida: false,
            keyModificar: 0,
            esGuardado: false,
            esGuardadoNuevo: false,
            //input-name
            labelName: this.$t('app.nombre_parcela'),
            valueName: '',
            disabledName: false,
            inputTypeName: 'text',
            placeholderName: this.$t('app.place_nombre_parcela'),
            invalidMessageName: '',
            //input-email
            labelDesc: this.$t('app.desc_parcela'),
            valueDesc: '',
            disabledDesc: false,
            inputTypeDesc: 'text',
            placeholderDesc: this.$t('app.place_desc_parcela'),
            invalidMessageDesc: '',
            dibujaPoligono: false,
            verCrearRapida: false,
            verBtnCrearPar: true,
            refreshDibujo: 0,
            coordenadasParcel: [ [ [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ] ] ],
            verSeleccionaPolygon: true,
            featuresss: [],
            visibleAlertaEliminar: false,
            keyComponentMap: 0,
            keyPagination: 0,
            nombreParcelaEliminar: ``,
            componentDrop: 0,
            is_staff: false,
            metric: "Hm2",
            erorCompaGeoloc: '',
            mostrarIconErrGeoloc: '',
            //Parcelas Cooperativas

            totalParcelasCoops: 0,
            coopSeleccionada: '',
            //Cooperativas ADM
            mostrarListaCooperativas: false,
            cooperativesList: Array(),
            cooperativeSelect: '',
            cooperativeSelectObj: Object(),
            mostarListaParcelsCoops: false

        }
    },
    methods: {
        actionChangedToggle(value){
            this.checkedToggleMostarTexto = value
        },
        crearParcela(){
            this.verSeleccionaPolygon = false
            this.verEdicionRapida = false
            this.verCrearRapida = true
            this.verBtnCrearPar = false
            this.dibujaPoligono = true
            this.parcelaSeleccionada = 0
            this.disabledSave = false
            this.guardadoOKMsg = ''
        },
        cancelarEdicion(){
            this.keyModificar +=1
            this.verEdicionRapida = false
            this.verCrearRapida = false
            this.verBtnCrearPar = true
            this.refreshDibujo += 1
            this.featuresss = []
            this.refreshDibujo += 1
            this.verSeleccionaPolygon = true
            this.dibujaPoligono = false
            this.disabledSave = false
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
            
            
            if(this.parcelaSeleccionada){
                this.coordinatesBuenas(this.coordinatesEditadas)
            }
            
            this.verErrorDraw = false
            
        },
        metricaparcela(area){
            if(this.enterprise.type_metric == "Acre"){
                const onehecttoAcre = 2.4710538146717
                const acre = onehecttoAcre * area
                this.metric = "Acre"
                return  acre.toFixed(4)
            }
            return area
        
        },
        coordinatesBuenas(ArrayCoor){
            if(this.parcelaSeleccionada){
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
            let path = `${this.$apiURL}/parcel_filter/?enterprise_id=${this.enterprise.id}&polygon=${polygonObject}`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                if(response.data.features.length){
                    this.errorDraw = ''
                    this.verErrorDraw = false
                    response.data.features.forEach(parcela =>{
                        if(this.parcelaSeleccionada == parcela.id){
                            this.parcelaSeleccionadaName = `${parcela.properties.name}`
                        }
                        if(this.parcelaSeleccionada != parcela.id){
                            this.errorDraw += `"${parcela.properties.name}"  `
                            if(!this.parcelaSeleccionada){
                                this.featuresss = []
                                this.refreshDibujo += 1
                                this.dibujaPoligono = true
                            }
                        }
                    })
                    if(this.errorDraw){
                        this.verErrorDraw = true
                        this.disabledSave = true
                        this.errorDraw = `${this.$t('map.parcela_solapada_con')}  ${this.errorDraw}`
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
                    this.errorDraw = `${this.$t('map.parcela_solapada_misma')}`
                    this.colorParcela = 'red'
                    if(!this.parcelaSeleccionada){
                        this.featuresss = []
                        this.refreshDibujo += 1
                        this.dibujaPoligono = true
                    }
                }else{
                    this.verErrorDraw = false
                    this.disabledSave = false
                    this.colorParcela = 'green'
                    this.compruebaLimites()
                }
            })
            .catch(error => {
                console.warn(error)
            })
        },
        compruebaLimites(){
            let path = `${this.$apiURL}/enterprises_except/${this.enterprise.id}/?parcel=${this.parcelaSeleccionada}`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                let hectareas_ant = 0
                this.enterprise.parcels.features.forEach(parcel =>{
                    hectareas_ant += parcel.properties.area
                })
                const porcentaje_ant = (parseFloat(hectareas_ant) / parseFloat(response.data.hectares_available)  * 100)
                const porcentaje_now = ((parseFloat(response.data.parcels.area__sum)+parseFloat(this.area)) / parseFloat(response.data.hectares_available) * 100)
                if(parseFloat(porcentaje_ant) < parseFloat(porcentaje_now)){
                    if(porcentaje_now > 100.00){
                        this.verErrorDraw = true
                        this.disabledSave = true
                        this.errorDraw = `${this.$t('map.sup_area_parcel')}`
                        this.colorParcela = 'red'
                        if(!this.parcelaSeleccionada){
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
        onclickTile(){
            if(this.expand){
                this.expand = false
                this.$refs.dropDownLayersResp._props.up = true
                this.$refs.layersControlersResponsive.style['max-height'] = ''
                this.$refs.layersControlersResponsive.style['overflow-y'] = ''
                this.componentDrop +=1
            }else{
                this.expand = true
                this.$refs.dropDownLayersResp._props.up = false
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
        moveend(){
            this.cargaFechasSentinel()
        },
        setPlace(place){
            //console.info(place.geometry.viewport.keys())
            //const lat = (place.geometry.viewport.Za.i + place.geometry.viewport.Za.j) / 2
            //const long = (place.geometry.viewport.Va.i + place.geometry.viewport.Va.j) / 2
            //this.center = [long, lat]
            this.center = [place.geometry.location.lng(), place.geometry.location.lat()]
            this.zoom = 15
        },
        selecionaPolygon(po){
            
            this.verEdicionRapida = true
            this.verCrearRapida = false
            this.verBtnCrearPar = false
            this.refreshDibujo += 1
            this.parcelaSeleccionada = po.values_.geometry.values_.id
            const coordenadasGeometricas = po.getGeometry().getExtent()
            const ex = coordenadasGeometricas[0] + (coordenadasGeometricas[2]-coordenadasGeometricas[0])/2;
            const ye = coordenadasGeometricas[1] + (coordenadasGeometricas[3]-coordenadasGeometricas[1])/2;
            var source = new proj4.Proj('EPSG:3785'); 
            var dest = new proj4.Proj('EPSG:4326');  
            const newCenter = proj4(source, dest, [ex, ye])
            this.center = [newCenter[0], newCenter[1]]
        }, 
        actionChangeParcels(valor){
            this.keyModificar +=1
            this.verEdicionRapida = false
            this.verCrearRapida = false
            this.verBtnCrearPar = true
            this.refreshDibujo += 1
            this.parcelaSeleccionada = valor
            const coordenadasGeometricas = this.$refs[this.parcelaSeleccionada+'parcela'][0].$geometry.extent_
            const ex = coordenadasGeometricas[0] + (coordenadasGeometricas[2]-coordenadasGeometricas[0])/2;
            const ye = coordenadasGeometricas[1] + (coordenadasGeometricas[3]-coordenadasGeometricas[1])/2;
            var source = new proj4.Proj('EPSG:3785'); 
            var dest = new proj4.Proj('EPSG:4326');  
            const newCenter = proj4(source, dest, [ex, ye])
            this.center = [newCenter[0], newCenter[1]]
        },
        actionChangeOpacity(valor){
            this.opacitylayer = valor/100;
        },
        actionChangeClouds(valor){
            this.maxcc = valor
            
        },
        actionChangeDate(valor){
            const arrFechas = valor.split(', ')
            if(arrFechas.length == 1){
                this.time = "2019-01-01/"+valor
            }
        },
        actionClickDate(){
            this.cargaFechasSentinel()
        },
        actionChangeLayers(valor){
            if(valor == "INTERPRETACIN-MULTIFACTOR" || valor == "ESAS-SCENE"){
                this.verColoresEsas = true
            }else{
                this.verColoresEsas = false
            }

            if(valor == "NDVI"){
                this.verColorNDVI = true
            }else{
                this.verColorNDVI = false
            }

            if(valor == "MOISTURE_INDEX"){
                this.verColorMoisture = true
            }else{
                this.verColorMoisture = false
            }

            this.SentinelLayer = valor
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
                    sessionStorage.setItem('is_coop_user', response.data[0].cooperative_user)
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
                    sessionStorage.clear();
                    this.$session.destroy()
                    setTimeout(function(){ window.location.reload() }, 500);
                })
            }
        },
        getPermisosUser(id){
            /*
            const path = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                this.$root.$i18n.locale = response.data.language
            })
            */
            const pathRol = `${this.$apiURL}/permisos/${id}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(pathRol)
            .then(response => {
                //---------------------------------------------------------------
                //this.$session.set('is_coop_user', response.data.cooperative_user)
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
                this.$parent.$parent.is_coop_user = this.$session.get('is_coop_user')
                this.$parent.$parent.customLinkCoop = 'edit-cooperative?cooperative='+this.$session.get('enterprise')
                //---------------------------------------------------------------
                this.montarMapa()
            })
            .catch(error => console.info(error))
        },
        changePaginacionParcelsCoop(array, page_size, page_number){
            // human-readable page numbers usually start with 1, so we reduce 1 in the first argument
            return array.slice((page_number - 1) * page_size, page_number * page_size);
        },
        changePaginacion(event){
            this.pageSize = event.length
            this.pagePar = event.page
            this.montarMapa()
        },
        seleccionaEmpresa(empresa){
            this.keyModificar +=1
            this.verEdicionRapida = false
            this.empresaSelect = empresa
            this.mostarListaParcelsCoops = false
            if(empresa == 'all'){
                this.isActiveLoading = true
                this.montarMapaAllCoopParcels()
            }else{
                this.montarMapa()
            }
            
            //
        },
        seleccionaCoop(empresa){
            this.keyModificar +=1
            this.verEdicionRapida = false
            this.cooperativeSelect = empresa
            this.isActiveLoading = true
            this.mostarListaParcelsCoops = true
            this.montarMapaAllCoopParcelsAdm(empresa)

            
            //
        },
        montarMapaAllCoopParcelsAdm(coop_id){
            console.info(coop_id)
            this.mostrarListaEmpresasCoop = false
            let path = `${this.$apiURL}/cooperativesonenrlt/${coop_id}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios.get(path)
            .then(async response => {
                this.cooperativeSelectObj = response.data
                //this.enterprisesList = response.data.enterprises
                let parcelCount = 0
                response.data.enterprises.map(enterprise => {
                    parcelCount = parcelCount + enterprise.parcels.features.length
                })
                this.totalParcelasCoops = parcelCount
                this.isActiveLoading = false
            })
            
        },
        montarMapaAllCoopParcels(){
            if(sessionStorage.getItem('is_coop_user') == 'true'){
                this.mostrarListaEmpresasCoop = true
                let path = `${this.$apiURL}/cooperativesonenrlt/${sessionStorage.getItem('enterprise')}/`
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios.get(path)
                .then(async response => {
                    this.enterprisesList = response.data.enterprises
                    let parcelCount = 0
                    response.data.enterprises.map(enterprise => {
                        parcelCount = parcelCount + enterprise.parcels.features.length
                    })
                    this.totalParcelasCoops = parcelCount
                    this.isActiveLoading = false
                })
            }
        },
        montarMapa(){
            //console.info(this.$session.get('is_coop_user'))
            this.isActiveLoading = true
            let path = `${this.$apiURL}/enterprises/${sessionStorage.getItem('enterprise')}/?size=${this.pageSize}&page=${this.pagePar}`
            if(sessionStorage.getItem('is_superuser') == 'true' || sessionStorage.getItem('is_systemadmin') == 'true'){
                this.mostrarListaEmpresas = true
                this.mostrarListaCooperativas = true
                getAllCooperatives()
                .then(response => this.cooperativesList = response.data)
                if(this.empresaSelect){
                    path = `${this.$apiURL}/enterprises/${this.empresaSelect}/?size=${this.pageSize}&page=${this.pagePar}`
                }else{
                    path = `${this.$apiURL}/enterprises/`
                }
            }else if(sessionStorage.getItem('is_coop_user') == 'true'){
                this.mostrarListaEmpresasCoop = true
                path = `${this.$apiURL}/cooperativesonenrlt/${sessionStorage.getItem('enterprise')}/`
            }
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(async response => { 
                if(sessionStorage.getItem('is_coop_user') == 'false' || sessionStorage.getItem('is_superuser') == 'true' || sessionStorage.getItem('is_systemadmin') == 'true'){
                    if(response.data.length){
                    this.enterprisesList = response.data
                    this.enterprise = response.data[0]
                    this.stepTwoMap()
                    }else{
                        this.enterprise = response.data
                        this.stepTwoMap()
                    }
                }else{
                    this.enterprisesList = response.data.enterprises
                    //*detectar si es "all"
                    if(this.empresaSelect && this.empresaSelect != 'all'){
                        const result = response.data.enterprises.filter(enterprise => enterprise.id === this.empresaSelect)
                        this.enterprise = result[0]
                        this.stepTwoMap()
                    }else{
                        this.enterprise = response.data.enterprises[0]
                        this.stepTwoMap()
                    }
                    
                }
                
                this.metric = this.enterprise.type_metric
                //disabledAddNewParcela
                let hectareas_ant = 0
                this.enterprise.parcels.features.forEach(parcel =>{
                    hectareas_ant += parcel.properties.area
                    parcel.properties.area = this.metricaparcela(parcel.properties.area)
                    //this.metricaparcela(parcel.properties.area)
                })
                
                const porcentaje_ant = (parseFloat(hectareas_ant) / parseFloat(this.enterprise.hectares_available)  * 100)
                if(parseFloat(porcentaje_ant) >= 100.00){
                    this.disabledAddNewParcela = true
                }else{
                    this.disabledAddNewParcela = false
                }
            })
            .catch(error =>{
                console.warn(error)
                if(error.response.status == 500 && error.response.data.split(' ')[0] == 'EmptyPage'){
                    console.log('ultima')
                }
            })
            
        },
        stepTwoMap(){
            this.urlSent = `${this.$sentinelURL}/ogc/wms/${this.enterprise.sentinel_instance}`
            this.urlProcessingApi =`${this.$sentinelURL}/ogc/wms/${this.enterprise.sentinel_instance}`
            this.urlSent = `${this.$sentinelURL}/ogc/wms/${this.enterprise.sentinel_instance}`
            this.urlProcessingApi =`${this.$sentinelURL}/ogc/wms/${this.enterprise.sentinel_instance}`
            if(this.parcelaSeleccionada && this.esGuardado){
                if(this.esGuardadoNuevo){
                    const newParcel = this.enterprise.parcels.features.filter((parcela)=>{return parcela.id == this.parcelaSeleccionada})
                    const primerpol = newParcel[0].geometry.coordinates
                    const polygon = L.polygon(primerpol)
                    const bounds = polygon.getBounds();
                    const latLng = bounds.getCenter();
                    this.center = [latLng.lat, latLng.lng]
                    this.esGuardadoNuevo = false
                }else{
                    this.actionChangeParcels(this.parcelaSeleccionada)
                }
                this.esGuardado = false
            }else{
                const primerpol = this.enterprise.parcels.features[0].geometry.coordinates
                const polygon = L.polygon(primerpol)
                const bounds = polygon.getBounds();
                const latLng = bounds.getCenter();
                this.center = [latLng.lat, latLng.lng]
            }
            this.zoom = 18
            var allCoordinates = Array();
            this.enterprise.parcels.features.forEach(element => {
                allCoordinates.push(element.geometry.coordinates)
            });
            this.cargaTotalParcels(this.enterprise.id)
            this.cargaFechas()
            this.cargaParcelasSentinel(allCoordinates)
            this.cargaFechasSentinel()
            this.cargaOpcionesLayersSentinel(this.enterprise.sentinel_instance)
            //this.cargaLocalizacionActual()
        },
        cargaParcelasSentinel(parcelas){
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
                'name': `${this.enterprise.name}`,
                "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                "additionalData": {
                    "showLogo": false,
                    "showWarnings": false,
                    "imageQuality": 100,
                    "disabled": false
                },
                'areaOfInterest': {
                    'type': "MultiPolygon",
                    'coordinates': parcelas
                    ,"crs": {
                        "type": "name",
                        "properties": {
                            "name": "urn:ogc:def:crs:EPSG::4326"
                        }
                    }
                }
            })
            instanceIns.put("/configuration/v1/wms/instances/"+this.enterprise.sentinel_instance, bodyIns, configIns).then(resp => {
                if(resp.status != 200){
                    console.warn(resp)
                }
                this.componentKey += 1
            })
            this.isActiveLoading = false
        },
        cargaOpcionesLayersSentinel(sentinelInstance){
            const instanceIns = axios.create({
                baseURL: this.$sentinelURL
            })
            const configIns = {
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                    'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
                }
            }
            instanceIns.get("/configuration/v1/wms/instances/"+sentinelInstance+"/layers", configIns).then(resp =>{
                if(resp.status != 200){
                    console.warn(resp)
                }
                this.layersSentinel = resp.data
            })
        },
        cargaFechasSentinel(){
            this.isActiveLoading2 = true,
            this.isVisibleLoad2= true
            setTimeout(() => {
                const instanceIns = axios.create({
                    baseURL: this.$sentinelURL
                })
                var MyDate = new Date();
                var MyDateString;
                MyDate.setDate(MyDate.getDate());
                MyDateString = ('0' + MyDate.getDate()).slice(-2) + '/' + ('0' + (MyDate.getMonth()+1)).slice(-2)
                MyDateString = MyDate.getFullYear()+'-'+('0' + (MyDate.getMonth()+1)).slice(-2)+'-'+('0' + MyDate.getDate()).slice(-2)
                instanceIns.get(`/ogc/wfs/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?REQUEST=GetFeature&TYPENAMES=S2.TILE&OUTPUTFORMAT=application/json&TIME=2020-01-01/${MyDateString}&BBOX=${this.$refs.map.$map.previousExtent_}&SRSNAME=EPSG:3857`).then(resp => {
                    if(resp.status != 200){
                        console.warn(resp)
                    }else{
                        
                        const respuesta = resp.data.features
                        const fechasArray = Array()
                        respuesta.forEach(feature =>{
                            fechasArray.push(feature.properties.date)
                        })
                        this.valueDates = fechasArray.reverse()
                        
                        setTimeout(() => {
                            this.$refs.cambiosFechas.$refs.date.value = ''
                            this.isActiveLoading2 = false,
                            this.isVisibleLoad2= false
                        }, 1000);
                    }
                })
            }, 1000);
        },
        guardadoPoligono(){
            if(!this.parcelaSeleccionadaName){
                this.enterprise.parcels.features.forEach(parcel =>{
                    if(parcel.id == this.parcelaSeleccionada){
                        this.parcelaSeleccionadaName = parcel.properties.name
                    }
                })
            }
            if(!this.verErrorDraw){
                if(this.parcelaSeleccionada){
                    const path = `${this.$apiURL}/parcels/${this.parcelaSeleccionada}/`;
                    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                    axios
                    .put(path, {
                        name: this.parcelaSeleccionadaName,
                        polygon: this.poligonObjecto,
                        area: this.area,
                        enterprise: this.enterprise.id,
                        user_updated: sessionStorage.getItem('user')
                    })
                    .then(() => {    
                        this.esGuardado = true                    
                        this.montarMapa()
                        this.cancelarEdicion()
                        setTimeout(()=>{
                            this.$refs.map.render()
                            this.componentKey += 1
                            //this.time = `01-01-${parseInt(this.random(2020, 2100))}`
                            //window.location.reload()
                        },5000)
                        
                        
                        //this.urlSent = `${this.$sentinelURL}/ogc/wms/${this.enterprise.sentinel_instance}`
                        //this.urlProcessingApi =`${this.$sentinelURL}/ogc/wms/${this.enterprise.sentinel_instance}`
                    })
                    .catch(error => {
                        console.info(error)
                    });
                }else{
                    const path = `${this.$apiURL}/parcels/`;
                    axios
                    .post(path, {
                        name: this.$refs.inputName.$refs.input.value,
                        description: this.$refs.inputDesc.$refs.input.value,
                        polygon: this.poligonObjecto,
                        area: this.area,
                        enterprise: this.enterprise.id,
                        user_created: sessionStorage.getItem('user')
                    })
                    .then((response) => {
                        this.valueName = ``
                        this.valueDesc = ``
                        this.featuresss = []
                        this.refreshDibujo += 1
                        this.dibujaPoligono = false
                        this.esGuardado = true
                        this.esGuardadoNuevo = true 
                        this.parcelaSeleccionada = response.data.id 
                        this.montarMapa()
                        this.cancelarEdicion()
                    })
                    .catch(error => {
                        if (error.response.data.name)
                            this.invalidMessageName = error.response.data.name[0];
                        if (error.response.data.polygon)
                            this.verErrorDraw = true
                            this.errorDraw = `${this.$t('map.establecer_limites_parcela')}`
                    });   
                }
            }
        },
        eliminarPoligono(){
            const newParcel = this.enterprise.parcels.features.filter((parcela)=>{return parcela.id == this.parcelaSeleccionada})
            if(newParcel[0].properties.name)
                this.nombreParcelaEliminar = newParcel[0].properties.name
            this.$refs.alerta_eliminar.dataVisible = true
        },
        confirmaElimar(){
            if(this.parcelaSeleccionada){
                const path = `${this.$apiURL}/parcels/${this.parcelaSeleccionada}/`
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .delete(path)
                .then(() => {
                    this.parcelaSeleccionada = 0
                    this.$refs.alerta_eliminar.dataVisible = false
                    this.montarMapa();
                    this.cancelarEdicion()
                })
                .catch(response =>{
                    console.log(response.error)
                });
            }
            
        },
        cargaImagenBuena(){
        },
        cargaTotalParcels(enterprise){            
            let path = `${this.$apiURL}/enterprises_count/${enterprise}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.totalParcelas = response.data.parcels
            }).catch(error =>{
                console.warn(error.response)
            });
            
        },
        cargaFechas(){
            var MyDate = new Date();
            var MyDateString;
            MyDate.setDate(MyDate.getDate());
            MyDateString = ('0' + MyDate.getDate()).slice(-2) + '/' + ('0' + (MyDate.getMonth()+1)).slice(-2)
            MyDateString = MyDate.getFullYear()+'-'+('0' + (MyDate.getMonth()+1)).slice(-2)+'-'+('0' + MyDate.getDate()).slice(-2)
            this.time = "2019-01-01/"+MyDateString
        },
        isMobile() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return true
            } else {
                return false
            }
        },
        random(min, max) {
            return min + Math.random() * (max - min);
        },
        onBuscar(search){
            const path = `${this.$apiURL}/enterprises/${this.enterprise.id}/?size=${this.pageSize}&page=${this.pagePar}&parcel_mame=${search}`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                //this.enterprise.parcels.features = response.data.features
                //this.stepTwoMap()
                this.enterprise = response.data
                this.stepTwoMap()
                this.totalParcelas = response.data.parcels.features.length
                this.keyPagination +=1
            })
            .catch(error => {
                console.warn(error)
            })
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
        }
    },
    
    created() {
        
    },
    mounted(){
        this.getDatosUser()
        this.$parent.$parent.is_superuser = true
        this.$parent.$parent.is_superuser = false,
        this.$parent.$parent.is_staff = false,
        this.$parent.$parent.is_systemadmin = false,
        this.$parent.$parent.is_enterpriseadmin = false
    }
}
</script>
<style scoped>
    .mapa{
        display: flex;
        height: 100vh !important;
        position: absolute;
    }
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
