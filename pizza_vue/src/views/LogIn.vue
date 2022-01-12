<template>
  <div class="container mt-5">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log in</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Name</label>
            <div class="control">
              <input type="text" name="username" class="input" v-model="username">
            </div>
          </div>

          <div class="field">
            <label>Password</label>
            <div class="control">
              <input type="***REMOVED***" name="***REMOVED***" class="input" v-model="***REMOVED***">
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-success">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'LogIn',
  data() {
    return {
      username: '',
      ***REMOVED***: '',
      errors: []
    }
  },
  methods: {
    async submitForm() {
      this.$store.commit('setIsLoading', true)
      axios.defaults.headers.common['Authorization'] = ''
      localStorage.removeItem('token')
      const formData = {
        username: this.username,
        ***REMOVED***: this.***REMOVED***
      }
      await axios
          .post('/api/v1/auth/token/login/', formData)
          .then(response => {
            const token = response.data.auth_token
            this.$store.commit('setToken', token)
            axios.defaults.headers.common['Authorization'] = 'Token ' + token
            localStorage.setItem('token', token)
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }
            } else if (error.message) {
              this.errors.push('Something went wrong. Please try again!')
            }
          })
      await axios
          .get('/api/v1/users/me/')
          .then(response => {
            this.$store.commit('setUser', {
              'userid': response.data.id,
              'username': response.data.username,
              'email': response.data.email,
              'date_joined': response.data.date_joined,
            })
            localStorage.setItem('username', response.data.username)
            localStorage.setItem('userid', response.data.id)
            localStorage.setItem('email', response.data.email)
            localStorage.setItem('date_joined', response.data.date_joined)
            this.$router.push('/my-account')
          })
          .catch(error => {
            console.log(error)
          })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>