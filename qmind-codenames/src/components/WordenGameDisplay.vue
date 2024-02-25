<template>
  <h1>Worden's Stats</h1>

  <p>Words Left: {{movesLeft()}} / {{totalMoves()}}</p>
  <h2>Previous Moves</h2>
  <p v-for="(g) in state.game" key="g" v-if="state.game.length">
    Worden used <div class="hint">{{ g.hint }}</div> and played <div class="moves">{{ g.words.join(", ") }}</div>.
  </p>


</template>
<script setup>
import {reactive, computed} from 'vue';
import {store} from '@/store.js'

const state = reactive({
  game: computed(() => {
    const moves = store.previousAiGuesses;
    const hints = store.previousAiHints;

    const game_moves=[];
    const length = Math.min(moves.length, hints.length)
    for (let i = 0; i < length; i++){
      game_moves.push({
        words: moves[i],
        hint: hints[i]
      })
    }
    return game_moves;
  }),
})



function movesLeft(){
  return store.teamTwoWordObjects.filter(word => !word.flipped).length
}
function totalMoves(){
  return store.teamTwoWordObjects.length
}
</script>
<style>
.hint{
  display: inline;
  font-weight: bold;
  color: red;
}
.moves{
  display: inline;
  font-weight: bold;
  color: green;
}
</style>