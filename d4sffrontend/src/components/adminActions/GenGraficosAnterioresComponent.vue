<template>
    <div class="bx--grid" @mousedown="keepPositionScroll" @mouseup="putPositionScroll">
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <h2>Informes Anteriores <img src="../../assets/agriculture-analytics.svg" style="width: 40px;"></h2>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <cv-select
                    theme=""
                    :label="$t('map.listado_empresas')"
                    :hide-label="false"
                    :inline="false"
                    :disabled="false"
                    @change="seleccionaEmpresa"
                    v-model="selectValueEmpresa"
                >
                    <cv-select-option :value="''" disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                    <cv-select-optgroup label="Todas las Empresas" v-if="is_superuser || is_systemadmin">
                        <cv-select-option :value="`all`" v-if="is_superuser || is_systemadmin">{{$t("map.most_todas_empresas")}}</cv-select-option>
                        <cv-select-option v-for="empresa in arrEmpresasList" :value="String(empresa.id)"  v-bind:key="empresa.id">
                            {{empresa.name}}
                        </cv-select-option>
                    </cv-select-optgroup>
                    <cv-select-optgroup :label="`Cooperativa ${cooperativa.name}`" v-bind:key="cooperativa.id" v-for="cooperativa in arrCooperativas">
                        <cv-select-option :value="`coop_${cooperativa.id}`">{{$t("map.most_todas_empresas")}}</cv-select-option>
                        <cv-select-option v-for="empresa in getSortedCooperativa(cooperativa).enterprises" :value="String(empresa.id)"  v-bind:key="empresa.id">
                            {{empresa.name}}
                        </cv-select-option>
                    </cv-select-optgroup>
                </cv-select>
            </div>
        </div>
        <br>
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <p><strong><u>IMPORTANTE:</u></strong> Los informes anteriores al 04-08-2022 (incluido) se van a descargar siempre con imágenes, la opción de descargar los informes con/sin imágenes se implementó a partir de esa fecha.</p>
                <br><p>{{$t("adminEnterprise.info_nav")}}</p>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <div id="sentinelLayersList">
                    <cv-data-table
                        :sortable="false"
                        :pagination="{ numberOfItems: historicoAnterior.length, pageSizes: [10, 15, 20, 25, historicoAnterior.length] }" @pagination="actionOnPagination"
                        :columns="columnas"
                        :title="`Informes Generados`"
                        @sort="onSort"
                        v-model="rowSelects"
                        ref="tableLstadoT2MultiCoop"
                        searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
                        @row-select-change="changeRowsUnique"
                    >
                        <template v-if="true" slot="actions">
                            <cv-search :placeholder="$t('graficos.buscar_nombre')" @input="onBuscar"></cv-search>
                        </template>
                        <template v-if="rowSelects.length == 1" slot="batch-actions">
                            <cv-button @click="verDatosFecha">
                                {{$t("graficos.ver_datos")}} Ordenado por Fecha
                                <Charbar20 class="bx--btn__icon"/>
                            </cv-button> 
                        </template>
                        <template v-if="rowSelects.length == 1" slot="batch-actions">
                            <cv-button @click="verDatosParcelas">
                                {{$t("graficos.ver_datos")}} Agrupado por Parcelas
                                <Charbar20 class="bx--btn__icon"/>
                            </cv-button> 
                        </template>
                        <template v-if="rowSelects.length == 1" slot="batch-actions">
                            <cv-button @click="descargaExcel" v-if="true">
                                {{$t("graficos.desc_excel")}}
                                <Download16 class="bx--btn__icon"/>
                            </cv-button>
                        </template>
                        <template v-if="rowSelects.length == 1" slot="batch-actions">
                            <cv-button @click="descargaExcelConImagenes" v-if="true">
                                {{$t("graficos.desc_excel_img")}}
                                <Download16 class="bx--btn__icon"/>
                            </cv-button>
                        </template>            
                        <template v-if="rowSelects.length == 1" slot="batch-actions">
                            <cv-button @click="showEditarInforme" >
                                {{$t("graficos.editar")}}
                                <Edit32 class="bx--btn__icon" />
                            </cv-button>
                        </template>
                        <template v-if="rowSelects.length > 1" slot="batch-actions">
                            <cv-button @click="showModificarInformes" >
                                {{$t("graficos.unificar_informes")}}
                                <AppConnectivity32 class="bx--btn__icon"/>
                            </cv-button>
                        </template>
                        <template v-if="true" slot="batch-actions">
                            <cv-button @click="delInforme">
                                {{$t("graficos.del_informe")}}
                                <TrashCan32 class="bx--btn__icon" />
                            </cv-button>
                        </template>
                        <template slot="data">
                            <cv-data-table-row
                                v-for="feature in historicoAnterior.slice(start, start+length)"
                                :key="`${feature.id}`"
                                :value="`${feature.id}`"
                                :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"
                            >
                                <cv-data-table-cell>{{feature.nombre}}</cv-data-table-cell>
                                <cv-data-table-cell>{{feature.capa}}</cv-data-table-cell>
                                <cv-data-table-cell>{{dateFormat(feature.created)}}</cv-data-table-cell>
                                <cv-data-table-cell>{{getEstado(feature)}} <img src="../../assets/information--square--filled.svg" style="width: 15px; cursor:pointer" title="Parcelas reportadas por Sentinel" @click="modalerrores(feature)" v-if="feature.error"> </cv-data-table-cell>
                                <cv-data-table-cell>{{feature.fechaInicio}} - {{feature.fechaFin}}</cv-data-table-cell>
                                <cv-data-table-cell style="text-aling: center">
                                    <img src="../../assets/mostly-cloudy.svg" style="width: 15px;" v-if="feature.includeClouds"> 
                                    <img src="../../assets/outlook-severe.svg" style="width: 15px;" v-else>
                                    <label v-if="feature.includeClouds">  Sí</label>
                                    <label v-else>  No</label>
                                </cv-data-table-cell>
                                <cv-data-table-cell v-if="is_superuser">{{getUserName(feature.user_created)}}</cv-data-table-cell>
                                <cv-data-table-cell>{{getEnterpriseName(feature.enterprise_id)}}</cv-data-table-cell>
                            </cv-data-table-row>
                        </template>
                    </cv-data-table>
                </div>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <ChartLine :datos="graficoData" v-if="verGraficNDVI" :key="`chart_line_ndvi_${timestamp}`"/>
                <ChartLineMois :datos="graficoData" v-if="verGraficMois" :key="`chart_line_mois_${timestamp}`"/>
            </div>
        </div>
        <div class="bx--row">
            <div class="bx--col">
                <ChartBar :datos="graficoData" v-if="verGraficNDVI" :key="`chart_bar_ndvi_${timestamp}`"/>
                <ChartBarMois :datos="graficoData" v-if="verGraficMois" :key="`chart_bar_mois_${timestamp}`"/>
            </div>
        </div>
        <div class="bx--row">
            <div class="bx--col">
                <TableColors :urlMedia="$apiURLMedia" :datos="graficoData" v-if="verGraficNDVI" :key="`table_ndvi_${timestamp}`"/>
                <TableColorsMois :urlMedia="$apiURLMedia" :datos="graficoData" v-if="verGraficMois" :key="`table_mois_${timestamp}`"/>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <SentImage :urlMedia="$apiURLMedia" :datos="graficoData" v-if="verImagenSent" :key="`imgs_${timestamp}`"/>
            </div>
        </div>
        <cv-modal
        ref="alerta_eliminar"
        kind="danger"
        @primary-click="eliminarInformesConfirm">
            <template slot="label">{{$t("graficos.seguro")}}</template>
            <template slot="title">{{$t("graficos.eliminar")}}</template>
            <template slot="content">
            <p>{{$t("graficos.seguro_parcel_del")}}</p>
            </template>
            <template slot="secondary-button">{{$t("graficos.cancelar")}}</template>
            <template slot="primary-button">{{$t("graficos.eliminar")}}</template>
        </cv-modal>

        <cv-modal
            ref="editar_informe"
            @primary-click="changeNameInforme"
        >
            <template slot="label">{{$t('graficos.modifica_infor')}}</template>
            <template slot="title">{{$t('graficos.modifica_infor')}}</template>
            <template slot="content">
                <div class="bx--grid bx--grid--condensed">
                    <div class="bx--row">
                        <div class="bx--col">
                            <!-- Nombre de Informe -->
                            <div class="bx--form-item">
                                <label for="text-input-Nombre" class="bx--label">{{$t('graficos.nombre_informe')}}</label>
                                <input v-model="nombreInformeNew" id="text-input-Nombre" type="text" class="bx--text-input">
                            </div>
                        </div>
                    </div>
                </div>
            </template>
            <template slot="secondary-button">{{$t("graficos.cancelar")}}</template>
            <template slot="primary-button">{{$t('graficos.guardar')}}</template>
        </cv-modal>
        <cv-modal
            ref="unificarInformeForm"
            @primary-click="unificaInformes"
            @secondary-click="$refs.unificarInformeForm.hide()"
        >
            <template v-if="true" slot="label"></template>
            <template v-if="true" slot="title">{{$t('graficos.unificar_informes')}}</template>
            <template v-if="true" slot="content" id="contenido">
                <div class="bx--grid bx--grid--condensed">
                    <div class="bx--row">
                        <!-- Nombre de Informe -->
                        <div class="bx--form-item">
                            <label for="text-input-Nombre" class="bx--label">{{$t('graficos.nombre')}}</label>
                            <input v-model="nombreInformeNewUnificado" id="text-input-Nombre" type="text" class="bx--text-input" :placeholder="$t('graficos.nombre')">
                        </div>
                    </div>
                    <br>
                    <div class="bx--row">
                        <div class="bx--col">
                            <div class="bx--form-item">
                                <cv-checkbox
                                    :label="$t('graficos.eliminar_informe_origin')"
                                    :checked="false"
                                    value="true"
                                    :mixed="false"
                                    v-model="checkDellInforme"
                                >
                                </cv-checkbox>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div class="bx--row">
                        <div class="bx--col">
                            <h4>{{$t("graficos.resumen_unifica")}}</h4>
                            <cv-data-table
                                :columns="[
                                    this.$t('graficos.parcelas'),
                                    'Capa',
                                    this.$t('graficos.rango_fechas_sel'),
                                    {
                                        'label': this.$t('graficos.creado'),
                                    },
                                ]"
                            >
                                <template slot="data">
                                    <cv-data-table-row  v-for="informe in informesSeleccionados" :value="String(informe.id)" :key="String(informe.id)">
                                        <cv-data-table-cell>{{informe.nombre}}</cv-data-table-cell>
                                        <cv-data-table-cell>{{informe.capa}}</cv-data-table-cell>
                                        <cv-data-table-cell>{{dateFormat(informe.created)}}</cv-data-table-cell>
                                        <cv-data-table-cell>{{informe.fechaInicio}} - {{informe.fechaFin}}</cv-data-table-cell>
                                    </cv-data-table-row>
                                </template>
                            </cv-data-table>
                        </div>
                    </div>
                </div>
            </template>
            <template v-if="true" slot="secondary-button">{{$t("graficos.cancelar")}}</template>
            <template v-if="true" slot="primary-button">{{$t("graficos.unificar")}}</template>
        </cv-modal>
        <cv-modal
        ref="errores"
        @primary-click="$refs.errores.hide()"
        >
            <template slot="title">Parcelas reportadas por Sentinel</template>
            <template slot="content">
            <p style="white-space: pre-line">Sentinel ha reportado algún posible error al obtener los datos de la/s parcela/s:
            <br> 
            {{getErrores(informeErrores)}}
            Por favor, revisa el informe y solicita de nuevo esas parcelas en caso de que falte algún dato.</p>
            </template>
            <template slot="primary-button">OK</template>
        </cv-modal>
        <AlertaGeneral ref="alertaGenerall" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
    </div>
