<template>
    <div id="control_der">
        <div id="edicionParcela">
            <p>{{$t("map.edit_rapido")}} - {{parcelSelected.properties.name}}</p>
            <div class="errorDraw" v-if="verErrorDraw"><br>{{`${errorDrawMsg}`}}</div>
            <br>
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
            <!-- D4SF-79 -->
            Area {{parcelSelected.properties.area ? parcelSelected.properties.area : areaForNewPolygon}}
            <!-- Area {{areaForNewPolygon ? areaForNewPolygon : parcelSelected.properties.area}} -->
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
            <br>
            <hr>
            <br>
            <p>{{$t("map.elimina_parcela")}}</p>
            <br>
            <cv-button
                style="width: 100%"
                kind="danger"
                size="small"
                :disabled="false"
                @click="eliminarPoligono"
            >
            {{$t("map.eliminar")}}
            </cv-button>
            <br>
            <br>
            <cv-button
                style="width: 100%"
                kind="primary"
                size="small"
                :disabled="false"
                @click="limpiarDibujo"
            >
                Volver a dibujar
            </cv-button>
        </div>
        <cv-modal
        ref="alerta_eliminar"
        kind="danger"
        :visible="visibleAlertaEliminar"
        @primary-click="confirmaElimar">
            <template slot="label">{{$t("map.seguro")}}</template>
            <template slot="title">{{$t("map.eliminar")}}</template>
            <template slot="content">
            <p>{{$t("map.seguro_parcel_del")}} {{valueName}}?</p>
            </template>
            <template slot="secondary-button">{{$t("map.cancelar")}}</template>
            <template slot="primary-button">{{$t("map.eliminar")}}</template>
        </cv-modal>
    </div>
</template>
<script>
import {putParcelPolygon, getEnterprise, setParcelsForInstance, deleteParcel} from '@/crudFunctions/crudEnterprise'
export default {
    name: 'ControllerQuickEdit',
    props: {
        parcelSelected: Object,
        verErrorDraw: Boolean,
        errorDrawMsg: String,
        coordinatesPoly: String,
        valueDesc: String,
        valueName: String,
        arrEnterprises: Array,
        arrCooperativas: Array,
        areaForNewPolygon: Number,
    },
    data() {
        return {
            invalidMessageDesc: '',
            invalidMessageName: '',
            visibleAlertaEliminar: false
        }
    },
    components: {
        
    },
    methods: {
        guardadoPoligono(){
            let flag = false
            if(this.valueName == ''){
                this.invalidMessageName = this.$t("newEnterprise.campo_requerido")
                flag = true
            }
            if(flag){
                return false
            }
            if(this.areaForNewPolygon === 0){
                this.areaForNewPolygon = this.parcelSelected.properties.area
            }
            putParcelPolygon(this.coordinatesPoly, this.parcelSelected.id, this.valueName, this.valueDesc, this.areaForNewPolygon)
            .then(response => {
                getEnterprise(response.data.enterprise)
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
                    
                    setParcelsForInstance(response.data.name, allCoordinates, response.data.sentinel_instance)
                    .then(() => {
                        this.$emit('setSentinelClearCache')
                        this.$emit('setcoordinatesPoly', '')
                        this.$emit('setifQuickEdit', false)
                        this.$emit('setverErrorDraw', false)
                        this.$emit('setEnterprise', this.arrEnterprises)
                        this.$emit('setAllParcelsOfEnterprises', arrParcels)
                    })
                    .catch(err => console.info(err))
                })
            })            
        },
        cancelarEdicion(){ {
            this.$emit('setSentinelClearCache')
            this.$emit('setcoordinatesPoly', '')
            this.$emit('setifQuickEdit', false)
            this.$emit('setverErrorDraw', false)
            this.$emit('setClearParcels')


            // todo : eduardo
            this.$emit('setVerCrearParcel', true)
            this.$emit('setVerCrearParcelDraw', true)
            this.$emit('setverguardadoOK', false)
            this.$emit('setClearFeatures')
            this.$emit('clearCacheDraw')
        }},
        eliminarPoligono(){
            this.$refs.alerta_eliminar.dataVisible = true
        },
        limpiarDibujo(){
            
            
            
            /* this.$emit('setClearFeatures')
            this.$emit('setSentinelClearCache')
            this.$emit('setcoordinatesPoly', '') */

            

             
            this.$emit('setClearFeatures')
            this.$emit('setVerCrearParcel', false)
            this.$emit('setVerCrearParcelDraw', false)
            
            this.$emit('setverErrorDraw', true)

            //this.$emit('setifQuickEdit', false)
            //this.$emit('setverErrorDraw', false)
        },
        confirmaElimar(){
            /**
             * this.parcelSelected.id
             * this.parcelSelected.properties.enterprise_id
             */
            deleteParcel(this.parcelSelected.id)
            .then(response => {
                console.info(response.data)
                getEnterprise(this.parcelSelected.properties.enterprise_id)
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
                    this.parcelaSeleccionada = 0
                    this.$refs.alerta_eliminar.dataVisible = false
                    this.montarMapa();
                    this.cancelarEdicion()
                    /*setParcelsForInstance(response.data.name, allCoordinates, response.data.sentinel_instance)
                    .then(() => {
                        this.$emit('setSentinelClearCache')
                        this.$emit('setcoordinatesPoly', '')
                        this.$emit('setifQuickEdit', false)
                        this.$emit('setverErrorDraw', false)
                        this.$emit('setEnterprise', this.arrEnterprises)
                        this.$emit('setAllParcelsOfEnterprises', arrParcels)
                    })
                    .catch(err => console.info(err))*/
                })
            })
            .catch(err => console.info(err))
            
            /*
            if(this.parcelaSeleccionada){
                const path = `${this.$apiURL}/parcels/${this.parcelaSeleccionada}/`
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .delete(path)
                .then(() => {
                    this.parcelaSeleccionada = 0
                    this.$refs.alerta_eliminar.dataVisible = false
                    this.montarMapa();
                    this.cancelarEdicion()
                })
                .catch(response =>{
                    console.log(response.error)
                });
            }
            */
            
        },
    },
    mounted: function () {
        
        
    },
    beforeCreate(){
        
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
</style>