import axios from 'axios'

const sentinelURL = `https://services.sentinel-hub.com`
const layers = [
    {
        "id": "AGRICULTURE",
        "title": "Agriculture",
        "description": "Based on bands 11, 8A and 2",
        "styles": [
            {
                "name": "default",
                "dataProduct": {
                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/991"
                }
            }
        ],
        "orderHint": 0,
        "dataset": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
        },
        "datasetSource": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
        },
        "defaultStyleName": "default",
        "datasourceDefaults": {
            "upsampling": "BICUBIC",
            "mosaickingOrder": "mostRecent",
            "temporal": false,
            "maxCloudCoverage": 20.0,
            "previewMode": "PREVIEW",
            "type": "S2L1C"
        }
    },
    {
        "id": "FALSE_COLOR",
        "title": "False color (vegetation)",
        "description": "",
        "styles": [
            {
                "name": "default",
                "description": "Default layer style",
                "dataProduct": {
                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/6"
                }
            }
        ],
        "orderHint": 0,
        "dataset": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
        },
        "datasetSource": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
        },
        "defaultStyleName": "default",
        "datasourceDefaults": {
            "upsampling": "BICUBIC",
            "mosaickingOrder": "mostRecent",
            "temporal": false,
            "maxCloudCoverage": 20.0,
            "previewMode": "PREVIEW",
            "type": "S2L1C"
        }
    },
    {
        "id": "NDVI",
        "title": "NDVI (Normalized Difference Vegetation Index)",
        "description": "Value = colorMap((B08 - B04) / (B08 + B04))",
        "styles": [
            {
                "name": "default",
                "description": "Default layer style",
                "dataProduct": {
                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/923"
                }
            }
        ],
        "orderHint": 34,
        "dataset": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
        },
        "datasetSource": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
        },
        "defaultStyleName": "default",
        "datasourceDefaults": {
            "upsampling": "BICUBIC",
            "mosaickingOrder": "mostRecent",
            "temporal": false,
            "maxCloudCoverage": 20.0,
            "previewMode": "PREVIEW",
            "type": "S2L1C"
        }
    },
    {
        "id": "MOISTURE_INDEX",
        "title": "Moisture Index",
        "description": "Based on combination of bands (B8A - B11)/(B8A + B11)",
        "styles": [
            {
                "name": "default",
                "dataProduct": {
                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/1242"
                }
            }
        ],
        "orderHint": 6,
        "dataset": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
        },
        "datasetSource": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
        },
        "defaultStyleName": "default",
        "datasourceDefaults": {
            "upsampling": "BICUBIC",
            "mosaickingOrder": "mostRecent",
            "temporal": false,
            "maxCloudCoverage": 20.0,
            "previewMode": "PREVIEW",
            "type": "S2L1C"
        }
    },
    {
        "id": "TRUE_COLOR",
        "title": "Natural color (true color)",
        "description": "Based on bands 4,3,2",
        "styles": [
            {
                "name": "default",
                "dataProduct": {
                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/84"
                }
            }
        ],
        "orderHint": 8,
        "dataset": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
        },
        "datasetSource": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1"
        },
        "defaultStyleName": "default",
        "datasourceDefaults": {
            "upsampling": "BICUBIC",
            "mosaickingOrder": "mostRecent",
            "temporal": false,
            "maxCloudCoverage": 20.0,
            "previewMode": "PREVIEW",
            "type": "S2L1C"
        }
    },
    {
        "id": "ESAS-SCENE",
        "title": "Interpretación Multifactor",
        "description": "",
        "styles": [
            {
                "name": "default",
                "description": "Default layer style",
                "dataProduct": {
                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L2A/dataproducts/1259"
                }
            }
        ],
        "orderHint": 0,
        "dataset": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L2A"
        },
        "datasetSource": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L2A/sources/2"
        },
        "defaultStyleName": "default",
        "datasourceDefaults": {
            "mosaickingOrder": "mostRecent",
            "temporal": false,
            "maxCloudCoverage": 50.0,
            "type": "S2L2A"
        }
    },
    {
        "id": "NDWI",
        "title": "NDWI",
        "description": "",
        "styles": [
            {
                "name": "default",
                "description": "Default layer style",
                "dataProduct": {
                    "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/811",
                    "id": 811,
                    "name": "NDWI.INDEX",
                    "description": "NDWI (Normalized Difference Water Index) - INDEX",
                    "evalScript": "//VERSION=3\n\nfunction evaluatePixel(samples) {\n    let val = index(samples.B03, samples.B08);\n    return [val, samples.dataMask];\n}\n\nfunction setup() {\n  return {\n    input: [{\n      bands: [\n        \"B03\",\n        \"B08\",\n        \"dataMask\"\n      ]\n    }],\n    output: {\n      bands: 2\n    }\n  }\n}\n\n",
                    "dataset": {
                        "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
                    },
                    "baseProduct": "NDWI",
                    "visualization": "INDEX",
                    "scriptVersion": 3,
                    "listed": true,
                    "additionalData": {
                        "preV3EquivalentId": 144
                    }
                }
            }
        ],
        "orderHint": 0,
        "dataset": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
        },
        "datasetSource": {
            "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1",
            "id": 1,
            "description": "Sentinel S2 - L1C",
            "settings": {
                "indexServiceUrl": "https://services.sentinel-hub.com/index"
            },
            "dataset": {
                "@id": "https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C"
            }
        },
        "defaultStyleName": "default",
        "datasourceDefaults": {
            "mosaickingOrder": "mostRecent",
            "temporal": false,
            "maxCloudCoverage": 50,
            "type": "S2L1C"
        },
    }
]
export async function crearInstanciaTempMapaCoop(coopId, enterprises_in_coop) {
    var allCoordinates = Array();
    enterprises_in_coop.map(enterprise => {
        enterprise.parcels.features.map(parcel => {
            allCoordinates.push(parcel.geometry.coordinates)
        })
    })
    const instanceIns = axios.create({
        baseURL: sentinelURL
    })
    const configIns = {
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
        }
    }
    const data = {
        'name': `Polygons4MapCoop-${coopId}`,
        'additionalData': {
            'showLogo': false,
            'showWarnings': false,
            'imageQuality': 30,
            'disabled': false
        },
        'areaOfInterest': {
            'type': "MultiPolygon",
            'coordinates': allCoordinates
            ,"crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::4326"
                }
            }
        }
    }
    //Creamos la instancia en sentinel
    let idInstance = ''
    await instanceIns.post("/configuration/v1/wms/instances", data, configIns)
    .then(async response => {
        if(response.status == 201){
            //si obtenemos un ok estalecemos los layers
            idInstance = response.data.id
            await Promise.all(layers.map(async (layer) => {
                await instanceIns.post("/configuration/v1/wms/instances/"+idInstance+"/layers", layer, configIns).then(() => {})
            }));
        }
    })

    return {'idInstancia': idInstance, 'allCoordinates': allCoordinates}
}