<template>
    <div class="bx--grid" @mousedown="keepPositionScroll" @mouseup="putPositionScroll">
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <h2>Generador de Informes <img src="../../assets/crop-growth.svg" style="width: 40px;"></h2>
                <p>{{$t("adminEnterprise.info_nav")}}</p>
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
                        <cv-select-option v-for="empresa in arrEmpresasList" :value="String(empresa.id)" v-bind:key="empresa.id">
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
        <div class="bx--row">
            <div class="bx--col-sm-2 bx--col-md-2 bx--col-lg-2">
                <cv-progress
                :initial-step="rowSelects.length ? selectValueCapa.length ? timeValuesArr.length ?  3 : 2 : 1 : 0"
                :steps="steps"
                :vertical="true"></cv-progress>
            </div>
            <div class="bx--col">
                <cv-accordion @change="actionChangeAccordeon" ref="acc">
                    <cv-accordion-item :open="open[0]">
                        <template slot="title">Nombre de informe y Selección de Parcelas </template>
                        <template slot="content">
                            <!-- Nombre de informe -->
                            <div class="bx--row">
                                <div class="bx--col">
                                    <p style="font-size: 14px">Indica a continuación el nombre que le quieres poner al informe que se va a generar.</p>
                                    <br>
                                    <cv-text-input
                                        :label="$t('graficos.nombre_informe')"
                                        v-model="nombreInforme"
                                        :disabled="false"
                                    ></cv-text-input>
                                </div>
                            </div>
                            <!-- Tabla de parcelas -->
                            <br>
                            <div class="bx--row">
                                <div class="bx--col">
                                    <div id="sentinelLayersList">
                                        <p style="font-size: 14px">Selecciona a continuación las parcelas sobre las que quieres realizar la consulta. Puedes utilizar el buscador para encontrar la/s parcela/s que necesitas. Para poder ver el nombre de todas las parcelas, por favor utiliza el selector que encontrarás en la parte inferior de la tabla.</p>
                                        <br>
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
                                            :title="$t('graficos.parcel_list')"
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
                                                    Revisa la tabla-resumen de la parte inferior para generar el Informe
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
                                    </div>
                                </div>
                            </div>
                        </template>
                    </cv-accordion-item>
                    <cv-accordion-item :open="open[1]">
                        <template slot="title">Selección de capas y Nubes</template>
                        <template slot="content" style="padding-right: 0">
                            <!-- Capas -->
                            <div class="bx--row">
                                <div class="bx--col-sm-4 bx--col-md-4 bx--col-lg-4">
                                    <p style="font-size: 14px">¿Qué información quieres consultar? Elige a continuación una de las opciones que se muestran.</p>
                                    <br>
                                    <cv-select :label="$t('graficos.sel_layer_sen')" v-model="selectValueCapa">
                                        <cv-select-option value="NDVI">{{$t("graficos.NDVI")}}</cv-select-option>
                                        <cv-select-option value="MOISTURE_INDEX">{{$t("graficos.mostisture_index")}}</cv-select-option>
                                    </cv-select>
                                </div>
                                <div class="bx--col">
                                    <p style="font-size: 14px">¿Quieres incluir detección de nubes en el informe? Esta información se verá reflejada en el informe, añadiendo una nueva imagen real y marcando en rojo la zona con cualquier tipo de nube así como el porcentaje de nubes.</p>
                                    <br>
                                    <cv-toggle
                                        :checked="checked_clouds"
                                        v-model="checked_clouds"
                                        label="Incluir análisis de Nubes"
                                        value="check-clouds"
                                        :small="false"
                                        :disabled="false"
                                        :hide-label="false">
                                        <template v-if="true" slot="text-left">No</template>
                                        <template v-if="true" slot="text-right">Sí</template>
                                    </cv-toggle>
                                </div>
                            </div>
                            <!-- Nubes -->
                        </template>
                    </cv-accordion-item>
                    <cv-accordion-item :open="open[2]">
                        <template slot="title">Selección de Fechas</template>
                        <template slot="content" style="padding-right: 0">
                            <div class="bx--row">
                                <div class="bx--col">
                                    <p style="font-size: 14px">Especifica a continuación el intervalo de fechas sobre el que quieres realizar la consulta. A la hora de generar el informe se mostrarán únicamente las imágenes de fechas disponibles en Sentinel.</p>
                                    <br>
                                    <cv-date-picker
                                        kind="range"
                                        :dateLabel="$t('graficos.fecha_incio')"
                                        :date-end-label="$t('graficos.fecha_fin')"
                                        :cal-options="calOptions"
                                        @change="actionChangeDateRange"
                                        :value="valueRange">
                                    </cv-date-picker>
                                    <p style="font-size: 12px; color: red" v-if="verErrorIntervalo">No se ha seleccionado ningún intervalo de fechas</p>
                                </div>
                            </div>
                            <br>
                            <div class="bx--row">
                                <div class="bx--col">
                                    <p style="font-size: 14px">Utilizando la siguiente opción se puede ver las fechas en las que hay fotografías dentro del intervalo de fechas escogido.</p>
                                    <br>
                                    <cv-date-picker
                                        kind="single"
                                        :cal-options="calOptions"
                                        :dateLabel="`Consultar fechas disponibles`"
                                        :value="valueDates"
                                        placeholder="mm/dd/yyyy"
                                        ref="cambiosFechas"
                                        style="width: 100%!important"
                                    ></cv-date-picker>
                                    <cv-button kind="primary" :disabled="false" v-if="rowSelects.length && timeValuesArr.length" @click="getFechasSentBBOX()">Consultar</cv-button>
                                    <cv-inline-loading
                                    :ending-text="`Cargado`"
                                    :error-text="`Error`"
                                    :loading-text="`Cargando..`"
                                    :loaded-text="`Cargando..`"
                                    :state="`loading`"
                                    v-if="verCargandoFechasBbox"></cv-inline-loading>
                                </div>
                            </div>
                        </template>
                    </cv-accordion-item>
                    <cv-accordion-item :open="open[3]">
                        <template slot="title">Resumen de Informe</template>
                        <template slot="content" style="padding-right: 0">
                                <div class="bx--row"  v-if="rowSelects.length">
                                    <div class="bx--col">
                                        <p style="font-size: 14px">Puedes utilizar el botón de Ver número de imágenes para que se haga una comprobación a Sentinel de las imágenes disponibles en el intervalo de fechas seleccionado así como las fechas en las que hay imagen del satélite.</p>
                                    </div>
                                </div>
                                <br>
                                <div class="bx--row">
                                    <div class="bx--col">
                                        <p style="font-size: 14px; color: red" v-if="disabledGenerar">En el intervalo de fechas seleccionado no hay ninguna imagen disponible para generar. Por favor, especifica otro intervalo de fechas en la zona superior.</p>
                                        <br>
                                        <cv-button kind="primary" v-if="rowSelects.length" @click="getFechas()">Ver número de imágenes</cv-button>
                                        <cv-inline-loading
                                        :ending-text="`Cargado`"
                                        :error-text="`Error`"
                                        :loading-text="`Cargando..`"
                                        :loaded-text="`Cargando..`"
                                        :state="`loading`"
                                        v-if="verCargandoImagenes"></cv-inline-loading>
                                        <p style="font-size: 14px; color: red" v-if="verTimeoutNumImg">Sentinel no ha podido procesar la previsualización de la obtención del número total de imágenes debido al volumen de datos. Esta previsualización es independiente de la generación del informe, por favor procede con la generación mediante el botón de Generar.</p>
                                    </div>
                                </div>
                                <br>
                                <div class="bx--row" v-if="rowSelects.length">
                                    <div class="bx--col">
                                        <cv-data-table
                                            :columns="[
                                                    {
                                                        key: 'name',
                                                        label: this.$t('graficos.nombre'),
                                                        'sortable': false
                                                    },
                                                    {
                                                        key: 'imgnum',
                                                        label: 'Número de Imagenes',
                                                        'sortable': false
                                                    },
                                                    {
                                                        key: 'fecha',
                                                        label: 'Fechas',
                                                        'sortable': false
                                                    },
                                                    {
                                                        key: 'fecha',
                                                        label: 'Max. Porcentaje Nubes Encontrado',
                                                        'sortable': false
                                                    }
                                                ]"
                                        >
                                            <template slot="data">
                                                <cv-data-table-row
                                                    v-for="feature in rowSelects"
                                                    :key="`${feature}`"
                                                    :value="`${feature}`"
                                                    :aria-label-for-batch-checkbox="`Custom aria label for row ${feature} batch`"
                                                    v-html="getData(feature)"
                                                >
                                                    
                                                </cv-data-table-row>
                                            </template>
                                        </cv-data-table>
                                    </div>
                                </div>
                                <br>
                                <div class="bx--row"  v-if="rowSelects.length">
                                    <div class="bx--col">
                                        <p style="font-size: 14px">Tomando como base las pruebas realizadas, el tiempo estimado de procesado será el siguiente</p>
                                    </div>
                                </div>
                                <br>
                                <div class="bx--row" v-if="rowSelects.length">
                                    <div class="bx--col">
                                        <div class="bx--grid">
                                            <cv-list :ordered="false">
                                                <cv-list-item>50 imágenes – 2 minutos</cv-list-item>
                                                <cv-list-item>100 imágenes – 4 minutos</cv-list-item>
                                                <cv-list-item>200 imágenes – 8 minutos</cv-list-item>
                                                <cv-list-item>400 imágenes – 16 minutos</cv-list-item>
                                            </cv-list>
                                        </div>
                                    </div>
                                </div>
                                <br>
                                <div class="bx--row">
                                    <div class="bx--col">
                                        <cv-button kind="primary" :disabled="disabledGenerar" v-if="rowSelects.length" @click="generarInforme()">{{$t("graficos.generar")}}</cv-button>
                                    </div>
                                </div>
                        </template>
                    </cv-accordion-item>
                </cv-accordion>
            </div>
        </div>
        <br>
        <br>
        <cv-modal ref="modal_procesando">
        <template slot="label">{{this.$t('graficos.gen_iformes')}}</template>
        <template slot="title">{{this.$t('graficos.gen_iformes')}}</template>
        <template slot="content"
            ><p>
                {{this.$t('graficos.grafico_procensandose')}}
            </p></template
            >
            <template slot="primary-button">{{this.$t('graficos.gen_informes_acceptar')}}</template>
        </cv-modal>
        <AlertaGeneral ref="alertaGenerall" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
    </div>
