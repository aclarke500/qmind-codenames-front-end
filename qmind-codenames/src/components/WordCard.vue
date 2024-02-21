<template>
  <div class="container" :class="{selected:props.wordObject.selected, bust:state.bomb, flipped:state.flipped}" 
  @click="cardClicked()">
    <p>{{ wordObject.word }}</p>
  </div>
</template>
<script setup>
import { computed, reactive, } from 'vue';
/**
 * Takes in wordObject which represents the state of the card. 
 * This will be modified by the parent component.
 */

const props = defineProps(['word', 'wordObject']);
const emits = defineEmits(['card-clicked']);

const state = reactive({
  flipped:computed(()=>props.wordObject.flipped),
  bomb:computed(()=>props.wordObject.bust),
});

function cardClicked(){
  props.wordObject.selected = !props.wordObject.selected;
  emits('card-clicked', props.wordObject);
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
}

.selected{
  background-color: #f1660f;
  border-radius: 5px;
  cursor: pointer;
}

.flipped{
  background-color: #f10fe9;
  border-radius: 5px;
  cursor: pointer;
}

.bust{
  background-color: red;
  border-radius: 5px;
  cursor: pointer;
}
</style>
