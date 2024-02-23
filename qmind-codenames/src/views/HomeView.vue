<template>
  <h1>Qmind CodeNames</h1>
  <h3>Select words with the clue: </h3>
  <div id="hint">{{ state.hint }}</div>

  <div class="row" v-for="(row) in state.wordRows" key="row">
    <div v-for="(word) in row" key="word">
      <WordCard :wordObject="word" class="card" 
      @wrong-word="changeTurns()"
      @assassin="userClickedAssassin()"
      @click="checkGameState()"
      />
    </div>
  </div>
  <h3>It is the {{ store.player }}'s Turn</h3>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import WordCard from '@/components/WordCard.vue';
import {createWordObjects} from '@/libraries/word.js';
import { store, assignBackendWordsToStore } from '@/store.js'
import { computerMove, checkForWinners, checkAssassinWord }  from '@/libraries/game.js';


const route = useRoute();

const state = reactive({
  numRows: 5,
  numCols: 5,
  words: null,
  wordRows: [],
  hint: null,
});

function playerWins(){
  alert('Player Wins!');
  location.reload();
}
function warrusWins(){
  alert('Warrus Wins!');
  location.reload();
}

function checkGameState(){
  const c = checkAssassinWord();
  const s = store;
  if (checkAssassinWord() && store.player == 'AI'){
    playerWins();
  }
  const winners = checkForWinners();
  if (!winners){
    return;
  }
  if (winners === 'teamOne'){
    playerWins();
  } else if (winners === 'teamTwo'){
    warrusWins();
  } 
}


async function changeTurns(){
  if (store.player == 'Human'){
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
// /**
//  * Fetches words from the server
//  */
// async function assignBackendWordsToStore() {
//   const response = await fetch('http://127.0.0.1:5000/model', {
//     method: 'GET',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   });
//   const data = await response.json();
//   console.log(data);
//   // bind data from backend
//   state.hint = data.message;
//   store.assassinWord = data.assassin.split(' ');
//   store.bystanderWords = data.neutral.split(' ');
//   store.teamOneWords = data.targets.split(' ');
//   store.teamTwoWords = data.negative.split(' ');
//   // figure out dimensions of the board
//   const numWords = getLengthOfArrays([
//     store.bystanderWords,
//     store.assassinWord,
//     store.teamOneWords,
//     store.teamTwoWords
//   ])

//   store.numCols = Math.sqrt(numWords);
//   state.numCols = store.numCols
//   store.numRows = Math.sqrt(numWords);
//   state.numRows = store.numRows
//   assignStoreWordsToState(); // update the reactive state of the board
// }




async function assignStoreWordsToState() {
  createWordObjects(); // creates word objects and stores them in store.wordObjects
  for (let i = 0; i < state.numRows; i++) {
    let row = [];
    for (let j = 0; j < state.numCols; j++) {
      const word = store.wordObjects[i * state.numCols + j];
      row.push(word);
    }
    state.wordRows.push(row);
  }
  state.numCols = store.numCols;
  state.numRows = store.numRows;
  state.hint = store.hint;
  store.computerGuessIndex = 0;
}

function userClickedAssassin()
{
  alert('You clicked the assassin word! Game Over');
  location.reload();
}

onMounted(async() => {
  // // check if we have a custom board in store
  // if (route.params.customBoard && (store.teamOneWords)) {
  //   assignStoreWordsToState();
  // } 
  // else assignBackendWordsToStore(); // also updates state
  // if no custom board, fetch from backend
  if (!(route.params.customBoard || (store.teamOneWords))) {
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

#hint {
  display: inline;
  color: #0f1af1;
  font-size: 2rem;
  font-weight: bold;
}

h3 {
  margin-bottom: 0;
}

button {
  margin: 10px;
  background-color: #ed7777;
  height: 5rem;
  width: 5rem;
  border: 2px solid black;
  border-radius: 15%;
}
</style>