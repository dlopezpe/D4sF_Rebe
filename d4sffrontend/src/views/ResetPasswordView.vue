<template>
  <div class="ResetPassView">
    <ResetPasswordComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import ResetPasswordComponent from '@/components/ResetPasswordComponent.vue'

export default {
    name: 'ResetPasswordView',
    components: {
        ResetPasswordComponent
    }
}
</script>