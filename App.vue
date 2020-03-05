<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <HelloWorld msg="practice for get/post method"/>
  </div>
    <!-- <div id="app">
    <el-menu :default-active="activeIndex" mode="horizontal" router>
      <el-menu-item index="getmethod" :route="{ name:'getmethod' }">Get</el-menu-item>
      <el-menu-item index="postmethod" :route="{ name:'postmethod' }">Post</el-menu-item>
      <el-menu-item>
        <a href="https://element.eleme.io" target="_blank">Link</a>
      </el-menu-item>
    </el-menu>
    <router-view />

//   </div> -->
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}

// export default {
//   name: 'app',
//   data () {
//     return {
//       activeIndex: this.$route.name
//     }
//   }
// }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
a {
  text-decoration: none;
} */
</style>