<template>
    <div class="header">
<div class="left">
 <button @click="customBoard()">Custom Board</button>
</div>

    <div class="centre">
      <h1>Qmind CodeNames</h1>
      <h2 id="hint">Your clue: <div id="hint-word">{{ store.hint }}</div></h2>
    </div>

    <div class="right">
      <h3 id="move-display">{{ state.player }} Move</h3>
    </div>
  </div>
</template>
<script setup>
import { store } from '@/store';
import { reactive, computed } from 'vue';
import router from '@/router';
const state = reactive({
  player: computed(() => {
    if (store.player == 'AI') {
      return "Warrus'";
    } else {
      return "Player's";
    }
  })
});

function customBoard() {
  router.push('/design-board');
}
</script>

<style scoped>
.header{
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;

}

h1, h2, h3 {
  margin: 0;
  padding: 0;
}
.left, .right, .centre {
  flex: 1;
}

.left, .right {
  margin-top: 2rem;
}



#move-display{
  display: inline;
  font-size: 2rem;
  font-weight: bold;

}
#hint-word {
  display: inline-block;
  color: #ea2b51;
  /* font-size: 2rem; */
  font-weight: bold;
}
#hint{
  margin-top: 1rem;
}

button {
  font-size:large;
  font-weight: bold;
  margin: 10px;
  background-color: #ed7777;
  height: 5rem;
  width: 5rem;
  border: 2px solid black;
  border-radius: 15%;
}
button:hover {
  background-color: #ea2b51;
  border: black 3px solid;
  cursor: pointer;
  transition: all 0.5s ease;
}

</style>