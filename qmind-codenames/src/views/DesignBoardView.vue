<template>
  <div class="container">
    <h1>Enter the words for your board:</h1>
    <input type="text" v-model="state.word" @keyup.enter="addWord" />


    <h2>Team 1 Words</h2>
    <div v-for="word in state.teamOneWords" :key="word" class="wordList">{{ word }},</div>
    <h2>Team 2 Words</h2>
    <div v-for="word in state.teamTwoWords" :key="word">{{ word }}</div>

    <h2>Bystander Words:</h2>
    <div v-for="word in state.bystanderWords" :key="word">{{ word }}</div>

    <h2>Assassin Word:</h2>
    <div>{{ state.assassinWord }}</div>

  </div>
</template>
<script setup>
import { reactive } from 'vue';
import router from '@/router';
import { store } from '@/store.js';

const state = reactive({
  word: '',
  teamOneWords: [],
  teamTwoWords: [],
  assassinWord: '',
  bystanderWords: [],
  gameSize: { // 3x3 grid
    teamWords: 3, // 2*
    assassinWord: 1,
    bystanderWords: 2,
  }
});


function addWord() {
  if (state.teamOneWords.length < state.gameSize.teamWords) {
    state.teamOneWords.push(state.word);
  } else if (state.teamTwoWords.length < state.gameSize.teamWords) {
    state.teamTwoWords.push(state.word);
  } else if (state.bystanderWords.length < state.gameSize.bystanderWords) {
    state.bystanderWords.push(state.word);
  } else if (state.assassinWord === '') {
    state.assassinWord = state.word;
    submitWords();
  }
  state.word = '';
}

async function submitWords() {
  const words = {
    teamOneWords: state.teamOneWords,
    teamTwoWords: state.teamTwoWords,
    bystanderWords: state.bystanderWords,
    assassinWord: state.assassinWord,
  };

  store.teamOneWords = state.teamOneWords;
  store.teamTwoWords = state.teamTwoWords;
  store.bystanderWords = state.bystanderWords;
  store.assassinWord = state.assassinWord;

  const response = await fetch('http://127.0.0.1:5000/custom_board', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({words: words}),
  });
  console.log(response);
  router.push({
    name:'home',
    params:{
      customBoard: true,
    }
  });
}

</script>

<style scoped>
.wordList {
  display: inline;
  margin-right: 10px;

}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  border: 1px solid black;
  /* width: 100%; */
  /* height: 100%; */
}
</style>