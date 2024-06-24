import axios from 'axios'

const url_api = process.env.VUE_APP_URL_API
//const url_api_sentinel = process.env.VUE_APP_URL_API_SENTINEL
//const url_api_media = process.env.VUE_APP_URL_API_MEDIA

export function getComunidades(){
    return axios.get(`${url_api}/sigpac/get_comunidades/`)
}
export function getProvincias(comunidad){
    return axios.get(`${url_api}/sigpac/get_provincias/?comunidad=${comunidad}`)
}
export function getMunicipios(provincia){
    return axios.get(`${url_api}/sigpac/get_municipios/?provincia=${provincia}`)
}
export function getAgregados(provincia,municipio){
    return axios.get(`${url_api}/sigpac/get_agregados/?provincia=${provincia}&municipio=${municipio}`)
}
export function getZonas(provincia,municipio,agregado){
    return axios.get(`${url_api}/sigpac/get_zonas/?provincia=${provincia}&municipio=${municipio}&agregado=${agregado}`)
}
export function getPoligonos(provincia,municipio,agregado,zona){
    return axios.get(`${url_api}/sigpac/get_poligonos/?provincia=${provincia}&municipio=${municipio}&agregado=${agregado}&zona=${zona}`)
}
export function getParcelas(provincia,municipio,agregado,zona,poligono){
    return axios.get(`${url_api}/sigpac/get_parcelas/?provincia=${provincia}&municipio=${municipio}&agregado=${agregado}&zona=${zona}&poligono=${poligono}`)
}
export function getRecintos(provincia,municipio,agregado,zona,poligono,parcela){
    return axios.get(`${url_api}/sigpac/get_recintos/?provincia=${provincia}&municipio=${municipio}&agregado=${agregado}&zona=${zona}&poligono=${poligono}&parcela=${parcela}`)
}
export function getDirect(dato){
    return axios.get(`${url_api}/sigpac/get_direct/?dato=${dato}`)
}