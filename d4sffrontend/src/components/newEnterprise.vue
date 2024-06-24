<template>
    <cv-modal
        :auto-hide-off='autoHideOff'
        @primary-click="actionPrimary"
        ref="editarUserForm"
    >
        <template v-if="use_label" slot="label"><div id="targetClose" @mouseenter="cerrarModal">{{$t("newEnterprise.nueva")}}</div></template>
        <template v-if="true" slot="title">{{$t("newEnterprise.nueva")}}</template>
        <template v-if="use_content" slot="content" class="formcontent" ref="content_form">
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelNombre"
                        value=""
                        :disabled="disabledNombre"
                        :type="inputTypeNombre"
                        :placeholder="placeholderNombre"
                        :invalid-message="invalidMessageNombre"
                        ref="inputNameEnterprise"
                        id="input-MIRLwtCq"
                    ></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelCif"
                        value=""
                        :disabled="disabledCif"
                        :type="inputTypeCif"
                        :placeholder="placeholderCif"
                        :invalid-message="invalidMessageCif"
                        ref="inputCif"
                        id="input-MIRLwtCq"
                    ></cv-text-input>
                </div>
                
                
            </div>
            <br>
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelDir"
                        value=""
                        :disabled="disabledDir"
                        :type="inputTypeDir"
                        :placeholder="placeholderDir"
                        :invalid-message="invalidMessageDir"
                        ref="inputDir"
                        id="input-MIRLwtCq"
                    ></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelHec"
                        value=""
                        :disabled="disabledHec"
                        :type="inputTypeHec"
                        :placeholder="placeholderHec"
                        :invalid-message="invalidMessageHec"
                        ref="inputHec"
                        id="input-MIRLwtCq"
                    ></cv-text-input>
                </div>
            </div>
            <br>
            <div class="bx--row">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="$t('newEnterprise.tel_enterprise')"
                        placeholder="910000000"
                        :value="telEmpresa"
                        ref="telEmpresa"
                        :invalid-message="invalidMessageTelEmpresa"
                        ></cv-text-input>
                </div>
                  <div class="bx--col-lg-6 bx--col-md-6 bx--col-sm-4">
                     
                    <cv-select v-model="metricSelect" @change="changemetri()"
                    :label="inputTypeHec"
                    :disabled="disabled"
                    :invalid-message="invalidMessage">
                        <cv-select-option disabled selected hidden>Choose an option</cv-select-option>
                        <cv-select-option
                            v-for="(metri, i) in metrics"
                            :key="`metri-${i}`"
                            :value="metri"
                        >
                            {{ metri }}
                        </cv-select-option>
                    </cv-select>
                    </div>
            </div>
            <br>
            <div class="bx--row" v-if="verUserRegis">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <h4>{{$t("newEnterprise.usuarioAdministrador")}}</h4>
                </div>
            </div>
            <br>
            <div class="bx--row"  v-if="verUserRegis">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="label"
                        :value="value"
                        :disabled="disabled"
                        :type="inputType"
                        :placeholder="placeholder"
                        :invalid-message="invalidMessage"
                        ref="inputName"
                        id="input-MIRLwtCq"
                    ></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelLast"
                        :value="valueLast"
                        :disabled="disabled"
                        :type="inputType"
                        :placeholder="placeholderLast"
                        :invalid-message="invalidMessageLast"
                        ref="inputNameLast"
                        id="input-MIRLwtCq"
                    ></cv-text-input>
                </div>
            </div>
            <br>
            <div class="bx--row"  v-if="verUserRegis">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelMail"
                        :value="valueMail"
                        :disabled="disabledMail"
                        :type="inputTypeMail"
                        :placeholder="placeholderMail"
                        :invalid-message="invalidMessageMail"
                        ref="inputMail"
                        id="input-3zcRveTf"
                    ></cv-text-input>
                </div>
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelPhone"
                        :invalid-message="invalidMessagePhone"
                        :disabled="disabledPhone"
                        placeholder="910000000"
                        :value="valuePhone"
                        ref="inputNumberPhone"
                    ></cv-text-input>
                </div>
                 <div class="bx--col-lg-6 bx--col-md-6 bx--col-sm-4">
                
                     <cv-select v-model="metricSelect" 
                    :label="inputTypeHec"
                    :hide-label="false"
                    :inline="false"
                    :value="metricSelect"
                    :disabled="false"
                    :helper-text="helperText"
                    :invalid-message="invalidMessage">

                        <cv-select-option
                            v-for="(metri, i) in metrics"
                            :key="`metri-${i}`"
                            :value="metri"
                        >
                            {{ metri }}
                        </cv-select-option>
                    </cv-select>
                </div>
            </div>
            <br>
            <div class="bx--row"  v-if="verUserRegis">
                <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                    <cv-text-input
                        :label="labelPassword"
                        :value="valuePassword"
                        :disabled="disabledPassword"
                        :type="inputTypePassword"
                        :placeholder="placeholderPassword"
                        :invalid-message="invalidMessagePassword"
                        ref="inputPassword"
                        v-if="showPassword"
                    ></cv-text-input>
                </div>
            </div>
        </template>
        <template v-if="use_primaryButton" slot="primary-button">{{$t("newEnterprise.guardar")}}</template>
    </cv-modal>
