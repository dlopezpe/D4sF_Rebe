<template>
    <div class="bx--grid">
        <br>
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <h2>Importar Parcelas para Hit22 desde .kml o .kmz <img src="../../assets/agriculture-analytics.svg" style="width: 40px;"></h2>
            </div>
        </div>
        <br>
        <div id="txt-explicativo" class="bx--row">
            <div class="bx--col">
                <p><b>ATENCION: </b>Confirmar la exportacion supone el borrado de las parcelas de la empresa seleccionada para crear las parcelas del archivo sin duplicados.</p>
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
                helperText="Los formatos permitidos son .kml y .kmz"
                :accept="['.kml']['.kmz']"
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
                    @click="importarParcelas"
                >
                    Subir archivo y ver resumen de importación
                </cv-button>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <p>Parcelas compatibles con Sentinel {{procesadas.length}}</p>
                <br>
                <cv-data-table
                    :columns="['Nombre de parcela']" 
                    :data="procesadas"   
                    ref="table"
                ></cv-data-table>
            </div>
            <div class="bx--col">
                <p>Errores en Sentinel {{errores.length}}</p>
                <br>
                <cv-data-table
                    :columns="['Nombre de parcela']" 
                    :data="errores"   
                    ref="table"
                ></cv-data-table>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col">
                <p>Se van a importar {{totalParcelas}} Parcelas</p>
                <cv-button
                    kind="primary"
                    :disabled="totalParcelas ? false : true"
                    @click="importarParcelasConfirmar">
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
import {importParcelsFromFileKML} from '@/crudFunctions/crudEnterprise'
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
            errores: [],
            cambiadas: [],
            totalParcelas: 0
        }
    },
    methods: {
        actionVisibleModal(action){
            this.visibleModal = action
        },
        
        onChangeFiles(file){
            this.file = file
        },
        importarParcelas(){
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
            console.info('Importando parcelas')
            this.isActiveLoading = true
            importParcelsFromFileKML(this.file[0].file, this.selectValueEmpresa, false,'true')
            .then(response => {
                this.isActiveLoading = false
                console.info(response.data)
                const formattedProcesadas = []
                response.data.procesadas.map(item => {
                    formattedProcesadas.push([item])
                })
                const formattedErrores = []
                response.data.Overlaps.map(item => { 
                    formattedErrores.push([item])
                })
                const formattedCambiadas = []
                response.data.cambiadas.map(item => {
                    formattedCambiadas.push([item])
                })
                this.procesadas = formattedProcesadas
                this.errores = formattedErrores
                this.totalParcelas = response.data.totalparcelas
                this.cambiadas = formattedCambiadas

            })
            .catch(error => {
                this.isActiveLoading = false
                console.error(error)
                this.mensajeAlerta = `Error al importar parcelas`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            })
        },

        importarParcelasConfirmar(){
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
            console.info('Importando parcelas')
            this.isActiveLoading = true
            importParcelsFromFileKML(this.file[0].file, this.selectValueEmpresa, true, 'true')
            .then((response) => {
                console.log(response)
                this.isActiveLoading = false
                this.mensajeAlerta = `Parcelas importadas correctamente`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            })
            .catch(error => {
                console.log(error)
                this.isActiveLoading = false
                this.mensajeAlerta = `Error al importar parcelas`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            })
            this.mensajeAlerta = `Parcelas importadas correctamente`
            this.tipoAlerta = `success`
            this.$refs.alertaGenerall.verAlerta()
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