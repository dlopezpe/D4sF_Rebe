<template>
    <div>
        <cv-form>
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input :label="$t('newEnterprise.nombre_enterprise')" placeholder="Example Inc."
                        :value="nombreEmpresa" class="" ref="nombreEmpresa"
                        :invalid-message="invalidMessageNombre"></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input :label="$t('newEnterprise.cif_enterprise')" placeholder="B810..." :value="cifEmpresa"
                        ref="cifEmpresa" :invalid-message="invalidMessageCif"></cv-text-input>
                </div>
            </div>
            <br>
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input :label="$t('newEnterprise.direccion_enterprise')" placeholder="Example Ave., Spain"
                        :value="direccionEmpresa" ref="direccionEmpresa"
                        :invalid-message="invalidMessageDir"></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input :label="$t('newEnterprise.tel_enterprise')" placeholder="910000000" :value="telEmpresa"
                        ref="telEmpresa" :invalid-message="invalidMessageTelEmpresa"></cv-text-input>
                </div>
            </div>
            <br>
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input :label="$t('newEnterprise.hectareas_disponible')" placeholder="2.374"
                        :value="hectareas_disponibles" ref="hectareasDisponibles" :invalid-message="invalidMessageHec"
                        :disabled="disabledHec()"></cv-text-input>
                </div>
                <div class="bx--col-lg-2 bx--col-md-4 bx--col-sm-4">

                    <cv-select v-model="metricSelect" :label="inputTypeHec" :hide-label="false" :inline="false"
                        :value="metricSelect" :disabled="false" :invalid-message="invalidMessageMetric">

                        <cv-select-option v-for="(metri, i) in metrics" :key="`metri-${i}`" :value="metri">
                            {{ metri }}
                        </cv-select-option>
                    </cv-select>
                </div>
                <!-- D4SF-88 -->
                <div class="bx--col-lg-2 bx--col-md-4 bx--col-sm-4">
                    <cv-select v-model="continentSelect" label='Continente' :hide-label="false" :inline="false"
                        :value="continentSelect" :disabled="false" helper-text="">

                        <cv-select-option v-for="(continent, i) in continents" :key="`conti-${i}`" :value="continent">
                            {{ continent }}
                        </cv-select-option>
                    </cv-select>
                </div>

                <div class="bx--col-lg-2 bx--col-md-2 bx--col-sm-4">
                    <cv-select v-model="isMonitorSelect" id="isMonitorSelect" label='Añadir a monitorización'
                        :hide-label="false" :inline="false" :value="isMonitorSelect" :disabled="false">
                        <cv-select-option v-for="option in monitorOptions.options" :key="option.value"
                            :value="option.value">
                            {{ option.text }}
                        </cv-select-option>
                    </cv-select>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2" style="margin-top: 17px">
                    <cv-select v-model="estadoSeleccionado" :size="md" :inline="inline" label='Selecciona un estado'>
                        <cv-select-option disabled selected hidden value="placeholder-item">{{ estadoActual ? 'Activa' :
                            'Inactiva' }}</cv-select-option>
                        <cv-select-option value="1">{{ $t("adminEnterprise.activo") }}</cv-select-option>
                        <cv-select-option value="0">{{ $t("adminEnterprise.inactivo") }}</cv-select-option>
                    </cv-select>
                    <p>
                        {{ $t("adminEnterprise.txt_seguro_enterprise_status") }}
                    </p>
                </div>
            </div>
            <br>
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-button icon="" @click="guardarDatosEmpresa">
                        {{ $t("newEnterprise.guardar") }}
                    </cv-button>
                </div>
            </div>

        </cv-form>
        <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
    </div>
</template>
<script>
import axios from "axios";
import AlertaGeneral from "../components/AlertaGeneral";

