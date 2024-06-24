<template>
<div>
    <Board/>
    <div class="MapView">
        <GenGraficosComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import GenGraficosComponent from '@/components/adminActions/GenGraficosComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        GenGraficosComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>