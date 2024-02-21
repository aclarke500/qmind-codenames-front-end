<template>
  <div class="container" :class="{wrong:wordObject.wrongGuess, correct:wordObject.correctGuess}" 
  @click="cardClicked()">
    <p>{{ wordObject.word }}</p>
  </div>
</template>
<script setup>
/**
 * Takes in wordObject which represents the state of the card. 
 * This will be modified by the parent component.
 */

const props = defineProps(['wordObject']);

async function cardClicked(){
  const response = await fetch('http://127.0.0.1:5000/check_word', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ word: props.wordObject.word }),
  });
  const data = await response.json();
  if (data.correct){
    props.wordObject.guessedRight();
  } else {
    props.wordObject.guessedWrong();
  }
}
</script>
<style>
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
