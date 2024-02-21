<template>
  <h1>Qmind CodeNames</h1>
  <h3>Select words with the clue: </h3>
  <div id="hint">{{state.hint }}</div>

  <div class="row" v-for="(row) in state.wordRows" key="row">
    <div v-for="(word) in row" key="word">
      <WordCard :wordObject="word" class="card" @card-clicked="(word) => cardClicked(word)" />
    </div>
  </div>

</template>

<script setup>
import { reactive, onMounted } from 'vue';
import WordCard from '@/components/WordCard.vue';
import Word from '@/libraries/word.js';

const state = reactive({
  numRows: 5,
  numCols: 5,
  words: null,
  wordRows: [],
  hint:null,
});


/**
 * Sets the words in the state to a 2D array
 */
function setWords() {
  for (let i = 0; i < state.numRows; i++) {
    let row = [];
    for (let j = 0; j < state.numCols; j++) {
      const word = state.words[i * state.numCols + j];
      row.push(new Word(word));
    }
    state.wordRows.push(row);
  }

}

/**
 * Fetches words from the server
 */
async function getWords() {
  const response = await fetch('http://127.0.0.1:5000/load_board', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json();
  state.words = data.words;
  state.hint = data.hint;
  const s = state;
  setWords();

}



onMounted(() => {
  getWords();
});

</script>
<style>
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
h3{
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