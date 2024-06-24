<template>
    <div class="Graficos">
      <div class="bx--grid" style="padding-left: 1rem!important; padding-right: 1rem!important;max-width: 100%!important;">
        <div class="bx--row">
          <div class="bx--col-sm-1 bx--col-md-2 bx--col-lg-12">
            <h3>{{$t("graficos.gen_grafico_t_two")}}</h3>
            <cv-loading
            :small="true"
            :active="isActiveLoading"
            :overlay="true" v-if="isVisibleLoad"></cv-loading>
            <cv-loading
            :small="true"
            :active="isActiveLoading2"
            :overlay="true" v-if="isVisibleLoad2"></cv-loading>
            <!--SelectEnterprise-->
            <br><br>
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
                <br>
            </div>
            <div v-if="mostrarListaEmpresas" id="sentinelLayers">
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
            <br><br>
            <cv-text-input
              :label="$t('graficos.nombre_informe')"
              v-model="nombreInformeT2"
              :disabled="false"
              :value="$t('graficos.grafico_tipo_dos')"></cv-text-input>
            <br><br>


            <div class="bx--row">
              <div class="bx--col-lg-3">
                <cv-select :label="$t('graficos.sel_layer_sen')" @change="chageCapas">
                  <cv-select-option selected value="NDVI">{{$t("graficos.NDVI")}}</cv-select-option>
                  <cv-select-option value="MOISTURE_INDEX">{{$t("graficos.mostisture_index")}}</cv-select-option>
                </cv-select>
              </div>
              <div class="bx--col-lg-3">
                <cv-date-picker
                  kind="single"
                  :date-label="$t('graficos.fecha')"
                  @change="chageFecha" :cal-options="calOptions">
                </cv-date-picker>
              </div>
            </div>
            <br>
            <br>
            <div class="bx--row">
              <div class="bx--col">
            <!--DataTable-->
                <cv-data-table
                  v-if="empresaSelect !== 'all' && mostarListaParcelsCoops == false"
                  :sortable="true"
                  :columns="[
                    {
                    key: 'name',
                    label: this.$t('graficos.nombre'),
                    },
                    {
                    key: 'description',
                    label: this.$t('graficos.descrip')
                    },
                    {
                    key: 'heactareas',
                    label: this.$t('graficos.hectareas'),
                    },
                ]
                "
                  @sort="onSort"
                  :title="$t('graficos.parcel_list')"
                  ref="tableLstadoT2"
                  :pagination="{ numberOfItems: enterprise.parcels.features.length, pageSizes: [10, 15, 20, 25, enterprise.parcels.features.length] }" @pagination="actionOnPagination"
                  @search="onFilter" searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
                >
                  <template v-if="true" slot="actions">
                      <cv-search :placeholder="$t('graficos.buscar_nombre')" @input="onBuscar"></cv-search>
                  </template>
                  <template v-if="true" slot="batch-actions">
                    <cv-button @click="generaInforme">
                      {{$t("graficos.generar")}}
                      <Analytics20 class="bx--btn__icon" />
                  </cv-button>  
                  </template>
                  <template slot="data">
                    <cv-data-table-row
                        v-for="feature in enterprise.parcels.features.slice(start, start+length)"
                        :key="`${feature.id}`"
                        :value="`${feature.id}`"
                        :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"
                    >
                        <cv-data-table-cell>{{feature.properties.name}}</cv-data-table-cell>
                        <cv-data-table-cell>{{feature.properties.description}}</cv-data-table-cell>
                        <cv-data-table-cell>{{metricaparcela(feature.properties.area)}}</cv-data-table-cell>
                    </cv-data-table-row>
                  </template>
                </cv-data-table>
            <!--EndDataTable-->
            <!--DataTable-->
                <cv-data-table
                  v-else-if="empresaSelect == 'all' && mostarListaParcelsCoops == false"
                  :sortable="true"
                  :columns="[
                    {
                    key: 'name',
                    label: this.$t('graficos.nombre'),
                    },
                    {
                    key: 'description',
                    label: this.$t('graficos.descrip')
                    },
                    {
                    key: 'heactareas',
                    label: this.$t('graficos.hectareas'),
                    },
                    {
                    key: 'empresa',
                    label: 'Empresa',
                    },
                ]
                "
                  @sort="onSort"
                  :title="$t('graficos.parcel_list')"
                  ref="tableLstadoT2MultiCoop"
                  :pagination="{ numberOfItems: enterprise.parcels.features.length, pageSizes: [10, 15, 20, 25, enterprise.parcels.features.length] }" @pagination="actionOnPagination"
                  @search="onFilter" searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
                >
                  <template v-if="true" slot="actions">
                      <cv-search :placeholder="$t('graficos.buscar_nombre')" @input="onBuscar"></cv-search>
                  </template>
                  <template v-if="true" slot="batch-actions">
                    <cv-button @click="generaInformeMultiCoop">
                      {{$t("graficos.generar")}}
                      <Analytics20 class="bx--btn__icon" />
                  </cv-button>  
                  </template>
                  <template slot="data" v-for="enterprise in enterprisesList">
                    <cv-data-table-row
                        v-for="feature in enterprise.parcels.features.slice(start, start+length)"
                        :key="`${feature.id}`"
                        :value="`${feature.id}`"
                        :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"
                    >
                        <cv-data-table-cell>{{feature.properties.name}}</cv-data-table-cell>
                        <cv-data-table-cell>{{feature.properties.description}}</cv-data-table-cell>
                        <cv-data-table-cell>{{metricaparcelaCoop(feature.properties.area, enterprise)}}</cv-data-table-cell>
                        <cv-data-table-cell>{{enterprise.name}}</cv-data-table-cell>
                    </cv-data-table-row>
                  </template>
                </cv-data-table>
            <!--EndDataTable-->
            <!--DataTable-->
                <cv-data-table
                  v-else-if="empresaSelect != 'all' && mostarListaParcelsCoops == true"
                  :sortable="true"
                  :columns="[
                    {
                    key: 'name',
                    label: this.$t('graficos.nombre'),
                    },
                    {
                    key: 'description',
                    label: this.$t('graficos.descrip')
                    },
                    {
                    key: 'heactareas',
                    label: this.$t('graficos.hectareas'),
                    },
                    {
                    key: 'empresa',
                    label: 'Empresa',
                    },
                ]
                "
                  @sort="onSort"
                  :title="$t('graficos.parcel_list')"
                  ref="tableLstadoT2MultiCoop"
                  :pagination="{ numberOfItems: enterprise.parcels.features.length, pageSizes: [10, 15, 20, 25, enterprise.parcels.features.length] }" @pagination="actionOnPagination"
                  @search="onFilter" searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
                >
                  <template v-if="true" slot="actions">
                      <cv-search :placeholder="$t('graficos.buscar_nombre')" @input="onBuscar"></cv-search>
                  </template>
                  <template v-if="true" slot="batch-actions">
                    <cv-button @click="generaInformeMultiCoop">
                      {{$t("graficos.generar")}}
                      <Analytics20 class="bx--btn__icon" />
                  </cv-button>  
                  </template>
                  <template slot="data" v-for="enterprise in cooperativeSelectObj.enterprises">
                    <cv-data-table-row
                        v-for="feature in enterprise.parcels.features.slice(start, start+length)"
                        :key="`${feature.id}`"
                        :value="`${feature.id}`"
                        :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"
                    >
                        <cv-data-table-cell>{{feature.properties.name}}</cv-data-table-cell>
                        <cv-data-table-cell>{{feature.properties.description}}</cv-data-table-cell>
                        <cv-data-table-cell>{{metricaparcelaCoop(feature.properties.area, enterprise)}}</cv-data-table-cell>
                        <cv-data-table-cell>{{enterprise.name}}</cv-data-table-cell>
                    </cv-data-table-row>
                  </template>
                </cv-data-table>
            <!--EndDataTable-->
              </div>
            </div>
          </div>
          <br><br>
        </div>
        <div class="bx--row">
          <div class="bx--col-sm-1 bx--col-md-2 bx--col-lg-12">
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
        <template slot="title">{{this.$t('graficos.grafico_tipo_dos')}}</template>
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
import SentImage from '@/components/charts/imageSent.vue'
import ChartBar from '@/components/charts/chartBar.vue'
import TableColors from '@/components/charts/tableColors.vue'
import AlertaGeneral from "@/components/AlertaGeneral";
import ChartBarMois from '@/components/charts/chartBarMois.vue'
import ChartLineMois from '@/components/charts/chartLineMois.vue'
import TableColorsMois from '@/components/charts/tableColorsMois.vue'
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
      verGraficNDVI: false,
      verGraficMois: false,
      verImagenSent: false,
      nombreInformeT2: '',
      sortable: false,
      start: 0,
      length: 10,
      columns3: [
            {
            key: "name",
            label: this.$t('graficos.nombre'),
            },
            {
            key: "description",
            label: this.$t('graficos.descrip')
            },
            {
            key: "heactareas",
            label: this.$t('graficos.hectareas'),
            },
        ],
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
      labelLayers: 'Sentinel Layers',
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
      fechasSentinel: Array,
      numImages: 0,
      historicoAnterior: Array(),
      columnsHistorico: [
        this.$t('graficos.parcelas'),
        this.$t('graficos.rang_fechas')
      ],
      parcelasSelecc: Array(),
      polygonsSelecc: Array(),
      busqueda: ``,
      columa: ``,
      ordena: ``,
      fechaGenerar: ``,
      parcelasSeleccionadasId: Array(),
      //multiempresa
      esCooperative: false,

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
                     console.log(acre.toFixed(4));
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
    formateaHectareas(area){
      return Math.round((area + Number.EPSILON) * 100) / 100
    },
    chageFecha(date){
      this.fechaGenerar = date
    },
    chageCapas(capa){
      this.SentinelLayer = capa
    },
    onBuscar(search){
            this.busqueda = search
            const path = `${this.$apiURL}/enterprises/${this.enterprise.id}/?size=1000000000&page=1&parcel_mame=${search}&colum_name=${this.columa}&order=${this.ordena}`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                this.enterprise.parcels.features = response.data.parcels.features;
            })
            .catch(error => {
                console.warn(error)
            })
        },
    onSort(order) {
          const index = order.index
          let column = ``
          const orden = order.order
          
          switch (index) {
              case '0':
                  column = `name`
                  break
              case '1':
                  column = `name`
                  break
              case '2':
                  column = 'area'
                  break
              case '3':
                  column = 'area'
                  break
              default:
                  column = `name`
          }
          console.info(column, order)
          
      },
    actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
    generaInforme(){
      const rowSeleccionados = this.$refs.tableLstadoT2.selectedRows
      this.parcelasSeleccionadasId = rowSeleccionados
      this.parcelasSelecc = Array()
      this.urlSentinel = Array()
      this.polygonsSelecc = Array()
      rowSeleccionados.map(parcel =>{
        this.actionChangeParcels(parcel)
        const parcelaSelect = this.enterprise.parcels.features.filter((parcela)=>{
            return parcela.id == parcel
        })
        this.parcelasSelecc.push(parcelaSelect[0].properties.name)
      }) 
      this.toProcesar(this.urlSentinel, this.parcelasSelecc)
    },
    generaInformeMultiCoop(){
      const selecionado = this.$refs.tableLstadoT2MultiCoop.selectedRows
      this.parcelasSeleccionadasId = selecionado
      const empresasininforme = []
      this.parcelasSelecc = Array()
      this.urlSentinel = Array()
      this.enterprisesList.filter(empresa => {
        empresa.parcels.features.map(parcel => {
          if(selecionado.includes(String(parcel.id))){
            this.actionChangeParcelsPoligon(parcel)
            this.parcelasSelecc.push(parcel.properties.name)
            empresasininforme.push(empresa.id)
          }
        })
      })
      const unicos = empresasininforme.filter((valor, indice) => {
          return empresasininforme.indexOf(valor) === indice;
        }
      );
      if(unicos.length > 1){
        this.toProcesar2(this.urlSentinel, this.parcelasSelecc, true, '')
      }else{
        this.toProcesar2(this.urlSentinel, this.parcelasSelecc, false, unicos[0])
      }
      
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
        this.empresaSelect = empresa
        if(empresa == 'all'){
          this.montarMapaAllCoopParcels()
        }else{
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
      { //GEneramos el poligono
        const result = this.enterprise.parcels.features.filter(feature => feature.id == valor)
        this.idParcela = valor
        const polygon = L.polygon(result[0].geometry.coordinates)
        this.poligonoSelect = result[0].geometry.coordinates
        const bboxP = `${polygon.getBounds()._northEast.lng},${polygon.getBounds()._northEast.lat},${polygon.getBounds()._southWest.lng},${polygon.getBounds()._southWest.lat}`
        this.bbox = bboxP
        this.urlSentinel.push(bboxP)
        this.polygonsSelecc.push(this.poligonoSelect)
        //this.cargaFechasSentinel()
      }
    },
    actionChangeParcelsPoligon(valor){
      { //GEneramos el poligono
        const result = [valor]
        const polygon = L.polygon(result[0].geometry.coordinates)
        this.poligonoSelect = result[0].geometry.coordinates
        const bboxP = `${polygon.getBounds()._northEast.lng},${polygon.getBounds()._northEast.lat},${polygon.getBounds()._southWest.lng},${polygon.getBounds()._southWest.lat}`
        this.bbox = bboxP
        this.urlSentinel.push(bboxP)
        this.polygonsSelecc.push(this.poligonoSelect)
        //this.cargaFechasSentinel()
      }
    },
    ultimaFechaSentinel(bbox){
      var MyDate = new Date();
      var MyDateString;
      MyDate.setDate(MyDate.getDate());
      MyDateString = ('0' + MyDate.getDate()).slice(-2) + '/' + ('0' + (MyDate.getMonth()+1)).slice(-2)
      MyDateString = MyDate.getFullYear()+'-'+('0' + (MyDate.getMonth()+1)).slice(-2)+'-'+('0' + MyDate.getDate()).slice(-2)
      const instanceIns = axios.create({
          baseURL: this.$sentinelURL
      })
      instanceIns.get(`/ogc/wfs/42df6c24-6d29-4259-9093-15ef7d3347a5?REQUEST=GetFeature&TYPENAMES=S2.TILE&OUTPUTFORMAT=application/json&TIME=2020-01-01/${MyDateString}&BBOX=${bbox}&SRSNAME=EPSG:4326`).then(resp => {
          if(resp.status != 200){
              console.warn(resp)
          }else{
            const respuesta = resp.data.features
            this.urlSentinel.push(`https://services.sentinel-hub.com/ogc/wms/42df6c24-6d29-4259-9093-15ef7d3347a5?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS=NDVI&TIME=${respuesta[0].properties.date}&CRS=EPSG%3A4326&WIDTH=2248&HEIGHT=1449&BBOX=${this.bbox}`)
          }
      })
    },
    cargaFechasSentinel(){
      const instanceIns = axios.create({
          baseURL: this.$sentinelURL
      })
      instanceIns.get(`/ogc/wfs/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?REQUEST=GetFeature&TYPENAMES=S2.TILE&OUTPUTFORMAT=application/json&TIME=${this.time}&BBOX=${this.bbox}&SRSNAME=EPSG:4326`).then(resp => {
          if(resp.status != 200){
              console.warn(resp)
          }else{
              /*
              console.log("compoenente 1")
              const respuesta = resp.data.features
              const fechasArray = Array()
              respuesta.forEach(feature =>{
                  fechasArray.push(feature.properties.date)
              })
              this.valueDates = fechasArray.reverse()
              */
              //const respuesta = resp.data.features
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
                  'name': `Polygons4Graficos`,
                  "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                  "additionalData": {
                      "showLogo": false,
                      "showWarnings": false,
                      "imageQuality": 30,
                      "disabled": false
                  },
                  'areaOfInterest': {
                      'type': "Polygon",
                      'coordinates': this.poligonoSelect
                      ,"crs": {
                          "type": "name",
                          "properties": {
                              "name": "urn:ogc:def:crs:EPSG::4326"
                          }
                      }
                  }
              })
              instanceIns.put("/configuration/v1/wms/instances/42df6c24-6d29-4259-9093-15ef7d3347a5", bodyIns, configIns).then(resp => {
                  if(resp.status != 200){
                      console.warn(resp)
                      this.$parent.isActiveLoading2 = false
                  }else{
                    /*
                    const fechasArray = Array()
                    respuesta.forEach(feature =>{
                        fechasArray.push(feature.properties.date)
                    })
                    const urlSentinell = Array()
                    const fechasSentinell = Array()
                    fechasArray.reverse().forEach(fecha =>{
                      urlSentinell.push(`https://services.sentinel-hub.com/ogc/wms/42df6c24-6d29-4259-9093-15ef7d3347a5?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS=NDVI&TIME=${fecha}&CRS=EPSG%3A4326&WIDTH=2248&HEIGHT=1449&BBOX=${this.bbox}`)
                      fechasSentinell.push(fecha)
                    })
                    let uniqueFechas = [...new Set(fechasSentinell)];
                    this.numImages = uniqueFechas.length
                    
                    this.urlSentinel = urlSentinell
                    this.fechasSentinel = fechasSentinell
                    */
                  }
              })
              
          }
      })
    },
    toProcesar(arrURL, fechasSentinel){
      setTimeout(() => {
        //this.isActiveLoading = true
        let path = `${this.$apiURL}/procesadot2/`
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .post(path, {
          parcela: this.nombreInformeT2 ? this.nombreInformeT2 : '0',
          urlSentinel: arrURL, //arr url
          fechas: fechasSentinel, //Arr parcelas
          polygon: this.polygonsSelecc,
          enterprise_id: this.enterprise.id,
          capa: this.SentinelLayer,
          fechaElegida: this.fechaGenerar,
          id_parcelas: this.parcelasSeleccionadasId,
          esCooperative: false
        })
        .catch(() =>{
        })
      }, 1000);
      this.$refs.modal_procesando.show()
    },
    toProcesar2(arrURL, fechasSentinel, esCooperative, empresa_id){
      setTimeout(() => {
        //this.isActiveLoading = true
        let path = `${this.$apiURL}/procesadot2/`
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .post(path, {
          parcela: this.nombreInformeT2 ? this.nombreInformeT2 : '0',
          urlSentinel: arrURL, //arr url
          fechas: fechasSentinel, //Arr parcelas
          polygon: this.polygonsSelecc,
          enterprise_id: !esCooperative ? empresa_id : (this.mostarListaParcelsCoops == true ? this.cooperativeSelectObj.id : sessionStorage.getItem('enterprise')),
          capa: this.SentinelLayer,
          fechaElegida: this.fechaGenerar,
          id_parcelas: this.parcelasSeleccionadasId,
          esCooperative: esCooperative
        })
        .catch(() =>{
        })
      }, 1000);
      this.$refs.modal_procesando.show()
    },
    init(){
      this.isActiveLoading = true
      this.ketComponentDate +=1
      //let path = `${this.$apiURL}/enterprises/${sessionStorage.getItem('enterprise')}/?size=${this.pageSize}&page=${this.pagePar}`
      let path = `${this.$apiURL}/enterprises/${sessionStorage.getItem('enterprise')}/?size=1000000000&page=${this.pagePar}`
      if(sessionStorage.getItem('is_superuser') == 'true' || sessionStorage.getItem('is_systemadmin') == 'true'){
          this.mostrarListaEmpresas = true
          this.mostrarListaCooperativas = true
          getAllCooperatives()
          .then(response => this.cooperativesList = response.data)
          if(this.empresaSelect){
              //path = `${this.$apiURL}/enterprises/${this.empresaSelect}/?size=${this.pageSize}&page=${this.pagePar}`
              path = `${this.$apiURL}/enterprises/${this.empresaSelect}/?size=1000000000&page=${this.pagePar}`
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
          this.$session.set('is_coop_user', response.data.cooperative_user)
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
    this.getInformesAnteriores()
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