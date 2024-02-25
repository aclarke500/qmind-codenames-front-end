<template>
<div class="modal-backdrop">
  <div class="modal-content">
    <div v-if="winner=='human'">
      <h1>Congratulations!</h1>
      <p>{{ message }}</p>
      <h2>You beat Worden, and single handedly pushed back the singularity!</h2>
    </div>
    <div v-else-if="winner=='AI'">
      <h1>Oh no!</h1>
      <p>{{ message }}</p>
      <h2>Worden has won, and the singularity is upon us!</h2>
    </div>
    <button @click="playAgain()">Play Again</button>
  </div>
</div>
</template>
<script setup>

const emits = defineEmits(['playAgain'])
const props = defineProps(['message', 'winner'])

function playAgain(){
  emits('playAgain')
}
</script>
<style scoped>
/* The modal background */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Dimmed background */
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  z-index: 1; /* Ensure it sits above other content */
}

/* The modal box itself */
.modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 700px; /* Or whatever width you prefer */
  height: 400px; /* Or whatever height you prefer */
  background-color: rgb(50, 42, 158);
  padding: 20px;
  border: 5px solid black;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional: Adds a subtle shadow */
  z-index: 2; /* Ensure it sits above the backdrop */
}



button {
  background-color: rgb(0, 134, 251);
  border-radius: 5px;
  border: none;
  padding: 10px;
  margin: 10px;
  width: 5rem;
  height: 5rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}
button:hover {
  background-color: red;
  transition: all 0.3s ease;
}
h1{
  margin-bottom: 4rem;
  font:3rem;
}
</style>