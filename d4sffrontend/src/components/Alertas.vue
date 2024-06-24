<template>
    <cv-toast-notification
        kind="error"
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
    name: "Alerta",
    props: {
        tituloAlert: String
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
        },
        doClose(){
            this.visibleAlerta = false
            console.log(this.$refs)
        }
    }   
};
</script>

<style scoped>
.bx--toast-notification{
    position: absolute;
    bottom: 0;
    right: 0;
    
}
</style>