<template>
  <GameOverModal v-if="state.gameOver" @play-again="reload()"
  :message="state.message" :winner="state.winner"/>
<GameHeader />

  <div class="container">
    <div class="left">
      <GameHistory />
    </div>
<div class="centre">
  <div class="row" v-for="(row) in state.wordRows" key="row">
    <div v-for="(word) in row" key="word">
      <WordCard :wordObject="word" class="card" @wrong-word="changeTurns()" 
      @assassin="gameOver('You clicked the assassin word!', 'AI')" 
      @click="checkGameState()"/>
    </div>
  </div>
  </div>
    <div class="right">
      <WordenGameDisplay v-if="store.teamOneWordObjects"/>
    </div>
</div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { createWordObjects } from '@/libraries/word.js';
import { store, assignBackendWordsToStore, updateHumanHint, clearData, getScore, updateScore } from '@/store.js'
import { computerMove, checkForWinners, checkAssassinWord } from '@/libraries/game.js';

import WordCard from '@/components/WordCard.vue';
import GameHeader from '@/components/GameHeader.vue';
import WordenGameDisplay from '@/components/WordenGameDisplay.vue';
import GameHistory from '@/components/GameHistory.vue';
import GameOverModal from '@/components/GameOverModal.vue';


const route = useRoute();

const state = reactive({
  numRows: 5,
  numCols: 5,
  words: null,
  wordRows: [],
  hint: null,
  gameOver:false,
});


function reload() {
  location.reload();
}

function checkGameState() {
  if (checkAssassinWord() && store.player == 'AI') {
    gameOver("HA! That stupid AI got sucked to saddle point and clicked the assassin word. 'Artificial' Intelligence ain't so intelligent after all.", 'human');
  }
  const winners = checkForWinners();
  if (!winners) {
    return true;
  }
  if (winners === 'teamOne') {
    gameOver('Player Wins!', 'human');
  } else if (winners === 'teamTwo') {
    gameOver('Worden Wins!', 'AI');
  }
  return false;
}


async function changeTurns() {
  if (store.player == 'Human') {
    store.player = 'AI';
    const compMove = await computerMove();
    const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
    await wait(500);
    if (checkGameState()) changeTurns();
  } else {
    await updateHumanHint();
    store.player = 'Human';
  }
}

async function assignStoreWordsToState() {
  const s = store;
  state.numCols = store.numCols;
  state.numRows = store.numRows;
  createWordObjects(); // creates word objects and stores them in store.wordObjects
  for (let i = 0; i < state.numRows; i++) {
    let row = [];
    for (let j = 0; j < state.numCols; j++) {
      const word = store.wordObjects[i * state.numCols + j];
      row.push(word);
    }
    state.wordRows.push(row);
  }

  state.hint = store.hint;
  store.computerGuessIndex = 0;
  console.log(state.wordRows);
}


async function gameOver(message, winner) {
  await updateScore(winner);
  state.gameOver = true;
  state.message = message;
  state.winner = winner;
}

onMounted(async () => {
  clearData();
  if (!(route.params.customBoard && (store.teamOneWords))) {
    // if no custom board, assign backend words to store
    await assignBackendWordsToStore();
  }

  await assignStoreWordsToState();
  updateHumanHint();
  getScore();
});

</script>
<style scoped>

.container{
  display: flex;
  flex-direction: columns;
}

.right{
margin-top: 5rem;
}

.left, .right{
  flex: 1;
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  align-items: center;
}

.centre {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex: 1;
}

.card {
  border: 1px solid black;
  margin: 5px;
  flex:1;
}

.row {
  flex: 1;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

</style>