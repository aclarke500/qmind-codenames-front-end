<template>
<GameHeader />
  <div class="row" v-for="(row) in state.wordRows" key="row">
    <div v-for="(word) in row" key="word">
      <WordCard :wordObject="word" class="card" @wrong-word="changeTurns()" @assassin="userClickedAssassin()"
        @click="checkGameState()" />
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import WordCard from '@/components/WordCard.vue';
import GameHeader from '@/components/GameHeader.vue';
import { createWordObjects } from '@/libraries/word.js';
import { store, assignBackendWordsToStore } from '@/store.js'
import { computerMove, checkForWinners, checkAssassinWord } from '@/libraries/game.js';


const route = useRoute();

const state = reactive({
  numRows: 5,
  numCols: 5,
  words: null,
  wordRows: [],
  hint: null,
});

function playerWins() {
  alert('Player Wins!');
  location.reload();
}
function wordenWins() {
  alert('Worden Wins!');
  location.reload();
}

function checkGameState() {
  const c = checkAssassinWord();
  const s = store;
  if (checkAssassinWord() && store.player == 'AI') {
    playerWins();
  }
  const winners = checkForWinners();
  if (!winners) {
    return;
  }
  if (winners === 'teamOne') {
    playerWins();
  } else if (winners === 'teamTwo') {
    wordenWins();
  }
}


async function changeTurns() {
  if (store.player == 'Human') {
    store.player = 'AI';
    const compMove = await computerMove();
    const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
    await wait(500);
    checkGameState();
    changeTurns();
  } else {
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

function userClickedAssassin() {
  alert('You clicked the assassin word! Game Over');
  location.reload();
}

onMounted(async () => {
  if (!(route.params.customBoard && (store.teamOneWords))) {
    await assignBackendWordsToStore();
  }
  assignStoreWordsToState();
});

</script>
<style scoped>

.card {
  border: 1px solid black;
  /* flex: 1; */
  margin: 5px;
}

.row {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

</style>