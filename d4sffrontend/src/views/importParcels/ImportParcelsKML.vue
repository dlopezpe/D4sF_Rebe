<template>
<div>
    <Board/>
    <div class="MapView">
        <InportParcelsKMLComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import InportParcelsKMLComponent from '@/components/importParcels/InportParcelsKMLComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        InportParcelsKMLComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>