import axios from 'axios'

const url_api = process.env.VUE_APP_URL_API
const url_api_sentinel = process.env.VUE_APP_URL_API_SENTINEL
const url_api_media = process.env.VUE_APP_URL_API_MEDIA

export function getEnterprise(enterprise){
    return axios.get(`${url_api}/enterprises/${enterprise}/?size=${99999999}&page=${1}`)
}

export function getAllEnterprises(is_monitor = true){
    if(is_monitor){
        return axios.get(`${url_api}/enterprises_active/?&size=${99999999}&page=${1}`)
    }
    return axios.get(`${url_api}/enterprises_active/?size=${99999999}&page=${1}`)
}

export function getAllActiveEnterprises() {
    return axios.get(`${url_api}/enterprises_active/?size=${99999999}&page=${1}`)
}
export function getAllActiveEnterprisesAndMonitor(){
    return axios.get(`${url_api}/enterprises_active_and_monitor/?&size=${99999999}&page=${1}`)
}

export function updateTrazasEnterprises(usuario, fecha_hora, status, enterprise){
    return axios.post(`${url_api}/enterprises/`, {
        usuario: usuario,
        fecha_hora: fecha_hora,
        status: status,
        enterprise: enterprise,
        email: sessionStorage.getItem('email')
    })
}

export function getLayersFromSentinel(){
    
    const instanceIns = axios.create({
        baseURL: url_api_sentinel
    })
    const configIns = {
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
        }
    }
    
    
    return instanceIns.get("/configuration/v1/wms/instances/2440dd85-0720-4c4c-bea2-7982fa8aa9b1/layers", configIns)
}

export function setParcelsForInstance(enterpriseName, parcels, instance){
    console.info("setParcelsForInstance ....................",enterpriseName, parcels, instance)
    
    const instanceIns = axios.create({
        baseURL: url_api_sentinel
    })
    const configIns = {
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': "Bearer "+localStorage.getItem('ApiAccessToken')
        }
    }

    

    const bodyIns = JSON.stringify({
        'name': `${enterpriseName}`,
        "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",// TODO: userid
        "additionalData": {
            "showLogo": false,
            "showWarnings": false,
            "imageQuality": 100,
            "disabled": false
        },
        'areaOfInterest': {
            'type': "MultiPolygon",
            'coordinates': parcels
            ,"crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::4326"
                }
            }
        }
    })
    return instanceIns.put("/configuration/v1/wms/instances/"+instance, bodyIns, configIns)
}

export function getFechasSentinel(bbox){
    console.warn("getFechasSentinel ....................")
    const instanceIns = axios.create({
        baseURL: url_api_sentinel
    })
    var MyDate = new Date();
    var MyDateString;
    MyDate.setDate(MyDate.getDate());
    MyDateString = ('0' + MyDate.getDate()).slice(-2) + '/' + ('0' + (MyDate.getMonth()+1)).slice(-2)
    MyDateString = MyDate.getFullYear()+'-'+('0' + (MyDate.getMonth()+1)).slice(-2)+'-'+('0' + MyDate.getDate()).slice(-2)
    return instanceIns.get(`/ogc/wfs/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?REQUEST=GetFeature&TYPENAMES=S2.TILE&OUTPUTFORMAT=application/json&TIME=2020-01-01/${MyDateString}&BBOX=${bbox}&SRSNAME=EPSG:3857`)
}

export function checkValidPolygon(polygonObj, enterprise_id){
    
    return axios.get(`${url_api}/parcel_filter/?enterprise_id=${enterprise_id}&polygon=${polygonObj}`)
}

export function putParcelPolygon(polygonObj, parcel_id, name, description, area){
    
    return axios.put(`${url_api}/parcel/${parcel_id}/`, {
        polygon: polygonObj,
        name: name,
        description: description,
        area: area
    })
}

export function deleteParcel(parcel_id){
    return axios.delete(`${url_api}/parcel/${parcel_id}/`)
}

export function createQuickParcel(name, description, polygon, area, enterprise, user_created){
    
    console.info(`${url_api}/parcels/`,name, description, polygon, area, enterprise, user_created)
    return axios.post(`${url_api}/parcels/`, {
        name: name, 
        description: description,
        polygon: polygon,
        area: area,
        enterprise: enterprise,
        user_created: user_created
    })
}

export function createInformes(nombre, layer, time_values, id_parcelas, esCooperative, enterprise_id, includeClouds){
    return axios.post(`${url_api}/procesadonew/`, {
        nombre: nombre, 
        capa: layer,
        fechaInicio: time_values[0],
        fechaFin: time_values[1],
        id_parcelas: id_parcelas,
        enterprise_id: enterprise_id,
        esCooperative: esCooperative,
        includeClouds: includeClouds
    })
}

export function getInformesAnterioresNew(enterprise_id='all', columna='created', orden='descending'){
    return axios.get(`${url_api}/procesadonew/?enterprise_id=${enterprise_id}&order=${orden}&colum_name=${columna}`)
}

export function delInformesAnterioresNew(id_parcelas){
    return axios.delete(`${url_api}/procesadonew/`, {
        data: {
            id_parcelas: id_parcelas
        }
    })
}

