<template>
<div>
    <Board/>
    <div class="MapView">
        <ParcelsToSentinelComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import ParcelsToSentinelComponent from '@/components/adminActions/ParcelsToSentinelComponent.vue'

export default {
    name: 'Home',
    components: {
        Board,
        ParcelsToSentinelComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>