<template>
    <div>
        <div class="bx--row">
            <div class="bx--col">
                <ChartLine :datos="dataSent" :key="keyComponent" :layer="layer" v-if="verNDVI"/>
            </div>
        </div>
        <div class="bx--row">
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3"></div>
            <div class="bx--col-sm-12 bx--col-md-6 bx--col-lg-6" id="colSlider" style="margin-top: 60px;">
                <cv-slider 
                    id="pruebasSlider"
                    @change="onChangeSlider" 
                    label="Selecciona una fecha" 
                    :minLabel="fechasArr[0]" 
                    :maxLabel="fechasArr[fechasArr.length - 1]" 
                    :hideTextInput="true" min="0" 
                    :value="value"
                    :max="(fechasArr.length - 1)"> </cv-slider>
            </div>
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3"></div>
        </div>
        <div class="bx--row">
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-5"></div>
            <div class="bx--col-sm-12 bx--col-md-6 bx--col-lg-2" style="text-align: center; margin-top: 12px; font-weight: bold; margin-bottom: 12px;">
                <cv-text-input
                id="inputCursor"
                label="Fecha Seleccionada"
                :value="fechaSel">
                </cv-text-input>
            </div>
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-5"></div>
        </div>
        <div class="bx--row">
            <div class="bx--col" style="margin-top: 20px; margin-bottom: 120px;">
            <p><strong>Recuerda: </strong>la información de fecha teórica de recogida sólo se podrá introducir en las parcelas de la empresa con campaña de producción activa, en este caso únicamente Agraz.</p>
                <cv-accordion v-if="verNDVITabla" style="padding-right:0%">
                    <cv-accordion-item>
                        <template slot="title">Ver detalles</template>
                        <template slot="content">
                            <TableColors :datos="dataSent" :key="keyComponent" :datosCampana="dataCampana" :datosProduccion="dataProduccion" :datoempresa="empresa" v-if="verNDVITabla"/>
                        </template>
                    </cv-accordion-item>
                </cv-accordion>
                <cv-accordion v-if="verMOIS">
                    <cv-accordion-item>
                        <template slot="title">Ver detalles</template>
                        <template slot="content">
                            <TableColorsMois :datos="dataSent" :key="keyComponent" :datosCampana="dataCampana" :datosProduccion="dataProduccion" :datoempresa="empresa" v-if="verMOIS"/>
                        </template>
                    </cv-accordion-item>
                </cv-accordion>
            </div>
        </div>
    </div>
</template>

<script>
import ChartLine from '@/components/monitor/chartLine.vue'
import TableColors from '@/components/monitor/tableColors.vue'
import TableColorsMois from '@/components/monitor/tableColorsMois.vue'
export default {
    name: 'Visor',
    props: {
        data: Object(),
        dataCampana:Object(),
        dataProduccion:Object(),
        fechasArr: Array(),
        fechaSel: String,
        layer:String,
        empresa:String,
    },
    components: {
        ChartLine,
        TableColors,
        TableColorsMois
    },
    data() {
        return {
            verNDVI: false,
            verNDVITabla: false,
            verMOIS: false,
            prueba:"Prueba",
            value: 0,
            //fechaSel: 'AAAA',
            isActiveLoading: false,
            isVisibleLoad: true,
            dataAmarillos: Array(),
            dataAzules: Array(),
            dataRojos: Array(),
            dataVerdes: Array(),
            dataAmarillosAltos: Array(),
            dataAmarillosMedios: Array(),
            dataAmarillosBajos: Array(),
            dataAzulesAltos: Array(),
            dataAzulesMedios: Array(),
            dataAzulesBajos: Array(),
            dataRojosAltos: Array(),
            dataRojosMedios: Array(),
            dataRojosBajos: Array(),
            dataVerdesAltos: Array(),
            dataVerdesMedios: Array(),
            dataC1: Array(),
            dataC2: Array(),
            fechasC0: Array(),
            fechasC1: Array(),
            fechasC2: Array(),
            fechas: Array(),
            options: {
                responsive: true,
                maintainAspectRatio: false,
                hoverMode: "index",
                stacked: this.isMobile(),
                title: {
                    display: true,
                    text: this.$t('graficos.grafico_ndvi'),
                },
            },
            //data: Array(),
            //
            datosCampana:{},
            datosProduccion:{},
            datoempresa:"",
            fechasKeys: [],
            dataSent:Object(),
            keyComponent: 0,
        }
    },
    methods: {
        onChangeSlider(value){
            this.value = value
            this.fechaSel = this.fechasArr[value]
            //console.info(this.data[this.fechasArr[value]])
            if( this.data[this.fechasArr[value]].resultado !== "No hay datos disponibles"){
                this.dataSent = this.data[this.fechasArr[value]].resultado
                this.datosCampana=this.dataCampana
                this.datosProduccion=this.dataProduccion
                this.verNDVI = true
                if(this.layer === 'NDVI'){
                    this.verNDVITabla = true
                    this.verMOIS = false
                }else{
                    this.verNDVITabla = false
                    this.verMOIS = true
                }
                
                this.keyComponent += 1
            }else{
                this.verNDVI = false
            }
            /*
            if(value === 0){
                this.fechaSel = this.fechasArr[value]
            }else{
                this.fechaSel = this.fechasArr[value-1]
            }
            */
        }
    },
    mounted: function () {
        //console.info(this.data)
        const keys = Object.keys(this.data)
        this.fechasKeys = keys
        /*
        keys.forEach(key =>{
            console.info(key)
            console.info(this.data[key])
        })
        */
        //console.info('User Logged')
    },
    beforeCreate(){
        //console.info(this.data)
        const keys = Object.keys(this.data)
        this.fechasKeys = keys
        /*
        keys.forEach(key =>{
            console.info(key)
        })
        */

    }
}
</script>
<style >
.bx--slider-text-input{
    display: none;
}
.bx--accordion__content{
    padding-right: 0px!important;
}
.cien{
    padding-right: 0px!important;
}
</style>