export function putInformesAnterioresNew(id_informe, nombre){
    return axios.put(`${url_api}/procesadonew/${id_informe}/`, {
        id: id_informe,
        nombre: nombre
    })
}

export function putInformesUnificarNew(nombre, enterprise_id, informes_sel, checkDellInforme, capa){
    return axios.put(`${url_api}/unificarInformes/`, {
        nombre: nombre,
        enterprise_id: enterprise_id,
        informes_sel: informes_sel,
        check_dell: checkDellInforme,
        capa: capa
    })
}

export function getFechasParcelsPreCreate(id_parcelas, time_values){
    return axios.post(`${url_api}/procesadonewfechas/`, {
        id_parcelas: id_parcelas,
        fechaInicio: time_values[0],
        fechaFin: time_values[1],
    })
}

export function getFechasParcelsBBOX(id_parcelas, time_values){
    return axios.post(`${url_api}/getbbox/`, {
        id_parcelas: id_parcelas,
        fechaInicio: time_values[0],
        fechaFin: time_values[1],
    })
}

export function getInformeAnteriorData(filename){
    return axios.get(`${url_api_media}/${filename}`)
}

export function getUsersList(){
    return axios.get(`${url_api}/profiles/`)
}

export function getUsersListProfiles(){
    return axios.get(`${url_api}/profiledata/`)
}

export function getFechasSentinelForInformes(bbox){
    const instanceIns = axios.create({
        baseURL: url_api_sentinel
    })
    var MyDate = new Date();
    var MyDateString;
    MyDate.setDate(MyDate.getDate());
    MyDateString = ('0' + MyDate.getDate()).slice(-2) + '/' + ('0' + (MyDate.getMonth()+1)).slice(-2)
    MyDateString = MyDate.getFullYear()+'-'+('0' + (MyDate.getMonth()+1)).slice(-2)+'-'+('0' + MyDate.getDate()).slice(-2)
    return instanceIns.get(`/ogc/wfs/5c9f425a-f830-4164-8a6c-6059bcf1b7d3?REQUEST=GetFeature&TYPENAMES=S2.TILE&OUTPUTFORMAT=application/json&TIME=2020-01-01/${MyDateString}&BBOX=${bbox}&SRSNAME=EPSG:4326`)
}

export function importParcelsFromFile(file, enterprise_id, confirm_import){
    const formData = new FormData()
    formData.append('file', file)
    formData.append('enterprise_id', enterprise_id)
    formData.append('confirm_import', confirm_import)
    return axios.post(`${url_api}/parcelasImportFromFile/`, formData)
}
export function importParcelsFromFileKML(file, enterprise_id, confirm_import,client = false){
    const formData = new FormData()
    formData.append('file', file)
    formData.append('enterprise_id', enterprise_id)
    formData.append('confirm_import', confirm_import)
    // only for new document import client Hint22
    if (client) {
        formData.append('client', client)
    }

    return axios.post(`${url_api}/parcelasImportFromFileKML/`, formData)
}
export function importParcelsFromGeoJSON(file, enterprise_id, confirm_import,borrado){
    const formData = new FormData()
    formData.append('file', file)
    formData.append('enterprise_id', enterprise_id)
    formData.append('confirm_import', confirm_import)
    formData.append('borrado', borrado)
    return axios.post(`${url_api}/parcelasImportFromGeoJSON/`, formData)
}
export function importCampanaFromFile(file, enterprise_id, confirm_import){
    const formData = new FormData()
    formData.append('file', file)
    formData.append('enterprise_id', enterprise_id)
    formData.append('confirm_import', confirm_import)
    return axios.post(`${url_api}/campanaImportFromFile/`, formData)
}

//FUNCIONES DE RECEPCION DE DATOS DE CAMPAÑA SIEMBRA Y PRODUCCION
export function getDataCampaign(finicio, ffin, parcels){
    return axios.post(`${url_api}/campana/data/`, {
        finicio: finicio,
        ffin: ffin,
        parcels: parcels,
    })
}
export function getDataSiembra(finicio, ffin, parcels){
    return axios.post(`${url_api}/siembra/data/`, {
        finicio: finicio,
        ffin: ffin,
        parcels: parcels,
    })
}
export function getDataProduccion(finicio, ffin, parcels){
    return axios.post(`${url_api}/produccion/data/`, {
        finicio: finicio,
        ffin: ffin,
        parcels: parcels,
    })
}
export function establecer_recogida(parcelas, fechaRecogida){
    return axios.put(`${url_api}/campana/recogida/`, {
        fecha:fechaRecogida,
        parcelas: parcelas,
    })
}
export function generarinforme(id){
    return axios.post(`${url_api}/generarinforme/generar/`, {
        id:id,
    })
}


//https://services.sentinel-hub.com/ogc/wfs/2440dd85-0720-4c4c-bea2-7982fa8aa9b1?REQUEST=GetFeature&TYPENAMES=S2.TILE&OUTPUTFORMAT=application/json&TIME=2020-01-01/2021-06-16&BBOX=-825672.7795364739,4638963.246627347,-542855.7748813218,4785110.844708604&SRSNAME=EPSG:3857