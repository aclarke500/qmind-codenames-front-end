<template>
  <div class="container" :class="{wrong:wordObject.wrongGuess, correct:wordObject.correctGuess}" 
  @click="cardClicked()">
    <p>{{ wordObject.word }}</p>
  </div>
</template>
<script setup>
import { checkWord } from '@/libraries/game';
const props = defineProps(['wordObject']);
const emits = defineEmits(['assassin', 'wrongWord'])

function cardClicked(){
  const guess = checkWord(props.wordObject);
  if (guess === 'correct'){
    props.wordObject.correctGuess = true;
  } else if (guess === 'wrong'){
    props.wordObject.wrongGuess = true;
    emits('wrongWord')
  }
  else if (guess === 'assassin'){
    emits('assassin')
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


.correct,
.wrong {
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease; /* This will animate all properties over a 300ms duration with an ease timing function */
}

.correct {
  background-color: #f10fe9;
}

.wrong {
  background-color: red;
}

</style>
