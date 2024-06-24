<template>
<div>
    <Board/>
    <div class="MapView">
        <SentinelInstancesRefreshParcels/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import SentinelInstancesRefreshParcels from '@/components/adminActions/SentinelInstancesRefreshParcels.vue'

export default {
    name: 'Home',
    components: {
        Board,
        SentinelInstancesRefreshParcels
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>