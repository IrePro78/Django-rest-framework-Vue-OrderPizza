<template>

</template>

<script>
import axios from "axios"
export default {
  name: "LogOut",
  mounted() {
    this.logout()
  },
  methods: {
    async logout() {
      await axios
      .post('/api/v1/token/logout/')
      .then(response => {
        console.log(response, 'Logged out')
      })
      .catch(error => {
        console.log(JSON.stringify(error))
      })
      axios.defaults.headers.common['Authorization'] = ''

      localStorage.removeItem('token')
      localStorage.removeItem('userid')
      localStorage.removeItem('username')

      this.$store.commit('removeToken')

      await this.$router.push('/')
    }
  }
}
</script>
