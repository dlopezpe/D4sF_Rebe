<template>
    <div>
        <div class="bx--row" ref="editarEmpresaDatos">
            <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                <cv-text-input
                    :label="$t('newCoop.nombre')"
                    :value="coopName"
                    :disabled="false"
                    :type="`text`"
                    :placeholder="$t('newCoop.nombrePlace')"
                    :invalid-message="invalidMessageNombre"
                    ref="inputNameCoop"
                ></cv-text-input>
            </div>
            <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                <cv-text-input
                    :label="$t('newCoop.direction')"
                    :value="coopDirection"
                    :disabled="false"
                    :type="`text`"
                    :placeholder="$t('newCoop.directionPlace')"
                    :invalid-message="invalidMessageDirection"
                    ref="inputDirectionCoop"
                ></cv-text-input>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                <cv-text-input
                    :label="$t('newCoop.phone')"
                    :value="coopPhone"
                    :disabled="false"
                    :type="`text`"
                    :placeholder="$t('newCoop.phonePlace')"
                    :invalid-message="invalidMessagePhone"
                    ref="inputPhoneCoop"
                ></cv-text-input>
            </div>
            <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                <cv-text-input
                    :label="$t('newCoop.cif')"
                    :value="coopCif"
                    :disabled="false"
                    :type="`text`"
                    :placeholder="$t('newCoop.cifPlace')"
                    :invalid-message="invalidMessageCif"
                    ref="inputCifCoop"
                ></cv-text-input>
            </div>
        </div>
        <br>
        <div class="bx--row">
            <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                <cv-button
                    icon=""
                    @click="guardarDatosCoop" >
                    {{$t("newEnterprise.guardar")}}
                </cv-button>
            </div>
        </div>
        <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
    </div>
</template>
<script>
import axios from "axios";
import AlertaGeneral from "@/components/AlertaGeneral";
export default {
    name: "EditarCooperativeComponent",
    props: {
        cooperativeId: String
    },
    components: {
        AlertaGeneral
    },
    data() {
        return{
            invalidMessageNombre: ``,
            invalidMessageDirection: ``,
            invalidMessagePhone: ``,
            invalidMessageCif: ``,
            mensajeAlerta: ``,
            tipoAlerta: ``,
            //Inputs
            coopName: ``,
            coopDirection: ``,
            coopPhone: ``,
            coopCif: ``
        }
    },
    methods: {
        getDatosCoop(){
            const path = `${this.$apiURL}/cooperatives/${this.$route.query.cooperative}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                this.coopName = response.data.name
                this.coopDirection = response.data.direction
                this.coopPhone = response.data.phone_number
                this.coopCif = response.data.cif
            })
            .catch(error =>{
                console.warn(error)
            })
        },
        guardarDatosCoop(){
            let path = `${this.$apiURL}/cooperatives/${this.$route.query.cooperative}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .put(path, {
                name: this.$refs.inputNameCoop.$refs.input.value,
                direction: this.$refs.inputDirectionCoop.$refs.input.value,
                phone_number: this.$refs.inputPhoneCoop.$refs.input.value,
                cif: this.$refs.inputCifCoop.$refs.input.value,
            })
            .then(() => {
                this.mensajeAlerta = this.$t('editCoop.edit_coop_success')
                this.tipoAlerta = 'success'
                this.$refs.alertaGeneral.verAlerta()
                this.invalidMessageNombre = ``
                this.invalidMessageDirection = ``
                this.invalidMessagePhone = ``
                this.invalidMessageCif = ``
            })
            .catch(error => {
                if(error.response.data.name[0].includes('not be blank')){
                    this.invalidMessageNombre = `${this.$t('newCoop.invalido_blank')}`
                }
            })
        }
    },
    mounted(){
        this.getDatosCoop()
    },
    created(){}
}
</script>
<style scoped>

</style>