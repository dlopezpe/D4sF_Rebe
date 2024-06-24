<template>
    <div class="bx--grid-fluid" id="gridContainer">
        <div class="bx--row-fixed" id="rowLogin">
            <div class="bx--col-sm-12 bx--col-md-3 bx--col-lg-3" id="bxFormLogin">
                <div>
                    <img alt="D4SF" id="logo" src="../assets/logo-D4SF-login.png">
                    
                    <h2 id="loginTitle">
                        Login
                    </h2>
                    <cv-text-input
                    :label="$t('login.email')"
                    placeholder="example@example.com"
                    :invalid-message="errorEmail"
                    @input="quitarErrorEmail"
                    type="email" id="emailInput" ref="emailInput" v-model="email"></cv-text-input>
                    <br>
                    <cv-text-input
                    :label="$t('login.password')"
                    :placeholder="$t('login.password')"
                    v-model="password"
                    :invalid-message="errorPass"
                    @input="quitarErrorPass"
                    type="password" id="passInput" ref="passInput"></cv-text-input>
                    <br>
                    <cv-toast-notification v-if="visibleAlert" 
                    kind="error"
                    sub-title="Usuario o contraseña inválidos"
                    @close="doClose"
                    low-contrast="false"
                    class="errorlogin"></cv-toast-notification>
                    <br>
                    <cv-button
                        id="loginButt"
                        @click="login">
                        Login
                        <cv-loading
                            :small="true"
                            :active="isActiveLoading"
                            :overlay="false" v-if="isVisibleLoad"></cv-loading>
                    </cv-button>
                    <br>
                    <br>
                    <p>
                        <cv-link
                        :href="href"
                        @click="recordarPass"
                        :disabled="disabledLinkRecordar"
                        :inline="inline">
                            {{$t("login.olvidar_pass")}}
                        </cv-link>
                    </p>
                </div>
                <img alt="D4SF" id="logoSMB" src="../assets/logo-SMB-login.png">
            </div>
        </div>
        <RecordarPassComponent ref="recordarPassComponent" />
    </div>
</template>
<script>
import axios from "axios";
import RecordarPassComponent from "../components/RecordarPassComponent";

export default {
    name: "LoginComponent",
    props: {},
    components: {RecordarPassComponent},
    data() {
        return {
            isActiveLoading: false,
            isVisibleLoad: false,
            disabledLinkRecordar: false,
            href: "javascript:void(0)",
            inline: false,
            email: "",
            password: "",
            errorEmail: "",
            errorPass: "",
            visibleAlert: false,
        }
    },
    methods: {
        recordarPass(){
            this.$refs.recordarPassComponent.visible = true
        },
        login(){
            this.isActiveLoading = true
            this.isVisibleLoad = true
            const path = `${this.$apiURL}/signin/`;
            axios
            .post(path, {"email": this.$refs.emailInput.$refs.input.value,"password":this.$refs.passInput.$refs.input.value})
            .then(response => {
                sessionStorage.setItem("apiAccess", response.data.token);
                sessionStorage.setItem("email", this.$refs.emailInput.$refs.input.value);
                
                setTimeout(() =>{
                    this.isActiveLoading = false
                    this.isVisibleLoad = false
                    if(sessionStorage.getItem("apiAccess")){
                        this.$router.push("/map");
                    }
                }, 1000)
            })
            .catch(error =>{
                this.isActiveLoading = false
                this.isVisibleLoad = false
                console.info(error)
                if(!error.response.status){
                    this.login
                }
                if(error.response.data.email)
                    this.errorEmail = error.response.data.email[0]
                if(error.response.data.password)
                    this.errorPass = error.response.data.password[0]
                if(error.response.data.non_field_errors){
                    this.visibleAlert = true
                    this.password = ""
                }
            })
            /*
            const instanceIns = axios.create({
                baseURL: this.$apiURL
            })
            const configIns = {
                headers: {
                    "Content-Type": "application/json",
                }
            }
            const bodyIns = JSON.stringify({
                "email":this.email,
                "password":this.password,
                
            })
            instanceIns.post("/signin/", bodyIns, configIns).then(resp => {
                console.info(resp)
                sessionStorage.setItem("apiAccess", resp.data.token);
                var cookie = sessionStorage.getItem("apiAccess")
                this.$router.push("/");
                if(cookie != null){
                    //this.getDatosUser();
                    this.$router.push("/");
                }else{
                    this.$router.push("/login");
                }
                
            }).catch(error => {
                console.info(error.data)
                if(error.status == 400){
                    if(error.response.data.email)
                        this.errorEmail = error.response.data.email[0]
                    if(error.response.data.password)
                        this.errorPass = error.response.data.password[0]
                    if(error.response.data.non_field_errors)
                        this.visibleAlert = true
                        this.password = ""
                }
                if(error.status == 401){
                    console.info(error)
                    this.login()
                }
            })
            */
        },
        doClose(){
            this.visibleAlert = false
        },
        quitarErrorPass(){
            this.errorPass = ''
        },
        quitarErrorEmail(){
            this.errorEmail = ''
        }
    },
    created(){
        var userLang = navigator.language || navigator.userLanguage; 
        if (userLang == 'es-ES'){
            this.$root.$i18n.locale = 'es'
        }else{
            this.$root.$i18n.locale = 'en'
        }
    }
}
</script>
<style scoped>
    #gridContainer{
        background-image: url('../assets/fondo-login-D4SF-v2.png');
        background-repeat: no-repeat;
        background-size: cover;
    }
    #gridContainer, #rowLogin, #bxFormLogin{
        height: 100vh;
    }
    #bxFormLogin{
        background-color: #f4f4f4;
        padding-top: 3%;
    }
    #rowLogin{
        padding: 0%;
    }
    #loginTitle{
        margin-bottom: 48px;
    }
    #loginButt{
        width: 100%;
    }
    #logo{
        width: 100%;
        max-width: 280px;
        margin-bottom: 5%;
    }
    .errorlogin{
        width: 100%;
    }
    #logoSMB{
        position: absolute;
        left: 19px;
        bottom: 10px;
    }
</style>