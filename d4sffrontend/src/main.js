import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueI18n from 'vue-i18n'

import "carbon-components/css/carbon-components.css";
import CarbonComponentsVue from "@carbon/vue/src/index";
import { CarbonIconsVue } from '@carbon/icons-vue';
import TrashCan32 from '@carbon/icons-vue/es/trash-can/32';
import Edit32 from '@carbon/icons-vue/es/edit/32';
import Download16 from '@carbon/icons-vue/es/download/16';
import Logout20 from '@carbon/icons-vue/es/logout/20';
import UserAvatarFilledAlt20 from '@carbon/icons-vue/es/user--avatar--filled--alt/20'
import ChevronSortUp20 from '@carbon/icons-vue/es/chevron--sort--up/20'
import ChevronSortDown20 from '@carbon/icons-vue/es/chevron--sort--down/20'
import Charbar20 from '@carbon/icons-vue/es/chart--bar/20'
import Analytics20 from '@carbon/icons-vue/es/analytics/20'
import Translate20 from '@carbon/icons-vue/es/translate/20'
import Language20 from '@carbon/icons-vue/es/language/20'
import Location16 from '@carbon/icons-vue/es/location/16'
import AppConnectivity32 from '@carbon/icons-vue/es/compare/32'
import Account from '@carbon/icons-vue/es/account/20'


import axios from "axios";
import qs from "qs"

import VueLayers from 'vuelayers';
import 'vuelayers/lib/style.css';

import VueCharts from 'vue-chartjs'
import VueSession from 'vue-session'

import * as VueGoogleMaps from "vue2-google-maps";
import VueGeolocation from 'vue-browser-geolocation';

Vue.use(VueGeolocation);

Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyCUm1xbbEuxPBCHkQJ8oXmCgtB8NotFsMo",
    libraries: "places" // necessary for places input
  }
});

import moment from 'moment'
Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY hh:mm')
  }
});

  //Variables Globales
Vue.prototype.$sentinelURL = `https://services.sentinel-hub.com`
Vue.prototype.$apiURL = process.env.VUE_APP_URL_API
Vue.prototype.$apiURLMedia = process.env.VUE_APP_URL_API_MEDIA
console.log(process.env.VUE_APP_URL_API);
Vue.prototype.$apiKeyBing = `Ajf7rbOuQ1cg5-D5vOeqPxZ7PR1k5Uc_3XMYEZSRGqqx0-LdXnYfflWQfQfIHD5-`

//Variables globales de usuario
Vue.prototype.$enterprise = '';
//Sentinel
const client_id = "33467c23-fada-4405-8a5b-33ee38169273"
const client_secret = "&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:"
const instance = axios.create({
  baseURL: `https://services.sentinel-hub.com`
})
const config = {
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
}
const body = qs.stringify({
  client_id,
  client_secret,
  grant_type: "client_credentials"
})
instance.post("/oauth/token", body, config).then(resp => {
  Object.assign(instance.defaults, {headers: {authorization: `Bearer ${resp.data.access_token}`}})
  localStorage.setItem('ApiAccessToken', resp.data.access_token)
})
  //Declaracion de componentes
Vue.use(CarbonComponentsVue);
Vue.use(CarbonComponentsVue);
Vue.use(CarbonIconsVue, {
  components: {
    TrashCan32, Edit32, Download16, Logout20, UserAvatarFilledAlt20,
    ChevronSortUp20, ChevronSortDown20, Charbar20, Analytics20,
    Translate20, Language20, Location16, AppConnectivity32,
    Account
  },
});

Vue.use(VueLayers, {
  dataProjection: 'EPSG:4326',
})
Vue.use(VueCharts)
Vue.use(VueSession)
Vue.use(VueI18n)

Vue.config.productionTip = false




//Traduccion
/*

:title="$t('login.perfil')"
{{$t("login.fechas_disponibles")}}
this.$t('login.perfil')
${this.$t('login.parcela_solapada_con')}
*/

