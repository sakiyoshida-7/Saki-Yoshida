<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button v-on:click="get_test"> get </button>
    <button v-on:click="post_test"> post </button>

  </div>
  
</template>

<script>
import axios from 'axios'
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  methods: {
    get_test : function () {
    axios.get('http://127.0.0.1:5000/test_get')
      .then(response => {
      console.log("getできました！",); 
      console.log("status", response.status); 
      console.log("body", response.data); 
      return response
    // catchでエラー時の挙動を定義する
    }).catch(err => {
        console.log('err:', err);
    });

    },
    post_test : function() {
    const data = { message : 'postのデータ　'}
    axios.post('http://127.0.0.1:5000/test_post', data)
      .then(response => {
      console.log("postできました！"); 
      console.log("body", response.data);
      return response
    }).catch(err => {
        console.log('err:', err);
    });
    }
  }
}

console.log("hoge");

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
} */
</style>
