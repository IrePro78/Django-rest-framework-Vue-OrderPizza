<template>
  <div class="container mt-5">
    <h1 class="title">Edit profile</h1>
    <hr>
    <div class="columns ">
      <div class="column is-4 is-offset-1">

        <form @submit.prevent="changeUsername">
          <div class="field">
            <label>Change username</label>
            <div class="field ">
              <p class="control has-icons-left">
                <input type="text" name="username" class="input" v-model="username">
                <span class="icon is-small is-left">
                  <i class="fas fa-user"></i>
                </span>
              </p>
            </div>
            <br>
            <div class="field">
              <p class="control has-icons-left">
                <input class="input" type="password" placeholder="please enter your current password" name="password"
                       v-model="password">
                <span class="icon is-small is-left">
                  <i class="fas fa-lock"></i>
                </span>
              </p>
            </div>
          </div>
          <div class="notification is-danger" v-if="errors1.length">
            <p v-for="error_username in errors1" v-bind:key="error_username">{{ error_username }}</p>
          </div>
          <div class="field">
            <div class="control">
              <button class="button is-success">Submit</button>
            </div>
          </div>
        </form>

        <form @submit.prevent="changeEmail">
          <div class="field mt-4">
            <label>Change email</label>
            <div class="field">
              <p class="control has-icons-left">
                <input type="email" name="email" class="input" v-model="email">
                <span class="icon is-small is-left">
                  <i class="fas fa-envelope"></i>
               </span>
              </p>
            </div>
          </div>
          <div class="notification is-danger" v-if="errors2.length">
            <p v-for="error_email in errors2" v-bind:key="error_email">{{ error_email }}</p>
          </div>
          <div class="field">
            <div class="control">
              <button class="button is-success">Submit</button>
            </div>
          </div>
        </form>
      </div>

      <div class="column is-4 is-offset-2">
        <form @submit.prevent="changePassword">
          <div class="field">
            <label>Change password</label>
            <div class="field">
              <p class="control has-icons-left">
                <input class="input" type="password" placeholder="please enter your current password" name="current_password"
                       v-model="current_password">
                <span class="icon is-small is-left">
                  <i class="fas fa-lock"></i>
                </span>
              </p>
            </div>
            <br>
            <div class="field">
              <p class="control has-icons-left">
                <input class="input" type="password" placeholder="please enter your new password" name="new_password"
                       v-model="new_password">
                <span class="icon is-small is-left">
                  <i class="fas fa-lock"></i>
                </span>
              </p>
            </div>
          </div>
          <div class="notification is-danger" v-if="errors3.length">
            <p v-for="error_username in errors3" v-bind:key="error_username">{{ error_username }}</p>
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
import axios from "axios";
import {toast} from "bulma-toast";

export default {
  name: "EditProfile",
  data() {
    return {
      username: '',
      email: '',
      password: '',
      current_password: '',
      new_password: '',
      errors1: [],
      errors2: [],
      errors3: [],
    }
  },
  mounted() {
    this.getUserDetails()
  },
  methods: {
    async changeEmail() {
      this.errors2 = []
      if (this.email === '') {
        this.errors2.push('The email address is missing')
      }
      if (this.email === this.$store.state.user.email) {
        this.errors2.push('The new email is the same')
      }
      if (!this.errors2.length) {
        this.$store.commit('setIsLoading', true)
        const email = {
          email: this.email
        }
        await axios
            .patch('/api/v1/users/me/', email)
            .then(response => {
              console.log(response)
              toast({
                message: 'The address email was updated',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
              })
              this.$store.commit('setUser', {
                'userid': response.data.id,
                'username': response.data.username,
                'email': response.data.email,
              })
              localStorage.setItem('email', this.email)
            })
            .catch(error => {
              console.log(error)
            })
        this.$store.commit('setIsLoading', false)
      }
    },

    async changeUsername() {
      this.errors1 = []
      if (this.username === '') {
        this.errors1.push('The username is missing')
      }
      if (this.username === this.$store.state.user.username) {
        this.errors1.push('The new username is the same')
      }
      if (!this.errors1.length) {
        this.$store.commit('setIsLoading', true)
        const username = {
          new_username: this.username,
          current_password: this.password
        }
        await axios
            .post('/api/v1/users/set_username/', username)
            .then(response => {
              toast({
                message: 'The username was updated',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
              })
              console.log(response)
              this.password = ''
              this.$store.commit('setUser', {
                'userid': localStorage.getItem('userid'),
                'username': this.username,
                'email': localStorage.getItem('email'),
              })
              localStorage.setItem('username', this.username)
            })
            .catch(error => {
              console.log(error)
              this.password = ''
              if (error.response.status === 400) {
                toast({
                  message: 'Please enter the correct password',
                  type: 'is-danger',
                  dismissible: true,
                  pauseOnHover: true,
                  duration: 2000,
                  position: 'center',
                })
              }
            })
        this.$store.commit('setIsLoading', false)
      }
    },
    async changePassword() {
      this.errors3 = []
      if (this.current_password === '') {
        this.errors3.push('The current password is missing')
      }
      if (this.new_password === '') {
        this.errors3.push('The new password is missing')
      }
      if (this.new_password.length < 8) {
        this.errors3.push('The password is too short')
      }
      if (this.current_password === this.new_password) {
        this.errors3.push('The new password is the same')
      }
      if (!this.errors3.length) {
        this.$store.commit('setIsLoading', true)
        const formData = {
          current_password: this.current_password,
          new_password: this.new_password
        }
        console.log(formData)
        await axios
            .post('/api/v1/users/set_password/', formData)
            .then(response => {
              console.log(response.data, 'Password changed')

              toast({
                message: 'Password was changed, please log in again',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
              })
              this.$router.push('/log-out')
              this.$router.push('/log-in')
            })
            .catch(error => {
              if (error.response.status === 400) {
                this.password = ''
                toast({
                  message: 'The current password is incorrect',
                  type: 'is-danger',
                  dismissible: true,
                  pauseOnHover: true,
                  duration: 2000,
                  position: 'bottom-right',
                })
              }
              console.log(error)
            })
        this.$store.commit('setIsLoading', false)
      }
    },
    async getUserDetails() {
      this.$store.commit('setIsLoading', true)
      this.username = this.$store.state.user.username
      this.email = this.$store.state.user.email
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>

<style scoped>
</style>