const messages = {
  es: {
    app: {
      monitor: 'Monitor',
      dashboard: 'Dashboard',
      administracion: 'Administración',
      administracion_empresas: 'Administración de Empresas',
      administracion_usuarios: 'Administración de Usuarios',
      graficos: 'Gráficos',
      alertas: 'Alertas',
      perfil: 'Perfil',
      desconect: 'Desconectar',
      administracion_cooperativas: 'Administración de Cooperativas',
      emprise: 'Empresa',
    },
    map: {
      most_todas_empresas: 'Mostrar todas las Parcelas',
      sel_empresa: 'Selecciona una Empresa',
      listado_empresas: 'Listado de Empresas',
      listado_parcelas: 'Listado de parcelas',
      listado_usuarios: 'Listado de usuarios',
      parcelas_de: 'Parcelas de',
      colors: 'Colores',
      fechas_disponibles: 'Fechas Disponibles',
      edit_rapido: 'Edición Rápida',
      guardar: 'Guardar',
      cancelar: 'Cancelar',
      elimina_parcela: 'Eliminar Parcela',
      eliminar: 'Eliminar',
      parcela_nueva: 'Nueva Parcela',
      crear_parcela: 'Crear Parcela',
      seguro: '¿Estás seguro?',
      seguro_parcel_del: '¿Seguro que quieres eliminar la parcela?',

      sent_layers: 'Sentinel Layers',
      sent_layers_sel: 'Selecciona un Layer de Sentinel',
      fecha: 'Fecha',
      opacidad: 'Opacidad',
      nombre_parcela: 'Nombre de la parcela',
      place_nombre_parcela: 'Nombre...',
      desc_parcela: 'Descripción de la Parcela',
      place_desc_parcela: 'Descripción...',
      parcela_solapada_con: 'La parcela se está solapando con',
      parcela_solapada_misma: 'La parcela se esta solapando a sí misma',
      sup_area_parcel: 'Se ha superado el Límite para la edición de parcelas, reduzca el area',
      establecer_limites_parcela: 'Tienes que establecer los límites de la parcela',
      intro_ubica: 'Introduce una ubicación',
      loc_no_disponible: 'La localización no es complatible con este dispositivo'
    },
    adminEnterprise: {
      listado_empresas: 'Listado de Empresas',
      info_nav: 'Para el correcto funcionamiento de la aplicación se recomienda utilizar los navegadores Chrome, Edge, Opera o Safari.',
      add_empresa: 'Añadir nueva Empresa',
      eliminar: 'Eliminar',
      guardar: "Guardar",
      editar: 'Editar',
      seguro: '¿Estás seguro?',
      seguro_enterprise_del: '¿Seguro que quieres eliminar el/las empresas/s?',
      txt_seguro_enterprise_status: 'Selecciona el estado que quieras proporcionar a esta empresa. Recuerda que si una empresa está Inactiva, no podrá consultarse en el mapa, solicitar nuevos informes y dejará de recibir actualizaciones del Monitor diario.',
      cancelar: 'Cancelar',
      activo: 'Activa',
      inactivo: 'Inactiva',
      nombre: 'Nombre',
      cif: 'CIF',
      editar_estado: 'Cambiar Estado',
      estado: 'Estado',
      hectareas_disponibles: 'Área disponible',
      hectareas_usadas: 'Área usada',
      solo_una_empresa: 'Solo tienes que seleccionar una empresa para esta acción',
      del_empresa_error: 'Ha ocurrido un error con la eliminación de la/s empresa/s',
      update_state_empresa_error: 'Ha ocurrido un error con la actualización del estado de la empresa',
    },
    newEnterprise: {
      editar_enterprise: 'Editar empresa',
      nueva: 'Nueva Empresa',
      tel_enterprise: 'Teléfono de la empresa',
      usuarioAdministrador: 'Usuario Administrador',
      guardar: 'Guardar',
      nombre_enterprise: 'Nombre de la Empresa',
      cif_enterprise: 'CIF de la Empresa',
      direccion_enterprise: 'Dirección de la Empresa',
      hectareas_disponible: 'Hectáreas Disponibles',
      tipo_Metrica: 'Tipo de Métrica',
      campo_requerido: 'Este campo es requerido',
      save_enterprise: 'Empresa Guardada Correctamente',
      save_status: 'Estado de la Empresa Guardado Correctamente',
    },
    empleados: {
      empleados_lista: 'Lista de Empleados',
      add: 'Añadir',
      eliminar: 'Eliminar',
      editar: 'Editar',
      seguro: '¿Estás seguro?',
      seguro_user_del: '¿Seguro que quieres eliminar el/los usuario/s?',
      cancelar: 'Cancelar',
      nombre: 'Nombre',
      apellido: 'Apellido',
      telefono: 'Teléfono',
      desarrollo: 'En desarrollo',
      un_user_selec: 'Solo tienes que seleccionar un usuario para esta acción',
      user_error: 'Ha ocurrido un error con la eliminación de los usuarios',

      guardar: 'Guardar',
      admin_enterprise: 'Administrador de la empresa',
      empleado_enterprise: 'Empleado',
      select_row: 'Debes seleccionar un rol',
      rol: 'Rol del Usuario',
      password: 'Contraseña',
      user_name: 'Nombre de Usuario',
      user_lastname: 'Apellido/s de Usuario',
      user_email: 'Correo electrónico',
      user_phone: 'Número de Teléfono',

      user_edit: 'Editar usuario',
      user_new: 'Nuevo Usuario',
      campo_requerido: 'Este campo es requerido',
      user_generado: 'Usuario Generado Correctamente, Le hemos enviado un email',
      user_guardado: 'Usuario Guardado Correctamente',
      perfil_guardado: 'Perfil Guardado Correctamente',

      label_lang: 'Idioma',
      esp: 'Español',
      eng: 'Inglés',

      edit_perfil: 'Editar Perfil'
    },
    parcelas: {
      parcel_list: 'Lista de Parcelas',
      place_buscar: 'Buscar Nombre',
      place_nuevo: 'Añadir nuevo',
      eliminar: 'Eliminar',
      editar: 'Editar',
      seguro: '¿Estás seguro?',
      seguro_parcel_del: '¿Seguro que quieres eliminar la/s parcela/s?',
      cancelar: 'Cancelar',

      nombre: 'Nombre',
      descrip: 'Descripción',
      hectareas: 'Área',
      desarrollo: 'En desarrollo',
      parcel_limit: 'Se ha superado el límite para la creación de nuevas parcelas',
      parcel_sel_alert: 'Solo tienes que seleccionar una parcela para esta acción',
      parcel_del_error: 'Ha ocurrido un error con la eliminación de las parcelas',

      guardar: 'Guardar',
      sigpac_pro: 'SIGPAC Progresivo',
      sigpac_direc: 'SIGPAC Directo',
      sigpac_error: 'Error En la Búsqueda',
      buscar: 'Buscar',
      ubicacion: 'Introduce una ubicación',

      comunidad: 'Comunidad',
      comunidad_sel: 'Selecciona Comunidad',
      provincia: 'Provincia',
      provincia_sel: 'Selecciona Provincia',
      municipio: 'Municipio',
      municipio_sel: 'Selecciona Municipio',
      agregado: 'Agregado',
      agregado_sel: 'Selecciona Agregado',
      zona: 'Zona',
      zona_sel: 'Selecciona Zona',
      poligono: 'Poligono',
      poligono_sel: 'Selecciona Poligono',
      parcela: 'Parcela',
      parcela_sel: 'Selecciona Parcela',
      recinto: 'Recinto',
      recinto_sel: 'Selecciona Recinto',

      parcel_name: 'Nombre de la parcela',
      place_name: 'Nombre...',
      parcel_descrip: 'Descripción de la Parcela',
      place_descrip: 'Descripción...',

      parcel_edit: 'Editar Parcela',
      parcela_solapada_con: 'La parcela se está solapando con',
      parcela_solapada_si: 'La parcela se esta solapando a sí misma',
      parcela_limite: 'Tienes que establecer los límites de la parcela',
      parcela_limite_area: 'Se ha superado el Límite para la edición de parcelas, reduzca el area',
      parcela_guardada: 'Parcela Guardada Correctamente',
      parcela_guardada_2: 'Parcela guardada correctamente. Recargue la pantalla para visualizarla en el mapa.',
      parcel_guardada_error_sent: 'Ha ocurrido un error en la creación de la parcela error: Conexión con Sentinel',
      parcel_nueva: 'Crear Nueva Parcela'
    },
    graficos:{
      grafico_procensandose: 'Tu informe se esta procesando, te enviaremos un mail cuando esté disponible',
      gen_iformes: 'Generación de Informes',
      gen_informes_acceptar: 'Aceptar',
      grafico_tipo_uno: 'Gráfico Tipo 1',
      grafico_tipo_dos: 'Gráfico Tipo 2',
      grafico_ant: 'Gáficos Anteriores',
      enterprise_list: 'Listado de Empresas',
      enterprise_sel: 'Selecciona una Empresa',
      inform_ant_de: 'Informes Anteriores de',
      unificar_informes: 'Unificar Informes',
      editar: 'Editar Nombre',
      ver_datos: 'Ver Datos',
      desc_excel: 'Informe sin imagenes',
      desc_excel_img:'Informe con imagenes',
      del_informe: 'Eliminar Informe',
      grafico_tipo: 'Gráfico tipo',
      eliminar: 'Eliminar',
      seguro: '¿Estás seguro?',
      seguro_parcel_del: '¿Seguro que quieres eliminar el/los Informes/s?',
      cancelar: 'Cancelar',
      parcela: 'Parcela',
      rango_fechas_sel: 'Rango de Fechas Seleccionadas',
      creado: 'Creado',
      analisis_nubes: 'Análisis de Nubes',
      solicitante_informe: 'Solicitante',
      tipo: 'Tipo',
      capa: 'Capa',
      del_informe_ok: 'Informe Eliminado correctamente',
      del_informe_error: 'Ha ocurrido un error con la eliminación del/los informe/s',
      select_one_informe: 'Solo debes seleccionar un Informe',

      gen_grafico_t_one: 'Generar Gráfico Tipo 1',
      ndvi: 'NDVI',
      NDVI: 'NDVI',
      mostisture_index: 'MOISTURE INDEX',
      parcels_de: 'Parcelas de',
      descrip: 'Descripción',
      hectareas: 'Hectáreas',
      puntos: 'Puntos',
      prev_pag: 'Página anterior',
      next_page: 'Página siguente',
      por_pagina: 'Por Página',
      imagen_por_gen: 'Imagenes por Generar:',
      gen_informe: 'Generar Informe',
      sel_layer_sen: 'Selecciona un Layer de Sentinel',
      sent_layers: 'Sentinel Layers',
      fecha_incio: 'Fecha Inicio',
      fecha_fin: 'Fecha Fin',
      parcelas: 'Parcela',
      rang_fechas: 'Rango de Fechas',
      informe_gen_ok: 'Informe generado correctamente',
      informe_gen_error: 'Ha ocurrido un error, intentelo más tarde',
      empresa:'Empresa',
      estado:'Estado del informe',
      nombre_informe: 'Nombre de informe',
      gen_grafico_t_two: 'Generar Gráfico Tipo 2',
      fecha: 'Fecha',
      buscar_nombre: 'Buscar Nombre',
      parcel_list: 'Lista de Parcelas',
      generar: 'Generar',
      nombre: 'Nombre',
      fecha_recogida:'Fecha de recogida',
      fecha_estimada_recogida:'Fecha estimada de recogida',
      grafico_ndvi: 'Gráfico NDVI',
      rojos_altos: 'Rojos Altos',
      rojos_medios: 'Rojos Medios',
      rojos_bajos: 'Rojos Bajos',
      amarillos_altos: 'Amarillos Altos',
      amarillos_medios: 'Amarillos Medios',
      amarillos_bajos: 'Amarillos Bajos',
      azules_altos: 'Azules Altos',
      azules_medios: 'Azules Medios',
      azules_bajos: 'Azules Bajos',
      verdes_medios: 'Verdes Medios',
      verdes_altos: 'Verdes Altos',

      tabla_colores: 'Tabla Colores',
      fecha_nombre: 'Fecha/Nombre',
      fecha_gen: 'Fecha Generación',
      imagen: 'Imagen',
      imagenClouds: 'Imagen Nubes',
      imagenTrueColor: 'Imagen True Color',
      clouds: 'Nubes',
      details: 'Ver detalles',

      grafico_mois: 'Gráfico MOISTURE INDEX',
      rojo_naran: 'Rojo/Naranja',
      amarillo: 'Amarillo',
      verde: 'Verde',
      azul_claro: 'Azul Claro',
      azul_medio: 'Azul Medio',
      azul_oscuro: 'Azul Oscuro',
      imagen_sent: 'Imágenes Sentinel',
      plantas: 'Plantas',
      cosecha: 'Cosecha',

      resumen_unifica: 'Resumen de Unificación',
      unificar: 'Unificar',
      eliminar_informe_origin: 'Eliminar los Informes Originales',

      modifica_infor: 'Modificar Informe',
      guardar: 'Guardar',
    },
    login: {
      email: 'Email',
      password: 'Contraseña',
      login_error: 'Usuario o contraseña inválidos',
      olvidar_pass: 'He olvidado la contraseña',
      login: 'login',
      recordar_contrasena: 'Recordar Contraseña',
      recordar_contrasena_error: 'Debes introducir un correo electrónico',
      introduce_correo: 'Introduce tu correo electrónico',
      recordar: 'Recordar',
      envio_mail: 'Le hemos enviado un email',
      recordar_error: 'No hay un usuario activo asociado con esta dirección de correo electrónico o la contraseña no se puede cambiar',

      reestablecer_pass: 'Reestablecer Contraseña',
      nueva_pass: 'Nueva contraseña',
      confirma_pass: 'Confirmar contraseña',
      reestablecer: 'Reestablecer',
      ir_login: 'Ir al Login',
      pass_no_iguales: 'Las contraseñas no son iguales',
      pass_reestablece: 'Se ha reestablecido la contraseña',
      pass_tiempo_exp: 'Ha expirado el tiempo para resetear la contraseña o ya se ha establecido la contraseña con este enlace'
    },
    adminCoop:{
      nombre: 'Nombre',
      cif: 'CIF',
      direction: 'Dirección',
      listado_coop: 'Listado de Cooperativas',
      add_coop: 'Nueva Cooperativa',
      editar_coop: 'Editar Cooperativa',
      delete_coop: 'Eliminar Cooperativa',
      seguro: '¿Estás seguro?',
      seguro_coop_del: '¿Seguro que quieres eliminar la/las Cooperativa/s?',
      cancelar: 'Cancelar',
      del_coop_ok: 'Se ha eliminado la/s Cooperativa/s correctamente',
      del_coop_ko: 'Ha ocurrido un error con el eliminado',
      eliminar: 'Eliminar',
    },
    newCoop: {
      nueva: 'Nueva Cooperativa',
      nombre: 'Nombre',
      nombrePlace: 'Jonh Doe Coop.',
      direction: 'Dirección',
      directionPlace: 'Amazing Ave.',
      phone: 'Teléfono de la Cooperativa',
      phonePlace: '91000000000',
      cif: 'CIF/Identificación de la Cooperativa',
      cifPlace: 'B819...',
      invalido_blank: 'Este campo es requerido',
      create_coop_success: 'Cooperativa creada correctamente'
    },
    editCoop: {
      title: 'Editar Cooperativa',
      edit_coop_success: 'Cooperativa Guardada correctamente',
      edit_coop_enterprises: 'Empresas de la Cooperativa',
      add_enterprise_coop: 'Editar empresas'

    }
  },
  en: {
    app: {
      monitor: 'Monitor',
      dashboard: 'Dashboard',
      administracion: 'Administration',
      administracion_empresas: 'Business Administration',
      graficos: 'Graphics',
      alertas: 'Alerts',
      perfil: 'Profile',
      desconect: 'Log Out',
      administracion_cooperativas: 'Cooperatives Administration',
      emprise:'Emprise'
    },
    map: {
      most_todas_empresas: 'Show all Parcels',
      sel_empresa: 'Select a Company',
      listado_empresas: 'List of Companies',
      listado_parcelas: 'List of parcels',
      listado_usuarios: 'List of users',
      parcelas_de: 'Parcels of',
      colors: 'Colors',
      fechas_disponibles: 'Available Dates',
      edit_rapido: 'Quick Edit',
      guardar: 'Save',
      cancelar: 'Cancel',
      elimina_parcela: 'Delete Parcel',
      eliminar: 'Delete',
      parcela_nueva: 'New Parcel',
      crear_parcela: 'Create Parcel',
      seguro: 'Are you sure?',
      seguro_parcel_del: 'Are you sure you want to delete the parcel',

      sent_layers: 'Sentinel Layers',
      sent_layers_sel: 'Select a Sentinel Layer',
      fecha: 'Date',
      opacidad: 'Opacity',
      nombre_parcela: 'Parcel name',
      place_nombre_parcela: 'Name ...',
      desc_parcela: 'Description of the Parcel',
      place_desc_parcela: 'Description...',
      parcela_solapada_con: 'The parcel is overlapping with',
      parcela_solapada_misma: 'The parcel is overlapping itself',
      sup_area_parcel: 'The limit for editing parcels has been exceeded, reduce the area',
      establecer_limites_parcela: 'You have to set the parcel limits',
      intro_ubica: 'Enter a location',
      loc_no_disponible: 'The location is not compliant with this device'
    },
    adminEnterprise: {
      listado_empresas: 'List of Companies',
      add_empresa: 'Add new Company',
      eliminar: 'Delete',
      editar: 'Edit',
      seguro: 'Are you sure?',
      seguro_enterprise_del: 'Are you sure you want to delete the company / ies?',
      cancelar: 'Candel',
      nombre: 'Name',
      cif: 'CIF',
      estado: 'Status',
      hectareas_disponibles: 'Available area',
      hectareas_usadas: 'Used area',
      solo_una_empresa: 'You only have to select a company for this action',
      del_empresa_error: 'An error has occurred with the deletion of the company / ies'
    },
    newEnterprise: {
      editar_enterprise: 'Edit Company',
      nueva: 'New Company',
      tel_enterprise: 'Company phone',
      usuarioAdministrador: 'Administrator User',
      guardar: 'Save',
      nombre_enterprise: 'Company Name',
      cif_enterprise: 'Company CIF',
      direccion_enterprise: 'Company Address',
      hectareas_disponible: 'Available Hectares',
      tipo_Metrica: 'Type of metrics',
      campo_requerido: 'This field is required',
      save_enterprise: 'Company Saved Successfully',
    },
    empleados: {
      empleados_lista: 'Employees List',
      add: 'Add',
      eliminar: 'Delete',
      editar: 'Edit',
      seguro: 'Are you sure?',
      seguro_user_del: 'Are you sure you want to delete the user / s?',
      cancelar: 'Cancel',
      nombre: 'Name',
      apellido: 'Surname',
      telefono: 'Phone',
      desarrollo: 'In development',
      un_user_selec: 'You only have to select a user for this action',
      user_error: 'An error occurred with the deletion of users',

      guardar: 'Save',
      admin_enterprise: 'Company administrator',
      empleado_enterprise: 'Employee',
      select_row: 'You must select a role',
      rol: 'User Role',
      password: 'Password',
      user_name: 'Username',
      user_lastname: 'User last name / s',
      user_email: 'Email',
      user_phone: 'Phone Number',

      user_edit: 'Edit user',
      user_new: 'New User',
      campo_requerido: 'This field is required',
      user_generado: 'User Generated Correctly, We have sent you an email',
      user_guardado: 'User Saved Correctly',
      perfil_guardado: 'Profile Saved Correctly',

      label_lang: 'Language',
      esp: 'Spanish',
      eng: 'English',
      edit_perfil: 'Edit Profile'
    },
    parcelas: {
      parcel_list: 'List of Parcels',
      place_buscar: 'Search Name',
      place_nuevo: 'Add new',
      eliminar: 'Delete',
      editar: 'Edit',
      seguro: 'Are you sure?',
      seguro_parcel_del: 'Are you sure you want to delete the parcel / s?',
      cancelar: 'Cancel',

      nombre: 'Name',
      descrip: 'Description',
      hectareas: 'Area',
      puntos: 'Points',
      desarrollo: 'In development',
      parcel_limit: 'The limit for creating new parcels has been exceeded',
      parcel_sel_alert: 'You only have to select a parcel for this action',
      parcel_del_error: 'An error occurred with the removal of parcels',
      guardar: 'Save',
      sigpac_pro: 'SIGPAC Progressive',
      sigpac_direc: 'SIGPAC Direct',
      sigpac_error: 'Search Error',
      buscar: 'Search',
      ubicacion: 'Enter a location',

      comunidad: 'Community',
      comunidad_sel: 'Select Community',
      provincia: 'Province',
      provincia_sel: 'Select Province',
      municipio: 'Municipality',
      municipio_sel: 'Select Municipality',
      agregado: 'Added',
      agregado_sel: 'Select Aggregate',
      zona: 'Zone',
      zona_sel: 'Select Zone',
      poligono: 'Polygon',
      poligono_sel: 'Select Polygon',
      parcela: 'Parcel',
      parcela_sel: 'Select Parcel',
      recinto: 'Enclosure',
      recinto_sel: 'Select Enclosure',

      parcel_name: 'Parcel name',
      place_name: 'Name...',
      parcel_descrip: 'Description of the Parcel',
      place_descrip: 'Description...',

      parcel_edit: 'Edit Parcel',
      parcela_solapada_con: 'The parcel is overlapping with',
      parcela_solapada_si: 'The parcel is overlapping itself',
      parcela_limite: 'You have to set the boundaries of the parcel',
      parcela_limite_area: 'The limit for the edition of parcels has been exceeded, reduce the area',
      parcela_guardada: 'Parcel Saved Correctly',
      parcela_guardada_2: 'Parcel saved correctly. Please reload the website to view the new parcel in the map.',
      parcel_guardada_error_sent: 'An error occurred in the creation of the parcel error: Connection with Sentinel',
      parcel_nueva: 'Create New Parcel'
    },
    graficos:{
      grafico_procensandose: 'Your report is being processed, we will send you an email when it is generated',
      gen_iformes: 'Report generation',
      gen_informes_acceptar: 'Accept',
      grafico_tipo_uno: 'Graph Type 1',
      grafico_tipo_dos: 'Graph Type 2',
      grafico_ant: 'Previous Graphics',
      enterprise_list: 'List of Companies',
      enterprise_sel: 'Select a Company',
      inform_ant_de: 'Previous Reports of',
      unificar_informes: 'Unify Reports',
      editar: 'Edit Name',
      ver_datos: 'View Data',
      desc_excel: 'Report without images',
      desc_excel_img: 'Report with images',
      del_informe: 'Delete Report',
      grafico_tipo: 'Graph type',
      eliminar: 'Delete',
      seguro: 'Are you sure?',
      seguro_parcel_del: 'Are you sure you want to delete the Report / s?',
      cancelar: 'Cancel',
      parcela: 'Parcel',
      rango_fechas_sel: 'Range of Selected Dates',
      analisis_nubes: 'Cloud analysis',
      solicitante_informe: 'Requester',
      creado: 'Created',
      tipo: 'Type',
      capa: 'Layer',
      del_informe_ok: 'Report Deleted successfully',
      del_informe_error: 'An error has occurred with the deletion of the report (s',
      select_one_informe: 'You should only select a Report',
      empresa:'Enterprise',
      gen_grafico_t_one: 'Generate Type 1 Chart',
      ndvi: 'NDVI',
      NDVI: 'NDVI',
      mostisture_index: 'MOISTURE INDEX',
      parcels_de: 'Parcels of',
      descrip: 'Description',
      hectareas: 'Hectares',
      prev_pag: 'Previous page',
      next_page: 'Next page',
      por_pagina: 'Per Page',
      imagen_por_gen: 'Images to Generate:',
      gen_informe: 'Generate Report',
      sel_layer_sen: 'Select a Sentinel Layer',
      sent_layers: 'Sentinel Layers',
      fecha_incio: 'Start date',
      fecha_fin: 'End date',
      parcelas: 'Parcel',
      rang_fechas: 'Date Range',
      informe_gen_ok: 'Report generated successfully',
      informe_gen_error: 'An error has occurred, please try again later',
      estado:'Report status',
      nombre_informe: 'Report name',
      gen_grafico_t_two: 'Generate Type 2 Chart',
      fecha: 'Date',
      buscar_nombre: 'Search Name',
      parcel_list: 'List of Parcels',
      generar: 'Generate',
      nombre: 'Name',
      fecha_recogida:'Picking date',
      fecha_estimada_recogida:'Estimated picking date',
      grafico_ndvi: 'NDVI graph',
      rojos_altos: 'Tall Reds',
      rojos_medios: 'Medium Reds',
      rojos_bajos: 'Low Reds',
      amarillos_altos: 'Tall Yellows',
      amarillos_medios: 'Medium Yellows',
      amarillos_bajos: 'Low Yellows',
      azules_altos: 'Tall Blues',
      azules_medios: 'Medium Blue',
      azules_bajos: 'Low Blues',
      verdes_medios: 'Medium green',
      verdes_altos: 'Verdes Altos',

      tabla_colores: 'Table Colors',
      fecha_nombre: 'Date / Name',
      fecha_gen: 'Generation Date',
      imagen: 'Image',
      imagenClouds: 'Image Clouds',
      imagenTrueColor: 'Image True Color',
      clouds: 'Clouds',
      details: 'See details',

      grafico_mois: 'Chart MOISTURE INDEX',
      rojo_naran: 'Red / Orange',
      amarillo: 'Yellow',
      verde: 'Green',
      azul_claro: 'Light Blue',
      azul_medio: 'Medium Blue',
      azul_oscuro: 'Dark Blue',
      imagen_sent: 'Sentinel Images',
      plantas: 'Plants',
      cosecha: 'Harvest',

      resumen_unifica: 'Summary of Unification',
      unificar: 'Unify',
      eliminar_informe_origin: 'Delete Original Reports',

      modifica_infor: 'Modify Report',
      guardar: 'Save',
    },
    login:{
      email: 'Email',
      password: 'Password',
      login_error: 'Invalid username or password',
      olvidar_pass: 'I have forgotten the password',
      login: 'login',
      recordar_contrasena: 'Remember Password',
      recordar_contrasena_error: 'You must enter an email',
      introduce_correo: 'Enter your email',
      recordar: 'Remember',
      envio_mail: 'We have sent you an email',
      recordar_error: 'There is no active user associated with this email address or the password cannot be changed',

      reestablecer_pass: ''
    },
    adminCoop:{
      nombre: 'Name',
      cif: 'CIF',
      direction: 'Direction',
      listado_coop: 'List of Cooperatives',
      add_coop: 'New Cooperative',
      editar_coop: 'Edit Cooperative',
      delete_coop: 'Delete Cooperativa',
      seguro: 'Are you sure?',
      seguro_coop_del: 'Are you sure you want to delete the Cooperative / s?',
      cancelar: 'Cancel',
      del_coop_ok: 'The Cooperativa / s has been deleted successfully',
      del_coop_ko: 'An error occurred with the deleted one',
      eliminar: 'Delete',
    },
    newCoop: {
      nueva: 'New Cooperative',
      nombre: 'Name',
      nombrePlace: 'Jonh Doe Coop.',
      direction: 'Direction',
      directionPlace: 'Amazing Ave.',
      phone: 'Cooperativa telephone',
      phonePlace: '91000000000',
      cif: 'CIF / Identification of the Cooperative',
      cifPlace: 'B819...',
      invalido_blank: 'This field is required',
      create_coop_success: 'Cooperative created successfully'
    },
    editCoop: {
      title: 'Edit Cooperative',
      edit_coop_success: 'Cooperative Saved successfully',
      edit_coop_enterprises: 'Cooperative Companies',
      add_enterprise_coop: 'Edit companies'

    }
  }
}
Vue.prototype.$locale_lang = 'es'
const i18n = new VueI18n({
  locale: Vue.prototype.$locale_lang, // set locale
  messages, // set locale messages
})


new Vue({
  router,
  i18n,
  render: h => h(App)
}).$mount('#app')
