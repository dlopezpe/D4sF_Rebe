<template>
    <div class="Charts">
        <br>
        <div class="bx--grid" style="padding-left: 1rem!important; padding-right: 1rem!important;max-width: 100%!important;">
            <cv-tabs
            :container="container"
            aria-label="navigation tab label">
                <cv-tab :label="$t('graficos.grafico_tipo_uno')">
                    <br>
                    <br>
                    <ChartComponent ref="ChartComponet"/>
                </cv-tab>
                <cv-tab :label="$t('graficos.grafico_tipo_dos')">
                    <br>
                    <br>
                    <ChartComponentT2 ref="ChartComponentT2"/>
                </cv-tab>
                <cv-tab :label="$t('graficos.grafico_ant')" >
                    <br>
                    <br>
                    <div class="bx--grid" style="padding-left: 1rem!important; padding-right: 1rem!important;max-width: 100%!important;">
                        <div class="bx--row">
                            <div class="bx--col-sm-12 bx--col-md-12 bx--col-lg-12">
                                <h3>{{$t("graficos.grafico_ant")}}</h3>
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
                                <br>
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
                                        <cv-select-option v-for="empresa in enterprisesList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                                            {{empresa.name}}
                                        </cv-select-option>
                                    </cv-select>
                                </div>
                                <br>
                                <br>
                                <h4 v-if="mostarListaParcelsCoops == false">{{$t("graficos.inform_ant_de")}} {{enterprise.name}}</h4>
                                <div>
                                    <cv-data-table
                                    v-if="mostarListaParcelsCoops === false"
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
                                    ]"  ref="tableHist" :key="componentTableHist">
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
                                                    <cv-overflow-menu-item @click="descargaExcelRow(String(historico.id))">{{$t("graficos.desc_excel")}}</cv-overflow-menu-item>
                                                    <cv-overflow-menu-item @click="delInformeRow(String(historico.id))">{{$t("graficos.del_informe")}}</cv-overflow-menu-item>
                                                </cv-overflow-menu>
                                            </cv-data-table-cell>
                                        </cv-data-table-row>
                                    </template>
                                    </cv-data-table>
                                </div>
                                <br><br>
                                <h4 v-if="mostrarListaEmpresasCoop && mostarListaParcelsCoops == false">Gáficos Anteriores de la Cooperativa</h4>
                                <div v-if="mostrarListaEmpresasCoop && mostarListaParcelsCoops == false">
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
                                <h4 v-if="mostarListaParcelsCoops == true">Gáficos Anteriores de la Cooperativa {{cooperativeSelectObj.name}}</h4>
                                <div v-if="mostarListaParcelsCoops == true">
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
                                        <cv-button @click="delInforme3">
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
                                                    <cv-overflow-menu-item @click="delInformeRow3(String(historico.id))">{{$t("graficos.del_informe")}}</cv-overflow-menu-item>
                                                </cv-overflow-menu>
                                            </cv-data-table-cell>
                                        </cv-data-table-row>
                                    </template>
                                    </cv-data-table>
                                </div>
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
                    </div>
                </cv-tab>
            </cv-tabs>
        </div>
        <AlertaGeneral ref="alertaGenerall" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        <UnificarInformes ref="unificarInformes" :informesSeleccionados="informesSell" :historico="historicoAnterior" :tipo="tipoInforUni" :capa="capaInforUni" :enterpriseID="enterprise.id"/>
        <EditarInforme ref="editarInforme" :informesSeleccionados="informeSell" :historico="historicoAnterior"/>
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
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import ChartComponent from '@/components/ChartComponentNDVIv2.vue'
import ChartComponentT2 from '@/components/ChartComponentNDVIT2.vue'
import ChartLine from '@/components/charts/chartLine.vue'
import ChartLineMois from '@/components/charts/chartLineMois.vue'
import SentImage from '@/components/charts/imageSent.vue'
import ChartBar from '@/components/charts/chartBar.vue'
import ChartBarMois from '@/components/charts/chartBarMois.vue'
import TableColors from '@/components/charts/tableColors.vue'
import TableColorsMois from '@/components/charts/tableColorsMois.vue'
import AlertaGeneral from "@/components/AlertaGeneral";
import UnificarInformes from "@/components/UnificarInforme.vue";
import EditarInforme from "@/components/EditarInforme.vue";
import {getAllCooperatives} from '../crudFunctions/crudCooperativas'
export default {
    name: 'Charts',
    components: {
        ChartComponent,
        ChartLine,
        SentImage,
        ChartBar,
        TableColors,
        AlertaGeneral,
        ChartComponentT2,
        ChartLineMois,
        ChartBarMois,
        TableColorsMois,
        UnificarInformes,
        EditarInforme
    },
    data () {
        return{
            showUnificar: false,
            showEditar: false,
            verGraficNDVI: false,
            verGraficMois: false,
            verImagenSent: false,
            mostrarListaEmpresas: false,
            mostrarListaEmpresasCoop: false,
            enterprisesList: Array(),
            start: 0,
            length: 10,
            start2: 0,
            length2: 10,
            mensajeAlerta: ``,
            tipoAlerta: `error`,
            container: false,
            selected: false,
            disabled: false,
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
            parcelasNames: Array(),
            dataSent:Object(),
            keyComponent: 0,
            componentTableHist: 0,
            componentTableHist2: 0,
            pageSize: 60,
            pagePar: 1,
            enterprise: Object(),
            column: 'created',
            orden: 'descending',
            informesSell: Array(),
            informeSell: Array(),
            capaInforUni: ``,
            tipoInforUni: ``,

            //for coops ADM
            mostrarListaCooperativas: false,
            cooperativesList: Array(),
            cooperativeSelect: '',
            cooperativeSelectObj: Object(),
            mostarListaParcelsCoops: false
        }
    },
    methods:{
        showModificarInformes(){
            this.$refs.unificarInformes.openModal()
        },
        showEditarInforme(){
            this.$refs.editarInforme.openModal()
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
        dateFormat(date){
            const dts = date.split('T')
            return dts[0]
        },
        onSort(order){
            const index = order.index
            this.orden = order.order
            switch (index) {
                case '2':
                    this.column = `created`
                    break
                case '3':
                    this.column = 'tipo'
                    break
                case '4':
                    this.column = 'capa'
                    break
                default:
                    this.column = `created`
            }
            this.getInformesAnteriores()
        },
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        actionOnPagination2(ev){
            this.start2 = ev.start-1
            this.length2 = ev.length
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
                    this.getInformesAnteriores();
                    this.componentTableHist +=1
                    this.mensajeAlerta = this.$t('graficos.del_informe_ok')
                    this.tipoAlerta = 'success'
                    this.$refs.alertaGenerall.verAlerta()
                })
                .catch(() =>{
                    this.getInformesAnteriores();
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
        parcelaName(id){
            const parcelaSelect = this.parcelasNames.filter((parcela)=>{
                return parcela.id == id
            })            
            if(parcelaSelect.length > 0){
                return parcelaSelect[0].properties.name
            }else{
                return 'Gráfico Generado de Parcela Eliminada'
            }
        },
        getInformesAnteriores(){
            let path = `${this.$apiURL}/procesado/?enterprise_id=${this.enterprise.id}&colum_name=${this.column}&order=${this.orden}`
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
        getInformesAnterioresCoop(){
            let path = `${this.$apiURL}/procesado/?enterprise_id=${sessionStorage.getItem('enterprise')}&colum_name=${this.column}&order=${this.orden}`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.historicoAnteriorCoop = response.data
            })
            .catch(error =>{
                console.warn(error)
            })
        },
        getParcelaName(){
            let path = `${this.$apiURL}/parcels/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.parcelasNames = response.data.features
            })
            .catch(error =>{
                console.warn(error)
            })
            
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
                this.$parent.is_superuser = response.data.is_superuser
                this.$parent.is_staff = response.data.is_staff,
                this.$parent.is_systemadmin = response.data.is_systemadmin,
                this.$parent.is_enterpriseadmin = response.data.is_enterpriseadmin
                this.$parent.customLinkEnterprise = 'edit-enterprise?enterprise='+this.$session.get('enterprise')
                this.$parent.$parent.is_coop_user = this.$session.get('is_coop_user')
                this.$parent.$parent.customLinkCoop = 'edit-cooperative?cooperative='+this.$session.get('enterprise')
                //---------------------------------------------------------------
                this.init()
            })
        },
        seleccionaEmpresa(empresa){
            this.empresaSelect = empresa
            this.mostarListaParcelsCoops = false
            this.init()
        },
        seleccionaCoop(empresa){
            this.mostarListaParcelsCoops = true
            this.getInformesAnterioresCoopADM(empresa)
        },
        getInformesAnterioresCoopADM(coop_id){
            this.mostrarListaEmpresasCoop = false
            let path = `${this.$apiURL}/cooperativesonenrlt/${coop_id}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios.get(path)
            .then(async response => {
                this.cooperativeSelectObj = response.data
                let path2 = `${this.$apiURL}/procesado/?enterprise_id=${coop_id}&colum_name=${this.column}&order=${this.orden}`
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .get(path2)
                .then(response => {
                    this.historicoAnteriorCoop = response.data
                })
                .catch(error =>{
                    console.warn(error)
                })
            })
            
        },
        init(){
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
                        this.getInformesAnteriores()
                    }else{
                        this.enterprise = response.data
                        this.getInformesAnteriores()
                    }
                }else{
                    this.enterprisesList = response.data.enterprises
                    if(this.empresaSelect){
                        const result = response.data.enterprises.filter(enterprise => enterprise.id === this.empresaSelect)
                        this.enterprise = result[0]
                    }else{
                        this.enterprise = response.data.enterprises[0]
                    }
                    this.getInformesAnteriores()
                    this.getInformesAnterioresCoop()
                }
            })
            .catch(error =>{
                console.warn(error)
                if(error.response.status == 500 && error.response.data.split(' ')[0] == 'EmptyPage'){
                    console.log('ultima')
                }
            })
        },
    },
    mounted () {
        const path = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
        this.getParcelaName()
        this.getDatosUser()
        this.init()
    },
    created (){
        const path = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
        this.init()
        this.getParcelaName()
    }

}
</script>