import axios from 'axios'


const url_api_monitor = `https://monitord4sf.devsmb.es`
//const url_api_monitor = `http://127.0.0.1:7000`

export function getDataMoisture(finicio, ffin, parcels){
    return axios.post(`${url_api_monitor}/moisturemonitor/data/`, {
        finicio: finicio,
        ffin: ffin,
        parcels: parcels,
    })
}

export function getDataNdvi(finicio, ffin, parcels){
    return axios.post(`${url_api_monitor}/ndvimonitor/data/`, {
        finicio: finicio,
        ffin: ffin,
        parcels: parcels,
    })
}

export function updateDataMoisture(finicio, ffin, parcels, enterprise){
    return axios.post(`${url_api_monitor}/moisturemonitor/parcelas/`, {
        finicio: finicio,
        ffin: ffin,
        parcels: parcels,
        enterprise: enterprise,
        email: sessionStorage.getItem('email')
    })
}

export function updateDataNdvi(finicio, ffin, parcels, enterprise){
    return axios.post(`${url_api_monitor}/ndvimonitor/parcelas/`, {
        finicio: finicio,
        ffin: ffin,
        parcels: parcels,
        enterprise: enterprise,
        email: sessionStorage.getItem('email')
    })
}

export function exportToMoisture(data,paramsString = ""){

    let dataRequest = {
        'data': data,
        'email': sessionStorage.getItem('email')
    }
    
    let monitor_url = `${url_api_monitor}/moisturemonitor/exportexcel/`;
    //let monitor_url = `http://127.0.0.1:7000/moisturemonitor/exportexcel/`;
    if (paramsString != ""){
        monitor_url = `${url_api_monitor}/moisturemonitor/exportexcel/${paramsString}`;
        //monitor_url = `http://127.0.0.1:7000/moisturemonitor/exportexcel/${paramsString}`;
    }
    return axios.post(monitor_url, dataRequest)
}

export function exportToNdvi(data,paramsString = ""){
    
    let dataRequest = {
        'data': data,
        'email': sessionStorage.getItem('email')
    }
    let monitor_url = `${url_api_monitor}/ndvimonitor/exportexcel/`;
    //let monitor_url = `http://127.0.0.1:7000/ndvimonitor/exportexcel/`;
    if (paramsString != ""){
        monitor_url = `${url_api_monitor}/ndvimonitor/exportexcel/${paramsString}`;
        //monitor_url = `http://127.0.0.1:7000/ndvimonitor/exportexcel/${paramsString}`;
    }
    return axios.post(monitor_url, dataRequest)
}



