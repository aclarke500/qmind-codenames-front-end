<template>
  <!-- removed while custom boards aren't supported -->
  <!-- <nav>
    <router-link to="/">Play</router-link> |
    <router-link to="/design-board">Custom Board</router-link>
  </nav> -->
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}

body{
  background-color: #2c3e50;
  color: white;
  font-family: 'Arial';
  overflow: hidden;
}
nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
