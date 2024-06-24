<template>
    <div class="Graficos">
      <div class="bx--grid" style="padding-left: 1rem!important; padding-right: 1rem!important;max-width: 100%!important;">
        <div class="bx--row">
          <div class="bx--col-sm-12 bx--col-md-2 bx--col-lg-3">
            <h3>Generar Gráfico Tipo 1 PP</h3>
            <cv-loading
            :small="true"
            :active="isActiveLoading"
            :overlay="true" v-if="isVisibleLoad"></cv-loading>
            <cv-loading
            :small="true"
            :active="isActiveLoading2"
            :overlay="true" v-if="isVisibleLoad2"></cv-loading>
            <br><br>
            <div v-if="mostrarListaEmpresas" id="sentinelLayers">
                <cv-select
                    theme=""
                    label="Listado de empresas"
                    :hide-label="false"
                    :inline="false"
                    :disabled="false"
                    @change="seleccionaEmpresa">
                    <cv-select-option disabled selected hidden>Selecciona una Empresa</cv-select-option>
                    <cv-select-option v-for="empresa in enterprisesList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                        {{empresa.name}}
                    </cv-select-option>
                </cv-select>
            </div>
            <div style="overflow-y: scroll;max-height: 500px;">
              <cv-structured-list selectable id="parcelList">
                    <template slot="headings">
                        <cv-structured-list-heading>Parcelas de {{enterprise.name}}</cv-structured-list-heading>
                    </template>
                    <template slot="items">
                        <cv-structured-list-item 
                        v-for="feature in enterprise.parcels.features" 
                        name="group-1" 
                        :value="String(feature.id)" 
                        v-bind:key="feature.id" 
                        :checked="feature.id == 1"
                        @change="actionChangeParcels"
                        ref="listaDeParcelas" >
                            <cv-structured-list-data>{{feature.properties.name}}</cv-structured-list-data>
                        </cv-structured-list-item>
                    </template>
                </cv-structured-list>
                
            </div>
            <div >
              <cv-pagination
                    backwards-text="Previous page"
                    forwards-text="Next page"
                    page-sizes-label="Por Página"
                    :page-sizes="[60, 90, 120, 150, 180, {label: `total(${totalParcelas})`, value: totalParcelas}]"
                    :isLastPage="true"
                    :forwards-button-disabled="false" @change="changePaginacion" style="overflow-x: scroll;"></cv-pagination>
            </div>
            <br>
            <br>
            <div>
              <cv-select label="Selecciona una Capa" @change="chageCapas">
                <cv-select-option selected value="NDVI">NDVI</cv-select-option>
                <cv-select-option value="MOISTURE_INDEX">MOISTURE INDEX</cv-select-option>
              </cv-select>
            </div>
            <br>
            <br>
            <div id="sentinelDate">
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
                  :dateLabel="dateLabel"
                  :date-end-label="dateEndLabel"
                  :cal-options="calOptions"
                  @change="actionChangeDateRange"
                  :value="valueRange" :key="ketComponentDate">
                  </cv-date-picker>
            </div>
            <br>
            <div>
              <p>Imagenes por Generar: {{numImages}}</p>
            </div>
            <br>
            <div>
              <cv-button
                kind="primary"
                size=""
                :disabled="false"
                @click="generaInforme"
              >
                Generar Informe
              </cv-button>
            </div>
            <br>
          </div>
          <div class="bx--col-sm-12 bx--col-md-2 bx--col-lg-9">
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
      mensajeAlerta: ``,
      tipoAlerta: `error`,
      isActiveLoading: false,
      isVisibleLoad: true,
      isActiveLoading2: false,
      isVisibleLoad2: true,
      mostrarListaEmpresas: false,
      enterprisesList: Array(),
      enterprise: Object(),
      layersSentinel: Array(),
      placeholderLayers: 'Selecciona un Layer de Sentinel',
      labelLayers: 'Sentinel Layers',
      totalParcelas: 0,
      pageSize: 60,
      pagePar: 1,
      bbox: '',
      keyComponent: 0,
      SentinelLayer: 'NDVI',
      dateLabel:"Fecha Inicio",
      dateEndLabel: "Fecha Fin",
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
        "Parcela",
        "Rango de Fechas"
      ]
    }
  },
  
  methods:{

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
        this.empresaSelect = empresa
        this.init()
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
      const result = this.enterprise.parcels.features.filter(feature => feature.id == valor)

      this.idParcela = valor
      const polygon = L.polygon(result[0].geometry.coordinates)
      this.poligonoSelect = result[0].geometry.coordinates
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
              console.log("compoenente 2")
              /*
              const respuesta = resp.data.features
              const fechasArray = Array()
              respuesta.forEach(feature =>{
                  fechasArray.push(feature.properties.date)
              })
              this.valueDates = fechasArray.reverse()
              */
              const respuesta = resp.data.features
              const instanceIns = axios.create({
                  baseURL: this.$sentinelURL
              })
              const configIns = {
                  headers: {
                      'Content-Type': 'application/json;charset=utf-8',
                      'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
                  }
              }
              let layer = JSON.stringify({})
              if(this.SentinelLayer == 'NDVI'){
                layer = JSON.stringify({
                  'id': 'NDVI',
                  'title': 'NDVI (Normalized Difference Vegetation Index)',
                  'description': 'Value = colorMap((B08 - B04) / (B08 + B04))',
                  'styles': [
                      {
                          'name': 'default',
                          'description': 'Default layer style',
                          'dataProduct': {
                              '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/256'
                          }
                      }
                  ],
                  'orderHint': 34,
                  'dataset': {
                      '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C'
                  },
                  'datasetSource': {
                      '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1'
                  },
                  'defaultStyleName': 'default',
                  'datasourceDefaults': {
                      'upsampling': 'BICUBIC',
                      'mosaickingOrder': 'mostRecent',
                      'temporal': false,
                      'maxCloudCoverage': 20.0,
                      'previewMode': 'PREVIEW',
                      'type': 'S2L1C'
                  }
                })
              }else{
                layer = JSON.stringify({
                  "id": "MOISTURE_INDEX",
                  "title": "Moisture Index",
                  "description": "Based on combination of bands (B8A - B11)/(B8A + B11)",
                  "styles": [
                      {
                          "name": "default",
                          "dataProduct": {
                              "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/425"
                          }
                      }
                  ],
                  "orderHint": 6,
                  "dataset": {
                      "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                  },
                  "datasetSource": {
                      "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
                  },
                  "defaultStyleName": "default",
                  "datasourceDefaults": {
                      "upsampling": "BICUBIC",
                      "mosaickingOrder": "mostRecent",
                      "temporal": false,
                      "maxCloudCoverage": 20.0,
                      "previewMode": "PREVIEW",
                      "type": "S2L1C"
                  }
                })
              }
              
              
              const bodyIns = JSON.stringify({
                  'name': `Polygons4GraficosType1Tmp`,
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
              instanceIns.post('/configuration/v1/wms/instances', bodyIns, configIns).then(resp =>{
                if(resp.statusText == "Created" || resp.status == 201){
                  //Obtenemos el id de la instancia
                  const idInstTmp = resp.data.id
                  //hacemos un put de las layers que queremos que tenga la ins
                  instanceIns.post(`/configuration/v1/wms/instances/${idInstTmp}/layers`, layer, configIns).then(respL => {
                    if(respL.statusText == "Created" || respL.status == 201){
                      const fechasArray = Array()
                      respuesta.forEach(feature =>{
                          fechasArray.push(feature.properties.date)
                      })
                      const urlSentinell = Array()
                      const fechasSentinell = Array()
                      fechasArray.reverse().forEach(fecha =>{
                        urlSentinell.push(`https://services.sentinel-hub.com/ogc/wms/${idInstTmp}?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS=${this.SentinelLayer}&TIME=${fecha}&CRS=EPSG%3A4326&WIDTH=2248&HEIGHT=1449&BBOX=${this.bbox}`)
                        fechasSentinell.push(fecha)
                      })
                      let uniqueFechas = [...new Set(fechasSentinell)];
                      this.numImages = uniqueFechas.length
                      this.urlSentinel = urlSentinell
                      this.fechasSentinel = fechasSentinell
                      this.instSentTmp = idInstTmp
                      }
                  })
                }
              })
              /*
              instanceIns.put("/configuration/v1/wms/instances/42df6c24-6d29-4259-9093-15ef7d3347a5", bodyIns, configIns).then(resp => {
                  if(resp.status != 200){
                      console.warn(resp)
                      this.$parent.isActiveLoading2 = false
                  }else{
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
                    
                  }
              })
              */
          }
      })
    },
    toProcesar(arrURL, fechasSentinel){
      setTimeout(() => {
        let uniqueFechas = [...new Set(fechasSentinel)];
        let uniqueURL = [...new Set(arrURL)];
        this.isActiveLoading = true
        let path = `${this.$apiURL}/procesado/`
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .post(path, {
          parcela: this.idParcela,
          urlSentinel: uniqueURL,
          fechas: uniqueFechas,
          enterprise_id: this.enterprise.id,
          capa: this.SentinelLayer
        })
        .then(response => {
          this.dataSent = response.data
          
          this.isActiveLoading = false
          this.mensajeAlerta = `Informe generado correctamente`
          this.tipoAlerta = 'success'
          //Eliminacion de la instancia del sentinel
          const instanceIns = axios.create({
              baseURL: this.$sentinelURL
          })
          const configIns = {
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
            }
          }
          instanceIns.delete(`/configuration/v1/wms/instances/${this.instSentTmp}`, configIns).then(resp =>{
            console.info(resp)
          })
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
        .catch(() =>{
          this.isActiveLoading = false
          this.mensajeAlerta = `Ha ocurrido un error, intentelo más tarde`
          this.tipoAlerta = 'error'
          this.$refs.alertaGeneral.verAlerta()
        })
      }, 1000);
    },
    init(){
      this.isActiveLoading = true
      this.ketComponentDate +=1
      let path = `${this.$apiURL}/enterprises/${sessionStorage.getItem('enterprise')}/?size=${this.pageSize}&page=${this.pagePar}`
      if(sessionStorage.getItem('is_superuser') == 'true' || sessionStorage.getItem('is_systemadmin') == 'true'){
          this.mostrarListaEmpresas = true
          if(this.empresaSelect){
              path = `${this.$apiURL}/enterprises/${this.empresaSelect}/?size=${this.pageSize}&page=${this.pagePar}`
          }else{
              path = `${this.$apiURL}/enterprises/`
          }
      }
      axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
      axios
      .get(path)
      .then(response => { 
          if(response.data.length){
              this.enterprisesList = response.data
              this.enterprise = response.data[0]
              this.stepTwoMap()
          }else{
              this.enterprise = response.data
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
    this.getDatosUser()
    this.getInformesAnteriores()
    this.$parent.$parent.is_superuser = true
    this.$parent.$parent.is_superuser = false,
    this.$parent.$parent.is_staff = false,
    this.$parent.$parent.is_systemadmin = false,
    this.$parent.$parent.is_enterpriseadmin = false
  },
  created(){
    this.getDatosUser()
    this.$parent.$parent.is_superuser = true
    this.$parent.$parent.is_superuser = false,
    this.$parent.$parent.is_staff = false,
    this.$parent.$parent.is_systemadmin = false,
    this.$parent.$parent.is_enterpriseadmin = false
  }
}
</script>