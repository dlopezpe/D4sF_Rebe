<script>
import { Radar } from "vue-chartjs";
import axios from "axios";

export default {
    extends: Radar,
    props: {
        bbox: String,
        sentinelLay: String,
        rangeTime: String
    },
    data() {
        return {
            dataC0: Array(),
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
                stacked: false,
                title: {
                    display: true,
                    text: "Grafico NDVI",
                },
            },
        }
    },

    methods: {},
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
            var data = {
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
            this.chartdata = data;
            this.renderChart(this.chartdata, this.options);
            this.$parent.isActiveLoading = false
        })
        .catch((error) => {
            console.warn(error);
            this.$parent.isActiveLoading = false
        });
    },
    };
</script>