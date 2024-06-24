<template>
    <div>
        <div class="bx--row" ref="editarEmpresaDatos">
            <div class="bx--col-lg-12 bx--col-md-12 bx--col-sm-12">
                <h4>{{$t('editCoop.edit_coop_enterprises')}}</h4>
            </div>
            <div class="bx--col-lg-12 bx--col-md-12 bx--col-sm-12">
                <cv-structured-list>
                    <template slot="headings">
                        <cv-structured-list-heading>{{$t('adminCoop.nombre')}}</cv-structured-list-heading>
                        <cv-structured-list-heading>{{$t('adminCoop.cif')}}</cv-structured-list-heading>
                    </template>
                    <template slot="items">
                        <cv-structured-list-item
                            v-for="enterprise in cooperative.enterprises"
                            :value="String(enterprise.id)"
                            v-bind:key="enterprise.id"
                        >
                            <cv-structured-list-data>{{enterprise.name}}</cv-structured-list-data>
                            <cv-structured-list-data>{{enterprise.cif}}</cv-structured-list-data>
                        </cv-structured-list-item>
                    </template>
                </cv-structured-list>
            </div>
            <div class="bx--col-lg-12 bx--col-md-12 bx--col-sm-12">
                <cv-button
                    icon=""
                    @click="editarEmpresasCoop" >
                    {{$t("editCoop.add_enterprise_coop")}}
                </cv-button>
            </div>
        </div>
        <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
        <EditCooperativeEnterprise ref="modal" :cooperative_id="$route.query.cooperative" />
    </div>
</template>
<script>
import axios from "axios";
import AlertaGeneral from "@/components/AlertaGeneral";
import EditCooperativeEnterprise from "../components/EditCooperativeEnterprise.vue"
export default {
    name: "EditarCooperativeComponent",
    props: {
        cooperativeId: String
    },
    components: {
        AlertaGeneral,
        EditCooperativeEnterprise
    },
    data() {
        return{
            cooperative: Object,
            empresasArr: Array(),
            mensajeAlerta: ``,
            tipoAlerta: ``,
        }
    },
    methods: {
        getDatosCoop(){
            const path = `${this.$apiURL}/cooperativesonenrlt/${this.$route.query.cooperative}/`
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response => {
                console.info(response.data)
                this.cooperative = response.data
                this.cooperative.enterprises = response.data.enterprises
                //this.getDatosEmpresas()
                //this.cooperative.enterprises = response.data.enterprises
            })
            .catch(error =>{
                console.warn(error)
            })
        },
        getDatosEmpresas(){
            this.empresasArr = Array()
            let path = ``
            this.cooperative.enterprises.forEach(enterprise => {
                path = `${this.$apiURL}/enterprises/${enterprise}/`;
                axios
                .get(path)
                .then(response => {
                    this.empresasArr.push(response.data)
                })
            });
            this.cooperative.enterprises = this.empresasArr
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
        },
        editarEmpresasCoop(){
            this.$refs.modal.openModal()
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