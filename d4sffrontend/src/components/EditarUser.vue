<template>
    <cv-modal
        :close-aria-label="closeAriaLabel"
        :size="size"
        :primary-button-disabled="primaryButtonDisabled"
        :auto-hide-off='autoHideOff'
        @primary-click="actionPrimary"
        ref="editarUserForm"
    >
        <template v-if="use_label" slot="label"><div id="targetClose" @mouseenter="cerrarModalNuevoEmpleado">{{title_card}}</div></template>
        <template v-if="use_title" slot="title">{{subtitle_card}} {{userSeleccionado}}</template>
        <template v-if="use_content" slot="content" class="formcontent" ref="content_form">
                <div class="bx--row">
                    <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                        <cv-text-input
                            :label="$t('empleados.user_name')"
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
                            :label="$t('empleados.user_lastname')"
                            :value="valueLast"
                            :disabled="disabled"
                            :type="inputType"
                            :placeholder="$t('empleados.user_lastname')"
                            :invalid-message="invalidMessageLast"
                            ref="inputNameLast"
                            id="input-MIRLwtCq"
                        ></cv-text-input>
                    </div>
                </div>
                <br>
                <div class="bx--row">
                    <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                        <cv-text-input
                            :label="$t('empleados.user_email')"
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
                            :label="$t('empleados.user_phone')"
                            :invalid-message="invalidMessagePhone"
                            :disabled="disabledPhone"
                            :value="valuePhone"
                            ref="inputNumberPhone"
                        ></cv-text-input>
                    </div>
                </div>
                <br>
                <div class="bx--row">
                    <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2" v-if="false">
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
                    <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                        <cv-dropdown 
                        :value="valueRol"
                        :label="$t('empleados.rol')"
                        ref="inputRol"
                        :disabled="disabledRol">
                            <cv-dropdown-item value="is_enterpriseadmin">{{$t("empleados.admin_enterprise")}}</cv-dropdown-item>
                            <cv-dropdown-item value="is_staff">{{$t("empleados.empleado_enterprise")}}</cv-dropdown-item>
                        </cv-dropdown>
                    </div>
                    <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                        <cv-dropdown 
                        :label="$t('empleados.label_lang')"
                        :value="valueLang"
                        ref="inputLang"
                        >
                        <cv-dropdown-item  value="es">{{$t("empleados.esp")}}</cv-dropdown-item>
                        <cv-dropdown-item value="en">{{$t("empleados.eng")}}</cv-dropdown-item>
                        </cv-dropdown >
                    </div>
                </div>
        </template>
        <template v-if="use_primaryButton" slot="primary-button">{{$t("empleados.guardar")}}</template>
    </cv-modal>
</template>
<script>
import axios from "axios";

