<template>
    <div id="div_buscador">
            <gmap-autocomplete @place_changed="setPlace"  class="form-control bx--text-input" :placeholder="$t('map.intro_ubica')" style="with: 100%">
            </gmap-autocomplete>
        </div>
</template>
<script>
export default {
    name: 'ControllerQuickEdit',
    props: {
        parcelSelected: Object,
        verErrorDraw: Boolean,
        errorDrawMsg: String,
        coordinatesPoly: String
    },
    data() {
        return {
        }
    },
    components: {
        
    },
    methods: {
        setPlace(place){
            //console.info(place.geometry.viewport.keys())
            //const lat = (place.geometry.viewport.Za.i + place.geometry.viewport.Za.j) / 2
            //const long = (place.geometry.viewport.Va.i + place.geometry.viewport.Va.j) / 2
            //this.center = [long, lat]
            this.$emit('setCenter', [place.geometry.location.lng(), place.geometry.location.lat()])
        }
    },
    mounted: function () {
    },
    beforeCreate(){
        
    }
}
</script>
<style scoped>
    #control_der{
        margin-top: 58px;
        padding: 10px;
        background-color: #f4f4f4;
        position: fixed;
        top: 0px;
        right: 8px;
    }
    .errorDraw{
        color: #da1e28;
        font-weight: 400;
        font-size: 12px;
    }
    #div_buscador{
        position: fixed;
        width: 40vw;
        padding: 10px;
        margin-top: 0px;
        margin-left: 500px;
    }
</style>