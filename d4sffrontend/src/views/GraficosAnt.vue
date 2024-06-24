<template>
    <div>
        <Board />
        <div class="GraficosView">
            <GraficosController />
        </div>
        <AlertaGeneral ref="alertaGeneral" :tituloAlert="mensajeAlerta" :tipoAlert="tipoAlerta" />
    </div>
</template>

<script>
// @ is an alias to /src
import Board from "@/views/Board.vue";
import GraficosController from "@/components/GraficosController.vue";
//import MapComponent2 from '@/components/MapComponent2.vue'
//import MapComponentOL from '@/components/MapComponentOL.vue'
//import axios from "axios";
//

export default {
    name: "Home",
    components: {
        GraficosController,
        Board,
    },
    data() {
        return {
            mensajeAlerta: "", 
            tipoAlerta: "error"
        }
    },
    mounted: function () {
        //console.info('User Logged')
    },
};
</script>