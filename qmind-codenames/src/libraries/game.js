import { store } from '@/store'
import { getWordObject } from './word';

/**
 * Determines if the computers move should end
 * @param {String} guessWord 
 * @returns {Boolean}
 */
function endTurn(guessWord){
  if (store.teamTwoWords.includes(guessWord)) return false;
  if (store.bystanderWords.includes(guessWord) || store.teamOneWords.includes(guessWord)) return true;
  if (guessWord == store.assassinWord || store.assassinWord[0]) return true;
  let wordenHasUnselectedCards = false; 
  store.teamTwoWordObjects.forEach(wordObj =>{
    if (!wordObj.flipped){
      wordenHasUnselectedCards = true;
    }
  })
  return !wordenHasUnselectedCards;
}


/**
 * Takes the sorted board and returns the words for one computer move
 * @param {Array<String>} computerGuesses sorted order of words fetched from API
 * @returns {Array<String>} valid moves for the computer to make
 */
function trimComputerMoves(computerGuesses){
  const validGuesses = [];
  const guessWordObjects =  computerGuesses.map(wordLiteral=>getWordObject(wordLiteral));

  // add moves until computer makes a bad guess
  for (let i = 0; i < guessWordObjects.length; i++){
    validGuesses.push(guessWordObjects[i])
    if (endTurn(guessWordObjects[i].word)){
      return validGuesses;
    }
  }
  return validGuesses;
}

/**
 * Get words that haven't been selected yet
 * @param {Array<Word>} wordObjects 
 * @returns {Array<String>} word literals that haven't been flipped
 */
function getValidWords(wordObjects){
  const validWords = [];
  wordObjects.forEach((wordObj)=>{
    if(!wordObj.flipped) validWords.push(wordObj.word)
  })
  return validWords;
}

/**
 * Gets the state of game board formatted for the API call
 * @returns {Object} formatted for the AI API
 */
export function getCurrentGameBoard(){
  return {
    target_words:getValidWords(store.teamTwoWordObjects),
    negative_words:getValidWords(store.teamOneWordObjects),
    neutral_words:getValidWords(store.bystanderWordObjects),
    assassin_word:store.assassinWord[0], // if assassin selected game is over -> assassin not selected
  }
}

/**
 * Grabs the AI's sorted board from the API
 * and updates the store's hints
 * @returns {Array<String>}
 */
async function fetchComputerMoves(){
  const currentGameBoard = getCurrentGameBoard();
  const response = await fetch('http://127.0.0.1:5000/prompt-model', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(currentGameBoard)
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  // not good form to update here...but who cares
  store.aiHint = data.cpu_hint; 
  store.previousAiHints.push(store.aiHint);
  return data.similar_words;

}

/**
 * Handles the computers move.
 * Gets move and updates wordObjects/components.
 */
export async function computerMove() {
  // AI sorts the entire board
  const sortedBoard = await fetchComputerMoves();
  const compMove = trimComputerMoves(sortedBoard);
  // Wrap setTimeout in a promise
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
  store.previousAiGuesses.push([])
  for (let i = 0; i < compMove.length; i ++){
    await wait(50)
    compMove[i].clicked() // updates component/Obj
    store.previousAiGuesses[store.previousAiGuesses.length-1].push(compMove[i].word);
  }
}

/**
 * Checks if all words in an array are flipped.
 * @param {Array<Word>} arr 
 * @returns {Boolean} If all are flipped
 */
function allAreFlipped(arr){
  for (let i = 0; i < arr.length; i++){
    if (!arr[i].flipped) return false
  }
  return true;
}

/**
 * Checks if a team has won the game yet.
 * Does not consider if AI/player guessess assassin word.
 * @returns {String, Boolean} team name on win, else False
 */
export function checkForWinners(){
  if (allAreFlipped(store.teamOneWordObjects)) return 'teamOne';
  else if (allAreFlipped(store.teamTwoWordObjects)) return 'teamTwo';
  else return false;
}

/**
 * Checks if assassin word has been selected
 */
export function checkAssassinWord(){
  for (let i = 0; i < store.wordObjects.length; i++){
    if (store.wordObjects[i].wordType == 'assassin' && store.wordObjects[i].flipped) return true;
  }
  return false
}