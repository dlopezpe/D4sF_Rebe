<template>
    <cv-modal
        :auto-hide-off="false"
        ref="unificarInformeForm"
        @primary-click="unificaInformes"
        @secondary-click="$refs.unificarInformeForm.hide()"
        :close-aria-label="`Close`"
    >
        <template v-if="true" slot="label"></template>
        <template v-if="true" slot="title">{{$t('graficos.unificar_informes')}}</template>
        <template v-if="true" slot="content" id="contenido">
            <div class="bx--grid bx--grid--condensed">
                <div class="bx--row">
                    <div class="bx--col">
                        <!-- Nombre de Informe -->
                        <div class="bx--form-item">
                            <label for="text-input-Nombre" class="bx--label">{{$t('graficos.nombre')}}</label>
                            <input v-model="nombreInformeNew" id="text-input-Nombre" type="text" class="bx--text-input" :placeholder="$t('graficos.nombre')">
                        </div>
                    </div>
                </div>
                <br>
                <div class="bx--row">
                    <div class="bx--col">
                        <!-- Resumen de Informes -->
                        <div class="bx--form-item">
                            <cv-checkbox
                                :label="label_check"
                                :checked="false"
                                value="true"
                                :mixed="false"
                                v-model="checkDellInforme"
                            >
                            </cv-checkbox>
                        </div>
                    </div>
                </div>
                <br>
                <div class="bx--row">
                    <div class="bx--col">
                        <h4>{{$t("graficos.resumen_unifica")}}</h4>
                        <p>{{$t("graficos.capa")}} {{capa}}</p>
                        <p>{{$t("graficos.tipo")}} {{tipo}}</p>
                        <cv-data-table
                        :columns="[
                this.$t('graficos.parcelas'),
                this.$t('graficos.rango_fechas_sel'),
                {
                    'label': this.$t('graficos.creado'),
                },
            ]" >
                            <template slot="data">
                                <cv-data-table-row  v-for="informe in informesSeleccionados" :value="String(informe.id)" :key="String(informe.id)">
                                    <cv-data-table-cell v-if="informe.tipo == 1">
                                        {{parcelaName(informe.parcela)}}
                                    </cv-data-table-cell>
                                    <cv-data-table-cell v-else>
                                        {{informe.parcela}}
                                    </cv-data-table-cell>
                                    <cv-data-table-cell>
                                        {{informe.finifin}}
                                    </cv-data-table-cell>
                                    <cv-data-table-cell>
                                        {{dateFormat(informe.created)}}
                                    </cv-data-table-cell>
                                </cv-data-table-row>
                            </template>
                        </cv-data-table>
                    </div>
                </div>
            </div>
        </template>
        <template v-if="true" slot="secondary-button">{{$t("graficos.cancelar")}}</template>
        <template v-if="true" slot="primary-button">{{$t("graficos.unificar")}}</template>
    </cv-modal>
</template>
<script>
import axios from "axios";
export default {
    name: "UnificarInforme",
    props: {
        informesSell: [],
        informesSeleccionados: Array(),
        historico: Array(),
        tipo: String(),
        capa: String(),
        enterpriseID: String(),
        allParcelsOfEnterprises: Array()
    },
    data() {
        return {
            title_card: this.$t('graficos.unificar_informes'),
            text_input_label: this.$t('graficos.nombre'),
            label_check: this.$t('graficos.eliminar_informe_origin'),
            columnsHistorico: [
                this.$t('graficos.parcelas'),
                this.$t('graficos.rango_fechas_sel'),
                {
                    'label': this.$t('graficos.creado'),
                },
            ],
            nombreInformeNew: '',
            checkDellInforme: false,
            alias: ``
        }
    },
    methods: {
        parcelaName(id){
            const parcelaSelect = this.allParcelsOfEnterprises.filter((parcela)=>{
                return parcela.id == id
            })            
            if(parcelaSelect.length > 0){
                return parcelaSelect[0].properties.name
            }else{
                return 'Gráfico Generado de Parcela Eliminada'
            }
        },
        dateFormat(date){
            const dts = date.split('T')
            return dts[0]
        },
        openModal(){
            if(parseInt(this.tipo) == 1){
                this.parcela = this.informesSeleccionados[0].parcela
            }
            this.$refs.unificarInformeForm.show()
        },
        unificaInformes(){
            if(parseInt(this.tipo) == 2){
                this.parcela = this.nombreInformeNew
            }
            const path = `${this.$apiURL}/unificarInforme/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .post(path, {
                parcela: this.parcela,
                urlSentinel: ['pruebas'], //arr url
                //fechas: fechasSentinel, //Arr parcelas
                polygon: [this.informesSeleccionados],
                enterprise_id: this.enterpriseID,
                capa: this.capa,
                tipo: this.tipo,
                //fechaElegida: this.fechaGenerar
                checkDellOtros: this.checkDellInforme,
                alias: this.nombreInformeNew
            })
            .then(response => {
                console.info(response)
                this.$parent.mensajeAlerta = this.$t('graficos.informe_gen_ok')
                this.$parent.tipoAlerta = 'success'
                this.$emit('mensajeAlerta', this.$t('graficos.informe_gen_ok'))
                this.$emit('tipoAlerta', `success`)
                this.$emit('verAlerta')
                this.$emit('getInformesAnt')
                this.$refs.unificarInformeForm.hide()
            })
            .catch((error) =>{
                console.warn(error)
            })
        }
    }
}
</script>