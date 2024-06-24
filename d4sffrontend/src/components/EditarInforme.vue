<template>
    <cv-modal
        :auto-hide-off="false"
        ref="EditarInformeForm"
        @primary-click="unificaInformes"
        @secondary-click="$refs.unificarInformeForm.hide()"
        :close-aria-label="`Close`"
    >
        <template v-if="true" slot="label"></template>
        <template v-if="true" slot="title">{{$t('graficos.modifica_infor')}}</template>
        <template v-if="true" slot="content" id="contenido">
            <div class="bx--grid bx--grid--condensed">
                <div class="bx--row">
                    <div class="bx--col">
                        <!-- Nombre de Informe -->
                        <div class="bx--form-item">
                            <label for="text-input-Nombre" class="bx--label">{{$t('graficos.nombre_informe')}}</label>
                            <input v-model="nombreInformeNew" id="text-input-Nombre" type="text" class="bx--text-input" :placeholder="text_input_label">
                        </div>
                    </div>
                </div>
            </div>
            {{allParcelsOfEnterprises}}
        </template>
        <template v-if="true" slot="secondary-button">{{$t('graficos.cancelar')}}</template>
        <template v-if="true" slot="primary-button">{{$t('graficos.guardar')}}</template>
    </cv-modal>
</template>
<script>
import axios from "axios";
export default {
    name: "UnificarInforme",
    props: {
        informesSeleccionados: Array(),
        historico: Array(),
        allParcelsOfEnterprises: Array()
    },
    data() {
        return {
            title_card: `Modificar Informe`,
            text_input_label: `Nombre del Informe`,
            nombreInformeNew: '',
            alias: ``,
            parcela: Object(),
            mensajeAlerta: ``,
            tipoAlerta: `error`
        }
    },
    methods: {
        openModal(){
            let path = `${this.$apiURL}/ver_hist/${this.informesSeleccionados[0]}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                if(!response.data.alias){
                    this.parcela = this.historico.filter(informe => {
                        if(informe.id == this.informesSeleccionados[0]){
                            this.nombreInformeNew = (informe.tipo == 1) ? this.parcelaName(informe.parcela) : informe.parcela
                        }
                    })
                }else{
                    this.nombreInformeNew = response.data.alias
                }
            })
            .catch(error =>{
                console.warn(error)
            })
            this.$refs.EditarInformeForm.show()
        },
        parcelaName(id){
            const parcelaSelect = this.allParcelsOfEnterprises.filter((parcela)=>{
                return parcela.id == id
            })            
            if(parcelaSelect.length > 0){
                return parcelaSelect[0].properties.name
            }else{
                this.parcela = {tipo: 1}
                return 'Gráfico Generado de Parcela Eliminada'
            }
        },
        unificaInformes(){
            const path = `${this.$apiURL}/ver_hist/${this.informesSeleccionados[0]}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            if(this.parcela.tipo == 1){
                axios
                .put(path, {
                    alias: this.nombreInformeNew
                })
                .then(response => {
                    console.info(response)
                    this.$parent.mensajeAlerta = `Informe Guardado correctamente`
                    this.$parent.tipoAlerta = 'success'
                    this.$emit('mensajeAlerta', `Informe Guardado correctamente`)
                    this.$emit('tipoAlerta', `success`)
                    this.$emit('verAlerta')
                    this.$emit('getInformesAnt')
                    this.$refs.EditarInformeForm.hide()
                })
                .catch((error) =>{
                    console.warn(error)
                })
            }else{
                axios
                .put(path, {
                    parcela: this.nombreInformeNew
                })
                .then(response => {
                    console.info(response)
                    this.$parent.mensajeAlerta = `Informe Guardado correctamente`
                    this.$parent.tipoAlerta = 'success'
                    this.$emit('mensajeAlerta', `Informe Guardado correctamente`)
                    this.$emit('tipoAlerta', `success`)
                    this.$emit('verAlerta')
                    this.$emit('getInformesAnt')
                    this.$refs.EditarInformeForm.hide()
                })
                .catch((error) =>{
                    console.warn(error)
                })
            }
        }
    },
    mounted: function () {
        console.info('Pruebas')
    },
}
</script>