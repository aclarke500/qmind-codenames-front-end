<template>
  <div class="container">
    <h1>Enter the words for your board:</h1>
    <input type="text" v-model="state.word" @keyup.enter="addWord" />


    <div class="word-container">

      <div class="word-column">
        <h2>Team 1 Words</h2>
        <p>{{ state.gameSize.teamWords }} Words</p>
        <div v-for="word in state.teamOneWords" :key="word" class="wordList">{{ word }},</div>
      </div>

      <div class="word-column">
        <h2>Team 2 Words</h2>
        <p>{{ state.gameSize.teamWords }} Words</p>
        <div v-for="word in state.teamTwoWords" :key="word" class="wordList">{{ word }}</div>
      </div>

      <div class="word-column">
        <h2>Bystander Words:</h2>
        <p>{{ state.gameSize.bystanderWords }} Words</p>
        <div v-for="word in state.bystanderWords" :key="word" class="wordList">{{ word }}</div>
      </div>

      <div class="word-column">
        <h2>Assassin Word:</h2>
        <p>{{ state.gameSize.assassinWord }} Words</p>
        <div class="wordList">{{ state.assassinWord }}</div>
      </div>

    </div>



    <div class="options-container">
      <div class="custom-boards">

      </div>
      <div class="board-sizes">
        <h3>Select Board Size:</h3>
        <p @click="toggleBoardSize(3)" :class="{ selected: state.gameSize.size == 3 }">3x3</p>
        <p @click="toggleBoardSize(4)" :class="{ selected: state.gameSize.size == 4 }">4x4</p>
        <p @click="toggleBoardSize(5)" :class="{ selected: state.gameSize.size == 5 }">5x5</p>
      </div>

      <div class="right">
        <h3 class="custom-board-title">Prebuilt Boards:</h3>
        <div class="custom-boards">

          <button class='custom-board' v-for="board in state.customBoards" :key="board.name"
            @click="clickedCustomBoard(board)">
            {{ board.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive } from 'vue';
import router from '@/router';
import { loadCustomBoard } from '@/store.js';
import { customBoards } from '@/libraries/boards';

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
    size: 3,
  },
  customBoards: customBoards,
});


async function clickedCustomBoard(board) {
  await loadCustomBoard(board);
  router.push({
    name: 'home',
    params: {
      customBoard: true,
    }
  });
}

function toggleBoardSize(size) {
  if (size === 3) {
    state.gameSize = {
      teamWords: 3,
      assassinWord: 1,
      bystanderWords: 2,
      size: size,
    }
  } else if (size === 4) {
    state.gameSize = {
      teamWords: 6,
      assassinWord: 1,
      bystanderWords: 3,
      size: size,
    }
  } else if (size === 5) {
    state.gameSize = {
      teamWords: 10,
      assassinWord: 1,
      bystanderWords: 4,
      size: size,
    }
  }

}

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
  await loadCustomBoard({
    teamOneWords: state.teamOneWords,
    teamTwoWords: state.teamTwoWords,
    bystanderWords: state.bystanderWords,
    assassinWord: state.assassinWord,
    size: state.gameSize.size,
  });
  router.push({
    name: 'home',
    params: {
      customBoard: true,
    }
  });

}

</script>

<style scoped>
.wordList {
  display: block;
  margin-right: 10px;
  font-size: 2rem;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20px;

}


.word-container {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
  height: 350px;
}


.selected {
  color: red;
}


.options-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.board-sizes {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.custom-board-title {
  display: block;
}

.custom-boards {

  flex: 1;
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;  
  justify-content: center;
  align-items: center;
  /* justify-content: space-around; */
}

.right,
.left {
  flex: 1;
}

.custom-board {
  background-color: orange;
  border: none;
  padding: 10px;
  margin: 10px;
  width: 5rem;
  height: 5rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}
.custom-board:hover {
  background-color: red;
  transition: all 0.3s ease;
}
</style>