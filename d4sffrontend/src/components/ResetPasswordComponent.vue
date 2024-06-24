<template>
    <div id="container">
        <div class="bx--grid" id="gridContainer">
            <div class="bx--row">
                <div class="bx--col-lg"></div>
                <div class="bx--col-lg" id="modal">
                    
                        <h4>{{$t("login.reestablecer_pass")}}</h4>
                        <br><br>
                        <cv-text-input
                        :label="$t('login.nueva_pass')"
                        :placeholder="$t('login.nueva_pass')"
                        v-model="password"
                        :invalid-message="errorPass"
                        @input="quitarErrorPass"
                        type="password" id="passInput" ref="passInput"></cv-text-input>
                        <br><br>
                        <cv-text-input
                        :label="$t('login.confirma_pass')"
                        :placeholder="$t('login.confirma_pass')"
                        v-model="newPassword"
                        :invalid-message="newErrorPass"
                        @input="quitarErrorPass"
                        type="password" id="passInput" ref="passInput"></cv-text-input>
                        <br><br>
                        <cv-inline-notification v-if="visibleAlert" 
                        :kind.sync="kindNot"
                        :sub-title="mensageNot"
                        :action-label="actionlabel"
                        @action="doAction"
                        @close="doCloseRecordar"
                        low-contrast="false"
                        class="errorlogin"></cv-inline-notification>
                        <br><br>
                        <cv-button @click="establecerPass">{{$t("login.reestablecer")}}</cv-button>
                    
                </div>
                <div class="bx--col-lg"></div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
export default {
    name: "ResetPasswordComponent",
    props: {},
    components: {},
    data() {
        return {
            password: '',
            newPassword: '',
            errorPass: '',
            newErrorPass:'',
            visibleAlert: false,
            kindNot: 'error',
            mensageNot: '',
            actionlabel: this.$t('login.ir_login'),
        }
    },
    methods: {
        establecerPass(){
            if(this.password != this.newPassword){
                this.errorPass= this.$t('login.pass_no_iguales')
                this.newErrorPass= this.$t('login.pass_no_iguales')
                return false
                
            }
            const tokenUser = this.$route.query.token
            let path = `${this.$apiURL}/password_reset/verify-token`;
            axios
            .post(path, {
                token: tokenUser
            })
            .then(() => {
                    let path = `${this.$apiURL}/password_reset/confirm/`;
                    axios
                    .post(path, {
                        token: tokenUser,
                        password: this.password
                    })
                    .then(()=>{
                        this.visibleAlert = true
                        this.kindNot = `success`
                        this.mensageNot = this.$t('login.pass_reestablece')
                    })
                    .catch(error =>{
                        this.visibleAlert = true
                        this.kindNot = `error`
                        this.mensageNot = ''
                        this.mensageNot = error.response.data.password[0]
                    })
                
            })
            .catch(()=>{
                this.visibleAlert = true
                this.kindNot = `error`
                this.mensageNot = this.$t('login.pass_tiempo_exp')
            })
            
            
        },
        quitarErrorPass(){
            this.errorPass = ''
            this.newErrorPass = ''
            this.visibleAlert = false
        },
        doCloseRecordar(){
            this.visibleAlert = false
        },
        doAction(){
            this.$router.push("/login");
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
    #modal{
        padding-top: 1rem;
        padding-bottom: 1rem;
        background-color: #f4f4f4;
    }
    #container{
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