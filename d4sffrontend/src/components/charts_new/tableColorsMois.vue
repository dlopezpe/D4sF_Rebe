<template>
    <div>
        <h4>{{$t("graficos.tabla_colores")}} <img src="../../assets/crop-health.svg" style="width: 20px;"></h4>
        <br>
        <cv-data-table
        ref="table"
        @sort="onSort">
            <template slot="headings">
                <cv-data-table-heading :heading="$t('graficos.fecha_nombre')"/>

                <cv-data-table-heading :heading="$t('graficos.fecha_gen')"/>

                <cv-data-table-heading :heading="$t('graficos.rojo_naran')"/>
                <cv-data-table-heading :heading="$t('graficos.amarillo')"/>
                <cv-data-table-heading :heading="$t('graficos.verde')"/>

                <cv-data-table-heading :heading="$t('graficos.azul_claro')"/>
                <cv-data-table-heading :heading="$t('graficos.azul_medio')"/>
                <cv-data-table-heading :heading="$t('graficos.azul_oscuro')"/>
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
                        {{datos[key].naranja.porcent + `%`}}
                        <span v-if="datos[key].naranja.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].naranja.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="datos[key].naranja.porcent > 1.00" :style="`width: ${datos[key].naranja.porcent}%; height: 10px; background: #ff8000;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #ff8000;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].amarillo.porcent + `%`}}
                        <span v-if="datos[key].amarillo.area_porcen">
                            {{"-"}}
                            {{Math.round((datos[key].amarillo.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="datos[key].amarillo.porcent > 1.00" :style="`width: ${datos[key].amarillo.porcent}%; height: 10px; background: #ffdf00;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #ffdf00;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].verdes.porcent + `%`}}
                        <span v-if="datos[key].verdes.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].verdes.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="datos[key].verdes.porcent > 1.00" :style="`width: ${datos[key].verdes.porcent}%; height: 10px; background: #66ff98;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #66ff98;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].azul_claro.porcent + `%`}}
                        <span v-if="datos[key].azul_claro.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].azul_claro.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="datos[key].azul_claro.porcent > 1.00" :style="`width: ${datos[key].azul_claro.porcent}%; height: 10px; background: #02fefc;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #02fefc;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].azul_medio.porcent + `%`}}
                        <span v-if="datos[key].azul_medio.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].azul_medio.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="datos[key].azul_medio.porcent > 1.00" :style="`width: ${datos[key].azul_medio.porcent}%; height: 10px; background: #0087ff;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #0087ff;display: inline-block;`"></span>
                    </cv-data-table-cell>
                    <cv-data-table-cell>
                        {{datos[key].azul_oscuro.porcent + `%`}}
                        <span v-if="datos[key].azul_oscuro.area_porcent">
                            {{"-"}}
                            {{Math.round((datos[key].azul_oscuro.area_porcent + Number.EPSILON) * 100) / 100 + 'Ha'}}
                        </span>
                        <br>
                        <span v-if="datos[key].azul_oscuro.porcent > 1.00" :style="`width: ${datos[key].azul_oscuro.porcent}%; height: 10px; background: #2000ff;display: inline-block;`"></span>
                        <span v-else :style="`width: 2%; height: 10px; background: #2000ff;display: inline-block;`"></span>
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
                this.$t('graficos.rojo_naran'),
                this.$t('graficos.amarillo'),
                this.$t('graficos.verde'),
                this.$t('graficos.azul_claro'),
                this.$t('graficos.azul_medio'),
                this.$t('graficos.azul_oscuro'),
                'Nubes',
                this.$t('graficos.imagen')
            ],
            verFechaGen: false
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
    },
    
    mounted() {
        this.keys = Object.keys(this.datos)
    },
    
    };
</script>