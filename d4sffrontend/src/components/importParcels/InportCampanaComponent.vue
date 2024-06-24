<template>
    <div class="bx--grid">
        <br>
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <h2>Importar Campaña desde .xlsx <img src="../../assets/agriculture-analytics.svg" style="width: 40px;"></h2>
            </div>
        </div>
        <br>
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <p>Para poder importar los datos de campaña, el Excel debe contener las pestañas "Parcelas", "Datos Producción" y "Siembras"</p>
            </div>
        </div>
        <br>
        <div class="bx--row" style="margin-top: 20px;">
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3">
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
                        <cv-select-option v-for="empresa in cooperativa.enterprises" :value="String(empresa.id)"  v-bind:key="empresa.id">
                            {{empresa.name}}
                        </cv-select-option>
                    </cv-select-optgroup>
                </cv-select>
            </div>
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3">
                <cv-file-uploader
                kind=""
                label="Subir Archivo"
                helperText="El formato permitido es .xlsx o .xls"
                :accept="['.xlsx', '.xls']"
                :clear-on-reselect="false"
                :initial-state-uploading="false"
                :multiple="false"
                :removable="true"
                @change="onChangeFiles"
                remove-aria-label="Custom remove aria label" ref="fileUploader">
                </cv-file-uploader>
            </div>
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3">
                <cv-button
                    kind="primary"
                    :disabled="false"
                    @click="importarCampana"
                >
                    Importar
                </cv-button>
            </div>
        </div>
        <br>
        <h2>Pestaña parcelas</h2>
        <div class="bx--row">
            <div class="bx--col">
                <p>Parcelas importadas {{procesadas.length}}</p>
                <br>
                <cv-data-table :columns="['ID', 'PARCELA', 'CULTIVO', 'VARIEDAD', 'PLANTAS POR HA']">
                    <template slot="data" v-for="procesada in procesadas">
                        <cv-data-table-row 
                            v-for="feature in procesada"
                            :key="`${feature.id}`"
                            :value="`${feature.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"  >
                            <cv-data-table-cell>{{feature.ID_FINCA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PARCELA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.CULTIVO}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.VARIEDAD}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PLANTAS_HA}}</cv-data-table-cell>
                        
                        
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
            
            <div class="bx--col">
                <p>Errores parcelas {{erroresParcelas.length}}</p>
                <br>
                <cv-data-table :columns="['ID FINCA', 'PARCELA', 'ERROR']">
                    <template slot="data" v-for="error in erroresParcelas">
                        <cv-data-table-row 
                            v-for="feature in error"
                            :key="`${feature.id}`"
                            :value="`${feature.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"  >
                            <cv-data-table-cell>{{feature.ID_FINCA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PARCELA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.ERROR}}</cv-data-table-cell>
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
        </div>
        <br>
        <h2>Pestaña siembra</h2>
        <div class="bx--row">
            <div class="bx--col">
                <p>Siembras importadas {{siembras.length}}</p>
                <br>
                <cv-data-table :columns="['ID', 'PARCELA', 'FECHAS', 'VARIEDAD', 'PLANTAS REALES HA']">
                    <template slot="data" v-for="siembra in siembras">
                        <cv-data-table-row 
                            v-for="feature in siembra"
                            :key="`${feature.id}`"
                            :value="`${feature.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"  >
                            <cv-data-table-cell>{{feature.ID_FINCA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PARCELA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.FECHA_INICIO}} - {{feature.FECHA_FIN}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.VARIEDAD}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PLANTAS_REALES_HA}}</cv-data-table-cell>
                        
                        
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
            <div class="bx--col">
                <p>Errores siembras {{erroresSiembras.length}}</p>
                <br>
                <cv-data-table :columns="['ID FINCA', 'PARCELA', 'ERROR']">
                    <template slot="data" v-for="error in erroresSiembras">
                        <cv-data-table-row 
                            v-for="feature in error"
                            :key="`${feature.id}`"
                            :value="`${feature.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"  >
                            <cv-data-table-cell>{{feature.ID_FINCA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PARCELA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.ERROR}}</cv-data-table-cell>
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
        </div>

        <br>
        <h2>Pestaña Producción</h2>
        <div class="bx--row">
            <div class="bx--col">
                <p>Producciones importadas {{producciones.length}}</p>
                <br>
                <cv-data-table :columns="['ID', 'PARCELA', 'CULTIVO', 'VARIEDAD', 'PRODUCCION', 'FECHA TERMINO']">
                    <template slot="data" v-for="produccion in producciones">
                        <cv-data-table-row 
                            v-for="feature in produccion"
                            :key="`${feature.id}`"
                            :value="`${feature.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"  >
                            <cv-data-table-cell>{{feature.ID_FINCA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PARCELA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.CULTIVO}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.VARIEDAD}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PRODUCCION}} {{feature.TIPO_UD}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.FECHA_FIN}}</cv-data-table-cell>
                        
                        
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
            <div class="bx--col">
                <p>Errores producción {{erroresProducciones.length}}</p>
                <br>
                <cv-data-table :columns="['ID FINCA', 'PARCELA', 'ERROR']">
                    <template slot="data" v-for="error in erroresProducciones">
                        <cv-data-table-row 
                            v-for="feature in error"
                            :key="`${feature.id}`"
                            :value="`${feature.id}`"
                            :aria-label-for-batch-checkbox="`Custom aria label for row ${feature.id} batch`"  >
                            <cv-data-table-cell>{{feature.ID_FINCA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.PARCELA}}</cv-data-table-cell>
                            <cv-data-table-cell>{{feature.ERROR}}</cv-data-table-cell>
                        </cv-data-table-row>
                    </template>
                </cv-data-table>
            </div>
        </div>
        <br>

        <div class="bx--row">
            <div class="bx--col">
                <cv-button
                    kind="primary"
                    :disabled="totalParcelas ? false : true"
                    @click="importarCampanaConfirmar">
                    Confirmar importación
                </cv-button>
            </div>
        </div>
        <br>
        
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
        <AlertaGeneral ref="alertaGenerall" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        <cv-loading
            :active="isActiveLoading"
            :overlay="true">
        </cv-loading>

    
    </div>
