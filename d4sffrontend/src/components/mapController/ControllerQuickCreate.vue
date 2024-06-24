<template>
    <div id="control_der">
        <div id="btnCrearParcela" v-if="verCrearParcel">
            <cv-button
            kind="primary"
            size="small"
            :disabled="verErrorDraw"
            @click="crearParcela"
            >
            {{$t("map.crear_parcela")}}
            </cv-button>  
        </div>
        <div id="edicionParcela" v-if="!verCrearParcel">
            <p>{{$t("map.parcela_nueva")}}</p>
            <div>
            <cv-select
                theme=""
                :label="$t('map.listado_empresas')"
                :hide-label="false"
                :inline="false"
                :disabled="false"
                @change="seleccionaEmpresa"
                >
                <cv-select-option disabled selected hidden>{{$t("map.sel_empresa")}}</cv-select-option>
                <cv-select-optgroup label="Todas las Empresas" v-if="is_superuser || is_systemadmin">
                    <cv-select-option :value="`all`" v-if="is_superuser || is_systemadmin">{{$t("map.most_todas_empresas")}}</cv-select-option>
                    <cv-select-option v-for="empresa in listadoEmpresas" :value="String(empresa.id)"  v-bind:key="empresa.id">
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
            <div class="errorDraw" v-if="verErrorDraw"><br>{{`${errorDrawMsg}`}}</div>
            <p>Creando parcela para {{arrEnterprisesSelectedObj.name}}</p>
            <p>Area {{areaForNewPolygon}}</p>
            <cv-text-input
                :label="'Nombre de la parcela'"
                :value="valueName"
                :disabled="false"
                :type="'text'"
                :invalid-message="invalidMessageName"
                ref="inputName"
                id="input-MIRLwtCq"
                v-model="valueName">
            </cv-text-input>
            <br>
            <cv-text-input
                :label="'Descripción'"
                :value="valueDesc"
                :disabled="false"
                :type="'text'"
                :invalid-message="invalidMessageDesc"
                ref="inputDesc"
                id="input-3zcRveTf"
                v-model="valueDesc"
                ></cv-text-input>
            <br>
            <br>
            <br>
            <cv-button
                kind="primary"
                size="small"
                :disabled="verErrorDraw"
                @click="guardadoPoligono"
            >
                {{$t("map.guardar")}}
            </cv-button>
            <cv-button
                kind="danger"
                size="small"
                :disabled="false"
                @click="cancelarEdicion"
            >
                {{$t("map.cancelar")}}
            </cv-button>
            <br>
            <div class="guardadoOK" v-if="verguardadoOK"><br>{{`${guardadoOKMsg}`}}</div>
            <br>
            <cv-button
                kind="primary"
                size="small"
                :disabled="false"
                @click="limpiarDibujo"
            >
                Volver a dibujar
            </cv-button>
        </div>
    </div>
</template>
<script>
import {createQuickParcel, getEnterprise, setParcelsForInstance} from '@/crudFunctions/crudEnterprise'

