<template>
    <div class="Administracion">
        <EmployeeList />
        <br/>
        <GroupList />
        <br/>
        <RolList />
    </div>
</template>

<script>
// @ is an alias to /src
import EmployeeList from '@/views/EmployeeList.vue'
import GroupList from '@/views/GroupList.vue'
import RolList from '@/views/RolList.vue'

export default {
    name: 'Home',
    components: {
        EmployeeList,
        GroupList,
        RolList
    }
}
</script>