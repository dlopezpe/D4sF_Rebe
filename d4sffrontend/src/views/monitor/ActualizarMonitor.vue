<template>
<div>
    <Board/>
    <div class="MapView">
        <MonitorComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import MonitorComponent from '@/components/monitor/ActualizarMonitorComponent.vue'

export default {
    name: 'GenGraficos',
    components: {
        Board,
        MonitorComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>