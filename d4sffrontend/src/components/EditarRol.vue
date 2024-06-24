<!--
@modal-shown="actionShown"
@modal-hidden="actionHidden"
@modal-hide-request="actionHideRequest"
-->
<template>
    <cv-modal
        :close-aria-label="closeAriaLabel"
        :size="size"
        :primary-button-disabled="primaryButtonDisabled"
        :auto-hide-off="autoHideOff"
        @primary-click="actionPrimary"
        ref="editarRolForm"
    >
        <template v-if="use_label" slot="label">{{title_card}}</template>
        <template v-if="use_title" slot="title">{{subtitle_card}} {{userSeleccionado}}</template>
        <template v-if="use_content" slot="content">
            <cv-text-input
            :label="labelName"
            :value="valueName"
            :disabled="disabledName"
            :type="inputTypeName"
            :placeholder="placeholderName"
            :invalid-message="invalidMessageName"
            ref="inputName"
            id="input-MIRLwtCq"
            ></cv-text-input>

            <br/>

            <cv-text-input
            :label="labelDesc"
            :value="valueDesc"
            :disabled="disabledDesc"
            :type="inputTypeDesc"
            :placeholder="placeholderDesc"
            :invalid-message="invalidMessageDesc"
            ref="inputDesc"
            id="input-3zcRveTf"
            ></cv-text-input>

        </template>
        <template v-if="use_primaryButton" slot="primary-button">Guardar</template>
    </cv-modal>
</template>
<script>
import axios from "axios";
export default {
    name: "EditarGroup",
    props: {
        userSeleccionado: String
    },
    components: {},
    data() {
        return {
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
            //input-name
            labelName: 'Nombre del Rol',
            valueName: '',
            disabledName: false,
            inputTypeName: 'text',
            placeholderName: 'Nombre...',
            invalidMessageName: '',
            //input-email
            labelDesc: 'Descripción del Rol',
            valueDesc: '',
            disabledDesc: false,
            inputTypeDesc: 'text',
            placeholderDesc: 'Nombre...',
            invalidMessageDesc: '',
        };
    },
    methods: {
        openModal(userSelec) {
            this.$refs.editarRolForm.show();
            
            this.showPassword = false
            this.title_card = 'Editar Rol',
            this.subtitle_card = 'Editar Rol:'
            this.userSeleccionado = userSelec;
            const path = `${this.$apiURL}/roles/${this.userSeleccionado}/`;
            axios
                .get(path)
                .then(response => {
                    this.valueName = response.data.name;
                    this.valueDesc = response.data.description;
                })
                .catch( () => {
                    this.showPassword = true
                    this.title_card = 'Nuevo Rol'
                    this.subtitle_card = 'Crear nuevo Rol'
                    this.valueName = '';
                    this.valueDesc = '';
                });
        },
        actionPrimary() {
            let path = '';
            if(this.userSeleccionado){
                path = `${this.$apiURL}/roles/${this.userSeleccionado}/`;
                axios
                .put(path, {
                    name: this.$refs.inputName.$refs.input.value,
                    description: this.$refs.inputDesc.$refs.input.value,
                })
                .then(response => {
                    this.valueName = response.data.name;
                    this.valueDesc = response.data.description;
                    this.$parent.getUsers();
                    this.$refs.editarRolForm.hide();
                    this.invalidMessageName = "";
                    this.invalidMessageDesc = "";
                })
                .catch(error => {
                    console.info(error);
                    if (error.response.data.name)
                        this.invalidMessageName = error.response.data.name[0];
                    if (error.response.data.description)
                        this.invalidMessageDesc = error.response.data.description[0];
                });
            }else{
                path = `${this.$apiURL}/roles/`;
                axios
                .post(path, {
                    name: this.$refs.inputName.$refs.input.value,
                    description: this.$refs.inputDesc.$refs.input.value,
                })
                .then(response => {
                    this.valueName = response.data.name;
                    this.valueDesc = response.data.description;
                    this.$parent.getUsers();
                    this.$refs.editarRolForm.hide();
                    this.invalidMessageName = "";
                    this.invalidMessageDesc = "";
                })
                .catch(error => {
                    console.info(error);
                    if (error.response.data.name)
                        this.invalidMessageName = error.response.data.name[0];
                    if (error.response.data.description)
                        this.invalidMessageDesc = error.response.data.description[0];
                });
            }
            
            
        }
    }
    
};
</script>
<style scoped>
</style>