export default {
    name: "EditarUser",
    props: {
        userSeleccionado: String
    },
    components: {},
    data() {
        return {
            //Selector de idiomas
            labelLang: this.$t('empleados.label_lang'),
            valueLang: '',
            //selector roles
            valueRol: 'is_staff',
            invalidMessageRol: this.$t('empleados.select_row'),
            labelRol: this.$t('empleados.rol'),
            disabledRol: false,
            //card settings
            title_card: "",
            subtitle_card: "",
            closeAriaLabel: "Close",
            use_label: true,
            use_title: true,
            use_content: true,
            size: "",
            use_primaryButton: true,
            primaryButtonDisabled: false,
            autoHideOff: true,
            //input password
            labelPassword: this.$t('empleados.password'),
            disabledPassword: false,
            inputTypePassword: 'password',
            placeholderPassword: this.$t('empleados.password'),
            invalidMessagePassword: '',
            valuePassword: '',
            showPassword: false,
            //input-name
            label: this.$t('empleados.user_name'),
            disabled: false,
            inputType: "text",
            placeholder: this.$t('empleados.user_name'),
            invalidMessage: "",
            value: "",
            //input-name
            labelLast: this.$t('empleados.user_lastname'),
            placeholderLast: this.$t('empleados.user_lastname'),
            invalidMessageLast: "",
            valueLast: "",
            //input-email
            labelMail: this.$t('empleados.user_email'),
            disabledMail: false,
            inputTypeMail: "email",
            placeholderMail: "example@example.com",
            invalidMessageMail: "",
            valueMail: "",
            //numero de telefono
            labelPhone: this.$t('empleados.user_phone'),
            invalidMessagePhone: "",
            disabledPhone: false,
            valuePhone: "",
            //boton primario

            //datos
            user: '',
            is_enterpriseadmin: false,
            is_staff: false,
            password: '',
        };
    },
    methods: {
        cerrarModalNuevoEmpleado(){
            const titulo = document.querySelectorAll('[aria-label="Editar usuario "]');

            titulo[0].addEventListener('mouseenter', () => {
                console.log("Acabo de entrar");
                this.autoHideOff = false;
            });
            titulo[0].addEventListener('mouseleave', () => {
                // alert("Acabo de salir");
                this.autoHideOff = true;
            });
        },
        openModal(userSelec) {
            this.$refs.editarUserForm.show();
            
            this.showPassword = true
            this.title_card = this.$t('empleados.user_edit'),
            this.subtitle_card = this.$t('empleados.user_edit'),
            this.userSeleccionado = userSelec;
            const path = `${this.$apiURL}/profiles/${this.userSeleccionado}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                    this.value = response.data.first_name;
                    this.valueMail = response.data.email;
                    this.valuePhone = response.data.phone_number;
                    this.valueLast = response.data.last_name
                    this.user =  response.data.user
                    this.userLoginData(response.data.user)
                })
                .catch( () => {
                    this.showPassword = true
                    this.title_card = this.$t('empleados.user_new')
                    this.subtitle_card = this.$t('empleados.user_new')
                    this.value = '';
                    this.valueMail = '';
                    this.valueDesc = '';
                    this.valuePhone = '';
                    this.valueLast = '';
                });
            
        },
        userLoginData(user){
            const path = `${this.$apiURL}/profiledata/${user}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response =>{
                    console.info(response.data)
                    this.valueMail = response.data.email
                    this.is_enterpriseadmin = response.data.is_enterpriseadmin
                    this.is_staff = response.data.is_staff
                    if(response.data.is_enterpriseadmin)
                        this.valueRol = 'is_enterpriseadmin'
                    if(response.data.is_staff)
                        this.valueRol = 'is_staff'
                    this.password = response.data.password
                    this.valueLang = response.data.language
                })
        },
        actionPrimary() {
            let path = '';
            if(this.userSeleccionado){
                path = `${this.$apiURL}/profiles/${this.userSeleccionado}/`;
                axios
                .put(path, {
                    first_name: this.$refs.inputName.$refs.input.value,
                    last_name: this.$refs.inputNameLast.$refs.input.value,
                    //email: this.$refs.inputMail.$refs.input.value,
                    phone_number: this.$refs.inputNumberPhone.$refs.input.value,
                })
                .then(response => {
                    console.info(response.data)
                    this.value = response.data.first_name;
                    this.valueMail = response.data.email;
                    this.invalidMessageMail = "";
                    this.invalidMessage = "";
                    this.putUserData();
                })
                .catch(error => {
                    console.info(error)
                    const errors = error.response.data
                    if(errors.first_name)
                        this.invalidMessage = this.$t('empleados.campo_requerido')
                    if(errors.last_name)
                        this.invalidMessageLast = this.$t('empleados.campo_requerido')
                    if(errors.phone_number)
                        this.invalidMessagePhone = this.$t('empleados.campo_requerido')
                });
            }else{
                path = `${this.$apiURL}/signup`;
                const enterprise_id_ = (this.$route.query.enterprise) ? this.$route.query.enterprise : (this.$route.query.cooperative) ? this.$route.query.cooperative : ''
                const esCooperative = (this.$route.query.enterprise) ? false : (this.$route.query.cooperative) ? true : false
                axios
                .post(path, {
                    name: this.$refs.inputName.$refs.input.value,
                    phone: this.$refs.inputNumberPhone.$refs.input.value,
                    email: this.$refs.inputMail.$refs.input.value,
                    password: '',
                    is_staff: (this.$refs.inputRol.dataValue == 'is_staff') ? true : false,
                    is_enterpriseadmin: (this.$refs.inputRol.dataValue == 'is_enterpriseadmin') ? true : false,
                    language: this.$refs.inputLang.dataValue,
                    profile: {
                        first_name: this.$refs.inputName.$refs.input.value,
                        last_name: this.$refs.inputNameLast.$refs.input.value,
                        phone_number: this.$refs.inputNumberPhone.$refs.input.value,
                        enterprise_id: enterprise_id_,
                        cooperative_user: esCooperative
                    }
                })
                .then(response => {
                    console.info(response.data)
                    path = `${this.$apiURL}/password_reset/`;
                    axios
                    .post(path, {
                        email: this.$refs.inputMail.$refs.input.value,
                        type: 'new'
                    })
                    .then(response => {
                        if(response.status == 200){
                            this.$parent.getUsuariosEmpresa(enterprise_id_);
                            this.$refs.editarUserForm.hide();
                            this.$parent.mensajeAlerta = this.$t('empleados.user_generado')
                            this.$parent.tipoAlerta = 'success'
                            this.$parent.$refs.alertaGeneral.verAlerta()
                        }
                    })
                })
                .catch(error => {
                    const errors = error.response.data
                    if(errors.email)
                        this.invalidMessageMail = this.$t('empleados.campo_requerido')
                    if(errors.password)
                        this.invalidMessagePassword = this.$t('empleados.campo_requerido')
                    if(errors.profile.first_name)
                        this.invalidMessage = this.$t('empleados.campo_requerido')
                    if(errors.profile.last_name)
                        this.invalidMessageLast = this.$t('empleados.campo_requerido')
                    if(errors.profile.phone_number)
                        this.invalidMessagePhone = this.$t('empleados.campo_requerido')
                });
            }
            
        },
        putUserData(){
            const path = `${this.$apiURL}/profiledata/${this.user}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
                axios
                .put(path, {
                    email: this.$refs.inputMail.$refs.input.value,
                    is_staff: (this.$refs.inputRol.dataValue == 'is_staff') ? true : false,
                    is_enterpriseadmin: (this.$refs.inputRol.dataValue == 'is_enterpriseadmin') ? true : false,
                    language: this.$refs.inputLang.dataValue
                })
                .then(() =>{
                    const enterprise_id_ = (this.$route.query.enterprise) ? this.$route.query.enterprise : (this.$route.query.cooperative) ? this.$route.query.cooperative : ''
                    this.$parent.getUsuariosEmpresa(enterprise_id_);
                    this.$refs.editarUserForm.hide();
                    this.$parent.mensajeAlerta = this.$t('empleados.user_guardado')
                    this.$parent.tipoAlerta = 'success'
                    this.$parent.$refs.alertaGeneral.verAlerta()
                })
                .catch(error => {
                    const errors = error.response.data
                    if(errors.email)
                        this.invalidMessageMail = this.$t('empleados.campo_requerido')
                    
                })
            //}
            
        }
    }, 
    mounted(){
        const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path_lang)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })

        this.$refs.editarUserForm.$el.firstChild.style.width = '95%'
        this.$refs.editarUserForm.$el.firstChild.style.height = '65%'
        this.$refs.editarUserForm.$el.firstChild.style["max-with"] = '100%'
        this.$refs.editarUserForm.$el.firstChild.style["max-height"] = '100%';
        
        this.$refs.editarUserForm.$el.firstChild.childNodes[2].style["padding-right"] = '2%';
        this.$refs.editarUserForm.$el.firstChild.childNodes[2].style["margin-bottom"] = '2%';
        this.$refs.editarUserForm.$el.firstChild.childNodes[2].style["height"] = '95%';
        this.cerrarModalNuevoEmpleado();
    },
    created(){
        this.cerrarModalNuevoEmpleado();
    },
    beforeCreate(){
        this.cerrarModalNuevoEmpleado();
    }
};
</script>
<style scoped>
    .bx--modal-content{
        width: 100%;
        height: 100%!important;
        overflow: initial!important;
        overflow-y: initial!important;
    }
    .formcontent{
        width: 100%;
    }
</style>