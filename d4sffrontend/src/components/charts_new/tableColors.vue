<template>
    <div>
        <h4>{{$t("graficos.tabla_colores")}} <img src="../../assets/crop-health.svg" style="width: 20px;"></h4>
        <br>
        <cv-data-table
        ref="table">
            <template slot="headings">
                <cv-data-table-heading :heading="$t('graficos.fecha_nombre')"/>

                <cv-data-table-heading :heading="$t('graficos.fecha_gen')"/>

                <cv-data-table-heading :heading="$t('graficos.rojos_altos')"/>
                <cv-data-table-heading :heading="$t('graficos.rojos_medios')"/>
                <cv-data-table-heading :heading="$t('graficos.rojos_bajos')"/>

                <cv-data-table-heading :heading="$t('graficos.amarillos_altos')"/>
                <cv-data-table-heading :heading="$t('graficos.amarillos_medios')"/>
                <cv-data-table-heading :heading="$t('graficos.amarillos_bajos')"/>

                <cv-data-table-heading :heading="$t('graficos.azules_altos')"/>
                <cv-data-table-heading :heading="$t('graficos.azules_medios')"/>
                <cv-data-table-heading :heading="$t('graficos.azules_bajos')"/>

                <cv-data-table-heading :heading="$t('graficos.verdes_altos')"/>
                <cv-data-table-heading :heading="$t('graficos.verdes_medios')"/>
                <cv-data-table-heading :heading="$t('graficos.clouds')"/>

                <cv-data-table-heading :heading="$t('graficos.imagen')"/>
                <cv-data-table-heading :heading="$t('graficos.imagenClouds')"/>
                <cv-data-table-heading :heading="$t('graficos.imagenTrueColor')"/>
            </template>
            <template slot="data">
                <cv-data-table-row  v-for="key in keys" :value="String(key)" v-bind:key="key">
                    <cv-data-table-cell>
                        {{datos[key].nombre}}
                    </cv-data-table-cell>

                    <cv-data-table-cell>
                        {{datos[key].fecha}}
                    </cv-data-table-cell>
                    
                    <cv-data-table-cell>
                        {{datos[key].rojos.altos.porcent + `%`}}
                        <span v-if="datos[key].rojos.altos.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].rojos.altos.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].rojos.altos.porcent > 1.00) ? datos[key].rojos.altos.porcent : 2}%; height: 10px; background: #fe0103;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].rojos.medios.porcent + `%`}}
                        <span v-if="datos[key].rojos.medios.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].rojos.medios.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].rojos.medios.porcent > 1.00) ? datos[key].rojos.medios.porcent : 2}%; height: 10px; background: #9b0004;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].rojos.bajos.porcent + `%`}}
                        <span v-if="datos[key].rojos.bajos.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].rojos.bajos.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].rojos.bajos.porcent > 1.00) ? datos[key].rojos.bajos.porcent : 2}%; height: 10px; background: #680000;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].amarillos.altos.porcent + `%`}}
                        <span v-if="datos[key].amarillos.altos.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].amarillos.altos.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].amarillos.altos.porcent > 1.00) ? datos[key].amarillos.altos.porcent : 2}%; height: 10px; background: #ffff33;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].amarillos.medios.porcent + `%`}}
                        <span v-if="datos[key].amarillos.medios.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].amarillos.medios.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].amarillos.medios.porcent > 1.00) ? datos[key].amarillos.medios.porcent : 2}%; height: 10px; background: #cccc33;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].amarillos.bajos.porcent + `%`}}
                        <span v-if="datos[key].amarillos.bajos.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].amarillos.bajos.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].amarillos.bajos.porcent > 1.00) ? datos[key].amarillos.bajos.porcent : 2}%; height: 10px; background: #666600;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].azules.altos.porcent + `%`}}
                        <span v-if="datos[key].azules.altos.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].azules.altos.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].azules.altos.porcent > 1.00) ? datos[key].azules.altos.porcent : 2}%; height: 10px; background: #33ffff;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].azules.medios.porcent + `%`}}
                        <span v-if="datos[key].azules.medios.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].azules.medios.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].azules.medios.porcent > 1.00) ? datos[key].azules.medios.porcent : 2}%; height: 10px; background: #33cccc;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].azules.bajos.porcent + `%`}}
                        <span v-if="datos[key].azules.bajos.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].azules.bajos.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].azules.bajos.porcent > 1.00) ? datos[key].azules.bajos.porcent : 2}%; height: 10px; background: #006666;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].verdes.altos.porcent + `%`}}
                        <span v-if="datos[key].verdes.altos.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].verdes.altos.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].verdes.altos.porcent > 1.00) ? datos[key].verdes.altos.porcent : 2}%; height: 10px; background: #33ff33;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{(datos[key].verdes.medios.porcent) + `%`}}
                        <span v-if="datos[key].verdes.medios.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].verdes.medios.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span :style="`width: ${(datos[key].verdes.medios.porcent > 1.00) ? datos[key].verdes.medios.porcent : 2}%; height: 10px; background: #33cc33;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    
                    <cv-data-table-cell>
                        {{datos[key].nubes.porcent != 'n/a' ? datos[key].nubes.porcent + `%`: datos[key].nubes.porcent}}
                        <br>
                        <span :style="`width: ${(datos[key].nubes.porcent > 1.00) ? datos[key].nubes.porcent : 2}%; height: 10px; background: #f00;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        <img alt="" id=""  :src="`${urlMedia}/`+datos[key].img" style="width: 80px;">
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        <img v-if="datos[key].nubes.porcent != 'n/a'" alt="" id=""  :src="`${urlMedia}/cloud_`+datos[key].img" style="width: 80px;">
                    </cv-data-table-cell>
                    <cv-data-table-cell >
                        <img alt="" id=""  :src="`${urlMedia}/trueColor_`+datos[key].img" style="width: 80px;">
                    </cv-data-table-cell>
                </cv-data-table-row>
            </template>
        </cv-data-table>
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
            keys: Array(),
            "columns": [
                this.$t('graficos.fecha_nombre'),
                this.$t('graficos.rojos_altos'),
                this.$t('graficos.rojos_medios'),
                this.$t('graficos.rojos_bajos'),
                this.$t('graficos.amarillos_altos'),
                this.$t('graficos.amarillos_medios'),
                this.$t('graficos.amarillos_bajos'),
                this.$t('graficos.azules_altos'),
                this.$t('graficos.azules_medios'),
                this.$t('graficos.azules_bajos'),
                this.$t('graficos.verdes_altos'),
                this.$t('graficos.verdes_medios'),
                'Nubes',
                this.$t('graficos.imagen')
            ],
            verFechaGen: false
        }
    },
    methods: {
        
    },
    
    mounted() {
        this.keys = Object.keys(this.datos)
        console.info(this.keys)

    },
    verFechaGenfun(){
        this.verFechaGen = true
    }
    };
</script>