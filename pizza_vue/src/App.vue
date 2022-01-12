<!--<template>-->
<!--  <div id="nav">-->
<!--    <router-link to="/">Home</router-link> |-->
<!--    <router-link to="/about">About</router-link>-->
<!--  </div>-->
<!--  <router-view/>-->
<!--</template>-->

<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Pizza Ordering</strong></router-link>
      </div>

      <div class="navbar-menu">
        <div class="navbar-end">
          <template v-if="false">
            <router-link to="/menu" class="navbar-item">Menu</router-link>
            <router-link to="/sale" class="navbar-item">Sale</router-link>
            <router-link to="/delivery" class="navbar-item">Delivery</router-link>
            <router-link to="/orders/add" class="navbar-item">Order</router-link>
            <router-link to="/my-account" class="navbar-item">My account</router-link>

          </template>

          <template v-else>
            <router-link to="/" class="navbar-item">Home</router-link>

            <div class="navbar-item">
              <div class="buttons">
                <router-link to="/sign-up" class="button is-success"><strong>Sign up</strong></router-link>
                <router-link to="/log-in" class="button is-light">Log in</router-link>
              </div>
            </div>
          </template>
        </div>
      </div>
    </nav>

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2022</p>
    </footer>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'App',
    beforeCreate() {
      this.$store.commit('initializeStore')
      const token = this.$store.state.token
      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
      } else {
        axios.defaults.headers.common['Authorization'] = ""
      }
    }
  }
</script>





<style lang="scss">
@import "../node_modules/bulma";
</style>
