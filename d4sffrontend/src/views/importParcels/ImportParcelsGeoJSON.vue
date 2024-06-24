<template>
<div>
    <Board/>
    <div class="MapView">
        <InportParcelsGeoJSONComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import InportParcelsGeoJSONComponent from '@/components/importParcels/InportParcelsGeoJSONComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        InportParcelsGeoJSONComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>