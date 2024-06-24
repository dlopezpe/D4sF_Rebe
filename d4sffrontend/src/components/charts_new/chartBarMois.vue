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
            dataNaraja: Array(),
            dataAmarillos: Array(),
            dataVerdes: Array(),
            dataAzulClaro: Array(),
            dataAzulMedio: Array(),
            dataAzulOscuro: Array(),
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
                    text: this.$t('graficos.grafico_mois'),
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
            this.dataNaraja.push(this.datos[key].naranja.porcent)
            this.dataAmarillos.push(this.datos[key].amarillo.porcent)
            this.dataVerdes.push(this.datos[key].verdes.porcent)
            this.dataAzulClaro.push(this.datos[key].azul_claro.porcent)
            this.dataAzulMedio.push(this.datos[key].azul_medio.porcent)
            this.dataAzulOscuro.push(this.datos[key].azul_oscuro.porcent)
            this.fechas.push(`${this.datos[key].nombre} - ${this.datos[key].fecha}`);
        })
        this.data = {
            labels: this.fechas,
            datasets: [
                {
                    label: this.$t('graficos.rojo_naran'),
                    backgroundColor: "#ff8000",
                    borderColor: "#ff8000",
                    fill: false,
                    data: this.dataNaraja,
                },
                {
                    label: this.$t('graficos.amarillo'),
                    backgroundColor: "#ffdf00",
                    borderColor: "#ffdf00",
                    fill: false,
                    data: this.dataAmarillos,
                },
                {
                    label: this.$t('graficos.verde'),
                    backgroundColor: "#66ff98",
                    borderColor: "#66ff98",
                    fill: false,
                    data: this.dataVerdes,
                },
                {
                    label: this.$t('graficos.azul_claro'),
                    backgroundColor: "#02fefc",
                    borderColor: "#02fefc",
                    fill: false,
                    data: this.dataAzulClaro,
                },
                {
                    label: this.$t('graficos.azul_medio'),
                    backgroundColor: "#0087ff",
                    borderColor: "#0087ff",
                    fill: false,
                    data: this.dataAzulMedio,
                },
                {
                    label: this.$t('graficos.azul_oscuro'),
                    backgroundColor: "#2000ff",
                    borderColor: "#2000ff",
                    fill: false,
                    data: this.dataAzulOscuro,
                },

            ],
        };
        this.chartdata = this.data;
        this.renderChart(this.chartdata, this.options);
    },
};
</script>