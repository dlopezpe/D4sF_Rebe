<!--
@modal-shown="actionShown"
@modal-hidden="actionHidden"
@modal-hide-request="actionHideRequest"
-->
<template>
    <cv-modal
    :close-aria-label="closeAriaLabel"
    :size="size"
    :title="modalTitle"
    :primary-button-disabled="primaryButtonDisabled"
    :visible="visible"

    @primary-click="actionPrimary"
    :auto-hide-off="autoHideOff"
    ref="recordarPass">
        <template v-if="true" slot="title">{{modalTitle}}</template>
        <template v-if="use_contentWithInput" slot="content">
            <div class="bx--form-item">
                <label for="text-input-3h9mddk235a" class="bx--label">{{$t("login.introduce_correo")}}</label>
                <input v-model="emailPass" id="text-input-3h9mddk235a" type="email" class="bx--text-input" data-modal-primary-focus>
            </div>
            <div class="bx--form-item">
                <cv-toast-notification v-if="visibleAlert" 
                    :kind="kindNot"
                    :sub-title="mensageNot"
                    @close="doCloseRecordar"
                    low-contrast="false"
                    class="errorlogin"></cv-toast-notification>
            </div>
            </template>
        <template v-if="use_primaryButton" slot="primary-button">{{$t("login.recordar")}}</template>
    </cv-modal>
</template>
<script>
import axios from 'axios'
export default {
    name: "RecordarPassComponent",
    props: {
        
    },
    components: {},
    data() {
        return {
            closeAriaLabel: "Close",
            size: "xs",
            use_contentWithInput: true,
            use_secondaryButton: true,
            use_primaryButton: true,
            primaryButtonDisabled: false,
            visible: false,
            autoHideOff: false,
            modalTitle: this.$t('login.recordar_contrasena'),
            placeholderRecordar: `example@example.es`,
            emailPass: ``,
            emailPassInvalid: this.$t('login.recordar_contrasena_error'),
            mensage: ``,
            visibleAlert: false,
            kindNot: 'error',
            mensageNot: ''
        }
    },
    methods: {
        actionPrimary(){
            this.emailPassInvalid = this.$t('login.recordar_contrasena_error')
            const path = `${this.$apiURL}/password_reset/`;
            axios
            .post(path, {
                email: this.emailPass,
                type: 'reset'
            })
            .then(response => {
                if(response.status == 200){
                    this.kindNot = `success`
                    this.mensageNot = this.$t('login.envio_mail')
                    this.visibleAlert = true
                }
            })
            .catch(error => {
                console.warn(error.response)
                this.kindNot = `error`
                this.visibleAlert = true
                if(error.response.data.email[0] == "This field may not be blank.")
                    this.mensageNot = this.$t('login.recordar_contrasena_error')
                if(error.response.data.email[0] == "There is no active user associated with this e-mail address or the password can not be changed")
                    this.mensageNot = this.$t('login.recordar_error')
                
            })
        },
        actionHidden(){
            this.visible = false
            this.visibleAlert = false
        },
        doCloseRecordar(){
            this.visibleAlert = false
        },
    }
}
</script>
<style scoped>

</style>