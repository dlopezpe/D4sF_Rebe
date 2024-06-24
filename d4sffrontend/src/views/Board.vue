<template>
    <div>
        <cv-header aria-label="Carbon header" id="top-menu">
            <cv-header-menu-button aria-label="Header menu" aria-controls="side-nav" />
            <cv-skip-to-content href="#main-content">
            </cv-skip-to-content>
            <cv-header-name prefix="" to="/"><img alt="Vue logo" src="../assets/logo-cabecera.png"></cv-header-name>
            <cv-header-nav aria-label="Carbon nav">
                <cv-header-menu-item to="/map">{{$t("app.dashboard")}}</cv-header-menu-item>
                <cv-header-menu :aria-label="$t('app.administracion')" :title="$t('app.administracion')" v-if="is_superuser || is_systemadmin|| is_enterpriseadmin">
                    <cv-header-menu-item to="/admin-enterprises" v-if="is_superuser || is_systemadmin" >{{$t("app.administracion_empresas")}}</cv-header-menu-item>
                    <cv-header-menu-item to="/admin-users" v-if="is_superuser || is_systemadmin" >{{$t("app.administracion_usuarios")}}</cv-header-menu-item>
                    <cv-header-menu-item :to="customLinkEnterprise" v-else-if="is_enterpriseadmin && !is_coop_user" >{{$t("app.administracion_empresas")}}</cv-header-menu-item>
                    <cv-header-menu-item :to="customLinkCoop" v-else-if="is_enterpriseadmin && is_coop_user" >{{$t("app.administracion_cooperativas")}}</cv-header-menu-item>
                    <cv-header-menu-item to="/admin-cooperatives" v-if="is_superuser || is_systemadmin">{{$t("app.administracion_cooperativas")}}</cv-header-menu-item>
                </cv-header-menu>
                <!--<cv-header-menu-item to="/chart" v-if="is_superuser || is_systemadmin || is_enterpriseadmin">{{$t("app.graficos")}}</cv-header-menu-item>-->

                <cv-header-menu :aria-label="`SuperAdm Acciones`" :title="`SuperAdm Acciones`" v-if="is_superuser">
                    <cv-header-menu-item to="/importparcelsfromfile" v-if="is_superuser" >Importar Parcelas desde Archivo</cv-header-menu-item>
                    <cv-header-menu-item to="/importparcelsfromfileKML" v-if="is_superuser" >Importar Parcelas desde Archivo KML/KMZ</cv-header-menu-item>
                    <cv-header-menu-item to="/importparcelsHitfromfileKML" v-if="is_superuser" >Importar Parcelas desde Archivo KML/KMZ (empresa Hit)</cv-header-menu-item>
                    <cv-header-menu-item to="/importparcelsfromGeoJSON" v-if="is_superuser" >Importar Parcelas desde Archivo GeoJSON</cv-header-menu-item>
                    <cv-header-menu-item to="/parcelstosent" v-if="is_superuser" >Parcelas 2 Sentinel</cv-header-menu-item>
                    <cv-header-menu-item to="/sentinelinstancesrefresh" v-if="is_superuser" >Refresh Instances Parcels</cv-header-menu-item>
                    <cv-header-menu-item to="/gengraficosnew" v-if="is_superuser" >Nuevo Generador de Gráficos</cv-header-menu-item>
                    <cv-header-menu-item to="/gengraficosanterioresnew" v-if="is_superuser" >Nuevo Gráficos Anteriores</cv-header-menu-item>
                    <cv-header-menu-item to="/parcelstocheckhas" v-if="is_superuser" >Comprobar Has Parcelas</cv-header-menu-item>
                    <cv-header-menu-item to="/parcelstocheckhas" v-if="is_superuser" >Importar Parcelas desde Archivo</cv-header-menu-item>
                    <cv-header-menu-item to="/importcampanafromfile" v-if="is_superuser" >Importar Campaña desde Archivo</cv-header-menu-item>
                    
                </cv-header-menu>

                <cv-header-menu :aria-label="`Monitor`" :title="`Monitor`">
                    <cv-header-menu-item to="/monitor">Evolución de cultivo (Monitor)</cv-header-menu-item>    
                    <cv-header-menu-item to="/actualizarMonitor">Actualizar Monitor</cv-header-menu-item> 
                </cv-header-menu>

                <!-- <cv-header-menu-item to="/monitor" v-if="is_superuser  || is_systemadmin">{{$t("app.monitor")}}</cv-header-menu-item> -->

                <cv-header-menu :aria-label="`Informes`" :title="`Informes`" v-if="is_superuser || is_systemadmin || is_enterpriseadmin">
                    <cv-header-menu-item to="/gengraficosnew" v-if="is_superuser || is_systemadmin || is_enterpriseadmin">Generar Informe</cv-header-menu-item>
                    <cv-header-menu-item to="/gengraficosanterioresnew" v-if="is_superuser || is_systemadmin || is_enterpriseadmin">Informes Anteriores</cv-header-menu-item>
                </cv-header-menu>

            </cv-header-nav>
            <template slot="header-global">
                <cv-header-global-action aria-label="User avatar" :title="$t('app.perfil')" @click="editarPerfil" aria-controls="user-panel">
                    <UserAvatarFilledAlt20 />
                </cv-header-global-action>
                <cv-header-global-action aria-label="Logout" :title="$t('app.desconect')" @click="logOut" aria-controls="user-panel">
                    <Logout20 />
                </cv-header-global-action>
            </template>
        </cv-header>
        <EditarPerfil ref="editarPerfil"/>
    </div>
</template>
<script>
import EditarPerfil from "@/components/EditarPerfil";
import {getProfile, getPermisos} from '@/auth/index'
export default {
    name: 'Board',
    data() {
        return {
            is_superuser: false,
            is_staff: false,
            is_systemadmin: false,
            is_enterpriseadmin: false,
            is_coop_user: false,
            customLinkEnterprise: '',
            customLinkCoop: ''
        }
    },
    components: {
        EditarPerfil
    },
    methods: {
        editarPerfil(){
            this.$refs.editarPerfil.openModal()
        },
        logOut(){
            sessionStorage.removeItem("apiAccess");
            sessionStorage.removeItem("email");
            this.$session.destroy()
            this.$router.push("/login");
        }
    },
    mounted: function () {
        
        //console.info('User Logged')
    },
    beforeCreate(){
        getProfile()
        .then(response => {
            const user = response.data[0]
            this.customLinkEnterprise = `edit-enterprise?enterprise=${user.enterprise_id}`
            if(user.cooperative_user){
                this.customLinkCoop = `edit-cooperative?cooperative=${user.enterprise_id}`
            }
            getPermisos(response.data[0].user)
            .then(response => {
                this.is_superuser = response.data.is_superuser
                this.is_staff = response.data.is_staff
                this.is_systemadmin = response.data.is_systemadmin
                this.is_enterpriseadmin = response.data.is_enterpriseadmin
                this.is_coop_user = user.cooperative_user
            })
        })
    }
}
</script>
<style>
#nav {
    padding: 17px;
}

#nav a {
    font-weight: bold;
    color: #2c3e50;
}
#top-menu > nav > ul > li:nth-child(4) > ul,#top-menu > nav > ul > li:nth-child(3) > ul, #top-menu > nav > ul > li:nth-child(2) > ul{
    width:auto
}
#nav a.router-link-exact-active {
    color: #42b983;
}
#top-menu{
    position: static;
}
</style>