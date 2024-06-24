<template>
    <div class="bx--grid">
        <br>
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <h2>Evolución de cultivo (Monitor) <img src="../../assets/agriculture-analytics.svg" style="width: 40px;"></h2>
            </div>
        </div>
        <br>
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <p>Desde el Monitor podrás revisar de una forma rápida y visual la evolución de los cultivos en las parcelas seleccionadas y durante el intervalo de fechas deseado. Utiliza los filtros que encontrarás a continuación para concretar los datos, el informe de nubes se incluirá siempre independientemente de la selección que se haga.</p>
                <br><p><b>{{$t("adminEnterprise.info_nav")}}</b></p>
            </div>
        </div>
        <br>
        <div class="bx--row" style="margin-top: 20px;">
            <div class="bx--col-sm-12 bx--col-md-2 bx--col-lg-2">
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
            <div class="bx--col-sm-12 bx--col-md-2 bx--col-lg-2">
                <cv-button kind="primary" style="margin-top: 17px" @click="actionVisibleModal(true)">Seleccionar Parcelas</cv-button>
            </div>
            <div class="bx--col-sm-12 bx--col-md-2 bx--col-lg-2">
                <cv-select @change="onChangeLayer()" :label="$t('graficos.sel_layer_sen')" v-model="selectValueCapa">
                    <cv-select-option value="NDVI">{{$t("graficos.NDVI")}}</cv-select-option>
                    <cv-select-option value="MOISTURE_INDEX">{{$t("graficos.mostisture_index")}}</cv-select-option>
                </cv-select>
            </div>
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3">
                <cv-date-picker
                    kind="range"
                    :dateLabel="$t('graficos.fecha_incio')"
                    :date-end-label="$t('graficos.fecha_fin')"
                    :cal-options="calOptions"
                    @change="actionChangeDateRange"
                    :value="valueRange">
                </cv-date-picker>
            </div>
            <div class="bx--col-sm-12 bx--col-md-2 bx--col-lg-2">
                <cv-button kind="primary" style="margin-top: 17px" :disabled="disabledGenerar" v-if="rowSelects.length" @click="generarInforme()">Mostrar datos</cv-button>
            </div>
            
            <div class="bx--col-sm-12 bx--col-md-1 bx--col-lg-1">
                <cv-button kind="primary" style="margin-top: 17px" v-if="exportarExcel" @click="showModalImagesUser(true)">Exportar</cv-button>
            </div>
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3">
                <cv-button kind="primary" style="margin-top: 17px" v-if="exportarExcel" @click="showModalImagesUser(false)">Exportar sólo datos</cv-button>
            </div>
        </div>
        <br>
        <div id="txt-explicativo" class="bx--row" style="margin-top: 20px; margin-bottom: 20px;">
            <div class="bx--col">
                <p>En la gráfica se mostrarán solo los datos de los que se disponga información, es posible que se muestren parcelas sin datos en alguna fecha concreta. Dentro del rango de fechas seleccionado únicamente serán seleccionables en el slide aquellas que tengan algún dato.</p>
            </div>
        </div>
        <br>
        <Visor :data="data" :fechasArr="fechasArr" :layer="selectValueCapa" :key="keyComponentMonitor" :dataCampana="dataCampana" :dataProduccion="dataProduccion" :empresa="selectValueEmpresa"/>
        <cv-modal
            close-aria-label="Cerrar"
            size="large"
            :visible="visibleModal"
            @primary-click="actionPrimary"
            @modal-hidden="actionVisibleModal(false)"
            :auto-hide-off="false">
            <template v-if="true" slot="title">Selección de Parcelas</template>
            <template v-if="false" slot="title">{{empresa.name}}</template>
            <template v-if="true" slot="content" style="padding-right: 0%">
                <p>Selecciona a continuación las parcelas sobre las que quieres realizar la consulta. Puedes utilizar el buscador para encontrar la/s parcela/s que necesitas. Para poder ver el nombre de todas las parcelas, por favor utiliza el selector que encontrarás en la parte inferior de la tabla.</p>
                <cv-data-table
                :sortable="false"
                :pagination="{ 
                    numberOfItems: allParcelsOfEnterprisesFilter.length, 
                    pageSizes: [
                        {
                            value: 10,
                            label: '10'
                        }, 
                        {
                            value: 15,
                            label: '15'
                        },
                        {
                            value: 20,
                            label: '20'
                        }, 
                        {
                            value: 25,
                            label: '25'
                        }, 
                        {
                            value: allParcelsOfEnterprisesFilter.length,
                            label: 'Todas'
                        }
                    ] 
                }" 
                @pagination="actionOnPagination"
                :columns="[
                    {
                        key: 'name',
                        label: this.$t('graficos.nombre'),
                        'sortable': false
                    },
                    {
                        key: 'description',
                        label: this.$t('graficos.descrip'),
                        'sortable': false
                    },
                    {
                        key: 'heactareas',
                        label: this.$t('graficos.hectareas'),
                        'sortable': false
                    },
                    {
                        key: 'enterprise',
                        label: 'Empresa',
                        'sortable': false
                    },
                ]"
                @sort="onSort"
                v-model="rowSelects"
                ref="tableLstadoT2MultiCoop"
                searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter"
            >
                <template v-if="true" slot="actions">
                    <cv-search :placeholder="$t('graficos.buscar_nombre')" @input="onBuscar"></cv-search>
                </template>
                <template v-if="true" slot="batch-actions">
                    <cv-button>
                        
                    </cv-button>  
                </template>
                <template slot="data">
                    <cv-data-table-row
                        v-for="feature in allParcelsOfEnterprisesFilter.slice(start, start+length)"
                        :key="`${feature.id}`"
                        :value="`${feature.id}`"
                        :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"
                    >
                        <cv-data-table-cell>{{is_superuser ? feature.id+' - ' : ''}}{{feature.properties.name}}</cv-data-table-cell>
                        <cv-data-table-cell>{{feature.properties.description}}</cv-data-table-cell>
                        <cv-data-table-cell>{{feature.properties.area}}</cv-data-table-cell>
                        <cv-data-table-cell>{{getNameEnterprise(feature.properties.enterprise_id)}}</cv-data-table-cell>
                    </cv-data-table-row>
                </template>
            </cv-data-table>
            </template>
            <template slot="primary-button">Seleccionar</template>
        </cv-modal>
        
        

        <cv-modal
        ref="alerta_eliminar"
        :visible="visibleModalImages"
        kind="info"
        @primary-click="addImageReport(true)"
        @secondary-click="addImageReport(false)"
        >
            <template slot="label"></template>
            <template slot="title">Se va a descargar un archivo Excel con los datos de las parcelas y rango de fechas seleccionados.</template>
            <template slot="content">
             ¿Quieres incluir las imágenes en el archivo?
            </template>
            <template slot="secondary-button">No</template>
            <template slot="primary-button">Si</template>
            
            
        </cv-modal>
        
        <AlertaGeneral ref="alertaGenerall" :ishidden="true" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        <!-- only for specific scenario search by alertaGenerallModalReport  -->
        <AlertaGeneral ref="alertaGenerallModalReport" :ishidden="false" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        
    </div>
