<template>
<div>
    <Board/>
    <div class="MapView">
        <InportCampanaComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import InportCampanaComponent from '@/components/importParcels/InportCampanaComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        InportCampanaComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>