</template>

<script>
import {getProfile, getPermisos} from '@/auth/index'
import {getAllEnterprises, getEnterprise} from '@/crudFunctions/crudEnterprise'//getFechasSentinelForInformes
import {getAllCooperatives, getCooperative} from '@/crudFunctions/crudCooperativas'
import {importCampanaFromFile} from '@/crudFunctions/crudEnterprise'
import AlertaGeneral from "@/components/AlertaGeneral";
export default {
    name: 'Monitor',
    components: {AlertaGeneral},
    data(){
        return {
            isActiveLoading: false,
            exportarExcel: false,
            //
            keyComponentMonitor: 0,
            visibleModal: false,
            data: {},
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
            verTimeoutNumImg: false,
            //
            file: null,
            procesadas: [],
            erroresParcelas: [],
            cambiadas: [],
            totalParcelas: 0,
            siembras: [],
            erroresSiembras: [],
            producciones: [],
            erroresProducciones: []
        }
    },
    methods: {
        actionVisibleModal(action){
            this.visibleModal = action
        },
        
        onChangeFiles(file){
            this.file = file
        },
        importarCampana(){
            if(!this.file){
                console.info('No hay archivo')
                this.mensajeAlerta = `Debe seleccionar un archivo`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
                return
            }
            if(!this.selectValueEmpresa){
                console.info('No hay empresa')
                this.mensajeAlerta = `Debe seleccionar una empresa`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
                return
            }
            console.info('Importando campaña')
            this.isActiveLoading = true
            importCampanaFromFile(this.file[0].file, this.selectValueEmpresa, false)
            .then(response => {
                
                this.isActiveLoading = false

                const formattedProcesadas = []
                var parcelasTotales = 0
                response.data.campanas.map(item => {
                    formattedProcesadas.push([item])
                    parcelasTotales++
                })
                const formattedErroresParcelas = []
                response.data.erroresParcelas.map(item => {
                    formattedErroresParcelas.push([item])
                })

                const formattedSiembra = []
                response.data.siembra.map(item => {
                    formattedSiembra.push([item])
                })
                const formattedErroresSiembra = []
                response.data.erroresSiembra.map(item => {
                    formattedErroresSiembra.push([item])
                })

                const formattedProduccion = []
                response.data.produccion.map(item => {
                    formattedProduccion.push([item])
                })
                const formattedErroresProduccion = []
                response.data.erroresProduccion.map(item => {
                    formattedErroresProduccion.push([item])
                })

                this.procesadas = formattedProcesadas
                this.erroresParcelas = formattedErroresParcelas

                this.siembras = formattedSiembra
                this.erroresSiembras = formattedErroresSiembra

                this.producciones = formattedProduccion
                this.erroresProducciones = formattedErroresProduccion
                this.totalParcelas = parcelasTotales


            })
            .catch(error => {
                this.isActiveLoading = false
                console.error(error)
                this.mensajeAlerta = `Error al importar campaña`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            })
        },

        importarCampanaConfirmar(){
            if(!this.file){
                console.info('No hay archivo')
                this.mensajeAlerta = `Debe seleccionar un archivo`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
                return
            }
            if(!this.selectValueEmpresa){
                console.info('No hay empresa')
                this.mensajeAlerta = `Debe seleccionar una empresa`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
                return
            }
            console.info('Importando campaña')
            this.isActiveLoading = true
            importCampanaFromFile(this.file[0].file, this.selectValueEmpresa, true)
            .then(() => {
                this.isActiveLoading = false
                this.mensajeAlerta = `Campaña importada correctamente`
                this.tipoAlerta = `success`
                this.$refs.alertaGenerall.verAlerta()

            })
            .catch(error => {
                this.isActiveLoading = false
                console.error(error)
                this.mensajeAlerta = `Error al importar campaña`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            })
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
                        this.arrEmpresasList = response.data
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