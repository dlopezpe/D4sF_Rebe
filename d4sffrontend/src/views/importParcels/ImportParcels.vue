<template>
<div>
    <Board/>
    <div class="MapView">
        <InportParcelsComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import InportParcelsComponent from '@/components/importParcels/InportParcelsComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        InportParcelsComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>