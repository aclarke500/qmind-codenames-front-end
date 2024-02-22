<template>
  <h1>Qmind CodeNames</h1>
  <h3>Select words with the clue: </h3>
  <div id="hint">{{ state.hint }}</div>

  <div class="row" v-for="(row) in state.wordRows" key="row">
    <div v-for="(word) in row" key="word">
      <WordCard :wordObject="word" class="card" 
      @wrong-word="changeTurns()"/>
    </div>
  </div>
  <h3>It is the {{ store.player }}'s Turn</h3>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import WordCard from '@/components/WordCard.vue';
import Word from '@/libraries/word.js';
import { store } from '@/store.js'
import { computerMove }  from '@/libraries/game.js';


const route = useRoute();

const state = reactive({
  numRows: 3,
  numCols: 3,
  words: null,
  wordRows: [],
  hint: null,
});




async function changeTurns(){
  if (store.player == 'Human'){
    store.player = 'AI';
    await computerMove();
  } else {
    store.player = 'Human';
  }
  console.log(store.player);
}
/**
 * Fetches words from the server
 */
async function assignBackendWordsToStore() {
  const response = await fetch('http://127.0.0.1:5000/load_board', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json();
  console.log(data)
  store.assassinWord = data.assassinWord;
  console.log('ass word', store.assassinWord)
  store.bystanderWords = data.bystanderWords;
  store.teamOneWords = data.teamOneWords;
  store.teamTwoWords = data.teamTwoWords;
  assignStoreWordsToState();
}


function shuffle(arr) {
  return arr
    .map(value => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value)


}

async function assignStoreWordsToState() {
  const words = [...store.teamOneWords, ...store.teamTwoWords, ...store.bystanderWords, ...store.assassinWord];
  const shuffledWords = shuffle(words);
  for (let i = 0; i < state.numRows; i++) {
    let row = [];
    for (let j = 0; j < state.numCols; j++) {
      const word = shuffledWords[i * state.numCols + j];
      const wordObj = new Word(word)
      row.push(wordObj);
      store.wordObjects.push(wordObj);
    }
    state.wordRows.push(row);
  }
  console.log(words);
}


onMounted(() => {
  // check if we have a custom board in store
  if (route.params.customBoard && (store.teamOneWords)) {
    assignStoreWordsToState();
  } 
  else assignBackendWordsToStore(); // also updates state
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