</template>
<script>
//import {getParcelsNotSentinelInstance, postParcelsNotSentinelInstance} from '@/crudFunctions/crudSentinel.js'
import {getProfile, getPermisos} from '@/auth/index'
import {getAllEnterprises, getEnterprise, createInformes, getFechasParcelsPreCreate, getFechasParcelsBBOX, getAllActiveEnterprises} from '@/crudFunctions/crudEnterprise'//getFechasSentinelForInformes
import {getAllCooperatives, getCooperative} from '@/crudFunctions/crudCooperativas'
import AlertaGeneral from "@/components/AlertaGeneral";
export default {
    name: 'ParcelsToSentinelComponent',
    components: {
        AlertaGeneral
    },
    data(){
        return {
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
            activeEmpresas: [],
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
            verTimeoutNumImg: false,
            scrollPosition: 0,
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
        actionChangeAccordeon(ev){
            this.open = this.$refs.acc.state.map((item, index) => index === ev.changedIndex);
        },
        fetchActiveempresas(){
            getAllActiveEnterprises()
                .then(response => {
                    this.activeEmpresas = response.data;  // Asigna las empresas activas a tu variable de datos
                })
                .catch(error => {
                    console.error('Error al obtener empresas activas:', error);
                });
        },
        getFechas(){
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
                /*
                
                */

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
            
        },
        getFechasSentBBOX(){
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
                /*
                getFechasSentinelForInformes(response.data.toString())
                .then(response => {
                    
                })
                */
                this.verCargandoFechasBbox = false
            })
            .catch(() => this.verCargandoFechasBbox = false)
            
            
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
        toGenerar(id_enterprise, is_cooperative){
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
            
        },
        generarInforme(){
            const results = this.allParcelsOfEnterprisesFilter.filter(parcel => this.rowSelects.includes(String(parcel.id)))
            const enterprisesInResults = []
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
            }
        },
        actionChangeDateRange(range){
            this.disabledGenerar = false
            this.verErrorIntervalo = false
            console.info(range)
            this.timeValuesArr = [range.startDate, range.endDate]
            console.info(this.timeValuesArr)
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
        console.info(this.$refs.acc)
        this.getNow()
        this.fetchActiveempresas();
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
                    getAllActiveEnterprises()
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
</style>