<template>
    <div>
        <h4>{{$t("graficos.imagen_sent")}} <img src="../../assets/satellite.svg" style="width: 20px;"></h4>
        <br>
        <div class="bx--row">
            <div class="bx--col-sm-2 bx--col-md-2 bx--col-lg-2" v-for="key in keys" :value="String(key)" v-bind:key="key" style="text-align: center;">
                <cv-interactive-tooltip :visible="false">
                    <template v-if="true" slot="trigger">
                        <img alt="" id="" :src="`${urlMedia}/`+datos[key].img" style="width: 100%; max-width: 110px">
                    </template>
                    <template v-if="datos[key].nubes.porcent != 'n/a'" slot="content">
                        <img alt="" id="" :src="`${urlMedia}/cloud_`+datos[key].img" style="width: 100%; max">
                    </template>
                </cv-interactive-tooltip>
                <!--
                <div v-if="datos[key].nubes.porcent != 'n/a' && parseInt(datos[key].nubes.porcent) > 10">
                    <cv-interactive-tooltip :visible="false">
                        <template v-if="true" slot="label">
                            <p style="text-align: center;">{{datos[key].fecha}}</p>
                        </template>
                        <template v-if="datos[key].nubes.porcent != 'n/a'" slot="trigger"><img src="../../assets/radar--weather.svg" style="width: 20px;">
                        </template>
                        <template v-if="true" slot="content">
                            <p>En esta Imagen hemos detectado nubes en un {{datos[key].nubes.porcent != 'n/a' ? (parseInt(datos[key].nubes.porcent) > 99 ? 100 : datos[key].nubes.porcent) + `%`: datos[key].nubes.porcent}}</p>
                        </template>
                    </cv-interactive-tooltip>
                </div>
                
                <div v-else>
                    <p style="text-align: center;">{{datos[key].fecha}}</p>
                </div>
                -->
                <div>
                    <p style="text-align: center;">{{datos[key].fecha}}</p>
                    <p style="text-align: center;">{{datos[key].nombre}}</p>
                </div>
                <br>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    props: {
        datos: Object(),
        urlMedia: String
    },
    data() {
        return {
            time: ``,
            srcImage:``,
            keys: Array()
        }
    },
    methods: {
        
    },
    
    mounted() {
        this.keys = Object.keys(this.datos)
    },
    };
</script>
