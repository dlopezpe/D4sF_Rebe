<template>
    <div class="bx--grid">
        <cv-tabs :container="false" aria-label="navigation tab label">
            <!--
            <cv-tab :label="$t('graficos.grafico_tipo_uno')">
                <br>
                <br>
                <GraficoT1Controller
                    v-if="flagIndicatingDataHasBeenLoadedInVariables"
                    :arr-enterprises="arrEmpresas"
                    :arr-cooperativas="arrCooperativas"
                    :is_superuser="is_superuser"
                    :is_systemadmin="is_systemadmin"
                    :is_staff="is_staff"
                    :is_enterpriseadmin="is_enterpriseadmin"
                    :is_coop_user="is_coop_user"
                    :all-parcels-of-enterprises="allParcelsOfEnterprises"
                    :all-parcels-of-enterprises-filter="allParcelsOfEnterprisesFilter"

                    v-on:setCenter="center = $event"  
                    v-on:setToggleMostrarTexto="checkedToggleMostarTexto = $event"
                    v-on:setEnterprise="arrEmpresas = $event"
                    v-on:setSentinelLayer="SentinelLayer = $event"
                    v-on:setSentinelOpacity="opacitylayer = $event"
                    v-on:setFechaSentinel="time = $event"
                    v-on:setAllParcelsOfEnterprises="allParcelsOfEnterprises = $event, allParcelsOfEnterprisesFilter = $event"
                />
            </cv-tab>
            <cv-tab :label="$t('graficos.grafico_tipo_dos')">
                <br>
                <br>
                <GraficoT2Controller
                    v-if="flagIndicatingDataHasBeenLoadedInVariables"
                    :arr-enterprises="arrEmpresas"
                    :arr-cooperativas="arrCooperativas"
                    :is_superuser="is_superuser"
                    :is_systemadmin="is_systemadmin"
                    :is_staff="is_staff"
                    :is_enterpriseadmin="is_enterpriseadmin"
                    :is_coop_user="is_coop_user"
                    
                    :all-parcels-of-enterprises="allParcelsOfEnterprises"
                    :all-parcels-of-enterprises-filter="allParcelsOfEnterprisesFilter"
                    v-on:setEnterprise="arrEmpresas = $event"
                    v-on:setAllParcelsOfEnterprises="allParcelsOfEnterprises = $event, allParcelsOfEnterprisesFilter = $event"
                />
            </cv-tab>
            -->
            <cv-tab :label="$t('graficos.grafico_ant')" >
                <br>
                <br>
                <div class="bx--grid" v-if="flagIndicatingDataHasBeenLoadedInVariables">
                    <div class="bx--row">
                        <div class="bx--col">
                            <h3>{{$t("graficos.grafico_ant")}}</h3>
                        </div>
                    </div>
                    <br>
                    <div class="bx--row">
                        <div class="bx--col">
                            <GraficosAnterioresController 
                                v-if="flagIndicatingDataHasBeenLoadedInVariables && is_superuser || is_systemadmin || is_coop_user"
                                :arr-enterprises="arrEmpresas"
                                :arr-cooperativas="arrCooperativas"
                                :is_superuser="is_superuser"
                                :is_systemadmin="is_systemadmin"
                                :is_staff="is_staff"
                                :is_enterpriseadmin="is_enterpriseadmin"
                                :is_coop_user="is_coop_user"
                                :all-parcels-of-enterprises="allParcelsOfEnterprises"
                                :all-parcels-of-enterprises-filter="allParcelsOfEnterprisesFilter"

                                v-on:setEnterprise="arrEmpresas = $event"
                                v-on:setAllParcelsOfEnterprises="allParcelsOfEnterprises = $event, allParcelsOfEnterprisesFilter = $event"
                                v-on:setEmpresaSeleccionadaObj ="empresaSeleccionadaObj = $event"
                                v-on:setGetGraficosAnteriores ="getInformesAnteriores($event)"
                                v-on:setCooperativaSeleccionadaObj ="cooperativaSeleccionadaObj = $event"
                                v-on:setGetGraficosAnterioresCoop ="getInformesAnterioresCoop($event)"
                            />
                        </div>
                    </div>
                    <br>
                    
                    <div class="bx--row" v-if="Object.keys(cooperativaSeleccionadaObj).length == 0">
                        <div class="bx--col">
                            <div id="sentinelLayersList">
                                <h4>{{$t("graficos.inform_ant_de")}} {{empresaSeleccionadaObj.name}}</h4>
                                <cv-data-table
                                    @sort="onSort"
                                    @row-select-changes="agruparCompatible"
                                    :pagination="{ numberOfItems: historicoAnterior.length, pageSizes: [10, 15, 20, 25, historicoAnterior.length] }" @pagination="actionOnPagination"
                                    :columns="[
                                        this.$t('graficos.parcela'),
                                        this.$t('graficos.rango_fechas_sel'),
                                        {
                                            'label': this.$t('graficos.creado'),
                                            'sortable': true
                                        },
                                        {
                                            'label': this.$t('graficos.tipo'),
                                            'sortable': true
                                        },
                                        {
                                            'label': this.$t('graficos.capa'),
                                            'sortable': true
                                        },
                                        {
                                            key: '',
                                            label: ''
                                        },
                                    ]"
                                    ref="tableHist" :key="componentTableHist"
                                >
                                    <template v-if="true" slot="batch-actions" >
                                        <cv-button @click="showModificarInformes" v-if="showUnificar">
                                            {{$t("graficos.unificar_informes")}}
                                            <AppConnectivity32 class="bx--btn__icon"/>
                                        </cv-button>
                                        <cv-button @click="showEditarInforme" v-if="showEditar">
                                            {{$t("graficos.editar")}}
                                            <Edit32 class="bx--btn__icon" />
                                        </cv-button>
                                        <cv-button @click="verDatos">
                                            {{$t("graficos.ver_datos")}}
                                            <Charbar20 class="bx--btn__icon"/>
                                        </cv-button>
                                        <cv-button @click="descargaExcel" v-if="true">
                                            {{$t("graficos.desc_excel")}}
                                            <Download16 class="bx--btn__icon"/>
                                        </cv-button>
                                        <cv-button @click="delInforme">
                                            {{$t("graficos.del_informe")}}
                                            <TrashCan32 class="bx--btn__icon" />
                                        </cv-button>
                                    </template>
                                    <template slot="data">
                                        <cv-data-table-row  v-for="historico in historicoAnterior.slice(start, start+length)" @click="verDatos" :value="String(historico.id)" :key="String(historico.id)">
                                            <cv-data-table-cell v-if="historico.tipo == 1 && !historico.alias">
                                                {{parcelaName(historico.parcela)}} - {{historico.alias}}
                                            </cv-data-table-cell>
                                            <cv-data-table-cell v-else-if="historico.tipo == 1 && historico.alias">
                                                {{historico.alias}}
                                            </cv-data-table-cell>
                                            <cv-data-table-cell v-else>
                                                {{historico.parcela}}
                                            </cv-data-table-cell>
                                            <cv-data-table-cell>
                                                {{historico.finifin}}
                                            </cv-data-table-cell>
                                            <cv-data-table-cell>
                                                {{dateFormat(historico.created)}}
                                            </cv-data-table-cell>
                                            <cv-data-table-cell>
                                                {{$t("graficos.grafico_tipo")}} {{historico.tipo}}
                                            </cv-data-table-cell>
                                            <cv-data-table-cell>
                                                {{historico.capa}}
                                            </cv-data-table-cell>
                                        </cv-data-table-row>
                                    </template>
                                </cv-data-table>
                            </div>
                        </div>
                    </div>
                    <div class="bx--row" v-if="Object.keys(cooperativaSeleccionadaObj).length != 0">
                        <div class="bx--col" >
                            <h4>Gáficos Anteriores de la Cooperativa {{cooperativaSeleccionadaObj.name}}</h4>
                            <cv-data-table
                                @sort="onSort"
                                @row-select-changes="agruparCompatible"
                                :pagination="{ numberOfItems: historicoAnteriorCoop.length, pageSizes: [10, 15, 20, 25, historicoAnteriorCoop.length] }" @pagination="actionOnPagination2"
                                :columns="[
                                    this.$t('graficos.parcela'),
                                    this.$t('graficos.rango_fechas_sel'), 
                                    {
                                        'label': this.$t('graficos.creado'),
                                        'sortable': true
                                    },
                                    {
                                        'label': this.$t('graficos.tipo'),
                                        'sortable': true
                                    },
                                    {
                                        'label': this.$t('graficos.capa'),
                                        'sortable': true
                                    },
                                    {
                                        key: '',
                                        label: ''
                                    },
                                ]"  ref="tableHist2" :key="componentTableHist2">
                                <template v-if="true" slot="batch-actions" >
                                    <cv-button @click="verDatos2">
                                        {{$t("graficos.ver_datos")}}
                                        <Charbar20 class="bx--btn__icon"/>
                                    </cv-button>
                                    <cv-button @click="descargaExcel2" v-if="true">
                                        {{$t("graficos.desc_excel")}}
                                        <Download16 class="bx--btn__icon"/>
                                    </cv-button>
                                    <cv-button @click="delInforme2">
                                        {{$t("graficos.del_informe")}}
                                        <TrashCan32 class="bx--btn__icon" />
                                    </cv-button>
                                </template>
                                <template slot="data">
                                    <cv-data-table-row  v-for="historico in historicoAnteriorCoop.slice(start2, start2+length2)" @click="verDatos" :value="String(historico.id)" :key="String(historico.id)">
                                        <cv-data-table-cell v-if="historico.tipo == 1 && !historico.alias">
                                            {{parcelaName(historico.parcela)}}
                                        </cv-data-table-cell>
                                        <cv-data-table-cell v-else-if="historico.tipo == 1 && historico.alias">
                                            {{historico.alias}}
                                        </cv-data-table-cell>
                                        <cv-data-table-cell v-else>
                                            {{historico.parcela}}
                                        </cv-data-table-cell>
                                        <cv-data-table-cell>
                                            {{historico.finifin}}
                                        </cv-data-table-cell>
                                        <cv-data-table-cell>
                                            {{dateFormat(historico.created)}}
                                        </cv-data-table-cell>
                                        <cv-data-table-cell>
                                            {{$t("graficos.grafico_tipo")}} {{historico.tipo}}
                                        </cv-data-table-cell>
                                        <cv-data-table-cell>
                                            {{historico.capa}}
                                        </cv-data-table-cell>
                                        <cv-data-table-cell>
                                            <cv-overflow-menu flip-menu style="margin: 0 auto;">
                                                <cv-overflow-menu-item @click="verDatosRow2(String(historico.id))">{{$t("graficos.ver_datos")}}</cv-overflow-menu-item>
                                                <cv-overflow-menu-item @click="descargaExcelRow2(String(historico.id))">{{$t("graficos.desc_excel")}}</cv-overflow-menu-item>
                                                <cv-overflow-menu-item @click="delInformeRow2(String(historico.id))">{{$t("graficos.del_informe")}}</cv-overflow-menu-item>
                                            </cv-overflow-menu>
                                        </cv-data-table-cell>
                                    </cv-data-table-row>
                                </template>
                            </cv-data-table>
                        </div>
                    </div>
                    <div class="bx--row">
                        <div class="bx--col-sm-12 bx--col-md-12 bx--col-lg-12">
                            <br>
                            <ChartLine :datos="dataSent" :key="keyComponent" v-if="verGraficNDVI"/>
                            <ChartLineMois :datos="dataSent" :key="keyComponent" v-if="verGraficMois"/>
                            <br>
                            <ChartRadar :bbox="bbox" :sentinelLay="SentinelLayer" v-if="false" :rangeTime="time" :key="keyComponent"/>
                            <br>
                            <ChartBar :datos="dataSent" :key="keyComponent" v-if="verGraficNDVI"/>
                            <ChartBarMois :datos="dataSent" :key="keyComponent" v-if="verGraficMois"/>
                            <br>
                            <br>
                            <TableColors :urlMedia="$apiURLMedia" :datos="dataSent" :key="keyComponent" v-if="verGraficNDVI"/>
                            <TableColorsMois :urlMedia="$apiURLMedia" :datos="dataSent" :key="keyComponent" v-if="verGraficMois"/>
                            <br>
                            <SentImage :urlMedia="$apiURLMedia" :datos="dataSent" :key="keyComponent" v-if="verImagenSent"/>
                            <br>
                        </div>
                    </div>
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
                    <AlertaGeneral ref="alertaGenerall" :tituloAlert.sync="mensajeAlerta" :tipoAlert.sync="tipoAlerta" />
                    <UnificarInformes ref="unificarInformes"
                    :informes-sell.sync="informesSell"
                    :informes-seleccionados.sync="informesSell" 
                    :historico.sync="historicoAnterior" 
                    :tipo="tipoInforUni" 
                    :capa="capaInforUni" 
                    :enterpriseID.sync="empresaSeleccionadaObj.id"
                    :all-parcels-of-enterprises="allParcelsOfEnterprises"


                    v-on:mensajeAlerta="mensajeAlerta = $event"
                    v-on:tipoAlerta="tipoAlerta = $event"
                    v-on:verAlerta="$refs.alertaGenerall.verAlerta()"
                    v-on:getInformesAnt="getInformesAnteriores(empresaSeleccionadaObj.id)"
                    
                    />
                    <EditarInforme ref="editarInforme" 
                    :informesSeleccionados.sync="informeSell" 
                    :historico.sync="historicoAnterior"
                    :all-parcels-of-enterprises.sync="allParcelsOfEnterprises"

                    v-on:mensajeAlerta="mensajeAlerta = $event"
                    v-on:tipoAlerta="tipoAlerta = $event"
                    v-on:verAlerta="$refs.alertaGenerall.verAlerta()"
                    
                    v-on:getInformesAnt="getInformesAnteriores(empresaSeleccionadaObj.id)"
                    />
                    <cv-modal
                    ref="alerta_eliminar"
                    kind="danger"
                    @primary-click="eliminarUsuario">
                        <template slot="label">{{$t("graficos.seguro")}}</template>
                        <template slot="title">{{$t("graficos.eliminar")}}</template>
                        <template slot="content">
                        <p>{{$t("graficos.seguro_parcel_del")}}</p>
                        </template>
                        <template slot="secondary-button">{{$t("graficos.cancelar")}}</template>
                        <template slot="primary-button">{{$t("graficos.eliminar")}}</template>
                    </cv-modal>
                    <cv-modal
                    ref="alerta_eliminar2"
                    kind="danger"
                    @primary-click="eliminarUsuario2">
                        <template slot="label">{{$t("graficos.seguro")}}</template>
                        <template slot="title">{{$t("graficos.eliminar")}}</template>
                        <template slot="content">
                        <p>{{$t("graficos.seguro_parcel_del")}}</p>
                        </template>
                        <template slot="secondary-button">{{$t("graficos.cancelar")}}</template>
                        <template slot="primary-button">{{$t("graficos.eliminar")}}</template>
                    </cv-modal>
                    <cv-modal
                    ref="alerta_eliminar3"
                    kind="danger"
                    @primary-click="eliminarUsuario3">
                        <template slot="label">{{$t("graficos.seguro")}}</template>
                        <template slot="title">{{$t("graficos.eliminar")}}</template>
                        <template slot="content">
                        <p>{{$t("graficos.seguro_parcel_del")}}</p>
                        </template>
                        <template slot="secondary-button">{{$t("graficos.cancelar")}}</template>
                        <template slot="primary-button">{{$t("graficos.eliminar")}}</template>
                    </cv-modal>
                    
                </div>
                
            </cv-tab>
        </cv-tabs>
    </div>