</template>

<script>
import {getProfile, getPermisos} from '@/auth/index'
import {getDataNdvi, getDataMoisture, exportToMoisture, exportToNdvi} from '@/crudFunctions/crudMonitor'//getFechasSentinelForInformes
import {getAllEnterprises, getEnterprise, getDataCampaign,getDataProduccion} from '@/crudFunctions/crudEnterprise'//getFechasSentinelForInformes
import {getAllCooperatives, getCooperative} from '@/crudFunctions/crudCooperativas'
import AlertaGeneral from "@/components/AlertaGeneral";
import Visor from './VisorComponent'
export default {
    name: 'Monitor',
    components: {AlertaGeneral, Visor},
    data(){
        return {
            iswithGraphic: false,
            exportarExcel: false,
            //
            keyComponentMonitor: 0,
            visibleModal: false,
            visibleModalImages: false,
            data: {},
            dataCampana:{},
            dataProduccion:{},
            fechasArr: Array(),
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
            selectValueCapa: '',
            //
            SentinelLayer: 'NDVI',
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            time: ``,
            valueDates: [],
            valueRange: [],
            timeValuesArr: [],
            nombreInforme: `Gráfico - ${this.getNow()}`,
            checked_clouds: false,
            //
            tipoAlerta: `error`,
            mensajeAlerta: '',
            //
            fechasParcelasNumImages: {},
            verCargandoImagenes: false,
            //
            disabledGenerar: false,
            //
            verErrorIntervalo: false,
            verCargandoFechasBbox: false,
            //
            initialStep: 1,
            steps: [
                "Nombre de informe y Selección de Parcelas",
                "Selección de capas y Nubes",
                "Selección de Fechas",
                "Resumen de Informe",
            ],
            open: [false, false, false, false],
            verTimeoutNumImg: false
        }
    },
    methods: {
        // para ordenar las empresas de la cooperativa alfabéticamente
        getSortedCooperativa(cooperativa) {
            return {
                ...cooperativa,
                enterprises: cooperativa.enterprises.slice().sort((a, b) => {
                return a.name.localeCompare(b.name);
                }),
            };
        },
        onChangeLayer(){
            this.exportarExcel = false
        },
        actionVisibleModal(action){
            this.visibleModal = action
        },
        actionChangeAccordeon(ev){
            this.open = this.$refs.acc.state.map((item, index) => index === ev.changedIndex);
        },
        getFechas(){
            /*
            this.verTimeoutNumImg = false
            if(this.timeValuesArr.length === 0){
                this.mensajeAlerta = 'No se ha seleccionado ningún intervalo de fechas'
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                this.verErrorIntervalo = true
                return false
            }
            this.verCargandoImagenes = true
            let fechasNum = 0
            getFechasParcelsPreCreate(this.rowSelects, this.timeValuesArr)
            .then(response => {
                console.info(response.data)
                this.fechasParcelasNumImages = response.data
                //getFechasSentinelForInformes(response.data.toString())
                //.then(response => {console.info(response.data)})

                this.verCargandoImagenes = false
                console.info(response.data, Object.entries(response.data))
                Object.entries(response.data).forEach(entry => {
                    const [key, value] = entry;
                    console.log(key, value);
                    fechasNum = fechasNum + value.resultados.length
                });
                if(fechasNum === 0){
                    this.disabledGenerar = true
                }else{
                    this.disabledGenerar = false
                }
            })
            .catch(() => {this.verCargandoImagenes = false; this.verTimeoutNumImg = true})
            */
        },
        getFechasSentBBOX(){
            /*
            this.verCargandoFechasBbox = true
            getFechasParcelsBBOX(this.rowSelects, this.timeValuesArr)
            .then(response => {
                console.info(response.data)

                const respuesta = response.data
                    const fechasArray = Array()
                    respuesta.forEach(feature =>{
                        fechasArray.push(feature.properties.date)
                    })
                    this.valueDates = fechasArray.reverse()
                this.verCargandoFechasBbox = false
            })
            .catch(() => this.verCargandoFechasBbox = false)
            
            */
        },
        getData(feature){
            const result = this.allParcelsOfEnterprisesFilter.filter(parcel => feature == (String(parcel.id)))
            const fechas = []
            let porcentNubesHigh = 0
            let uniqueFechas = []
            if(this.fechasParcelasNumImages[feature]){
                this.fechasParcelasNumImages[feature].resultados.map(resultado => {
                    if(resultado.properties.cloudCoverPercentage > porcentNubesHigh){
                        porcentNubesHigh = resultado.properties.cloudCoverPercentage 
                    }
                    fechas.push(resultado.properties.date)
                })
                uniqueFechas = [...new Set(fechas)];
            }
            
            return `<td>${result[0].properties.name}</td>
            <td>${this.fechasParcelasNumImages[feature] ? uniqueFechas.length : ''}</td>
            <td>${this.fechasParcelasNumImages[feature] ? uniqueFechas : ''}</td>
            <td>${this.checked_clouds ? this.fechasParcelasNumImages[feature] ? porcentNubesHigh +'%' : '' : 'n/a'}</td>`
            
        },
        toGenerar(){
            /*
            if(!this.nombreInforme){
                this.mensajeAlerta = 'El campo Nombre de Informe no debe estar vacío'
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                return false
            }
            if(this.timeValuesArr.length === 0){
                this.mensajeAlerta = 'No se ha seleccionado ningún intervalo de fechas'
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                this.verErrorIntervalo = true
                return false
            }
            if(this.selectValueCapa.length === 0){
                this.mensajeAlerta = 'No se ha seleccionado ninguna capa de Sentinel'
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                this.verErrorIntervalo = true
                return false
            }
            createInformes(this.nombreInforme, this.selectValueCapa, this.timeValuesArr, this.rowSelects, is_cooperative, id_enterprise, this.checked_clouds)
            .then(() => {
                this.$refs.modal_procesando.show()
            })
            */
        },
        showModalImagesUser(iswithGraphicReport){
            this.iswithGraphic = iswithGraphicReport;
            this.$refs.alerta_eliminar.show();
        },
        addImageReport(isWithImage){ 
            this.exportar(isWithImage);
        },
        exportar(isWithImage = false){
            let paramsString = isWithImage ? "?image=true" : "?image=false";
            paramsString += "&IswithGraphic="+this.iswithGraphic;
            this.$refs.alerta_eliminar.hide(); 

            // show user message
            this.mensajeAlerta = 'El proceso se ha lanzado correctamente. Tenga paciencia, puede requerir varios minutos para completarse. En caso de error recibirá un correo electrónico informativo'
            this.tipoAlerta = 'info' 
            this.$refs.alertaGenerallModalReport.verAlerta()
            this.verErrorIntervalo = true
            
            if(this.selectValueCapa === 'NDVI'){
                
                exportToNdvi(this.data,paramsString)
                .then(response => {
                    if (Object.hasOwn(response.data, 'data')) {
                    window.open('https://monitord4sf.devsmb.es/media/parcels/'+response.data.data)
                        //window.open('http://127.0.0.1:7000/media/parcels/'+response.data.data)
                    }

                    if(response.data.message){
                        
                        this.mensajeAlerta = response.data.message
                        this.tipoAlerta = response.data.error ? 'error' : 'warning'
                        this.$refs.alertaGenerallModalReport.verAlerta(false)
                        this.verErrorIntervalo = true
                        
                        //this.$refs.alertaGenerall.hideAlert = false
                        return false
                    }

                    
                })
                .catch(() => {
                    this.mensajeAlerta = 'No se ha podido completar la solicitud'
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                    this.verErrorIntervalo = true
                    return false
                })
            }else{
                exportToMoisture(this.data,paramsString)
                .then(response => {

                    if (Object.hasOwn(response.data, 'data')) {
                    window.open('https://monitord4sf.devsmb.es/media/parcels/'+response.data.data)
                        //window.open('http://127.0.0.1:7000/media/parcels/'+response.data.data)
                    }

                    if(response.data.message){
                        
                        this.mensajeAlerta = response.data.message
                        this.tipoAlerta = response.data.error ? 'error' : 'warning' 
                        this.$refs.alertaGenerallModalReport.verAlerta()
                        this.verErrorIntervalo = true
                        return false
                    }

                })
                .catch(() => {
                    this.mensajeAlerta = 'No se ha podido completar la solicitud'
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                    this.verErrorIntervalo = true
                    return false
                })
            }
        },
        generarInforme(){
            // Consultamos si las parcelas existen
            const results = this.allParcelsOfEnterprisesFilter.filter(parcel => this.rowSelects.includes(String(parcel.id)))
            const parcelsId = []
            results.map(result => parcelsId.push(result.id))
            // Comprobaciones de fecha y capa
            if(this.timeValuesArr.length === 0){
                this.mensajeAlerta = 'No se ha seleccionado ningún intervalo de fechas'
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                this.verErrorIntervalo = true
                return false
            }
            if(this.selectValueCapa.length === 0){
                this.mensajeAlerta = 'No se ha seleccionado ninguna capa de Sentinel'
                this.tipoAlerta = 'error'
                this.$refs.alertaGenerall.verAlerta()
                this.verErrorIntervalo = true
                return false
            }
            if(this.selectValueCapa === 'NDVI'){
                getDataNdvi(this.timeValuesArr[0], this.timeValuesArr[1], parcelsId)
                .then(response => {
                    const fechasDetectadas = Object.keys(response.data)
                    const text = parcelsId.toString();
                    fechasDetectadas.map(fecha => {
                        const parcelsIdSinProcesar = text.split(",")
                        response.data[fecha].resultado.map(parcela => {
                            parcelsIdSinProcesar.splice(parcelsIdSinProcesar.indexOf(parcela.parcel.toString()), 1);
                        })
                        const results = this.allParcelsOfEnterprisesFilter.filter(parcel => parcelsIdSinProcesar.includes(String(parcel.id)))
                        results.map(parcela => {
                            response.data[fecha].resultado.push(
                                {
                                    "id": parcela.id,
                                    "parcel": parcela.id,
                                    "name": parcela.properties.name,
                                    
                                    "pix_azul_total": 0.0,
                                    "pix_azul_total_porcent": 0.0,
                                    "pix_azul_altos_total": 0.0,
                                    "pix_azul_altos_porcent": 0.0,
                                    "pix_azul_altos_area_porcent": 0.0,
                                    "pix_azul_medios_total": 0.0,
                                    "pix_azul_medios_porcent": 0.0,
                                    "pix_azul_medios_area_porcent": 0.0,
                                    "pix_azul_bajos_total": 0.0,
                                    "pix_azul_bajos_porcent": 0.0,
                                    "pix_azul_bajos_area_porcent": 0.0,
                                    "pix_amarillo_total": 0.0,
                                    "pix_amarillo_total_porcent": 0.0,
                                    "pix_amarillo_altos_total": 0.0,
                                    "pix_amarillo_altos_porcent": 0.0,
                                    "pix_amarillo_altos_area_porcent": 0.0,
                                    "pix_amarillo_medios_total": 0.0,
                                    "pix_amarillo_medios_porcent": 0.0,
                                    "pix_amarillo_medios_area_porcent": 0.0,
                                    "pix_amarillo_bajos_total": 0.0,
                                    "pix_amarillo_bajos_porcent": 0.0,
                                    "pix_amarillo_bajos_area_porcent": 0.0,
                                    
                                    "pix_rojo_total": 0.0,
                                    "pix_rojo_total_porcent": 0.0,
                                    "pix_rojo_altos_total": 0.0,
                                    "pix_rojo_altos_porcent": 0.0,
                                    "pix_rojo_altos_area_porcent": 0.0,
                                    "pix_rojo_medios_total": 0.0,
                                    "pix_rojo_medios_porcent": 0.0,
                                    "pix_rojo_medios_area_porcent": 0.0,
                                    "pix_rojo_bajos_total": 0.0,
                                    "pix_rojo_bajos_porcent": 0.0,
                                    "pix_rojo_bajos_area_porcent": 0.0,
                                    "pix_verde_total": 0.0,
                                    "pix_verde_total_porcent": 0.0,
                                    "pix_verde_altos_total": 0.0,
                                    "pix_verde_altos_porcent": 0.0,
                                    "pix_verde_altos_area_porcent": 0.0,
                                    "pix_verde_medios_total": 0.0,
                                    "pix_verde_medios_porcent": 0.0,
                                    "pix_verde_medios_area_porcent": 0.0,

                                    "nubes_porcent": 0,
                                    "plantas_reales": 0,
                                    "cosecha": 0
                                }
                            )
                            response.data[fecha].resultado.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
                        })
                    })
                    
                    this.exportarExcel = true
                    this.data = response.data
                    this.fechasArr = Object.keys(response.data)
                    this.keyComponentMonitor +=1
                })
                .catch(() => {
                    this.mensajeAlerta = 'No se ha podido completar la solicitud'
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                    this.verErrorIntervalo = true
                    return false
                })
            }else{
                getDataMoisture(this.timeValuesArr[0], this.timeValuesArr[1], parcelsId)
                .then(response => {
                    const fechasDetectadas = Object.keys(response.data)
                    const text = parcelsId.toString();
                    fechasDetectadas.map(fecha => {
                        const parcelsIdSinProcesar = text.split(",")
                        response.data[fecha].resultado.map(parcela => {
                            parcelsIdSinProcesar.splice(parcelsIdSinProcesar.indexOf(parcela.parcel.toString()), 1);
                        })
                        const results = this.allParcelsOfEnterprisesFilter.filter(parcel => parcelsIdSinProcesar.includes(String(parcel.id)))
                        results.map(parcela => {
                            response.data[fecha].resultado.push(
                                {
                                    "id": parcela.id,
                                    "parcel": parcela.id,
                                    "name": parcela.properties.name,
                                    "pix_naranja_total": 0.0,
                                    "pix_naranja_porcent": 0.0,
                                    "pix_naranja_area_porcent": 0.0,
                                    "pix_amarillo_total": 0.0,
                                    "pix_amarillo_porcent": 0.0,
                                    "pix_amarillo_area_porcent": 0.0,
                                    "pix_verde_total": 0.0,
                                    "pix_verde_porcent": 0.0,
                                    "pix_verde_area_porcent": 0.0,
                                    "pix_azul_claro_total": 0.0,
                                    "pix_azul_claro_porcent": 0.0,
                                    "pix_azul_claro_area_porcent": 0.0,
                                    "pix_azul_medio_total": 0.0,
                                    "pix_azul_medio_porcent": 0.0,
                                    "pix_azul_medio_area_porcent": 0.0,
                                    "pix_azul_oscuro_total": 0.0,
                                    "pix_azul_oscuro_porcent": 0.0,
                                    "pix_azul_oscuro_area_porcent": 0.0,

                                    "nubes_porcent": 0,
                                    "plantas_reales": 0,
                                    "cosecha": 0
                                }
                            )
                            response.data[fecha].resultado.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
                        })
                    })
                    this.exportarExcel = true
                    this.data = response.data
                    this.fechasArr = Object.keys(response.data)
                    this.keyComponentMonitor +=1
                })
                .catch(() => {
                    this.mensajeAlerta = 'No se ha podido completar la solicitud'
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                    this.verErrorIntervalo = true
                    return false
                })
            }

            getDataCampaign(this.timeValuesArr[0], this.timeValuesArr[1], parcelsId)
                .then(response => {
                    this.dataCampana=response.data
                    })
            getDataProduccion(this.timeValuesArr[0], this.timeValuesArr[1], parcelsId)
                .then(response => {
                    this.dataProduccion=response.data 
                    })
            
            /*
            results.map(result => {
                enterprisesInResults.push(result.properties.enterprise_id)
            })
            console.info('Resultados empresa => ',enterprisesInResults)
            const uniqueEmpresas = [...new Set(enterprisesInResults)]
            console.info('Unificamos empresa => ',uniqueEmpresas)
            if(uniqueEmpresas.length > 1){
                //*Es multiempresa
                console.info('Seleccion Multiempresa')
                //Comprobar si es cooperativa
                const enterprisesInResultsCoop = []
                this.arrCooperativas.map(cooperative => {
                    cooperative.enterprises.map(enterprise => {
                        if(uniqueEmpresas.includes(enterprise.id)){
                            enterprisesInResultsCoop.push(cooperative.id)
                        }
                    })
                })
                console.info('Resultado Cooperativas => ',enterprisesInResultsCoop)
                if(enterprisesInResultsCoop.length == uniqueEmpresas.length){
                    console.info('Todas las empresas Pertenecen a cooperativas')
                    const uniqueCoops = [...new Set(enterprisesInResultsCoop)]
                    if(uniqueCoops.length > 1){
                        console.info('MultiCoop')
                        console.info('Cooperativas', uniqueCoops)
                        console.info('No se puede generar el informe, parcelas de distintas Cooperativas')
                        this.mensajeAlerta = 'No se puede generar el informe, parcelas seleccionadas de distintas Cooperativas'
                        this.tipoAlerta = 'error'
                        this.$refs.alertaGenerall.verAlerta()
                    }else{
                        console.info('UniCoop')
                        console.info('Cooperativa', uniqueCoops)
                        this.toGenerar(uniqueCoops[0], true)
                    }
                }else{
                    console.info('No se puede generar el informe, Hay una empresa que no pertenece a ninguna cooperativa')
                    this.mensajeAlerta = 'No se puede generar el informe, en la selección hay parcelas que no pertenecen a ninguna cooperativa'
                    this.tipoAlerta = 'error'
                    this.$refs.alertaGenerall.verAlerta()
                }
            }else{
                console.info('Seleccion Uniempresa')
                this.toGenerar(uniqueEmpresas[0], false)
            }*/
        },
        actionChangeDateRange(range){
            this.disabledGenerar = false
            this.verErrorIntervalo = false
            this.timeValuesArr = [range.startDate, range.endDate]
            this.time = `${range.startDate}/${range.endDate}`
        },
        chageCapas(capa){
            this.SentinelLayer = capa
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
                        this.allParcelsOfEnterprisesFilter = arrParcels
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
                }
            }
        },
        getNow() {
            const today = new Date();
            const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            //const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            //const dateTime = date +' '+ time;
            //this.timestamp = dateTime;
            //console.info(dateTime)
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
                    column = 'enterprise'
                    break
                default:
                    column = `name`
            }
            if(orden == 'ascending'){
                this.allParcelsOfEnterprisesFilter.sort((a, b) => parseFloat(a.name) - parseFloat(b.name));
            }
            console.info(column)
        },
    },
    mounted: function () {
        //console.info(this.$refs.acc)
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
                
                if(this.is_superuser || this.is_systemadmin){
                    //console.info('entra')
                    getAllEnterprises()
                    .then(async response => {
                        this.arrEmpresas = response.data
                        //this.arrEmpresasList = response.data
                        // ordenar alfabeticamente
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
<style scoped>
    .bx--accordion__content{
        padding-right: 0px!important;
    }

    .bx--modal-container {
        overflow: unset !important;
    }
</style>
<style>
    .cien{
        padding-right: 0px!important;
    }

    .bx--modal-container {
        overflow: unset !important;
    }
</style>