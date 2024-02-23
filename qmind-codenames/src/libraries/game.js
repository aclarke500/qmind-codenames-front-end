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
}

/**
 * Determines the set of moves the computer is going to make
 * @returns {Array<String>} the list of moves the computer is making
 */
function getComputerTurn(){
  const computerMoves = [];
  let turnOver = false;
  while (!turnOver){
    const guessWord = store.computerGuesses[store.computerGuessIndex];
    const wordObj = getWordObject(guessWord);
    if (!wordObj.flipped) { // don't make a move if human flipped the word
      computerMoves.push(wordObj);
      turnOver = endTurn(guessWord);
    }
    store.computerGuessIndex++;
  }
  return computerMoves;
}

/**
 * Handles the computers move.
 * Gets move and updates wordObjects/components.
 */
export async function computerMove() {
  const compMove = getComputerTurn();
  // Wrap setTimeout in a promise
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

  for (let i = 0; i < compMove.length; i ++){
    await wait(250)
    compMove[i].clicked()
    await wait(500)
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