</template>
<script>
//import {getParcelsNotSentinelInstance, postParcelsNotSentinelInstance} from '@/crudFunctions/crudSentinel.js'
import {getProfile, getPermisos} from '@/auth/index'
import {getAllEnterprises, getEnterprise, createInformes, getInformesAnterioresNew,
getInformeAnteriorData, delInformesAnterioresNew,putInformesUnificarNew, putInformesAnterioresNew, getUsersList, getUsersListProfiles, generarinforme} from '@/crudFunctions/crudEnterprise'
import {getAllCooperatives, getCooperative} from '@/crudFunctions/crudCooperativas'
import SentImage from '@/components/charts_new/imageSent.vue'
import TableColors from '@/components/charts_new/tableColors.vue'
import TableColorsMois from '@/components/charts_new/tableColorsMois.vue'
import ChartLine from '@/components/charts_new/chartLine.vue'
import ChartLineMois from '@/components/charts_new/chartLineMois.vue'
import ChartBar from '@/components/charts_new/chartBar.vue'
import ChartBarMois from '@/components/charts_new/chartBarMois.vue'
import AlertaGeneral from "@/components/AlertaGeneral"
export default {
    name: 'ParcelsToSentinelComponent',
    components: {
        SentImage,
        TableColors,
        TableColorsMois,
        ChartLine,
        ChartBar,
        ChartBarMois,
        ChartLineMois,
        AlertaGeneral
    },
    data(){
        return {
            //
            selectValueEmpresa: '',
            //
            flagIndicatingDataHasBeenLoadedInVariables: false,
            //Usuario
            is_superuser: false,
            is_staff: false,
            is_systemadmin: false,
            is_enterpriseadmin: false,
            is_coop_user: false,
            //Empresas sel
            arrEmpresas: [],
            arrEmpresasList: [],
            arrCooperativas: [],
            allParcelsOfEnterprises: [],
            allParcelsOfEnterprisesFilter: [],
            //
            start: 0,
            length: 10,
            //
            rowSelects: [],
            //
            SentinelLayer: 'NDVI',
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            time: `${this.getNow()}/${this.getNow()}`,
            valueDates: [],
            valueRange: [],
            timeValuesArr: [this.getNow(), this.getNow()],
            nombreInforme: `Gráfico - ${this.getNow()}`,
            historicoAnterior: Array(),
            historicoAnteriorCoop: Array(),
            historicoSell: {},
            verGraficNDVI: false,
            verGraficMois: false,
            graficoData: {},
            verImagenSent: false,
            keyTableColors: 0,
            timestamp: 0,
            mostrar:true,
            //
            tipoAlerta: `error`,
            mensajeAlerta: '',
            //
            nombreInformeNew: '',
            //
            showUnificarInformes: false,
            //
            nombreInformeNewUnificado: `Gráfico Unificado - ${this.getNow()}`,
            checkDellInforme: false,
            informesSeleccionados: [],
            uniqueEmpresasUnificarId: '',
            uniqueCapaUnificar: '',
            usersList: [],
            usersListProfile: [],
            informeErrores:{},
            columnas:[
                            {
                                key: 'name',
                                label: this.$t('graficos.nombre'),
                                'sortable': false
                            },
                            {
                                key: 'capa',
                                label: this.$t('graficos.capa'),
                                'sortable': true
                            },
                            {
                                'label': this.$t('graficos.creado'),
                                'sortable': true
                            },
                            {
                                'label': this.$t('graficos.estado'),
                                'sortable': false
                            },
                            {
                                'label': this.$t('graficos.rango_fechas_sel'),
                                'sortable': false
                            },
                            {
                                'label': this.$t('graficos.analisis_nubes'),
                                'sortable': true
                            },
                            {
                                'label': this.$t('graficos.empresa'),
                                'sortable': false
                            },
                        ]
        }
    },
    methods: {
        keepPositionScroll(){
            this.scrollPosition = window.scrollY;
        },
        putPositionScroll(){
            setTimeout(() => {
                window.scrollTo(0, this.scrollPosition);
            }, 0);
        },
        // para ordenar las empresas de la cooperativa alfabéticamente
        getSortedCooperativa(cooperativa) {
            return {
                ...cooperativa,
                enterprises: cooperativa.enterprises.slice().sort((a, b) => {
                return a.name.localeCompare(b.name);
                }),
            };
        },
        getUserName(user_id){
            if(this.usersList && this.usersListProfile){
                const resultName = this.usersList.filter(user => user.id == user_id)
                if(resultName){
                    const resultEmail = this.usersListProfile.filter(user => user.id == resultName[0].user)
                    return `${resultName[0].first_name} - ${resultEmail[0].email}`
                }
            }
        },
        getEnterpriseName(id_empresa){
            const empresa=this.arrEmpresas.filter(y=>y.id==id_empresa)
            return empresa[0].name
        },
        getEstado(informe){
            if(!informe.esUnificado){
            if(informe.error && informe.estado==3){
                return "Terminado con posibles errores"
            }
            switch (informe.estado) {
                case '1':
                    return 'En Proceso (Obteniendo imagenes)'
                case '2':
                    return 'En proceso (Procesando excel)'
                case '3':
                    return 'Terminado'
                default:
                    return `No finalizado (errores en Sentinel)`
            }
            }else{
                return "Informe unificado"
            }
        },
        modalerrores(informe){
            this.informeErrores=informe
            this.$refs.errores.dataVisible = true
        },
        getErrores(informe){
            let codigo=""
            if(informe.parcelas_fallidas==null || informe.parcelas_fallidas.length==0){
                return "No hay datos especificos de que parcelas pueden presentar errores \n"
            }
            else{
                const fallidas=informe.parcelas_fallidas.trim().split(" ")
                for (let i in fallidas){
                    const result=this.allParcelsOfEnterprises.filter(x=>x.id==fallidas[i])
                    codigo+="ID= "+result[0].id+" Nombre= "+result[0].properties.name+'\n'
                }
                console.log(codigo)
                return codigo
            }
        },
        showModificarInformes(){
            if(this.comprobacionrows()){
                //const numSel = this.rowSelects.length
                const results = this.historicoAnterior.filter(historico => this.rowSelects.includes(historico.id) )
                const enterprisesInResults = []
                results.map(result => {
                    enterprisesInResults.push(result.enterprise_id)
                })
                const uniqueEmpresas = [...new Set(enterprisesInResults)]
                if(uniqueEmpresas.length > 1){
                    this.mensajeAlerta = 'Los informes seleccionados pertenecen a distintas empresas'
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                    return false
                }
                const capaInResults = []
                results.map(result => {
                    capaInResults.push(result.capa)
                })
                const uniqueCapa = [...new Set(capaInResults)]
                if(uniqueCapa.length > 1){
                    this.mensajeAlerta = 'Los informes seleccionados son de distintas capas'
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                    return false
                }
                this.uniqueEmpresasUnificarId = uniqueEmpresas[0]
                this.uniqueCapaUnificar = uniqueCapa[0]
                this.informesSeleccionados = results
                this.$refs.unificarInformeForm.dataVisible = true
            }
            else{
                this.mensajeAlerta = `"Las acciones a realizar sobre el informe se habilitarán una vez se haya generado completamente"`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }
        },
        unificaInformes(){
            //console.info(this.uniqueEmpresasUnificarId, this.informesSeleccionados, this.checkDellInforme, this.nombreInformeNewUnificado)
            putInformesUnificarNew(this.nombreInformeNewUnificado, this.uniqueEmpresasUnificarId, this.informesSeleccionados, this.checkDellInforme, this.uniqueCapaUnificar)
            .then(() => {
                this.mensajeAlerta = `Informe Generado correctamente`
                this.tipoAlerta = 'success'
                this.$refs.alertaGenerall.verAlerta()
                this.seleccionaEmpresa(this.selectValueEmpresa)
            })
            this.$refs.unificarInformeForm.hide()
        },
        showEditarInforme(){
            if(this.comprobacionrows()){
                //console.info('ver editar Informe')
                const result = this.historicoAnterior.filter(historico => this.rowSelects.includes(historico.id) )
                this.nombreInformeNew = result[0].nombre
                this.$refs.editar_informe.dataVisible = true
            }else{
                this.mensajeAlerta = `"Las acciones a realizar sobre el informe se habilitarán una vez se haya generado completamente"`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }
        },
        changeNameInforme(){
            putInformesAnterioresNew(this.rowSelects[0], this.nombreInformeNew)
            .then(() => {
                this.mensajeAlerta = `Informe Guardado correctamente`
                this.tipoAlerta = 'success'
                this.$refs.alertaGenerall.verAlerta()
                this.seleccionaEmpresa(this.selectValueEmpresa)
            })
            this.$refs.editar_informe.hide()
        },
        eliminarInformesConfirm(){
            delInformesAnterioresNew(this.rowSelects)
            .then(response => {
                console.info(response.data)
                this.seleccionaEmpresa(this.selectValueEmpresa)
                this.mensajeAlerta = this.$t('graficos.del_informe_ok')
                this.tipoAlerta = 'success'
                this.$refs.alertaGenerall.verAlerta()
                this.$refs.alerta_eliminar.hide()
            })
            console.info('Delete Informe/s', this.rowSelects)
        },
        changeRowsUnique(value){
            console.info(value)
        },
        descargaExcel(){
            if(this.rowSelects.length === 1 && this.comprobacionrows()){
                console.info('Correcta descarga de excel')
                const result = this.historicoAnterior.filter(historico => this.rowSelects.includes(historico.id) )
                window.URL = window.URL || window.webkitURL;
                let xhr = new XMLHttpRequest(),
                a = document.createElement('a'), file;
                xhr.open('GET', `${this.$apiURLMedia}/${result[0].xlsxFile}`, true);
                xhr.responseType = 'blob';
                xhr.onload = function () {
                    file = new Blob([xhr.response], { type : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                    a.href = window.URL.createObjectURL(file);
                    a.download = `${result[0].nombre}.xlsx`;  // Set to whatever file name you want
                    a.click();
                };
                xhr.send();
            }
            else{
                this.mensajeAlerta = `"Las acciones a realizar sobre el informe se habilitarán una vez se haya generado completamente"`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }
            console.info('Descarga Excel', this.rowSelects)
        },
        async descargaExcelConImagenes(){
            if (this.comprobacionrows()){
                //TODO ENDPOINT DE CREACION DE INFORME RETRUN NAME
                let nombre=await this.nombreinforme(this.rowSelects[0])
                console.log (nombre)
                await this.descargarinforme(nombre)
            }else{
                this.mensajeAlerta = `"Las acciones a realizar sobre el informe se habilitarán una vez se haya generado completamente"`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }
        },
        nombreinforme(id){
            return generarinforme(id)
        },
        descargarinforme(nombre){
            window.URL = window.URL || window.webkitURL;
                let xhr = new XMLHttpRequest(),
                a = document.createElement('a'), file;
                xhr.open('GET', `${this.$apiURLMedia}/${nombre['data'].data}`, true);
                xhr.responseType = 'blob';
                xhr.onload = function () {
                    file = new Blob([xhr.response], { type : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                    a.href = window.URL.createObjectURL(file);
                    a.download = `${nombre['data'].name}.xlsx`;  // Set to whatever file name you want
                    a.click();
                };
                xhr.send();
        },
        delInforme(){
            if(this.comprobacionrows()){
                this.$refs.alerta_eliminar.dataVisible = true
            }
            else{
                this.mensajeAlerta = `"Las acciones a realizar sobre el informe se habilitarán una vez se haya generado completamente"`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }
        },
        getNowCache() {
            const today = new Date();
            const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            const dateTime = date +' '+ time;
            this.timestamp = dateTime;
            //return date
        },
        verDatosFecha(){
            if(this.comprobacionrows()){
                //console.info(this.rowSelects)
                const result = this.historicoAnterior.filter(historico => this.rowSelects.includes(historico.id) )
                //console.info(result)
                this.historicoSell = result[0]
            
                getInformeAnteriorData(`order_${result[0].jsonFile}`)
                .then(response => {
                    //console.info(response.data)
                    this.graficoData = response.data
                    this.verImagenSent = true
                    if(result[0].capa === 'NDVI'){
                        this.verGraficNDVI = true
                        this.verGraficMois = false
                    }else{
                        this.verGraficNDVI = false
                        this.verGraficMois = true
                    }
                    this.getNowCache()
                })
            }
            else{
                this.mensajeAlerta = `"Las acciones a realizar sobre el informe se habilitarán una vez se haya generado completamente"`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }
        },
        verDatosParcelas(){
            if(this.comprobacionrows()){
                //console.info(this.rowSelects)
                const result = this.historicoAnterior.filter(historico => this.rowSelects.includes(historico.id) )
                //console.info(result)
                this.historicoSell = result[0]
            
                getInformeAnteriorData(`${result[0].jsonFile}`)
                .then(response => {
                    //console.info(response.data)
                    this.graficoData = response.data
                    this.verImagenSent = true
                    if(result[0].capa === 'NDVI'){
                        this.verGraficNDVI = true
                        this.verGraficMois = false
                    }else{
                        this.verGraficNDVI = false
                        this.verGraficMois = true
                    }
                    this.getNowCache()
                })
            }
            else{
                this.mensajeAlerta = `Las acciones a realizar sobre el informe se habilitarán una vez se haya generado completamente`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }
        },
        toGenerar(id_enterprise, is_cooperative){
            /*
            console.info('Nombre del Gráfico ', this.nombreInforme)
            console.info('Capa Seleccionada ', this.SentinelLayer)
            console.info('Fechas ', this.timeValuesArr)
            console.info('Parcelas ', this.rowSelects)
            console.info('Es Cooperativa ', is_cooperative)
            console.info('ID ', id_enterprise)
            */
            createInformes(this.nombreInforme, this.SentinelLayer, this.timeValuesArr, this.rowSelects, is_cooperative, id_enterprise)
        },
        dateFormat(dateRecorded){
            const dateObj = new Date(dateRecorded);
            const formatted = dateObj.toLocaleString('es-ES', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }).replace(/\//g, '-');
            return formatted;
        },
        generarInforme(){
            //console.info(this.rowSelects)
            const results = this.allParcelsOfEnterprisesFilter.filter(parcel => this.rowSelects.includes(String(parcel.id)))
            //console.info(results)
            const enterprisesInResults = []
            results.map(result => {
                enterprisesInResults.push(result.properties.enterprise_id)
            })
            //console.info('Resultados empresa => ',enterprisesInResults)
            const uniqueEmpresas = [...new Set(enterprisesInResults)]
            //console.info('Unificamos empresa => ',uniqueEmpresas)
            if(uniqueEmpresas.length > 1){
                //*Es multiempresa
                //console.info('Seleccion Multiempresa')
                //Comprobar si es cooperativa
                const enterprisesInResultsCoop = []
                this.arrCooperativas.map(cooperative => {
                    cooperative.enterprises.map(enterprise => {
                        if(uniqueEmpresas.includes(enterprise.id)){
                            enterprisesInResultsCoop.push(cooperative.id)
                        }
                    })
                })
                //console.info('Resultado Cooperativas => ',enterprisesInResultsCoop)
                if(enterprisesInResultsCoop.length == uniqueEmpresas.length){
                    console.info('Todas las empresas Pertenecen a cooperativas')
                    const uniqueCoops = [...new Set(enterprisesInResultsCoop)]
                    if(uniqueCoops.length > 1){
                        console.info('MultiCoop')
                        console.info('Cooperativas', uniqueCoops)
                        console.info('No se puede generar el informe, parcelas de distintas Cooperativas')
                    }else{
                        console.info('UniCoop')
                        console.info('Cooperativa', uniqueCoops)
                        this.toGenerar(uniqueCoops[0], true)
                    }
                }else{
                    console.info('No se puede generar el informe, Hay una empresa que no pertenece a ninguna cooperativa')
                }
            }else{
                console.info('Seleccion Uniempresa')
                this.toGenerar(uniqueEmpresas[0], false)
            }
        },
        actionChangeDateRange(range){
            console.info(range)
            this.timeValuesArr = [range.startDate, range.endDate]
            console.info(this.timeValuesArr)
            this.time = `${range.startDate}/${range.endDate}`
        },
        chageCapas(capa){
            this.SentinelLayer = capa
        },
        seleccionaEmpresa(empresa, columna='created', orden='descending'){
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
                        this.allParcelsOfEnterprisesFilter = arrParcels
                    })
                getInformesAnterioresNew(empresa, columna, orden)
                    .then(response => {
                        console.info(response.data)
                        this.historicoAnterior = response.data
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
                        this.arrEmpresas = response.data.enterprises
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                    })
                    getInformesAnterioresNew(result[1], columna, orden)
                    .then(response => {
                        console.info(response.data)
                        this.historicoAnterior= response.data
                    })
                }else{
                    getEnterprise(empresa)
                    .then(async response => {
                        response.data.parcels.features.map(parcel => {
                            arrParcels.push(parcel)
                        })
                        this.arrEmpresas = [response.data]
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                    })
                    getInformesAnterioresNew(empresa, columna, orden)
                    .then(response => {
                        console.info(response.data)
                        this.historicoAnterior= response.data
                    })
                }
            }
        },
        getNow() {
            const today = new Date();
            const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            const dateTime = date +' '+ time;
            //this.timestamp = dateTime;
            console.info(dateTime)
            return date
        },
        getNameEnterprise(value){
            const result = this.arrEmpresas.filter(enterprise => enterprise.id == value)
            return result[0].name
        },
        onBuscar(busqueda){
            if(busqueda){
                const result = this.allParcelsOfEnterprises.filter(parcel => parcel.properties.name.toUpperCase().includes(busqueda.toUpperCase()))
                this.allParcelsOfEnterprisesFilter = result
            }else{
                this.allParcelsOfEnterprisesFilter = this.allParcelsOfEnterprises
            }
        },
        actionOnPagination(ev){
            this.start = ev.start-1
            this.length = ev.length
        },
        onSort(order) {
            console.info(order)
            const index = order.index
            let column = ``
            const orden = order.order
            
            switch (index) {
                case '0':
                    column = `nombre`
                    break
                case '1':
                    column = `capa`
                    break
                case '2':
                    column = 'created'
                    break
                case '4':
                    column = 'includeClouds'
                    break
                default:
                    column = 'created'
            }
            this.seleccionaEmpresa(this.selectValueEmpresa, column, orden)
            .then(response => {
                this.historicoAnterior= response.data
            })
            /*
            if(orden == 'ascending'){
                this.allParcelsOfEnterprisesFilter.sort((a, b) => parseFloat(a.name) - parseFloat(b.name));
            }
            */
            console.info(column)
        },
        comprobacionrows(){
            let is_terminado
            const result = this.historicoAnterior.filter(historico => this.rowSelects.includes(historico.id))
            for (let i in result){
                if(result[i].estado==3 || result[i].esUnificado==true){
                    is_terminado =true
                }
                else{
                    return false
                }
            }
            console.log(is_terminado)
            return is_terminado
        },
    },
    mounted: function () {
        this.getNow()
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
                if(this.is_superuser){
                    this.columnas.splice(6,0,{'label': this.$t('graficos.solicitante_informe'),'sortable': false },)
                    getUsersList()
                    .then(response => {
                        this.usersList = response.data
                    })
                    getUsersListProfiles()
                    .then(response => {this.usersListProfile = response.data})
                }
                if(this.is_superuser || this.is_systemadmin){
                    console.info('entra')
                    getAllEnterprises()
                    .then(async response => {
                        this.arrEmpresas = response.data
                        //this.arrEmpresasList = response.data
                        this.arrEmpresasList = response.data.slice().sort((a, b) => {
                            return a.name.localeCompare(b.name);
                        });
                        const arrParcels = []
                        response.data.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                    })
                    getInformesAnterioresNew()
                    .then(response => {
                        console.info(response.data)
                        this.historicoAnterior = response.data
                    })
                }else if((this.is_enterpriseadmin || this.is_staff) && !this.is_coop_user){ 
                    getEnterprise(user.enterprise_id)
                    .then(async response => {
                        this.arrEmpresas = [response.data]
                        this.arrEmpresasList = [response.data]
                        const arrParcels = []
                        response.data.parcels.features.map(parcel => {
                            arrParcels.push(parcel)
                        })
                        this.allParcelsOfEnterprises = arrParcels
                        this.allParcelsOfEnterprisesFilter = arrParcels
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
                    })
                    getInformesAnterioresNew(user.enterprise_id)
                    .then(response => {
                        console.info(response.data)
                        this.historicoAnterior= response.data
                    })
                }else if(this.is_coop_user){
                    getCooperative(user.enterprise_id)
                    .then(response => {
                        this.arrCooperativas = [response.data]
                        //this.arrEmpresas = response.data.enterprises
                        this.flagIndicatingDataHasBeenLoadedInVariables = true
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
}
</script>