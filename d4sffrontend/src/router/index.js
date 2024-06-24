import Vue from 'vue'
import VueRouter from 'vue-router'
//import Home from '../views/Home.vue'
import EmployeeList from '../views/EmployeeList.vue'
import GroupList from '../views/GroupList.vue'
import RolList from '../views/RolList.vue'
import Administracion from '../views/Administracion.vue'
import ParcelasList from '../views/ParcelsList.vue'
import MapView from '../views/Map.vue'
import Login from '../views/Login.vue'
//import Charts from '../views/Charts.vue'
import AdminEnterprises from '../views/AdminEnterprises.vue'
import AdminUsers from '../views/AdminUsers.vue'
import EditarEmpresa from '../views/EditarEmpresa.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import AdminCooperatives from '../views/AdminCooperatives.vue'
import EditCooperative from '../views/EditCooperative.vue'
import ParcelsToSentinel from '../views/ParcelsToSentinel.vue'
import SentinelInstancesRefreshParcels from '../views/SentinelInstancesRefreshParcels.vue'
import GenGraficos from '../views/GenGraficos.vue'
import GenGraficosAnteriores from '../views/GenGraficosAnteriores.vue'
import GraficosAnt from '../views/GraficosAnt.vue'
import Monitor from '../views/monitor/Monitor.vue'
import ImportParcels from '../views/importParcels/ImportParcels.vue'
import ImportParcelsKML from '../views/importParcels/ImportParcelsKML.vue'
import ImportHitParcelsKML from '../views/importParcels/importparcelsHitfromfileKML.vue'
import ImportParcelsGeoJSON from '../views/importParcels/ImportParcelsGeoJSON.vue'
import ImportCampana from '../views/importCampana/ImportCampana.vue'
import ActualizarMonitor from '../views/monitor/ActualizarMonitor.vue'

import ParcelsToCheckHas from '../views/ParcelsToCheckHas'

import {getProfile, getPermisos} from '../auth/index'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'index',
    component: MapView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/parcelstosent',
    name: 'parcelstosent',
    component: ParcelsToSentinel,
    meta: {
      requiresAuth: true,
      is_admin: true
    }
  },
  {
    path: '/parcelstocheckhas',
    name: 'parcelstocheckhas',
    component: ParcelsToCheckHas,
    meta: {
      requiresAuth: true,
      is_admin: true
    }
  },
  {
    path: '/sentinelinstancesrefresh',
    name: 'sentinelinstancesrefresh',
    component: SentinelInstancesRefreshParcels,
    meta: {
      requiresAuth: true,
      is_admin: true
    }
  },
  {
    path: '/gengraficosnew',
    name: 'gengraficosnew',
    component: GenGraficos,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/monitor',
    name: 'monitor',
    component: Monitor,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/importparcelsfromfile',
    name: 'importparcelsfromfile',
    component: ImportParcels,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/importparcelsfromfileKML',
    name: 'importparcelsfromfileKML',
    component: ImportParcelsKML,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/importparcelsHitfromfileKML',
    name: 'importparcelsHitfromfileKML',
    component: ImportHitParcelsKML,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/importparcelsfromGeoJSON',
    name: 'importparcelsfromGeoJSON',
    component: ImportParcelsGeoJSON,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/importcampanafromfile',
    name: 'importcampanafromfile',
    component: ImportCampana,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/actualizarMonitor',
    name: 'actualizarMonitor',
    component: ActualizarMonitor,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/gengraficosanterioresnew',
    name: 'gengraficosanterioresnew',
    component: GenGraficosAnteriores,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/employees',
    name: 'Employees',
    component: EmployeeList,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/groups',
    name: 'Groups',
    component: GroupList,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/roles',
    name: 'Roles',
    component: RolList,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/administracion',
    name: 'Administracion',
    component: Administracion,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/parcelas',
    name: 'Parcels',
    component: ParcelasList,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/map',
    name: 'Map',
    component: MapView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/chart',
    name: 'Charts',
    component: GraficosAnt,
    meta: {
      requiresAuth: true,
      is_admin: true
    }
  },
  {
    path: '/admin-enterprises',
    name: 'AdminEnterprises',
    component: AdminEnterprises,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/admin-users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/edit-enterprise',
    name: 'EditarEmpresa',
    component: EditarEmpresa,
    meta: {
      requiresAuth: true,
    }
  },
  
  {
    path: '/reset_password',
    name: 'ResetPasswordView',
    component: ResetPasswordView,
    meta: {
      requiresAuth: false,
    }
  },
  {
    path: '/admin-cooperatives',
    name: 'AdminCooperatives',
    component: AdminCooperatives,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/edit-cooperative',
    name: 'EditCooperative',
    component: EditCooperative,
    meta: {
      requiresAuth: true,
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  to.matched.some(record => record.meta.requiresAuth)
  if(to.matched.some(record => record.meta.requiresAuth)) {
      if (sessionStorage.getItem('apiAccess') == null) {
          next({
              path: '/login',
              params: { nextUrl: to.fullPath }
          })
      } else {
          getProfile()
          .then(response => {
            getPermisos(response.data[0].user)
            .then(response => {
              if(to.matched.some(record => record.meta.is_admin)) {
                if(response.data.is_superuser == 1){
                    next()
                }
                else{
                    next({ name: '/'})
                }
              }else {
                next()
              }
            })
          })
      }
  } else if(to.matched.some(record => record.meta.guest)) {
      if(localStorage.getItem('apiAccess') == null){
          next()
      }
      else{
          next({ name: 'index'})
      }
  }else {
   
      next()
  }
})

export default router
