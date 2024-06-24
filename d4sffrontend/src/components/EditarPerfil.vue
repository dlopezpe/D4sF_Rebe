<template>
    <cv-modal
        :close-aria-label="closeAriaLabel"
        :size="size"
        :primary-button-disabled="primaryButtonDisabled"
        :auto-hide-off="autoHideOff"
        @primary-click="actionPrimary"
        ref="editarPerfilForm"
    >
        <template v-if="use_label" slot="label">{{title_card}}</template>
        <template v-if="use_title" slot="title">{{subtitle_card}} {{userSeleccionado}}</template>
        <template v-if="use_content" slot="content" class="formcontent" ref="content_form">
                <div class="bx--row">
                    <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                        <cv-text-input
                            :label="$t('empleados.user_name')"
                            :value="value"
                            :disabled="disabled"
                            :type="inputType"
                            :placeholder="$t('empleados.user_name')"
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
                    <div class="bx--col-lg-6 bx--col-md-4 bx--col-sm-2">
                        <cv-text-input
                            :label="$t('empleados.password')"
                            :value="valuePassword"
                            :disabled="disabledPassword"
                            :type="inputTypePassword"
                            :placeholder="$t('empleados.password')"
                            :invalid-message="invalidMessagePassword"
                            ref="inputPassword"
                            v-if="showPassword"
                        ></cv-text-input>
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
    name: "EditarPerfil",
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
            autoHideOff: false,
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
            id: ''
        };
    },
    methods: {
        openModal() {
            this.$refs.editarPerfilForm.show();
            
            this.showPassword = true
            this.title_card = this.$t('empleados.edit_perfil')
            this.subtitle_card = this.$t('empleados.edit_perfil')
            const path = `${this.$apiURL}/profile/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response => {
                    this.value = response.data[0].first_name;
                    this.valueMail = response.data[0].email;
                    this.valuePhone = response.data[0].phone_number;
                    this.valueLast = response.data[0].last_name
                    this.user =  response.data[0].user
                    this.id = response.data[0].id
                    this.valueLang = response.data[0].language
                    this.userLoginData(response.data[0].user)
                    
                })
                .catch(() => {
                    this.$refs.editarPerfilForm.hide();
                })
            
        },
        userLoginData(user){
            const path = `${this.$apiURL}/profiledata/${user}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
                .get(path)
                .then(response =>{
                    this.valueMail = response.data.email
                    this.password = response.data.password
                    this.valueLang = response.data.language
                })
        },
        actionPrimary() {
            let path = '';
            path = `${this.$apiURL}/profiles/${this.id}/`;
            axios
            .put(path, {
                first_name: this.$refs.inputName.$refs.input.value,
                last_name: this.$refs.inputNameLast.$refs.input.value,
                phone_number: this.$refs.inputNumberPhone.$refs.input.value,
            })
            .then(response => {
                this.value = response.data.first_name;
                this.valueMail = response.data.email;
                this.invalidMessageMail = "";
                this.invalidMessage = "";
                this.putUserData();
            })
            .catch(error => {
                const errors = error.response.data
                if(errors.first_name)
                    this.invalidMessage = this.$t('empleados.campo_requerido')
                if(errors.last_name)
                    this.invalidMessageLast = this.$t('empleados.campo_requerido')
                if(errors.phone_number)
                    this.invalidMessagePhone = this.$t('empleados.campo_requerido')
            });
        },
        putUserData(){
            const password = this.$refs.inputPassword.$refs.input.value
            const path = `${this.$apiURL}/profiledata/${this.user}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            if(password){
                axios
                .put(path, {
                    email: this.$refs.inputMail.$refs.input.value,
                    language: this.$refs.inputLang.dataValue,
                    password: (password) ? password: ''
                })
                .then(() =>{
                    this.$refs.editarPerfilForm.hide();
                    this.$parent.mensajeAlerta = this.$t('empleados.perfil_guardado')
                    this.$parent.tipoAlerta = 'success'
                    this.$parent.$refs.alertaGeneral.verAlerta()
                })
                .catch(error => {
                    const errors = error.response.data
                    if(errors.email)
                        this.invalidMessageMail = this.$t('empleados.campo_requerido')
                    if(errors.password)
                        this.invalidMessagePassword = this.$t('empleados.campo_requerido')
                    
                })
            }else{
                axios
                .put(path, {
                    email: this.$refs.inputMail.$refs.input.value,
                    language: this.$refs.inputLang.dataValue,
                })
                .then(() =>{
                    this.$root.$i18n.locale = this.$refs.inputLang.dataValue
                    this.$refs.editarPerfilForm.hide();
                    this.$parent.mensajeAlerta = this.$t('empleados.perfil_guardado')
                    this.$parent.tipoAlerta = 'success'
                    this.$parent.$refs.alertaGeneral.verAlerta()
                })
                .catch(error => {
                    const errors = error.response.data
                    if(errors.email)
                        this.invalidMessageMail = this.$t('empleados.campo_requerido')
                    if(errors.password)
                        this.invalidMessagePassword = this.$t('empleados.campo_requerido')
                    
                })
            }
        }
    },
    mounted(){
        if(this.$session.get('user')){
            const path = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
            axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
            axios
            .get(path)
            .then(response =>{
                this.$root.$i18n.locale = response.data.language
            })
        }
        this.$refs.editarPerfilForm.$el.firstChild.style.width = '95%'
        this.$refs.editarPerfilForm.$el.firstChild.style.height = '65%'
        this.$refs.editarPerfilForm.$el.firstChild.style["max-with"] = '100%'
        this.$refs.editarPerfilForm.$el.firstChild.style["max-height"] = '100%'
        
        this.$refs.editarPerfilForm.$el.firstChild.childNodes[2].style["padding-right"] = '2%'
        this.$refs.editarPerfilForm.$el.firstChild.childNodes[2].style["margin-bottom"] = '2%'
        this.$refs.editarPerfilForm.$el.firstChild.childNodes[2].style["height"] = '95%'
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