<template>
<div>
    <Board/>
    <div class="MapView">
        <ParcelsToCheckHasComponent/>
    </div>
</div>
</template>

<script>
import Board from '@/views/Board.vue'
import ParcelsToCheckHasComponent from '@/components/adminActions/ParcelsToCheckHasComponent.vue'

export default {
    name: 'Home',
    components: {
        Board,
        ParcelsToCheckHasComponent
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
}
</script>