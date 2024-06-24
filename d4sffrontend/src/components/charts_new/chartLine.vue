<script>
import { Line, LineChart  } from "vue-chartjs";
//import axios from "axios";

export default {
    extends: Line,
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
            this.fechas.push(`${this.datos[key].nombre} - ${this.datos[key].fecha}`);
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

<!--
mounted() {
            this.$parent.isActiveLoading = true
            //let polygon = `POLYGON((-119.1266816854477 34.271931652839704, -119.12474513053895 34.27060617031794, -119.1237473487854 34.271780930127605, -119.12561953067781 34.27311082708527, -119.1266816854477 34.271931652839704))`
            //const path = `http://services.sentinel-hub.com/ogc/fis/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?LAYER=MOISTURE_INDEX&STYLE=INDEX&CRS=EPSG%3A4326&TIME=2020-07-01/2020-07-29&GEOMETRY=POLYGON((-3.6887054443332095 40.45354910154713, -3.687872171385607 40.45350035612895, -3.687995553000292 40.4525268012414, -3.688802897913774 40.45260435959019, -3.6887054443332095 40.45354910154713))&RESOLUTION=10&MAXCC=5`;
            //const path = `http://services.sentinel-hub.com/ogc/fis/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?LAYER=MOISTURE_INDEX&STYLE=INDEX&CRS=EPSG%3A4326&TIME=2020-07-01/2020-07-29&GEOMETRY=${polygon}&RESOLUTION=10&MAXCC=5`;
            //POLYGON((-6.06374070942492 38.92361297152809, -6.062307357788086 38.9235402163643, -6.062545656451143 38.92081889300846, -6.064589194780493 38.92092776476749, -6.06374070942492 38.92361297152809))
            const path = `http://services.sentinel-hub.com/ogc/fis/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?LAYER=${this.sentinelLay}&STYLE=INDEX&CRS=EPSG%3A4326&TIME=${this.rangeTime}&BBOX=${this.bbox}&RESOLUTION=10&MAXCC=5`;
            axios
            .get(path)
            .then((response) => {
                //console.info(response.data);
                const keys = Object.keys(response.data);
                //console.info(keys);
                keys.forEach((key) => {
                response.data[key].forEach((element) => {
                    if (key == "C0") {
                        this.dataC0.push(element.basicStats.mean);
                    }
                    if (key == "C1") {
                        this.dataC1.push(element.basicStats.mean);
                    }
                    if (key == "C2") {
                        this.dataC2.push(element.basicStats.mean);
                    }
                        this.fechas.push(element.date);
                    //this.fechas+key.push(element.date)
                    //this.data.push(element.basicStats.mean)
                });
                });
                let fechasUnicas = [...new Set(this.fechas)];
                this.data = {
                labels: fechasUnicas.reverse(),
                datasets: [
                    {
                    label: "C0",
                    backgroundColor: "#f87979",
                    borderColor: "#f87979",
                    fill: false,
                    data: this.dataC0.reverse(),
                    },
                    {
                    label: "C1",
                    backgroundColor: "#5eff24",
                    borderColor: "#5eff24",
                    fill: false,
                    data: this.dataC1.reverse(),
                    },
                    {
                    label: "C2",
                    backgroundColor: "#248eff",
                    borderColor: "#248eff",
                    fill: false,
                    data: this.dataC2.reverse(),
                    },
                ],
                };
                this.chartdata = this.data;
                this.renderChart(this.chartdata, this.options);
                this.$parent.isActiveLoading = false
            })
            .catch((error) => {
                this.$parent.isActiveLoading = false
                console.warn(error);
            });
        },
-->