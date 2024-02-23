<template>
  <div class="container" 
  :class="{
    teamOne:wordObject.wordType == 'teamOne' && wordObject.flipped, 
    teamTwo:wordObject.wordType == 'teamTwo' && wordObject.flipped, 
    bystander:wordObject.wordType == 'bystander' && wordObject.flipped, 
    assassin:wordObject.wordType == 'assassin' && wordObject.flipped, 
  
  correct:wordObject.correctGuess}" 
  @click="cardClicked()">
    <p>{{ wordObject.word }}</p>
  </div>
</template>
<script setup>
import { store } from '@/store';
const props = defineProps(['wordObject']);
const emits = defineEmits(['assassin', 'wrongWord', 'click'])

function cardClicked(){
  if (props.wordObject.flipped || store.player == 'AI'){
    return
  }
  props.wordObject.clicked() // updates object and display
  emits('click') // gets view to check if we've won the game
  if (props.wordObject.wordType === 'assassin'){
    emits('assassin')
  } else if (props.wordObject.wordType === 'bystander'){
    emits('wrongWord')
  } else if (props.wordObject.wordType === 'teamTwo'){
    emits('wrongWord')
  }
}
</script>
<style scoped>
p {
  font-size: 1rem;
  color: #2c3e50;
  display:inline;
}
.container{
  width: 6rem;
  height: 6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
}
/* styles for on hover */
.container:hover{
  background-color: #f1c40f;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.1s ease; /* This will animate all properties over a 300ms duration with an ease timing function */
}


.teamOne, .teamTwo, .bystander, .assassin {
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.5s ease; /* This will animate all properties over a 300ms duration with an ease timing function */
}

.teamOne {
  background-color: #e5ede6;
}

.assassin {
  background-color: black;
}

.bystander {
  background-color: #f1c40f;
}

.teamTwo {
  background-color: red;
}

</style>