</template>

<script>
//import ChartComponent from '@/components/ChartComponentNDVIv2.vue'
import {getProfile, getPermisos} from '@/auth/index'
import {getAllEnterprises, getEnterprise} from '@/crudFunctions/crudEnterprise'//getEnterprise
import {getAllCooperatives, getCooperative} from '@/crudFunctions/crudCooperativas'
//import GraficoT1Controller from '@/components/GraficosTipo/GraficoT1Controller.vue'
//import GraficoT2Controller from '@/components/GraficosTipo/GraficoT2Controller.vue'
import GraficosAnterioresController from '@/components/GraficosTipo/GraficosAnterioresController.vue'

import axios from 'axios'

import AlertaGeneral from "@/components/AlertaGeneral";
import UnificarInformes from "@/components/UnificarInforme.vue";
import EditarInforme from "@/components/EditarInforme.vue";
import ChartLine from '@/components/charts/chartLine.vue'
import ChartLineMois from '@/components/charts/chartLineMois.vue'
import SentImage from '@/components/charts/imageSent.vue'
import ChartBar from '@/components/charts/chartBar.vue'
import ChartBarMois from '@/components/charts/chartBarMois.vue'
import TableColors from '@/components/charts/tableColors.vue'
import TableColorsMois from '@/components/charts/tableColorsMois.vue'
export default {
    name: "GraficosController",
    components: {
        //GraficoT1Controller,
        //GraficoT2Controller,
        GraficosAnterioresController,
        ChartLine,
        SentImage,
        ChartBar,
        TableColors,
        AlertaGeneral,
        ChartLineMois,
        ChartBarMois,
        TableColorsMois,
        UnificarInformes,
        EditarInforme
    },
    data(){
        return {
            flagIndicatingDataHasBeenLoadedInVariables: false,
            //Usuario
            is_superuser: false,
            is_staff: false,
            is_systemadmin: false,
            is_enterpriseadmin: false,
            is_coop_user: false,
            //Empresas sel
            arrEmpresas: [],
            arrCooperativas: [],
            allParcelsOfEnterprises: [],
            allParcelsOfEnterprisesFilter: [],
            //Graficos

            start: 0,
            length: 10,
            start2: 0,
            length2: 10,
            listadoEmpresas: this.arrEnterprises,
            historicoAnterior: Array(),
            historicoAnteriorCoop: Array(),
            columnsHistorico: [
                this.$t('graficos.parcela'),
                this.$t('graficos.rango_fechas_sel'), 
                {
                    'label': this.$t('graficos.creado'),
                    'sortable': true
                },
                {
                    'label': this.$t('graficos.tipo'),
                    'sortable': true
                },
                {
                    'label': this.$t('graficos.capa'),
                    'sortable': true
                },
                {
                    key: "",
                    label: ""
                },
            ],
            showUnificar: false,
            showEditar: false,
            verGraficNDVI: false,
            verGraficMois: false,
            verImagenSent: false,
            informesSell: Array(),
            informeSell: Array(),
            capaInforUni: ``,
            tipoInforUni: ``,
            componentTableHist: 0,
            empresaSeleccionadaID: '',
            empresaSeleccionadaObj: Object(),
            cooperativaSeleccionadaObj: Object(),
            column: 'created',
            orden: 'descending',
            keyComponent: 0,
            mensajeAlerta: ``,
            tipoAlerta: `error`
        }
    },
    methods: {
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        actionOnPagination2(ev){
            this.start2 = ev.start-1
            this.length2 = ev.length
        },
        dateFormat(date){
            const dts = date.split('T')
            return dts[0]
        },
        showEditarInforme(){
            console.info(this.editarInforme)
            this.$refs.editarInforme.openModal()
        },
        verDatosRow(row){
            this.$refs.tableHist.selectedRows.forEach(()=>{
                this.$refs.tableHist.selectedRows.pop()
            })
            this.$refs.tableHist.selectedRows.push(row)
            this.verDatos()
        },
        verDatos(){
            if(this.$refs.tableHist.selectedRows.length != 1){
                this.mensajeAlerta = this.$t('graficos.select_one_informe')
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                return false
            }
            const rowSeleccionado = this.$refs.tableHist.selectedRows;
            let path = `${this.$apiURL}/ver_hist/${rowSeleccionado}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                if(response.data.capa == 'NDVI'){
                    this.verGraficNDVI = true
                    this.verGraficMois = false
                }else{
                    this.verGraficNDVI = false
                    this.verGraficMois = true
                }
                path = `${this.$apiURLMedia}/${response.data.imagen}/`
                axios
                .get(path)
                .then(response => {
                    this.dataSent = response.data
                    this.verImagenSent = true
                    this.keyComponent +=1
                })
            })
            .catch(error =>{
                console.warn(error)
            })
            
        },
        verDatosRow2(row){
            this.$refs.tableHist2.selectedRows.forEach(()=>{
                this.$refs.tableHist2.selectedRows.pop()
            })
            this.$refs.tableHist2.selectedRows.push(row)
            this.verDatos2()
        },
        verDatos2(){
            if(this.$refs.tableHist2.selectedRows.length != 1){
                this.mensajeAlerta = this.$t('graficos.select_one_informe')
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                return false
            }
            const rowSeleccionado = this.$refs.tableHist2.selectedRows;
            let path = `${this.$apiURL}/ver_hist/${rowSeleccionado}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                if(response.data.capa == 'NDVI'){
                    this.verGraficNDVI = true
                    this.verGraficMois = false
                }else{
                    this.verGraficNDVI = false
                    this.verGraficMois = true
                }
                path = `${this.$apiURLMedia}/${response.data.imagen}/`
                axios
                .get(path)
                .then(response => {
                    this.dataSent = response.data
                    this.verImagenSent = true
                    this.keyComponent +=1
                })
            })
            .catch(error =>{
                console.warn(error)
            })
            
        },
        descargaExcelRow(row){
            this.$refs.tableHist.selectedRows.forEach(()=>{
                this.$refs.tableHist.selectedRows.pop()
            })
            this.$refs.tableHist.selectedRows.push(row)
            this.descargaExcel()
        },
        descargaExcel(){
            if(this.$refs.tableHist.selectedRows.length != 1){
                this.mensajeAlerta = this.$t('graficos.select_one_informe')
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                return false
            }
            const rowSeleccionado = this.$refs.tableHist.selectedRows;
            const parcelaSelect = this.historicoAnterior.filter((parcela)=>{
                return parcela.id == rowSeleccionado
            })
            let parcelaname = ``
            if(parcelaSelect[0].alias){
                parcelaname = parcelaSelect[0].alias
            }else{
                parcelaname = (parcelaSelect[0].tipo == 1) ? this.parcelaName(parcelaSelect[0].parcela) : parcelaSelect[0].parcela
            }
            

            window.URL = window.URL || window.webkitURL;
            var xhr = new XMLHttpRequest(),
                a = document.createElement('a'), file;
            xhr.open('GET', `${this.$apiURLMedia}/${parcelaSelect[0].xlsxFile}`, true);
            xhr.responseType = 'blob';
            xhr.onload = function () {
                file = new Blob([xhr.response], { type : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                a.href = window.URL.createObjectURL(file);
                a.download = `${parcelaname}.xlsx`;  // Set to whatever file name you want
                a.click();
            };
            xhr.send();
        },
        descargaExcelRow2(row){
            this.$refs.tableHist2.selectedRows.forEach(()=>{
                this.$refs.tableHist2.selectedRows.pop()
            })
            this.$refs.tableHist2.selectedRows.push(row)
            this.descargaExcel2()
        },
        descargaExcel2(){
            if(this.$refs.tableHist2.selectedRows.length != 1){
                this.mensajeAlerta = this.$t('graficos.select_one_informe')
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                return false
            }
            const rowSeleccionado = this.$refs.tableHist2.selectedRows;
            const parcelaSelect = this.historicoAnteriorCoop.filter((parcela)=>{
                return parcela.id == rowSeleccionado
            })
            let parcelaname = ``
            if(parcelaSelect[0].alias){
                parcelaname = parcelaSelect[0].alias
            }else{
                parcelaname = (parcelaSelect[0].tipo == 1) ? this.parcelaName(parcelaSelect[0].parcela) : parcelaSelect[0].parcela
            }
            

            window.URL = window.URL || window.webkitURL;
            var xhr = new XMLHttpRequest(),
                a = document.createElement('a'), file;
            xhr.open('GET', `${this.$apiURLMedia}/${parcelaSelect[0].xlsxFile}`, true);
            xhr.responseType = 'blob';
            xhr.onload = function () {
                file = new Blob([xhr.response], { type : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                a.href = window.URL.createObjectURL(file);
                a.download = `${parcelaname}.xlsx`;  // Set to whatever file name you want
                a.click();
            };
            xhr.send();
        },
        parcelaName(id){
            const parcelaSelect = this.allParcelsOfEnterprises.filter((parcela)=>{
                return parcela.id == id
            })            
            if(parcelaSelect.length > 0){
                return parcelaSelect[0].properties.name
            }else{
                return 'Gráfico Generado de Parcela Eliminada'
            }
        },
        seleccionaEmpresa(empresa){
            const arrParcels = []
            if(empresa == 'all'){
                getAllEnterprises()
                    .then(async response => {
                        response.data.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        this.arrEmpresas = response.data
                        this.allParcelsOfEnterprises = arrParcels
                        this.empresaSeleccionadaObj = response.data[0]
                        this.getInformesAnteriores(response.data[0].id)
                    })
            }else{
                const result = empresa.split('_')
                if(result[0] == 'coop'){
                    getCooperative(result[1])
                    .then(response => {
                        response.data.enterprises.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        this.arrEmpresas = response.data
                        this.allParcelsOfEnterprises = arrParcels
                        this.empresaSeleccionadaObj = response.data.enterprises[0]
                        this.getInformesAnteriores(response.data.enterprises[0].id)
                        this.cooperativaSeleccionadaObj = response.data
                        this.getInformesAnterioresCoop(response.data.id)
                    })
                }else{
                    getEnterprise(empresa)
                    .then(async response => {
                        response.data.parcels.features.map(parcel => {
                            arrParcels.push(parcel)
                        })
                        this.arrEmpresas = response.data
                        this.allParcelsOfEnterprises = arrParcels
                        this.empresaSeleccionadaObj = response.data
                        this.getInformesAnteriores(response.data.id)
                    })
                }
            }
        },
        delInformeRow(row){
            this.$refs.tableHist.selectedRows.forEach(()=>{
                this.$refs.tableHist.selectedRows.pop()
            })
            this.$refs.tableHist.selectedRows.push(row)
            this.delInforme()
        },
        delInforme(){
            this.$refs.alerta_eliminar.dataVisible = true
        },
        delInformeRow2(row){
            this.$refs.tableHist2.selectedRows.forEach(()=>{
                this.$refs.tableHist2.selectedRows.pop()
            })
            this.$refs.tableHist2.selectedRows.push(row)
            this.delInforme2()
        },
        delInformeRow3(row){
            this.$refs.tableHist2.selectedRows.forEach(()=>{
                this.$refs.tableHist2.selectedRows.pop()
            })
            this.$refs.tableHist2.selectedRows.push(row)
            this.delInforme3()
        },
        delInforme2(){
            this.$refs.alerta_eliminar2.dataVisible = true
        },
        delInforme3(){
            this.$refs.alerta_eliminar3.dataVisible = true
        },
        eliminarUsuario(){
            const rowSeleccionado = this.$refs.tableHist.selectedRows
            let flag = false
            rowSeleccionado.forEach(element => {
                console.log(element)
                const path = `${this.$apiURL}/ver_hist/${element}/`
                axios
                .delete(path)
                .then(() => {
                    this.getInformesAnteriores(this.empresaSeleccionadaObj.id);
                    this.componentTableHist +=1
                    this.mensajeAlerta = this.$t('graficos.del_informe_ok')
                    this.tipoAlerta = 'success'
                    this.$refs.alertaGenerall.verAlerta()
                })
                .catch(() =>{
                    this.getInformesAnteriores(this.empresaSeleccionadaObj.id);
                    this.mensajeAlerta = this.$t('graficos.del_informe_error')
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                });
            });
            if(flag){
                console.error('error')
                this.mensajeAlerta = this.$t('graficos.del_informe_error')
                this.$refs.alerta.verAlerta()
            }else{
                this.$refs.alerta_eliminar.hide()
            }
        },
        eliminarUsuario2(){
            const rowSeleccionado = this.$refs.tableHist2.selectedRows
            let flag = false
            rowSeleccionado.forEach(element => {
                console.log(element)
                const path = `${this.$apiURL}/ver_hist/${element}/`
                axios
                .delete(path)
                .then(() => {
                    this.getInformesAnterioresCoop();
                    this.componentTableHist +=1
                    this.mensajeAlerta = this.$t('graficos.del_informe_ok')
                    this.tipoAlerta = 'success'
                    this.$refs.alertaGenerall.verAlerta()
                })
                .catch(() =>{
                    this.getInformesAnterioresCoop();
                    this.mensajeAlerta = this.$t('graficos.del_informe_error')
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                });
            });
            if(flag){
                console.error('error')
                this.mensajeAlerta = this.$t('graficos.del_informe_error')
                this.$refs.alerta.verAlerta()
            }else{
                this.$refs.alerta_eliminar.hide()
            }
        },
        eliminarUsuario3(){
            const rowSeleccionado = this.$refs.tableHist2.selectedRows
            let flag = false
            rowSeleccionado.forEach(element => {
                console.log(element)
                const path = `${this.$apiURL}/ver_hist/${element}/`
                axios
                .delete(path)
                .then(() => {
                    this.getInformesAnterioresCoopADM(this.cooperativeSelectObj.id);
                    this.componentTableHist +=1
                    this.mensajeAlerta = this.$t('graficos.del_informe_ok')
                    this.tipoAlerta = 'success'
                    this.$refs.alertaGenerall.verAlerta()
                })
                .catch(() =>{
                    this.getInformesAnterioresCoopADM(this.cooperativeSelectObj.id);
                    this.mensajeAlerta = this.$t('graficos.del_informe_error')
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                });
            });
            if(flag){
                console.error('error')
                this.mensajeAlerta = this.$t('graficos.del_informe_error')
                this.$refs.alerta.verAlerta()
            }else{
                this.$refs.alerta_eliminar.hide()
            }
        },
        showModificarInformes(){
            this.$refs.unificarInformes.openModal()
        },
        agruparCompatible(arrSel){
            let capaAnt = ``
            let tipoAnt = ``
            let parcelaAnt = ``
            let flag = true
            var BreakException = {};
            let arrParcelsSel = Array()
            let arrParcelFilter = Array()
            try{
                if(arrSel.length > 1){
                    arrSel.forEach(element => {
                        arrParcelFilter = this.historicoAnterior.filter(informe => {
                            if(informe.id == element){
                                if(!capaAnt){
                                    capaAnt = informe.capa
                                }else{
                                    if(capaAnt != informe.capa){
                                        flag = false
                                        throw BreakException
                                    }
                                }
                                if(!tipoAnt){
                                    tipoAnt = informe.tipo
                                    parcelaAnt = informe.parcela
                                }else{
                                    if(parseInt(tipoAnt) != parseInt(informe.tipo)){
                                        flag = false
                                        throw BreakException
                                    }else if(parseInt(tipoAnt) == 1 && parcelaAnt != informe.parcela){
                                        flag = false
                                        throw BreakException
                                    }
                                }
                                return informe
                            }
                        })
                        arrParcelsSel.push(arrParcelFilter[0])
                    })
                }else{
                    flag = false
                    throw BreakException
                }
                
            } catch (e){
                if(!flag){
                    this.showUnificar = false
                    if(arrSel.length == 1){
                        this.showEditar = true
                        this.informeSell = arrSel
                    }else{
                        this.showEditar = false
                    }
                    throw e
                }
            }
            this.informesSell = arrParcelsSel
            this.capaInforUni = capaAnt
            this.tipoInforUni = tipoAnt
            this.showUnificar = true
        },
        getHistorico(){
            if(this.arrEmpresas.length){
                this.empresaSeleccionadaObj = this.arrEmpresas[0]
                this.getInformesAnteriores(this.arrEmpresas[0].id)
            }
            if(this.arrCooperativas.length){
                this.cooperativaSeleccionadaObj = this.arrCooperativas[0]
                this.getInformesAnterioresCoop(this.arrCooperativas[0].id)
            }
        },
        getInformesAnteriores(enterprise_id){
            let path = `${this.$apiURL}/procesado/?enterprise_id=${enterprise_id}&colum_name=${this.column}&order=${this.orden}`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                console.info('informes de la empresa:', this.empresaSeleccionadaObj.name)
                console.info(response.data)
                this.historicoAnterior = response.data
            })
            .catch(error =>{
                console.warn(error)
            })
        },
        getInformesAnterioresCoop(coop){
            let path = `${this.$apiURL}/procesado/?enterprise_id=${coop}&colum_name=${this.column}&order=${this.orden}`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                console.info('informes de la Cooperativa:', this.cooperativaSeleccionadaObj.name)
                console.info(response.data)
                this.historicoAnteriorCoop = response.data
            })
            .catch(error =>{
                console.warn(error)
            })
        },
    },
    beforeMount(){
        //this.getHistorico()
    },
    mounted: function () {
        //console.info('User Logged')
    },
    beforeCreate(){
        getProfile()
        .then(response => {
            const user = response.data[0]
            getPermisos(response.data[0].user)
            .then(response => {
                this.is_superuser = response.data.is_superuser
                this.is_staff = response.data.is_staff
                this.is_systemadmin = response.data.is_systemadmin
                this.is_enterpriseadmin = response.data.is_enterpriseadmin
                this.is_coop_user = user.cooperative_user
                /*
                //*Obtenemos la empresa del usuario
                const enterprise_id = user.enterprise_id
                getEnterprise(enterprise_id)
                .then(async response => {
                    this.parcelas = response.data.parcels
                    await this.arrEmpresas.push(response.data)
                    this.flagIndicatingDataHasBeenLoadedInVariables = false
                    this.timestamp()
                })
                */
                
                if(this.is_superuser || this.is_systemadmin){
                    console.info('entra')
                    getAllEnterprises()
                    .then(async response => {
                        this.arrEmpresas = response.data
                        const arrParcels = []
                        response.data.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                        this.getHistorico()
                    })
                }else if((this.is_enterpriseadmin || this.is_staff) && !this.is_coop_user){ 
                    getEnterprise(user.enterprise_id)
                    .then(async response => {
                        this.arrEmpresas = [response.data]
                        const arrParcels = []
                        response.data.parcels.features.map(parcel => {
                            arrParcels.push(parcel)
                        })
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                        this.getHistorico()
                    })
                }else if(this.is_coop_user){
                    getCooperative(user.enterprise_id)
                    .then(response => {
                        this.arrCooperativas = [response.data]
                        //this.arrEmpresas = response.data.enterprises
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                        this.getHistorico()
                    })
                }

                if(this.is_superuser || this.is_systemadmin){
                    getAllCooperatives()
                    .then(async response => {
                        this.arrCooperativas = response.data
                    })
                }
                this.isActiveLoading = false
                this.isVisibleLoad = false
            })
        })
    }
};
</script>