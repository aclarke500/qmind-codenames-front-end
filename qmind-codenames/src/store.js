import { reactive } from 'vue';

export const store = reactive({
  teamOneWords: null,
  teamTwoWords: null,
  assassinWord: null,
  bystanderWords: null,
  player:'Human',
  wordObjects:[]
})