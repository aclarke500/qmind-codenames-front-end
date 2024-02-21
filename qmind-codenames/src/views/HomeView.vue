<template>
  <h1>Qmind CodeNames</h1>
  <button @click="submitMove()">Submit Move</button>

  <div class="row" v-for="(row) in state.wordRows" key="row">
    <div v-for="(word) in row" key="word">
      <WordCard :wordObject="word" class="card" @card-clicked="(word) => cardClicked(word)" />
    </div>
  </div>

  <p>Selected words: {{ state.selectedWords }}</p>
</template>

<script setup>
import { reactive, onMounted, computed } from 'vue';
import WordCard from '@/components/WordCard.vue';

const state = reactive({
  numRows: 5,
  numCols: 5,
  words: null,
  wordRows: [],
  selectedWords: [],
});

function resetData(){
  state.wordRows.forEach(row=>{
    row.forEach(wordObject=>{
      wordObject.selected = false;
      wordObject.flipped = false;
    });
  });
  state.selectedWords = [];

}

/**
 * Submits the selected words to the server
 */
async function submitMove() {
  // get data
  const response = await fetch('http://127.0.0.1:5000/verify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ words: state.selectedWords }),
  });
  const data = await response.json();

  resetData();
  // update valid words
  data.valid_words.forEach((word) => {
    state.wordRows.forEach((row) => {
      row.forEach((wordObject) => {
        if (wordObject.word === word) {
          wordObject.flipped = true;
        }
      });
    });
  });
  // update bomb words
  data.bust_words.forEach((word) => {
    state.wordRows.forEach((row) => {
      row.forEach((wordObject) => {
        if (wordObject.word === word) {
          wordObject.bust = true;
        }
      });
    });
  });
}

/**
 * If the word is selected, add it to the selected words array. If it is not selected, remove it from the selected words array.
 * @param {Object} wordObject 
 */
function cardClicked(wordObject){
  if (wordObject.selected){
    state.selectedWords.push(wordObject.word);
  } else {
    state.selectedWords = state.selectedWords.filter((word)=>word!==wordObject.word);
  }
}

/**
 * Sets the words in the state to a 2D array
 */
function setWords() {
  for (let i = 0; i < state.numRows; i++) {
    let row = [];
    for (let j = 0; j < state.numCols; j++) {
      const word = state.words[i * state.numCols + j];
      const wordObject = {
        word: state.words[i * state.numCols + j],
        selected: false,
        bust:false,
        flipped:false,
      };
      row.push(wordObject);
    }
    state.wordRows.push(row);
  }
}

/**
 * Fetches words from the server
 */
async function getWords(){
  const response = await fetch('http://127.0.0.1:5000/load_board', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json();
  state.words = data.words;
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

button {
  margin: 10px;
  background-color: #ed7777;
  height: 5rem;
  width: 5rem;
  border: 2px solid black;
  border-radius: 15%;
}
</style>