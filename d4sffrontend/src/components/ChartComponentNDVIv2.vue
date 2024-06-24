<template>
    <div class="Graficos">
      <div class="bx--grid" style="padding-left: 1rem!important; padding-right: 1rem!important;max-width: 100%!important;">
        <div class="bx--row">
          <div class="bx--col-sm-12 bx--col-md-12 bx--col-lg-12">
            <h3>{{$t("graficos.gen_grafico_t_one")}}</h3>
            <cv-loading
            :small="true"
            :active="isActiveLoading"
            :overlay="true" v-if="isVisibleLoad"></cv-loading>
            <cv-loading
            :small="true"
            :active="isActiveLoading2"
            :overlay="true" v-if="isVisibleLoad2"></cv-loading>
            <br><br>
            <div class="bx--row">
              <div v-if="mostrarListaCooperativas" id="sentinelLayers" class="bx--col">
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
                  <br>
              </div>
            </div>
            <div class="bx--row">
              <div v-if="mostrarListaEmpresas" id="sentinelLayers" class="bx--col">
                  <cv-select
                      theme=""
                      :label="$t('graficos.enterprise_list')"
                      :hide-label="false"
                      :inline="false"
                      :disabled="false"
                      @change="seleccionaEmpresa">
                      <cv-select-option disabled selected hidden>{{$t("graficos.enterprise_sel")}}</cv-select-option>
                      <cv-select-option v-for="empresa in enterprisesList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                          {{empresa.name}}
                      </cv-select-option>
                  </cv-select>
              </div>
              <div v-if="mostrarListaEmpresasCoop" id="sentinelLayers" class="bx--col">
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
            </div>
            <br><br>
            <div class="bx--row">
              <div class="bx--col">
                <cv-text-input
                :label="$t('graficos.nombre_informe')"
                v-model="nombreInformeT1"
                :disabled="false"
                ></cv-text-input>
              </div>
            </div>
            <br><br>
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
            <br><br>
            <div class="bx--row" v-if="empresaSelect !== 'all'">
              <div class="bx--col">
                <cv-search :placeholder="`Buscar`" @input="onBuscar"></cv-search>
              </div>
            </div>
            <div class="bx--row">
              <div style="overflow-y: scroll;max-height: 500px;" class="bx--col" v-if="empresaSelect !== 'all' && mostarListaParcelsCoops == false">
                <cv-structured-list selectable id="parcelList">
                  <template slot="headings">
                      <cv-structured-list-heading>{{$t("graficos.parcels_de")}} {{enterprise.name}}</cv-structured-list-heading>
                      <cv-structured-list-heading>{{$t("graficos.descrip")}}</cv-structured-list-heading>
                      <cv-structured-list-heading>{{$t("graficos.hectareas")}}</cv-structured-list-heading>
                  </template>
                  <template slot="items">
                      <cv-structured-list-item 
                      v-for="feature in enterprise.parcels.features" 
                      name="group-1" 
                      :value="feature" 
                      v-bind:key="feature.id" 
                      @change="actionChangeParcels"
                      ref="listaDeParcelas" >
                          <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                          <cv-structured-list-data>{{feature.properties.description}}</cv-structured-list-data>
                          <cv-structured-list-data>{{metricaparcela(feature.properties.area)}}</cv-structured-list-data>
                      </cv-structured-list-item>
                  </template>
                </cv-structured-list>
              </div>
              <div style="overflow-y: scroll;max-height: 500px;" class="bx--col" v-else-if="empresaSelect === 'all' && mostarListaParcelsCoops == false">
                <cv-structured-list selectable id="parcelList">
                  <template slot="headings">
                      <cv-structured-list-heading>Todas las parcelas de la Cooperativa</cv-structured-list-heading>
                      <cv-structured-list-heading>{{$t("graficos.descrip")}}</cv-structured-list-heading>
                      <cv-structured-list-heading>{{$t("graficos.hectareas")}}</cv-structured-list-heading>
                      <cv-structured-list-heading>Empresa</cv-structured-list-heading>
                  </template>
                  <template slot="items" v-for="enterprise in enterprisesList">
                      <cv-structured-list-item 
                      v-for="feature in enterprise.parcels.features" 
                      name="group-1" 
                      :value="feature" 
                      v-bind:key="feature.id" 
                      @change="actionChangeParcels"
                      ref="listaDeParcelas" >
                          <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                          <cv-structured-list-data>{{feature.properties.description}}</cv-structured-list-data>
                          <cv-structured-list-data>{{metricaparcelaCoop(feature.properties.area, enterprise)}}</cv-structured-list-data>
                          <cv-structured-list-data>{{enterprise.name}}</cv-structured-list-data>
                      </cv-structured-list-item>
                  </template>
                </cv-structured-list>
              </div>
              <div style="overflow-y: scroll;max-height: 500px;" class="bx--col" v-else-if="empresaSelect != 'all' && mostarListaParcelsCoops == true">
                <cv-structured-list selectable id="parcelList">
                  <template slot="headings">
                      <cv-structured-list-heading>Todas las parcelas de la Cooperativa {{cooperativeSelectObj.name}}</cv-structured-list-heading>
                      <cv-structured-list-heading>{{$t("graficos.descrip")}}</cv-structured-list-heading>
                      <cv-structured-list-heading>{{$t("graficos.hectareas")}}</cv-structured-list-heading>
                      <cv-structured-list-heading>Empresa</cv-structured-list-heading>
                  </template>
                  <template slot="items" v-for="enterprise in cooperativeSelectObj.enterprises">
                      <cv-structured-list-item 
                      v-for="feature in enterprise.parcels.features" 
                      name="group-1" 
                      :value="feature" 
                      v-bind:key="feature.id" 
                      @change="actionChangeParcels"
                      ref="listaDeParcelas" >
                          <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                          <cv-structured-list-data>{{feature.properties.description}}</cv-structured-list-data>
                          <cv-structured-list-data>{{metricaparcelaCoop(feature.properties.area, enterprise)}}</cv-structured-list-data>
                          <cv-structured-list-data>{{enterprise.name}}</cv-structured-list-data>
                      </cv-structured-list-item>
                  </template>
                </cv-structured-list>
              </div>
            </div>
            <div class="bx--row">
              <div class="bx--col">
                <cv-pagination
                      :backwards-text="$t('graficos.prev_pag')"
                      :forwards-text="$t('graficos.next_page')"
                      :page-sizes-label="$t('graficos.por_pagina')"
                      :page-sizes="[60, 90, 120, 150, 180, {label: `total(${totalParcelas})`, value: totalParcelas}]"
                      :isLastPage="true"
                      :forwards-button-disabled="false" @change="changePaginacion" style="overflow-x: scroll;"></cv-pagination>
              </div>
            </div>
            <br>
            <br>
            <br>
            <div>
              <p>{{$t("graficos.imagen_por_gen")}} {{numImages}}</p>
            </div>
            <br>
            <div>
              <cv-button
                kind="primary"
                size=""
                :disabled="false"
                @click="generaInforme"
              >
                {{$t("graficos.gen_informe")}}
              </cv-button>
            </div>
            <br>
          </div>
        </div>
        <div class="bx--row">
          <div class="bx--col-sm-12 bx--col-md-12 bx--col-lg-12">
            <ChartLine :datos="dataSent" :key="keyComponent" v-if="verGraficNDVI"/>
            <ChartLineMois :datos="dataSent" :key="keyComponent" v-if="verGraficMois"/>
            <br>
            <ChartRadar :bbox="bbox" :sentinelLay="SentinelLayer" v-if="false" :rangeTime="time" :key="keyComponent"/>
            <br>
            <ChartBar :datos="dataSent" :key="keyComponent" v-if="verGraficNDVI"/>
            <ChartBarMois :datos="dataSent" :key="keyComponent" v-if="verGraficMois"/>
            <br>
            <TableColors :urlMedia="$apiURLMedia" :datos="dataSent" :key="keyComponent" v-if="verGraficNDVI"/>
            <TableColorsMois :urlMedia="$apiURLMedia" :datos="dataSent" :key="keyComponent" v-if="verGraficMois"/>
            <br>
            <SentImage :urlMedia="$apiURLMedia" :datos="dataSent" :key="keyComponent" v-if="verImagenSent"/>
            <br>
            <br>
            
          </div>
        </div>
      </div>
      <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
      
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
import axios from "axios";
import L from 'leaflet'
import ChartLine from '@/components/charts/chartLine.vue'
import ChartLineMois from '@/components/charts/chartLineMois.vue'
import SentImage from '@/components/charts/imageSent.vue'
import ChartBar from '@/components/charts/chartBar.vue'
import ChartBarMois from '@/components/charts/chartBarMois.vue'
import TableColors from '@/components/charts/tableColors.vue'
import TableColorsMois from '@/components/charts/tableColorsMois.vue'
import AlertaGeneral from "@/components/AlertaGeneral";
import {getAllCooperatives} from '../crudFunctions/crudCooperativas'
export default {
  name: 'CartCompoent',
  components: {
    ChartLine,
    SentImage,
    ChartBar,
    TableColors, 
    AlertaGeneral,
    ChartLineMois,
    ChartBarMois,
    TableColorsMois
  },
  data () {
    return{
      nombreInformeT1: ``,
      verGraficNDVI: false,
      verGraficMois: false,
      verImagenSent: false,
      mensajeAlerta: ``,
      tipoAlerta: `error`,
      isActiveLoading: false,
      isVisibleLoad: true,
      isActiveLoading2: false,
      isVisibleLoad2: true,
      mostrarListaEmpresas: false,
      mostrarListaEmpresasCoop: false,
      enterprisesList: Array(),
      enterprise: Object(),
      layersSentinel: Array(),
      placeholderLayers: this.$t('graficos.sel_layer_sen'),
      labelLayers: this.$t('graficos.sent_layers'),
      totalParcelas: 0,
      pageSize: 60,
      pagePar: 1,
      bbox: '',
      keyComponent: 0,
      SentinelLayer: 'NDVI',
      dateLabel: this.$t('graficos.fecha_incio'),
      dateEndLabel: this.$t('graficos.fecha_fin'),
      calOptions: {
        dateFormat: "Y-m-d"
      },
      valueRange: ``,
      time: '',
      ketComponentDate: 0,
      poligonoSelect: Array(),
      idParcela:0,
      dataSent:Object(),
      urlSentinel: Array(),
      instSentTmp: ``,
      fechasSentinel: Array,
      numImages: 0,
      historicoAnterior: Array(),
      columnsHistorico: [
        this.$t('graficos.parcelas'),
        this.$t('graficos.rang_fechas')
      ],
      //For coops
      enterprise_id_sel_parcel: '',
      //for coops ADM
      mostrarListaCooperativas: false,
      cooperativesList: Array(),
      cooperativeSelect: '',
      cooperativeSelectObj: Object(),
      mostarListaParcelsCoops: false
    }
  },
  
  methods:{
    metricaparcela(area){
      if(this.enterprise.type_metric == "Acre"){
          const onehecttoAcre = 2.4710538146717
          const acre = onehecttoAcre * area
          this.metric = "Acre"
          return  acre.toFixed(4)
      }
      return  this.formateaHectareas(area)
    },
    metricaparcelaCoop(area, enterprise){
      if(enterprise.type_metric == "Acre"){
          const onehecttoAcre = 2.4710538146717
          const acre = onehecttoAcre * area
          this.metric = "Acre"
          return  acre.toFixed(4)
      }
      return  this.formateaHectareas(area)
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
    formateaHectareas(area){
      return Math.round((area + Number.EPSILON) * 100) / 100
    },
    chageCapas(capa){
      this.SentinelLayer = capa
      this.cargaFechasSentinel()
    },
    generaInforme(){
      this.toProcesar(this.urlSentinel, this.fechasSentinel)
    },
    actionChangeDateRange(range){
      this.time = `${range.startDate}/${range.endDate}`
      if(range.endDate){
        this.cargaFechasSentinel()
      }
      //this.keyComponent +=1
    },
    seleccionaEmpresa(empresa){
      this.mostarListaParcelsCoops = false
      if(empresa == 'all'){
        this.empresaSelect = empresa
        this.montarMapaAllCoopParcels()
      }else{
        this.empresaSelect = empresa
        this.init()
      }
    },
    seleccionaCoop(empresa){
      this.mostarListaParcelsCoops = true
      this.montarMapaAllCoopParcelsAdm(empresa)
    },
    montarMapaAllCoopParcelsAdm(coop_id){
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
              console.info('total parcelas', parcelCount)
              this.totalParcelasCoops = parcelCount
              this.isActiveLoading = false
          })
      }
    },
    changePaginacion(event){
      this.pageSize = event.length
      this.pagePar = event.page
      this.init()
    },
    actionChangeDate(valor){
      this.time = "2019-01-01/"+valor;
    },
    actionChangeLayers(valor){
      this.SentinelLayer = valor
      this.keyComponent +=1
    },
    actionChangeParcels(valor){
      console.info(valor.properties.enterprise_id)
      const result = valor
      this.enterprise_id_sel_parcel = valor.properties.enterprise_id
      //const result = this.enterprise.parcels.features.filter(feature => feature.id == valor)
      this.nombreInformeT1 = result.properties.name
      this.idParcela = valor.id
      const polygon = L.polygon(result.geometry.coordinates)
      this.poligonoSelect = result.geometry.coordinates
      console.info(this.poligonoSelect)
      const bboxP = `${polygon.getBounds()._northEast.lng},${polygon.getBounds()._northEast.lat},${polygon.getBounds()._southWest.lng},${polygon.getBounds()._southWest.lat}`
      this.bbox = bboxP
      this.keyComponent +=1
      this.cargaFechasSentinel()
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
    toProcesar(arrURL, fechasSentinel){
      setTimeout(() => {
        let uniqueFechas = [...new Set(fechasSentinel)];
        //let uniqueURL = [...new Set(arrURL)];
        //this.isActiveLoading = true
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
        /*
        .then(response => {
          //this.dataSent = response.data
          
          //this.isActiveLoading = false
          
          this.mensajeAlerta = this.$t('graficos.informe_gen_ok')
          this.tipoAlerta = 'success'
          this.$refs.alertaGeneral.verAlerta()
          this.$parent.$parent.$parent.getInformesAnteriores()
          
          
          this.verImagenSent = true
          if(this.SentinelLayer == 'NDVI'){
            this.verGraficNDVI = true
            this.verGraficMois = false
          }else{
            this.verGraficNDVI = false
            this.verGraficMois = true
          }
          this.keyComponent +=1
          
        })
        */
        .catch(() =>{
          this.isActiveLoading = false
          this.mensajeAlerta = this.$t('graficos.informe_gen_error')
          this.tipoAlerta = 'error'
          this.$refs.alertaGeneral.verAlerta()
        })
      }, 1000);
      /*
      this.mensajeAlerta = this.$t('graficos.grafico_procensandose')
      this.tipoAlerta = 'info'
      this.$refs.alertaGeneral.verAlerta()
      */
      this.$refs.modal_procesando.show()
    },
    init(){
      this.isActiveLoading = true
      this.ketComponentDate +=1
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
      .then(response => { 
          if(sessionStorage.getItem('is_coop_user') == 'false'){
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
              if(this.empresaSelect){
                  const result = response.data.enterprises.filter(enterprise => enterprise.id === this.empresaSelect)
                  this.enterprise = result[0]
              }else{
                  this.enterprise = response.data.enterprises[0]
              }
              this.stepTwoMap()
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
      this.cargaTotalParcels(this.enterprise.id)
      this.cargaFechas()
      this.cargaOpcionesLayersSentinel(this.enterprise.sentinel_instance)
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
            this.isActiveLoading = false
        })
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
        this.time = `${MyDate.getFullYear()}-${('0' + (MyDate.getMonth()-1)).slice(-2)}-01/${MyDateString}`
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
                this.$parent.$parent.is_coop_user = this.$session.get('is_coop_user')
                this.$parent.$parent.customLinkCoop = 'edit-cooperative?cooperative='+this.$session.get('enterprise')
                //---------------------------------------------------------------
                this.init()
            })
    },
    getInformesAnteriores(){
      let path = `${this.$apiURL}/procesado/`
      axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
      axios
      .get(path)
      .then(response => {
        this.historicoAnterior = response.data
      })
      .catch(error =>{
        console.warn(error)
      })
    },
    verDatos(){
      const rowSeleccionado = this.$refs.tableHist.selectedRows;
      let path = `${this.$apiURL}/ver_hist/${rowSeleccionado}/`
      axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
      axios
      .get(path)
      .then(response => {
        path = `${this.$apiURLMedia}/${response.data.imagen}/`
        axios
        .get(path)
        .then(response => {
          this.dataSent = response.data
          this.keyComponent +=1
        })
      })
      .catch(error =>{
        console.warn(error)
      })
    },
    getParcelaName(id){
      let name = `hola`
      let path = `${this.$apiURL}/parcels/${id}/`
      axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
      axios
      .get(path)
      .then(response => {
        name = response.data.properties.name
      })
      .catch(error =>{
        console.warn(error)
      })
      return name
    }
  },
  mounted () {
    const path = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
    this.getDatosUser()
    //this.getInformesAnteriores()
    this.$parent.$parent.is_superuser = true
    this.$parent.$parent.is_superuser = false,
    this.$parent.$parent.is_staff = false,
    this.$parent.$parent.is_systemadmin = false,
    this.$parent.$parent.is_enterpriseadmin = false
  },
  created(){
    const path = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
    this.getDatosUser()
    this.$parent.$parent.is_superuser = true
    this.$parent.$parent.is_superuser = false,
    this.$parent.$parent.is_staff = false,
    this.$parent.$parent.is_systemadmin = false,
    this.$parent.$parent.is_enterpriseadmin = false
  }
}
</script>