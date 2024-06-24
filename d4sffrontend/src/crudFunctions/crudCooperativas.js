import axios from 'axios'

const url_api = process.env.VUE_APP_URL_API

export async function getAllCooperatives() {
    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
    return await axios.get(`${url_api}/cooperativesonenrlt/`)
}


export async function getCooperative(cooperativeID) {
    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
    return await axios.get(`${url_api}/cooperativesonenrlt/${cooperativeID}/`)
}