export default {
    name: 'ControllerQuickCreate',
    props: {
        verCrearParcel: Boolean,
        verErrorDraw: Boolean,
        errorDrawMsg: String,
        verguardadoOK: Boolean,
        guardadoOKMsg: String,
        coordinatesPoly: String,
        arrEnterprises: Array,
        arrEnterprisesSelected: Array,
        arrCooperativas: Array,
        is_superuser: Boolean,
        is_systemadmin: Boolean,
        areaForNewPolygon: Number,
        user: Object
    },
    data() {
        return {
            listadoEmpresas: this.arrEnterprises,
            arrEnterprisesSelectedObj: this.arrEnterprisesSelected[0],
            valueName:'',
            invalidMessageName:'',
            valueDesc:'',
            invalidMessageDesc:'',
            enterpriseForCreateParcel: ''
        }
    },
    components: {
        
    },
    methods: {
        seleccionaEmpresa(empresa){
            const result = this.listadoEmpresas.filter(enterprise => enterprise.id == empresa)
            console.info(result)
            this.arrEnterprisesSelectedObj = result[0]
            //this.arrEnterprisesSelected = result
            //this.enterpriseForCreateParcel = result
            this.$emit('setEnterpriseSelect', result)
            this.guardadoOKMsg = ''
        },
        crearParcela(){
            //setVerCrearParcel: muestra el formulario de creación de parcela y habilita el dibujo
            this.$emit('setVerCrearParcel', false)
            this.$emit('setverErrorDraw', true)
            this.$emit('setverguardadoOK', true)
            this.$emit('setVerCrearParcelDraw', false)
        },
        guardadoPoligono(){
            
            this.guardadoOKMsg = this.$t('parcelas.parcela_guardada_2')
            this.verguardadoOK = true
            // crea la parcela en el backend /parcels/
            createQuickParcel(this.valueName, this.valueDesc, this.coordinatesPoly, this.areaForNewPolygon, this.arrEnterprisesSelectedObj.id, this.user.id)
            .then(() => {
                // trae la informacion de la empresa y sus parcelas via get  
                getEnterprise(this.arrEnterprisesSelectedObj.id)
                .then(response => {
                    const allCoordinates = Array();
                    const arrParcels = []
                    
                    //const enterprise = response.data
                    const result = this.arrEnterprises.filter(enterprise => enterprise.id == response.data.id)
                    if(result.length == 1 && this.arrEnterprises.length > 1 ){
                        const posEnterprise = this.arrEnterprises.indexOf(result[0])
                        this.arrEnterprises[posEnterprise] = response.data
                        this.arrEnterprises.map(enterprise => {
                            enterprise.parcels.features.map(parcel => {
                                arrParcels.push(parcel)
                            })
                        })
                        response.data.parcels.features.map(parcel => {
                            allCoordinates.push(parcel.geometry.coordinates)
                        })
                    }else{
                        this.arrEnterprises[0] = response.data
                        response.data.parcels.features.map(parcel => {
                            allCoordinates.push(parcel.geometry.coordinates)
                            arrParcels.push(parcel)
                        })
                    }
                    this.guardadoOKMsg = this.$t('parcelas.parcela_guardada_2')
                    this.setverguardadoOK = true
                    setParcelsForInstance(response.data.name, allCoordinates, response.data.sentinel_instance)
                    .then(() => {
                        this.$emit('setSentinelClearCache')
                        this.$emit('setEnterprise', this.arrEnterprises)
                        this.$emit('setAllParcelsOfEnterprises', arrParcels)
                        this.cancelarEdicion()
                    })
                    .catch(err => console.info(err))
                })
            })
            /*
            name: this.$refs.inputName.$refs.input.value,
            description: this.$refs.inputDesc.$refs.input.value,
            polygon: this.poligonObjecto,
            area: this.area,
            enterprise: this.enterprise.id,
            user_created: sessionStorage.getItem('user')
            */
            /*
            putParcelPolygon(this.coordinatesPoly, this.parcelSelected.id)
            .then(response => {
                console.info(response.data)
                getEnterprise(response.data.enterprise)
                .then(response => {
                    const allCoordinates = Array();
                    response.data.parcels.features.map(parcel => {
                        allCoordinates.push(parcel.geometry.coordinates)
                    })
                    this.guardadoOKMsg = this.$t('parcelas.parcela_guardada_2')
                    this.setverguardadoOK = true
                    setParcelsForInstance(response.data.name, allCoordinates, response.data.sentinel_instance)
                    .then(response => {
                        console.info(response.data)
                        this.$emit('setSentinelClearCache')
                        this.$emit('setcoordinatesPoly', '')
                        this.$emit('setifQuickEdit', false)
                        this.$emit('setverErrorDraw', true)
                    })
                    .catch(err => console.info(err))
                })
            })
            */
        },
        cancelarEdicion(){ {
            this.$emit('setVerCrearParcel', true)
            this.$emit('setVerCrearParcelDraw', true)
            this.$emit('setverErrorDraw', false)
            this.$emit('setSentinelClearCache')
            this.$emit('setcoordinatesPoly', '')
            this.$emit('setifQuickEdit', false)
            this.$emit('setverErrorDraw', false)
            this.$emit('setverguardadoOK', false)
            this.$emit('setClearParcels')
            this.$emit('setClearFeatures')
            this.$emit('clearCacheDraw')
        }},
        limpiarDibujo(){
            this.$emit('setClearFeatures')
            this.$emit('setVerCrearParcel', false)
            this.$emit('setVerCrearParcelDraw', false)
        }
    },
    mounted: function () {
        
        
    },
    beforeCreate(){
        console.info(this.arrEnterprises)
    }
}
</script>
<style scoped>
    #control_der{
        margin-top: 58px;
        padding: 10px;
        background-color: #f4f4f4;
        position: fixed;
        top: 0px;
        right: 8px;
    }
    .errorDraw{
        color: #da1e28;
        font-weight: 400;
        font-size: 12px;
    }
    .guardadoOK{
        color: #00CC00;
        font-weight: 400;
        font-size: 12px;
    }
</style>