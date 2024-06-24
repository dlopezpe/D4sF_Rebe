<template>
    <cv-toast-notification
        :kind="tipoAlert"
        v-if="visibleAlerta"
        :title="tituloAlert"
        @close="doClose"
        :low-contrast="lowContrast"
        ref="alerta"
        style="transition-timing-function: cubic-bezier(0.2, 0, 1, 0.9);
    transition-duration: 2000ms;"
    ></cv-toast-notification>
</template>

<script>
export default {
    name: "AlertaGeneral",
    props: {
        tituloAlert: String,
        tipoAlert: String,
        ishidden: {
            type: Boolean,
            default: true
        }
    },
    data() {
        return {
            lowContrast: false,
            visibleAlerta: false,
        };
    },
    methods: {
        verAlerta() {
            this.visibleAlerta = true
            if(this.ishidden){
            setTimeout(() => {
                this.doClose()
            }, 3000)
            }
            
        },
        doClose(){
            this.visibleAlerta = false
        }
    }   
};
</script>

<style scoped>
.bx--toast-notification{
    position: absolute;
    bottom: 0;
    right: 0;
    z-index: 1;
}
</style>