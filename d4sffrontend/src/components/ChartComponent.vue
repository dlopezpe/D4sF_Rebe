<template>
    <div class="Graficos">
      <div class="bx--grid">
        <div class="bx--row">
          <div class="bx--col-sm-1 bx--col-md-2 bx--col-lg-4">
            <cv-loading
            :small="true"
            :active="isActiveLoading"
            :overlay="true" v-if="isVisibleLoad"></cv-loading>
            <cv-loading
            :small="true"
            :active="isActiveLoading2"
            :overlay="true" v-if="isVisibleLoad2"></cv-loading>
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
            <div style="">
              <cv-pagination
                    backwards-text="Previous page"
                    forwards-text="Next page"
                    page-sizes-label="Por Página"
                    :page-sizes="[60, 90, 120, 150, 180, {label: `total(${totalParcelas})`, value: totalParcelas}]"
                    :isLastPage="true"
                    :forwards-button-disabled="false" @change="changePaginacion"></cv-pagination>
            </div>
            <br>
            <div id="sentinelLayers">
                <cv-dropdown 
                    :placeholder="placeholderLayers" 
                    @change="actionChangeLayers" :label="labelLayers">
                        <cv-dropdown-item v-for="layer in layersSentinel" :value="layer.id" v-bind:key="layer.id" :selected="layer.id == 'AGRICULTURE'">{{layer.title}}</cv-dropdown-item>
                </cv-dropdown>
            </div>
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
            <SentImage :polygon="poligonoSelect" :sentinelLay="SentinelLayer" :rangeTime="time" :key="keyComponent"/>
          </div>
          <div class="bx--col-sm-1 bx--col-md-2 bx--col-lg-8">
            <ChartLine :bbox="bbox" :sentinelLay="SentinelLayer" :rangeTime="time" :key="keyComponent"/>
            <br>
            <ChartRadar :bbox="bbox" :sentinelLay="SentinelLayer" :rangeTime="time" :key="keyComponent"/>
            <br>
            <ChartBar :bbox="bbox" :sentinelLay="SentinelLayer" :rangeTime="time" :key="keyComponent"/>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
import axios from "axios";
import L from 'leaflet'
import ChartLine from '@/components/charts/chartLine.vue'
import ChartRadar from '@/components/charts/chartRadar.vue'
import ChartBar from '@/components/charts/chartBar.vue'
import SentImage from '@/components/charts/imageSent.vue'

export default {
  name: 'CartCompoent',
  components: {
      ChartLine,
      ChartRadar,
      ChartBar,
      SentImage
  },
  data () {
    return{
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
      SentinelLayer: 'AGRICULTURE',
      dateLabel:"Fecha Inicio",
      dateEndLabel: "Fecha Fin",
      calOptions: {
        dateFormat: "Y-m-d"
      },
      valueRange: ``,
      time: '',
      ketComponentDate: 0,
      poligonoSelect: Array()
    }
  },
  
  methods:{
    actionChangeDateRange(range){
      this.time = `${range.startDate}/${range.endDate}`
      this.keyComponent +=1
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
      const polygon = L.polygon(result[0].geometry.coordinates)
      this.poligonoSelect = result[0].geometry.coordinates
      const bboxP = `${polygon.getBounds()._northEast.lng},${polygon.getBounds()._northEast.lat},${polygon.getBounds()._southWest.lng},${polygon.getBounds()._southWest.lat}`
      this.bbox = bboxP
      this.keyComponent +=1
    },

    init(){
      this.isActiveLoading = true
      let date = new Date()

      let day = date.getDate()
      let month = date.getMonth() + 1
      let year = date.getFullYear()
      this.valueRange = ``
      if(month < 10){
        this.time = `${year}-0${month}-${day}`
      }else{
        this.time = `${year}-${month}-${day}`
      } 
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
        const MyDate = new Date();
        let MyDateString;
        MyDate.setDate(MyDate.getDate() + 20);
        MyDateString = (MyDate.getFullYear()+ '-' + ('0' + (MyDate.getMonth()+1)).slice(-2) +'-'+'0' + MyDate.getDate()).slice(-2);
        this.time = "2019-01-01/"+MyDateString
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
  },
  mounted () {
    this.getDatosUser()
    this.$parent.$parent.is_superuser = true
    this.$parent.$parent.is_superuser = false,
    this.$parent.$parent.is_staff = false,
    this.$parent.$parent.is_systemadmin = false,
    this.$parent.$parent.is_enterpriseadmin = false
  }
}
</script>