<template>
<div>
    <Board/>
    <div class="MapView">
        <GenGraficosAnterioresComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import GenGraficosAnterioresComponent from '@/components/adminActions/GenGraficosAnterioresComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        GenGraficosAnterioresComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>