</template>
<script>
import axios from "axios";

export default {
    name: "NewEnterprise",
    props: {
    },
    components: {
    
    },
    data() {
        return {
            autoHideOff: true,
            //metrics
            metrics: ['Ha', 'Acre'],
            metricSelect: 'Ha',
            verUserRegis: false,
            //Card
            use_label: true,
            use_content: true,
            use_primaryButton: true,
            //NOmbre de empresa input
            labelNombre: this.$t('newEnterprise.nombre_enterprise'),
            inputTypeNombre: 'text',
            placeholderNombre: 'Example Inc.',
            invalidMessageNombre: '',
            disabledNombre: false,
            //Cif de la empresa
            labelCif: this.$t('newEnterprise.cif_enterprise'),
            inputTypeCif: 'text',
            placeholderCif: 'B810...',
            invalidMessageCif: '',
            disabledCif: false,
            //Direccion de la empresa
            labelDir: this.$t('newEnterprise.direccion_enterprise'),
            inputTypeDir: 'text',
            placeholderDir: 'Example Ave., Spain',
            invalidMessageDir: '',
            disabledDir: false,
            //Hectareas Disponibles
            labelHec: this.$t('newEnterprise.hectareas_disponible'),
            inputTypeHec: this.$t('newEnterprise.tipo_Metrica'),
            placeholderHec: '100',
            invalidMessageHec: '',
            invalidMessageMetric: '',
            disabledHec: false,
            //input-name
            label: "Nombre de Usuario",
            disabled: false,
            inputType: "text",
            placeholder: "Nombre de Usuario",
            invalidMessage: "",
            value: "",
            //input-name
            labelLast: "Apellido/s de Usuario",
            placeholderLast: "Apellido/s de Usuario",
            invalidMessageLast: "",
            valueLast: "",
            //input-email
            labelMail: "Correo electrónico",
            disabledMail: false,
            inputTypeMail: "email",
            placeholderMail: "example@example.com",
            invalidMessageMail: "",
            valueMail: "",
            
            //numero de telefono
            labelPhone: "Número de Teléfono",
            invalidMessagePhone: "",
            disabledPhone: false,
            valuePhone: "",
            //input password
            labelPassword: 'Contraseña',
            disabledPassword: false,
            inputTypePassword: 'password',
            placeholderPassword: 'Contraseña',
            invalidMessagePassword: '',
            valuePassword: '',
            showPassword: true,
            layers: [],
            //
            invalidMessageTelEmpresa: '',
        };
    },
    methods: {
        cerrarModal(){
            const titulo = document.getElementById('targetClose');
            const header_entero = titulo.parentElement.parentElement;
            header_entero.addEventListener('mouseenter', () => {
                this.autoHideOff = false;
            });
            header_entero.addEventListener('mouseleave', () => {
                this.autoHideOff = true;
            });

        },
        openModal() {
            this.$refs.editarUserForm.show();
            this.layers = [
                {
                    "id": "AGRICULTURE",
                    "title": "Agriculture",
                    "description": "Based on bands 11, 8A and 2",
                    "styles": [
                        {
                            "name": "default",
                            "dataProduct": {
                                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/991"
                            }
                        }
                    ],
                    "orderHint": 0,
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                    },
                    "datasetSource": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
                    },
                    "defaultStyleName": "default",
                    "datasourceDefaults": {
                        "upsampling": "BICUBIC",
                        "mosaickingOrder": "mostRecent",
                        "temporal": false,
                        "maxCloudCoverage": 20.0,
                        "previewMode": "PREVIEW",
                        "type": "S2L1C"
                    }
                },
                {
                    "id": "FALSE_COLOR",
                    "title": "False color (vegetation)",
                    "description": "",
                    "styles": [
                        {
                            "name": "default",
                            "description": "Default layer style",
                            "dataProduct": {
                                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/6"
                            }
                        }
                    ],
                    "orderHint": 0,
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                    },
                    "datasetSource": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
                    },
                    "defaultStyleName": "default",
                    "datasourceDefaults": {
                        "upsampling": "BICUBIC",
                        "mosaickingOrder": "mostRecent",
                        "temporal": false,
                        "maxCloudCoverage": 20.0,
                        "previewMode": "PREVIEW",
                        "type": "S2L1C"
                    }
                },
                {
                    "id": "NDVI",
                    "title": "NDVI (Normalized Difference Vegetation Index)",
                    "description": "Value = colorMap((B08 - B04) / (B08 + B04))",
                    "styles": [
                        {
                            "name": "default",
                            "description": "Default layer style",
                            "dataProduct": {
                                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/923"
                            }
                        }
                    ],
                    "orderHint": 34,
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                    },
                    "datasetSource": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
                    },
                    "defaultStyleName": "default",
                    "datasourceDefaults": {
                        "upsampling": "BICUBIC",
                        "mosaickingOrder": "mostRecent",
                        "temporal": false,
                        "maxCloudCoverage": 20.0,
                        "previewMode": "PREVIEW",
                        "type": "S2L1C"
                    }
                },
                {
                    "id": "MOISTURE_INDEX",
                    "title": "Moisture Index",
                    "description": "Based on combination of bands (B8A - B11)/(B8A + B11)",
                    "styles": [
                        {
                            "name": "default",
                            "dataProduct": {
                                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/1242"
                            }
                        }
                    ],
                    "orderHint": 6,
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                    },
                    "datasetSource": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
                    },
                    "defaultStyleName": "default",
                    "datasourceDefaults": {
                        "upsampling": "BICUBIC",
                        "mosaickingOrder": "mostRecent",
                        "temporal": false,
                        "maxCloudCoverage": 20.0,
                        "previewMode": "PREVIEW",
                        "type": "S2L1C"
                    }
                },
                {
                    "id": "TRUE_COLOR",
                    "title": "Natural color (true color)",
                    "description": "Based on bands 4,3,2",
                    "styles": [
                        {
                            "name": "default",
                            "dataProduct": {
                                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/84"
                            }
                        }
                    ],
                    "orderHint": 8,
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                    },
                    "datasetSource": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
                    },
                    "defaultStyleName": "default",
                    "datasourceDefaults": {
                        "upsampling": "BICUBIC",
                        "mosaickingOrder": "mostRecent",
                        "temporal": false,
                        "maxCloudCoverage": 20.0,
                        "previewMode": "PREVIEW",
                        "type": "S2L1C"
                    }
                },
                {
                    "id": "ESAS-SCENE",
                    "title": "Interpretación Multifactor",
                    "description": "",
                    "styles": [
                        {
                            "name": "default",
                            "description": "Default layer style",
                            "dataProduct": {
                                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L2A/dataproducts/1259"
                            }
                        }
                    ],
                    "orderHint": 0,
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L2A"
                    },
                    "datasetSource": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L2A/sources/2"
                    },
                    "defaultStyleName": "default",
                    "datasourceDefaults": {
                        "mosaickingOrder": "mostRecent",
                        "temporal": false,
                        "maxCloudCoverage": 50.0,
                        "type": "S2L2A"
                    }
                },
                {
                    "id": "NDWI",
                    "title": "NDWI",
                    "description": "",
                    "styles": [
                        {
                            "name": "default",
                            "description": "Default layer style",
                            "dataProduct": {
                                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/811",
                                "id": 811,
                                "name": "NDWI.INDEX",
                                "description": "NDWI (Normalized Difference Water Index) - INDEX",
                                "evalScript": "//VERSION=3\n\nfunction evaluatePixel(samples) {\n    let val = index(samples.B03, samples.B08);\n    return [val, samples.dataMask];\n}\n\nfunction setup() {\n  return {\n    input: [{\n      bands: [\n        \"B03\",\n        \"B08\",\n        \"dataMask\"\n      ]\n    }],\n    output: {\n      bands: 2\n    }\n  }\n}\n\n",
                                "dataset": {
                                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                                },
                                "baseProduct": "NDWI",
                                "visualization": "INDEX",
                                "scriptVersion": 3,
                                "listed": true,
                                "additionalData": {
                                    "preV3EquivalentId": 144
                                }
                            }
                        }
                    ],
                    "orderHint": 0,
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                    },
                    "datasetSource": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1",
                        "id": 1,
                        "description": "Sentinel S2 - L1C",
                        "settings": {
                            "indexServiceUrl": "https://services.sentinel-hub.com/index"
                        },
                        "dataset": {
                            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                        }
                    },
                    "defaultStyleName": "default",
                    "datasourceDefaults": {
                        "mosaickingOrder": "mostRecent",
                        "temporal": false,
                        "maxCloudCoverage": 50,
                        "type": "S2L1C"
                    },
                }
            ]
        },
        actionPrimary(){
            let flag = false
            if(!this.$refs.inputNameEnterprise.$refs.input.value){this.invalidMessageNombre = `${this.$t('newEnterprise.campo_requerido')}`; flag=true}
            if(!this.$refs.inputCif.$refs.input.value){this.invalidMessageCif = `${this.$t('newEnterprise.campo_requerido')}`; flag=true}
            if(!this.$refs.inputDir.$refs.input.value){this.invalidMessageDir = `${this.$t('newEnterprise.campo_requerido')}`; flag=true}
            if(!this.$refs.telEmpresa.$refs.input.value){this.invalidMessageTelEmpresa = `${this.$t('newEnterprise.campo_requerido')}`; flag=true}                    
            if(!flag){
                let path = `${this.$apiURL}/enterprises/`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .post(path, {
                    name: this.$refs.inputNameEnterprise.$refs.input.value,
                    direction: this.$refs.inputDir.$refs.input.value,
                    cif: this.$refs.inputCif.$refs.input.value,
                    hectares_available: this.$refs.inputHec.$refs.input.value,
                    phone_number: this.$refs.telEmpresa.$refs.input.value,
                    type_metric: this.metricSelect
                })
                .then(response =>{
                    const idEnterprise = response.data.id
                    const instanceIns = axios.create({
                        baseURL: this.$sentinelURL
                    })
                    const configIns = {
                        headers: {
                            'Content-Type': 'application/json;charset=utf-8',
                            'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
                        }
                    }
                    const bodyIns = JSON.stringify({
                        'name': idEnterprise,
                        'description': idEnterprise,
                        "additionalData": {
                            "showWarnings": false,
                            "showLogo": false,
                            "forceFormat": "string",
                            "imageQuality": 0,
                            "disabled": false
                        },
                    })
                    //https://services.sentinel-hub.com/configuration/v1/wms/instances
                    instanceIns.post("/configuration/v1/wms/instances", bodyIns, configIns).then(resp => {
                        if(resp.status == 201){
                            console.warn(resp.data.id)
                            const layerid = resp.data.id
                            this.layers.forEach(layer =>{
                                instanceIns.post("/configuration/v1/wms/instances/"+layerid+"/layers", layer, configIns).then(() => {
                                    
                                })
                            })
                            path = `${this.$apiURL}/enterprises/${idEnterprise}/`;
                            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                            axios
                            .put(path, {
                                name: this.$refs.inputNameEnterprise.$refs.input.value,
                                direction: this.$refs.inputDir.$refs.input.value,
                                cif: this.$refs.inputCif.$refs.input.value,
                                hectares_avariable: this.$refs.inputHec.$refs.input.value,
                                phone_number: this.$refs.telEmpresa.$refs.input.value,
                                sentinel_instance: layerid,
                            })
                            .then(() =>{
                                this.$parent.obtenerListaEmpresas();
                                this.$refs.editarUserForm.hide();
                                this.$parent.mensajeAlerta = `${this.$t('newEnterprise.save_enterprise')}`
                                this.$parent.tipoAlerta = 'success'
                                this.$parent.$refs.alertaGeneral.verAlerta()
                            })
                        }
                    })
                })
                .catch(error => {
                    const errors = error.response.data
                    if(errors.name)
                        this.invalidMessageNombre =  `${this.$t('newEnterprise.campo_requerido')}`
                    if(errors.cif)
                        this.invalidMessageCif =  `${this.$t('newEnterprise.campo_requerido')}`
                    if(errors.direction)
                        this.invalidMessageDir =  `${this.$t('newEnterprise.campo_requerido')}`
                    if(errors.phone_number)
                        this.invalidMessageTelEmpresa =  `${this.$t('newEnterprise.campo_requerido')}`
                })
            }
        },

        getDatosUser(){
            if(sessionStorage.getItem("apiAccess")){
                const path = `${this.$apiURL}/profile/`;
                axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .get(path)
                .then(response => {
                    this.$session.start()
                    //---------------------------------------------------------------
                    this.$session.set('is_coop_user', response.data[0].cooperative_user)
                    this.$session.set('enterprise', response.data[0].enterprise_id)
                    this.$session.set('user', response.data[0].user)
                    sessionStorage.setItem('enterprise', response.data[0].enterprise_id)
                    sessionStorage.setItem('user', response.data[0].user)

                    let pathEnterpriseInstance = `${this.$apiURL}/enterprises/${response.data[0].enterprise_id}/`;
                    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                    axios.get(pathEnterpriseInstance)
                    .then(response =>{
                        sessionStorage.setItem('sI', response.data.sentinel_instance)
                    })
                    //---------------------------------------------------------------//
                    this.getPermisosUser(response.data[0].user)
                }).catch(error =>{
                    console.warn(error)
                })
            }
        },
        getPermisosUser(id){
            const pathRol = `${this.$apiURL}/permisos/${id}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(pathRol)
            .then(response => {
                //---------------------------------------------------------------
                this.$session.set('is_enterpriseadmin', response.data.is_enterpriseadmin)
                this.$session.set('is_staff', response.data.is_staff)
                this.$session.set('is_superuser', response.data.is_superuser)
                this.$session.set('is_systemadmin', response.data.is_systemadmin)
                sessionStorage.setItem('is_enterpriseadmin', response.data.is_enterpriseadmin)
                sessionStorage.setItem('is_staff', response.data.is_staff)
                sessionStorage.setItem('is_superuser', response.data.is_superuser)
                sessionStorage.setItem('is_systemadmin', response.data.is_systemadmin)
                this.$parent.$parent.is_superuser = response.data.is_superuser
                this.$parent.$parent.is_staff = response.data.is_staff,
                this.$parent.$parent.is_systemadmin = response.data.is_systemadmin,
                this.$parent.$parent.is_enterpriseadmin = response.data.is_enterpriseadmin
                this.$parent.$parent.customLinkEnterprise = 'edit-enterprise?enterprise='+this.$session.get('enterprise')
                this.$parent.$parent.is_coop_user = this.$session.get('is_coop_user')
                this.$parent.$parent.customLinkCoop = 'edit-cooperative?cooperative='+this.$session.get('enterprise')
                //---------------------------------------------------------------
            })
        },
    },
    created(){
        this.getDatosUser()
    }
}
</script>
<style scoped>

</style>