export default {
    name: "EditarEmpresaComponent",
    props: {
        idEmpresa: String
    },
    components: { AlertaGeneral },
    data() {
        return {
            metrics: ['Ha', 'Acre'],
            //D4SF-88
            continents: ['América', 'Europa'],
            continentSelect: null,
            idEnterprise: null,
            isMonitorSelect: null,
            monitorOptions: {
                options: [
                    { value: true, text: 'Si' },
                    { value: false, text: 'No' }
                ]
            },
            estadoActual: null,
            metricSelect: null,
            nombreEmpresa: '',
            cifEmpresa: '',
            direccionEmpresa: '',
            telEmpresa: '',
            hectareas_disponibles: '',
            type_metric: '',
            //
            invalidMessageNombre: '',
            invalidMessageCif: '',
            invalidMessageDir: '',
            invalidMessageTelEmpresa: '',
            mensajeAlerta: '',
            tipoAlerta: '',
            invalidMessageHec: '',
            invalidMessageMetric: '',
            idEmpresaEd: '',
            idUsuario: '',
            flag: false,
            inputTypeHec: this.$t('newEnterprise.tipo_Metrica'),

        }
    },
    methods: {
        disabledHec() {
            if (sessionStorage.getItem('is_superuser') == 'true' || sessionStorage.getItem('is_systemadmin') == 'true') {
                return false
            } else {
                return true
            }
        },
        getEnterpriseStatus() {

            const url = `${this.$apiURL}/enterprises/${this.$route.query.enterprise}/`;
            console.log("URL:", url);
            axios.get(url)
                .then(response => {
                    this.estadoActual = response.data.is_active;
                    console.log("Estado activo:", this.estadoActual);
                })
                .catch(error => {
                    console.error("Error al obtener el estado de la empresa:", error);
                    this.visibleAlertaConfirmacion = false;
                });
        },
        showAlert() {
            this.mensajeAlerta = `${this.$t('newEnterprise.save_enterprise')}`
            this.tipoAlerta = 'success'
            this.$refs.alertaGeneral.verAlerta()
        },
        getDatosEmpresa(idEmpresa) {

            this.idEmpresaEd = idEmpresa

            if (idEmpresa) {
                this.idEmpresaEd = idEmpresa;
                localStorage.setItem("enterprise", idEmpresa);
                sessionStorage.setItem("enterprise", localStorage.getItem("enterprise"));
            } else {
                this.idEmpresaEd = this.idEmpresaEd || localStorage.getItem("enterprise") || sessionStorage.getItem("enterprise");
            }
            const path = `${this.$apiURL}/enterprises/${this.idEmpresaEd}/`;

            /* Checkar que el path siempre tiene un valor no nulo / definido */

            console.log("Path getDatosEmpresa:", path);

            axios.defaults.headers.common['Authorization'] = "Bearer " + sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                    this.nombreEmpresa = response.data.name
                    this.cifEmpresa = response.data.cif
                    this.direccionEmpresa = response.data.direction
                    this.telEmpresa = response.data.phone_number
                    this.hectareas_disponibles = response.data.hectares_available
                    this.metricSelect = response.data.type_metric
                    this.estadoActual = response.data.is_active
                    //D4SF-88
                    this.continentSelect = response.data.continent
                    this.isMonitorSelect = response.data.is_monitor
                    // todo: solventar el problema de que no se guarda el valor de isMonitorSelect
                    if (this.isMonitorSelect == false) {
                        this.isMonitorSelect = 'No';
                    }
                })

        },
        async guardarDatosEmpresa() {
            this.flag = false;
            this.idUsuario = sessionStorage.getItem("user");
            this.idEnterprise = localStorage.getItem("enterprise");

            const path = `${this.$apiURL}/enterprises/${this.idEnterprise}/`;

            if (this.isMonitorSelect === 'No') {
                this.isMonitorSelect = false;
            }

            axios.defaults.headers.common['Authorization'] = "Bearer " + sessionStorage.getItem("apiAccess")

            axios.put(path, {
                name: this.$refs.nombreEmpresa.$refs.input.value,
                direction: this.$refs.direccionEmpresa.$refs.input.value,
                cif: this.$refs.cifEmpresa.$refs.input.value,
                phone_number: this.$refs.telEmpresa.$refs.input.value,
                hectares_available: this.$refs.hectareasDisponibles.$refs.input.value,
                type_metric: this.metricSelect,
                //D4SF-88
                continent: this.continentSelect,
                is_monitor: this.isMonitorSelect,
                is_active: this.estadoSeleccionado,
            }).then(() => {
                this.showAlert();
            }).catch(error => {
                this.flag = true;
                const errors = error.response.data
                if (errors.name)
                    this.invalidMessageNombre = `${this.$t('newEnterprise.campo_requerido')}`
                if (errors.cif)
                    this.invalidMessageCif = `${this.$t('newEnterprise.campo_requerido')}`
                if (errors.direction)
                    this.invalidMessageDir = `${this.$t('newEnterprise.campo_requerido')}`
                if (errors.phone_number)
                    this.invalidMessageTelEmpresa = `${this.$t('newEnterprise.campo_requerido')}`
                if (errors.hectares_available)
                    this.invalidMessageHec = `${this.$t('newEnterprise.campo_requerido')}`
            });
            if (!this.flag) {
                if (typeof this.estadoSeleccionado != 'undefined'){
                    this.insertTraza();
                }
                this.showAlert();
            }
        },
        insertTraza() {
            const path_trazas = `${this.$apiURL}/insert_trazas/`;
            axios.post(path_trazas, {
                id_user: this.idUsuario,
                enterprise_code: this.idEmpresaEd,
                old_status: this.estadoActual,
                status: this.estadoSeleccionado,
                crud: "Nuevo estado: " + this.estadoSeleccionado + " de la empresa: " + this.idEmpresaEd + " por el usuario: " + this.idUsuario
            })
        },
    },
};
</script> 
<style scoped></style>