import { reactive } from 'vue';

export const store = reactive({
  teamOneWords: null,
  teamTwoWords: null,
  assassinWord: null,
  bystanderWords: null,
  player: 'Human',
  wordObjects: [],
  teamOneWordObjects: null,
  teamTwoWordObjects: null,
  bystanderWordObjects: null,
  computerGuesses: null,
  computerGuessIndex: null, // computer recieves guesses on load, we get 
  hint:null,
  aiHint:null,

})

/**
 * Gets the length of an array of arrays
 * @param {Array<Array>} arr 
 */
function getLengthOfArrays(arr) {
  let sum = 0;
  arr.forEach(ar => {
    sum += ar.length;
  })
  return sum;
}

/**
 * Fetches words from the server
 */
export async function assignBackendWordsToStore() {
  const response = await fetch('http://127.0.0.1:5000/model', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json();
  console.log(data);
  // bind data from backend
  store.hint = data.hint;
  store.aiHint = data.hint;
  store.assassinWord = data.assassin.split(' ');
  store.bystanderWords = data.neutral.split(' ');
  store.teamTwoWords = data.targets.split(' ');
  store.teamOneWords = data.negative.split(' ');
  store.computerGuesses = data.similar_words;

  // figure out dimensions of the board
  const numWords = getLengthOfArrays([
    store.bystanderWords,
    store.assassinWord,
    store.teamOneWords,
    store.teamTwoWords
  ])

  store.numCols = Math.sqrt(numWords);
  store.numRows = Math.sqrt(numWords);
}

export async function loadCustomBoard(board) {
  try {
    const response = await fetch('http://127.0.0.1:5000/prompt-model', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        target_words: board.teamTwoWords,
        negative_words: board.teamOneWords,
        neutral_words: board.bystanderWords,
        assassin_word: board.assassinWord,
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data)
    store.computerGuesses = data.similar_words;
    store.computerGuessIndex = 0;
    store.hint = data.human_hint;
    store.aiHint = data.cpu_hint;
    store.teamOneWords = board.teamOneWords;
    store.teamTwoWords = board.teamTwoWords;
    store.bystanderWords = board.bystanderWords;
    store.assassinWord = [board.assassinWord]; 
    store.numCols = board.size; 
    store.numRows = board.size; 
    // Use the data from the response
  } catch (error) {
    console.error("Failed to load custom board:", error);
  }
}