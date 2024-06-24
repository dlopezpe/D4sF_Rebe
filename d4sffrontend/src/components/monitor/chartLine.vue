<script>
import { Bar, LineChart  } from "vue-chartjs";
//import axios from "axios";

export default {
    extends: Bar,
    props: {
        bbox: String,
        sentinelLay: String,
        rangeTime: String,
        datos: Object(),
        layer:String
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
            dataNaraja: Array(),
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
                scaleShowValues: true,
                scales: {
                    xAxes: [
                    {
                        stacked: true,
                        autoSkip: false
                    }
                    ],
                    yAxes: [
                    {
                        stacked: true
                    }
                    ]
                },
                title: {
                    display: true,
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
        console.info(this.layer)
        if(this.layer === 'NDVI'){
            this.datos.forEach(dato => {
                this.fechas.push(`${dato.name} - ${dato.nubes_porcent}%`)

                this.dataAmarillosAltos.push(dato.pix_amarillo_altos_porcent)
                this.dataAmarillosMedios.push(dato.pix_amarillo_medios_porcent)
                this.dataAmarillosBajos.push(dato.pix_amarillo_bajos_porcent)

                this.dataAzulesAltos.push(dato.pix_azul_altos_porcent)
                this.dataAzulesMedios.push(dato.pix_azul_medios_porcent)
                this.dataAzulesBajos.push(dato.pix_azul_bajos_porcent)

                this.dataRojosAltos.push(dato.pix_rojo_altos_porcent)
                this.dataRojosMedios.push(dato.pix_rojo_medios_porcent)
                this.dataRojosBajos.push(dato.pix_rojo_bajos_porcent)

                this.dataVerdesAltos.push(dato.pix_verde_altos_porcent)
                this.dataVerdesMedios.push(dato.pix_verde_medios_porcent)
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
        }else{
            this.datos.forEach(dato => {
                this.fechas.push(`${dato.name} - ${dato.nubes_porcent}%`)

                this.dataNaraja.push(dato.pix_naranja_porcent)
                this.dataAmarillos.push(dato.pix_amarillo_porcent)
                this.dataVerdes.push(dato.pix_verde_porcent)
                this.dataAzulClaro.push(dato.pix_azul_claro_porcent)
                this.dataAzulMedio.push(dato.pix_azul_medio_porcent)
                this.dataAzulOscuro.push(dato.pix_azul_oscuro_porcent)
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
        }
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