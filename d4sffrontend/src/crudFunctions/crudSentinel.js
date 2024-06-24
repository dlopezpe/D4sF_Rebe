import axios from 'axios'

const url_api = process.env.VUE_APP_URL_API
//const url_api_sentinel = process.env.VUE_APP_URL_API_SENTINEL

export function getParcelsNotSentinelInstance(){
    return axios.get(`${url_api}/parcelsnosentinstance/`)
}

export function postParcelsNotSentinelInstance(parcelsSelect){
    return axios.post(`${url_api}/parcelsnosentinstance/`, {
        parcelas: parcelsSelect
    })
}