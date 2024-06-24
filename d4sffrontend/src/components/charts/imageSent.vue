<template>
    <div>
        <h4>{{$t("graficos.imagen_sent")}}</h4>
        <br>
        <div class="bx--row">
            <div class="bx--col-sm-2 bx--col-md-2 bx--col-lg-1" v-for="key in keys" :value="String(key)" v-bind:key="key">
                <img alt="" id="" :src="`${urlMedia}/`+datos[key].img" style="width: 100%; max">
                <p style="text-align: center;">{{datos[key].fecha}}</p>
                <p style="text-align: center;" v-if="datos[key].fechaGenerada">
                    {{datos[key].fechaGenerada}}
                </p>
                <br>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    props: {
        datos: Object(),
        urlMedia: String
    },
    data() {
        return {
            time: ``,
            srcImage:``,
            keys: Array()
        }
    },
    methods: {
        
    },
    
    mounted() {
        this.keys = Object.keys(this.datos)
    },
    };
</script>
