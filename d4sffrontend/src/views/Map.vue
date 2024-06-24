<template>
<div>
  <Board/>
  <div class="MapView">
    <MapComponent4/>
  </div>
</div>
</template>

<script>
// @ is an alias to /src
import Board from '@/views/Board.vue'
import MapComponent4 from '@/components/MapComponent4.vue'
//import MapComponent2 from '@/components/MapComponent2.vue'
//import MapComponentOL from '@/components/MapComponentOL.vue'
//import axios from "axios";
//

export default {
  name: 'Home',
  components: {
    MapComponent4,
    Board
  },
  mounted: function () {
      
      //console.info('User Logged')
  },
}
</script>