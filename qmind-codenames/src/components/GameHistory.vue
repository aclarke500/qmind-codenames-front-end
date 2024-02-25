<template>
  <div v-if="dataIsLoaded()" class="container">

<h3>Human wins: {{ store.humanWins }}</h3>
<h3>Worden wins: {{ store.wordenWins }}</h3>

</div>
</template>
<script setup>
import { store } from '@/store.js'

function dataIsLoaded(){
  return store.wordenWins || store.wordenWins == 0 && store.humanWins || store.humanWins == 0;
}


</script>
<style scoped>
.container{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}
p{
  display: block;
}
</style>