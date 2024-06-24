<template>
  <div class="bx--grid" @mousedown="keepPositionScroll" @mouseup="putPositionScroll">
    <div class="employee-list">
      <cv-data-table
        :sortable="sortable"
        :columns="columns3"
        @sort="onSort"
        :title="$t('empleados.empleados_lista')"
        ref="table"
      >
        <template v-if="true" slot="actions">
          <cv-button small @click="actionNew">{{$t("empleados.add")}}</cv-button>
        </template>
        <template v-if="use_batchActions" slot="batch-actions">
          <cv-button @click="onBatchAction1">
            {{$t("empleados.eliminar")}}
            <TrashCan32 class="bx--btn__icon" />
          </cv-button>
          <cv-button @click="onBatchAction2">
            {{$t("empleados.editar")}}
            <Edit32 class="bx--btn__icon" />
          </cv-button>
          <cv-button @click="onBatchAction3" v-if="false">
            Descargar
            <Download16 class="bx--btn__icon" />
          </cv-button>
        </template>
        <template slot="data">
          <cv-data-table-row
            v-for="usuario in usuarios"
            :key="`${usuario.id}`"
            :value="`${usuario.id}`"
            :aria-label-for-batch-checkbox="`Custom aria label for row ${usuario.id} batch`"
          >
            <cv-data-table-cell>{{usuario.id}}</cv-data-table-cell>
            <cv-data-table-cell>{{usuario.name}}</cv-data-table-cell>
            <cv-data-table-cell>{{usuario.email}}</cv-data-table-cell>
            <cv-data-table-cell>{{usuario.phone}}</cv-data-table-cell>
          </cv-data-table-row>
        </template>
      </cv-data-table>
      <EditarUser ref="modal" :userSeleccionado="userSeleccionado" />
      <Alertas :tituloAlert="mensajeAlerta" ref="alerta" />
      <cv-modal
      ref="alerta_eliminar"
      kind="danger"
      :visible="visibleAlertaEliminar"
      @primary-click="actionPrimary">
        <template slot="label">{{$t("empleados.seguro")}}</template>
        <template slot="title">{{$t("empleados.eliminar")}}</template>
        <template slot="content">
          <p>{{$t("empleados.seguro_user_del")}}</p>
        </template>
        <template slot="secondary-button">{{$t("empleados.cancelar")}}</template>
        <template slot="primary-button">{{$t("empleados.eliminar")}}</template>
      </cv-modal>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Alertas from "../components/Alertas.vue";
import EditarUser from "../components/EditarUser.vue";
export default {
  name: "EmployeesList",
  props: {},
  components: {
    Alertas,
    EditarUser
  },
  data() {
    return {
      sortable: false,
      columns3: [
        {
          key: "id",
          label: "ID"
        },
        {
          key: "name",
          label: "Nombre"
        },
        {
          key: "email",
          label: "Correo"
        },
        {
          key: "phone",
          label: "Teléfono"
        },
        
      ],
      usuarios: [],
      basicPagination: false,
      use_batchActions: true,
      hasExpandingRows: false,
      use_slottedData: true,
      mensajeAlerta: "", 
      userSeleccionado: '',
      visibleAlertaEliminar: false,
      scrollPosition: 0
    };
  },
  methods: {
    keepPositionScroll(){
            this.scrollPosition = window.scrollY;
        },
    putPositionScroll(){
        setTimeout(() => {
            window.scrollTo(0, this.scrollPosition);
        }, 0);
    },
    getUsers() {
      const path = "${this.$apiURL}/employees/";
      axios
        .get(path)
        .then(response => {
          
          this.usuarios = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    onSort(order) {
      console.log(order.order);
    },
    onBatchAction2() {
      const rowSeleccionado = this.$refs.table.selectedRows;
      if (rowSeleccionado.length > 1) {
        this.mensajeAlerta =
          "Solo tienes que seleccionar un usuario para esta acción";
        this.$refs.alerta.verAlerta()
      } else {
        this.userSeleccionado = rowSeleccionado[0]
        this.$refs.modal.openModal(this.userSeleccionado)
      }
    },
    onBatchAction1(){
      
      this.$refs.alerta_eliminar.dataVisible = true
      console.warn(this.$refs.alerta_eliminar.dataVisible)
      
    },
    actionPrimary(){
      
      const rowSeleccionado = this.$refs.table.selectedRows
      let flag = false
      rowSeleccionado.forEach(element => {
        console.log(element)
        const path = `${this.$apiURL}/employees/${element}/`
        axios
          .delete(path)
          .then(() => {
            this.getUsers();
          })
          .catch(response =>{
            flag = true
            console.log(response.error)
          });
      });
      if(flag){
        console.error('error')
        this.mensajeAlerta = "Ha ocurrido un error con la eliminación de los usuarios";
        this.$refs.alerta.verAlerta()
      }else{
        this.$refs.alerta_eliminar.hide()
      }
      
    },
    doClose() {
      this.visibleAlerta = false;
    },
    actionNew(){
      this.$refs.modal.openModal()
    }
  },
  created() {
    this.getUsers();
  },
  mounted(){
    const path_lang = `${this.$apiURL}/profiledata/${this.$session.get('user')}/`;
        axios.defaults.headers.common['Authorization'] = "Bearer "+sessionStorage.getItem("apiAccess")
        axios
        .get(path_lang)
        .then(response =>{
            this.$root.$i18n.locale = response.data.language
        })
  }
};
</script>
<style scoped>
</style>