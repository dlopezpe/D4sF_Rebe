<script>
import { Bar, LineChart  } from "vue-chartjs";
//import axios from "axios";

export default {
    extends: Bar,
    props: {
        bbox: String,
        sentinelLay: String,
        rangeTime: String,
        datos: Object()
    },
    components: {
        LineChart
    },
    data() {
        return {
            isActiveLoading: false,
            isVisibleLoad: true,
            dataAmarillos: Array(),
            dataAzules: Array(),
            dataRojos: Array(),
            dataVerdes: Array(),
            dataAmarillosAltos: Array(),
            dataAmarillosMedios: Array(),
            dataAmarillosBajos: Array(),
            dataAzulesAltos: Array(),
            dataAzulesMedios: Array(),
            dataAzulesBajos: Array(),
            dataRojosAltos: Array(),
            dataRojosMedios: Array(),
            dataRojosBajos: Array(),
            dataVerdesAltos: Array(),
            dataVerdesMedios: Array(),
            dataC1: Array(),
            dataC2: Array(),
            fechasC0: Array(),
            fechasC1: Array(),
            fechasC2: Array(),
            fechas: Array(),
            options: {
                responsive: true,
                maintainAspectRatio: false,
                hoverMode: "index",
                stacked: this.isMobile(),
                title: {
                    display: true,
                    text: this.$t('graficos.grafico_ndvi'),
                },
            },
            data:Array()
        }
    },

    methods: {
        isMobile() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return true
            } else {
                return false
            }
        },
    },
    
    mounted() {
        const keys = Object.keys(this.datos)
        keys.forEach(key =>{
            this.datos[key]
            
            this.dataAmarillosAltos.push(this.datos[key].amarillos.altos.porcent)
            this.dataAmarillosMedios.push(this.datos[key].amarillos.medios.porcent)
            this.dataAmarillosBajos.push(this.datos[key].amarillos.bajos.porcent)

            
            this.dataAzulesAltos.push(this.datos[key].azules.altos.porcent)
            this.dataAzulesMedios.push(this.datos[key].azules.medios.porcent)
            this.dataAzulesBajos.push(this.datos[key].azules.bajos.porcent)

            
            this.dataRojosAltos.push(this.datos[key].rojos.altos.porcent)
            this.dataRojosMedios.push(this.datos[key].rojos.medios.porcent)
            this.dataRojosBajos.push(this.datos[key].rojos.bajos.porcent)
            
            this.dataVerdesAltos.push(this.datos[key].verdes.altos.porcent)
            this.dataVerdesMedios.push(this.datos[key].verdes.medios.porcent)
            this.fechas.push(this.datos[key].fecha);
        })
        this.data = {
            labels: this.fechas,
            datasets: [
                {
                    label: this.$t('graficos.rojos_altos'),
                    backgroundColor: "#fe0103",
                    borderColor: "#fe0103",
                    fill: false,
                    data: this.dataRojosAltos,
                },
                {
                    label: this.$t('graficos.rojos_medios'),
                    backgroundColor: "#9b0004",
                    borderColor: "#9b0004",
                    fill: false,
                    data: this.dataRojosMedios,
                },
                {
                    label: this.$t('graficos.rojos_bajos'),
                    backgroundColor: "#680000",
                    borderColor: "#680000",
                    fill: false,
                    data: this.dataRojosBajos,
                },
                {
                    label: this.$t('graficos.amarillos_altos'),
                    backgroundColor: "#ffff33",
                    borderColor: "#ffff33",
                    fill: false,
                    data: this.dataAmarillosAltos,
                },
                {
                    label: this.$t('graficos.amarillos_medios'),
                    backgroundColor: "#cccc33",
                    borderColor: "#cccc33",
                    fill: false,
                    data: this.dataAmarillosMedios,
                },
                {
                    label: this.$t('graficos.amarillos_bajos'),
                    backgroundColor: "#666600",
                    borderColor: "#666600",
                    fill: false,
                    data: this.dataAmarillosBajos,
                },
                {
                    label: this.$t('graficos.azules_altos'),
                    backgroundColor: "#33ffff",
                    borderColor: "#33ffff",
                    fill: false,
                    data: this.dataAzulesAltos,
                },
                {
                    label: this.$t('graficos.azules_medios'),
                    backgroundColor: "#33cccc",
                    borderColor: "#33cccc",
                    fill: false,
                    data: this.dataAzulesMedios,
                },
                {
                    label: this.$t('graficos.azules_bajos'),
                    backgroundColor: "#006666",
                    borderColor: "#006666",
                    fill: false,
                    data: this.dataAzulesBajos,
                },
                
                {
                    label: this.$t('graficos.verdes_altos'),
                    backgroundColor: "#33cc33",
                    borderColor: "#33cc33",
                    fill: false,
                    data: this.dataVerdesMedios,
                },
                {
                    label: this.$t('graficos.verdes_medios'),
                    backgroundColor: "#33ff33",
                    borderColor: "#33ff33",
                    fill: false,
                    data: this.dataVerdesAltos,
                },

            ],
        };
        this.chartdata = this.data;
        this.renderChart(this.chartdata, this.options);
    },
};
</script>