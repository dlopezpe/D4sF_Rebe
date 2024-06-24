<template>
<div>
    <Board/>
    <div class="MapView">
        <InportHitParcelsKMLComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import InportHitParcelsKMLComponent from '@/components/importParcels/InportHitParcelsKMLComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        InportHitParcelsKMLComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>