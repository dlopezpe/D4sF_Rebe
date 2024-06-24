<template>
    <div>
        <h4>{{$t("graficos.tabla_colores")}} <img src="../../assets/crop-health.svg" style="width: 20px;"></h4>
        <div class="bx--row ">
            <div class="bx--col">
                <cv-toggle
                    :checked=true
                    label="Ver columnas de colores"
                    value="check-2"
                    :small="true"
                    :hide-label="true"
                    @change="actionChangedToggleColores">
                    <template slot="text-left">Desactivadas las columnas con colores</template>
                    <template slot="text-right">Activadas las columnas con colores</template>
                </cv-toggle>
            </div>
            <div class="bx--col"> 
                <cv-toggle
                    :checked=true
                    label="ver columnas de imagenes"
                    value="check-1"
                    :small="true"
                    :hide-label="true"
                    @change="actionChangedToggleImagenes">
                    <template slot="text-left">Desactivada la presentacion de imagenes</template>
                    <template slot="text-right">Activada la presentacion de imagenes</template>
                </cv-toggle>
            </div>
        </div>
        <br>
        <cv-data-table
            ref="table"
            @sort="onSort"
            v-model="rowSelects"
            searchLabel="Filter" searchPlaceholder="Filter" searchClearLabel="Clear filter">
            <template slot="headings">
                <cv-data-table-heading :heading="$t('adminEnterprise.nombre')"/>

                <cv-data-table-heading :heading="$t('graficos.fecha_gen')" v-if="verFechaGen"/>

                <cv-data-table-heading v-if="vercolores" :heading="$t('graficos.rojo_naran')"/>
                <cv-data-table-heading v-if="vercolores" :heading="$t('graficos.amarillo')"/>
                <cv-data-table-heading v-if="vercolores" :heading="$t('graficos.verde')"/>

                <cv-data-table-heading v-if="vercolores" :heading="$t('graficos.azul_claro')"/>
                <cv-data-table-heading v-if="vercolores" :heading="$t('graficos.azul_medio')"/>
                <cv-data-table-heading v-if="vercolores" :heading="$t('graficos.azul_oscuro')"/>
                <cv-data-table-heading :heading="$t('graficos.clouds')"/>

                <cv-data-table-heading v-if="verimagenes" :heading="$t('graficos.imagen')"/>
                <cv-data-table-heading v-if="verimagenes" :heading="$t('graficos.imagenClouds')"/>
                <cv-data-table-heading v-if="verimagenes" :heading="$t('graficos.imagenTrueColor')"/>

                <cv-data-table-heading :heading="$t('graficos.plantas')"/>
                <cv-data-table-heading :heading="$t('graficos.cosecha')"/>
                <cv-data-table-heading :heading="$t('graficos.fecha_recogida')"/>
                <cv-data-table-heading :heading="$t('graficos.fecha_estimada_recogida')"/>
            </template>
            <template v-if="true" slot="batch-actions">
                <cv-button v-if="datoempresa==id_agraz">
                        
                </cv-button> 
            </template>
            <template slot="batch-actions">
                <cv-button @click="fechateorica" v-if="datoempresa==id_agraz">
                        Establecer fecha teórica de recogida
                        <Edit32 class="bx--btn__icon" />
                </cv-button>
            </template>
            <template slot="data">
                <cv-data-table-row  v-for="dato in datos" :value="String(dato.parcel)" v-bind:key="dato" :aria-label-for-batch-checkbox="`Custom aria label for row ${dato.id} batch`">
                    <cv-data-table-cell>
                        {{dato.name}}
                    </cv-data-table-cell>

                    <cv-data-table-cell v-if="vercolores">
                        {{dato.pix_naranja_porcent + `%`}}
                        <span v-if="dato.pix_naranja_area_porcent">
                            {{"-"}}
                            {{Math.round((dato.pix_naranja_area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="dato.pix_naranja_porcent > 1.00" :style="`width: ${dato.pix_naranja_porcent}%; height: 10px; background: #ff8000;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #ff8000;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="vercolores">
                        {{dato.pix_amarillo_porcent + `%`}}
                        <span v-if="dato.pix_amarillo_area_porcent">
                            {{"-"}}
                            {{Math.round((dato.pix_amarillo_area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="dato.pix_amarillo_porcent > 1.00" :style="`width: ${dato.pix_amarillo_porcent}%; height: 10px; background: #ffdf00;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #ffdf00;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="vercolores">
                        {{dato.pix_verde_porcent + `%`}}
                        <span v-if="dato.pix_verde_area_porcent">
                            {{"-"}}
                            {{Math.round((dato.pix_verde_area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="dato.pix_verde_porcent > 1.00" :style="`width: ${dato.pix_verde_porcent}%; height: 10px; background: #66ff98;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #66ff98;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="vercolores">
                        {{dato.pix_azul_claro_porcent + `%`}}
                        <span v-if="dato.pix_azul_claro_area_porcent">
                            {{"-"}}
                            {{Math.round((dato.pix_azul_claro_area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="dato.pix_azul_claro_porcent > 1.00" :style="`width: ${dato.pix_azul_claro_porcent}%; height: 10px; background: #02fefc;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #02fefc;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="vercolores">
                        {{dato.pix_azul_medio_porcent + `%`}}
                        <span v-if="dato.pix_azul_medio_area_porcent">
                            {{"-"}}
                            {{Math.round((dato.pix_azul_medio_area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="dato.pix_azul_medio_porcent > 1.00" :style="`width: ${dato.pix_azul_medio_porcent}%; height: 10px; background: #0087ff;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #0087ff;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="vercolores">
                        {{dato.pix_azul_oscuro_porcent + `%`}}
                        <span v-if="dato.pix_azul_oscuro_area_porcent">
                            {{"-"}}
                            {{Math.round((dato.pix_azul_oscuro_area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="dato.pix_azul_oscuro_porcent > 1.00" :style="`width: ${dato.pix_azul_oscuro_porcent}%; height: 10px; background: #2000ff;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #2000ff;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{dato.nubes_porcent + `%`}}
                        <span :style="`width: ${(dato.nubes_porcent > 1.00) ? dato.nubes_porcent : 2}%; height: 10px; background: #f904bb;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="verimagenes">
                        <img alt="" id=""  :src="`https://monitord4sf.devsmb.es/`+dato.image" style="width: 100px;">
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="verimagenes">
                        <img alt="" id=""  :src="`https://monitord4sf.devsmb.es/`+dato.nubesImage" style="width: 80px;">
                    </cv-data-table-cell>
                    <cv-data-table-cell v-if="verimagenes">
                        <img alt="" id=""  :src="`https://monitord4sf.devsmb.es/`+dato.trueColorImage" style="width: 80px;">
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{getdatoPlantas(dato)}}
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{getdatoCosecha(dato)}}
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{getdatofecha(dato)}}
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{getdatoestimacion(dato)}}
                    </cv-data-table-cell>
                </cv-data-table-row>
            </template>
        </cv-data-table>
        <cv-modal
            ref="establecer_fecha"
            @primary-click="establecer_fecha"
        >
            <template slot="label">Introduce a continuación la fecha estimada de recogida de las parcelas seleccionadas.</template>
            <template slot="title">Introduce a continuación la fecha estimada de recogida de las parcelas seleccionadas.</template>
            <template slot="content">
                <div class="bx--row">
                    <div class="bx--col">
                        <cv-date-picker
                            kind="single"
                            :cal-options="calOptions"
                            @change="actionChangeDate"
                            :dateLabel="$t('map.fecha')"
                            v-model="fechaRecogida"
                            placeholder="mm/dd/yyyy"
                            ref="cambiosFechas"
                            style="width: 100%!important"
                        ></cv-date-picker>
                    </div>
                </div>
            </template>
            <template slot="secondary-button">{{$t("graficos.cancelar")}}</template>
            <template slot="primary-button">{{$t('graficos.guardar')}}</template>
        </cv-modal>
        <AlertaGeneral ref="alertaGenerall" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
    </div>
</template>
<script>

import AlertaGeneral from "@/components/AlertaGeneral";
import {establecer_recogida} from '@/crudFunctions/crudEnterprise'
export default {
    components:{AlertaGeneral},
    props: {
        datosCampana: Object(),
        datosProduccion: Object(),
        datos: Object(),
        urlMedia: String,
        datoempresa:String,
    },
    data() {
        return {
            time: ``,
            srcImage:``,
            keys: Array(),
            calOptions: {
                "dateFormat": "Y-m-d"
            },
            "columns": [
                this.$t('adminEnterprise.nombre'),
                this.$t('graficos.rojo_naran'),
                this.$t('graficos.amarillo'),
                this.$t('graficos.verde'),
                this.$t('graficos.azul_claro'),
                this.$t('graficos.azul_medio'),
                this.$t('graficos.azul_oscuro'),
                this.$t('graficos.clouds'),
                this.$t('graficos.imagen'),
                this.$t('graficos.imagenClouds'),
                this.$t('graficos.plantas'),
                this.$t('graficos.cosecha'),
                this.$t('graficos.fecha_recogida'),
                this.$t('graficos.fecha_estimada_recogida'),
            ],
            verFechaGen: false,
            vercolores: true,
            verimagenes:true,
            rowSelects:[],
            fechaRecogida:"",
            //
            tipoAlerta: `error`,
            mensajeAlerta: '',
            //
            id_agraz:'7de27d39-1e42-4c6a-be53-67a72e1c98dc'
        }
    },
    methods: {
        compare( a, b ) {
            if ( a.last_nom < b.last_nom ){
                return -1;
            }
            if ( a.last_nom > b.last_nom ){
                return 1;
            }
            return 0;
        },
        getdatoPlantas(dato){
            try{
                const anio=dato.date.substring(0,4)
                const parcela=dato.parcel
                let plantas= this.datosCampana[anio].resultado.filter(x=>x.parcela==parcela)
                return plantas[0].plantas
            }
            catch (e){
                return "No hay datos"
            }
        },
        getdatoCosecha(dato){
            try{
                const anio=dato.date.substring(0,4)
                const parcela=dato.parcel
                let cosecha= this.datosProduccion[anio].resultado.filter(x=>x.parcela==parcela)
                return cosecha[0].produccion
            }
            catch(e){
                return "No hay datos"
            }
        },
        getdatofecha(dato){
            try{
                const anio=dato.date.substring(0,4)
                const parcela=dato.parcel
                let fecha= this.datosProduccion[anio].resultado.filter(x=>x.parcela==parcela)
                return fecha[0].fecha_fin
            }
            catch(e){
                return "No hay datos"
            }
        },
        getdatoestimacion(dato){
            try{
                const parcela=dato.parcel
                const anio=dato.date.substring(0,4)
                let plantas= this.datosCampana[anio].resultado.filter(x=>x.parcela==parcela)
                return plantas[0].fecha_recogida_estimada
            }
            catch (e){
                return "No hay datos"
            }
        },
        actionChangedToggleColores(value){
            this.vercolores=value
        },
        actionChangedToggleImagenes(value){
            this.verimagenes=value
        },
        fechateorica(){
            console.log(this.rowSelects)
            console.log(this.rowSelects.length)
            if (this.rowSelects.length<=0){
                this.mensajeAlerta = `No hay parcelas seleccionadas`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            }else{
                this.$refs.establecer_fecha.dataVisible = true
            }
        },
        async establecer_fecha(){
            await establecer_recogida(this.rowSelects, this.fechaRecogida)
            .then(() => {
                this.mensajeAlerta = `Fecha actualizada correctamente`
                this.tipoAlerta = `success`
                this.$refs.alertaGenerall.verAlerta()
            })
            .catch(() => {
                this.mensajeAlerta = `Error al actualizar la fecha`
                this.tipoAlerta = `error`
                this.$refs.alertaGenerall.verAlerta()
            })
            this.$refs.establecer_fecha.hide()
        },
    },
    
    mounted() {
        this.keys = Object.keys(this.datos)
    },
    
    };
</script>