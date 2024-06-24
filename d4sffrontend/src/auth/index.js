import axios from 'axios'

const url_api = process.env.VUE_APP_URL_API
export function auth(email, password){
    return axios.post(`${url_api}/signin/`, { "email": email, "password": password})
}

export function getProfile(){
    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
    return axios.get(`${url_api}/profile/`)
}

export function getPermisos(id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
    return axios.get(`${url_api}/permisos/${id}/`)
}