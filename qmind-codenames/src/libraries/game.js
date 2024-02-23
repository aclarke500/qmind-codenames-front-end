import { store } from '@/store'
import { getWordObject } from './word';

export function checkWord(wordObject) {
  if (store.teamOneWords.includes(wordObject.word)) {
    return 'correct'
  } else if (store.assassinWord.includes(wordObject.word)) {
    return 'assassin';
  } else return 'wrong'
}

function getNonGuessedWords() {
  const f = store.wordObjects.filter((wordObj)=>!wordObj.flipped)
  const m = f.map(wordObj =>
    wordObj.word
  )
  return m;
}


function endTurn(guessWord){
  if (store.teamTwoWords.includes(guessWord)) return false;
  if (store.bystanderWords.includes(guessWord) || store.teamOneWords.includes(guessWord)) return 'wrong';
  if (guessWord == store.assassinWord || store.assassinWord[0]) return 'assassin'
}

/**
 * Determines the set of moves the computer is going to make
 * @returns {Array<String>} the list of moves the computer is making
 */
function getComputerTurn(){
  const s = store;
  const computerMoves = [];
  let turnOver = false;
  while (!turnOver){
    debugger
    const guessWord = store.computerGuesses[store.computerGuessIndex];
    const wordObj = getWordObject(guessWord);
    if (!wordObj.flipped) {
      computerMoves.push(wordObj);
      turnOver = endTurn(guessWord);
    }
    store.computerGuessIndex++;
  }
  return computerMoves;
}

function checkComputerMoves(computerGuesses) {
  for (let i = 0; i < computerGuesses.length; i++) {
    const guess = computerGuesses[i];
    if (store.teamTwoWords.includes(guess)) continue;
    else if (store.bystanderWords.includes(guess) || store.teamOneWords.includes(guess)) {
      console.log(guess)
      return {
        result: 'wrong',
        numberOfGuesses: i + 1
      }
    } else if (store.assassinWord.includes(guess)) return {
      result: 'assassin',
      numberOfGuesses: i + 1
    };
  }
  return {
    result: 'winner',
    numberOfGuesses: i + 1
  };
}



export async function computerMove() {
  // const availableWords = getNonGuessedWords();
  // console.log(availableWords)
  // const response = await fetch('http://127.0.0.1:5000/guess_words', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify({ words: availableWords, hint: 'hint' })
  // })

  // const data = await response.json();
  // const guesses = data.guesses;
  // const result = checkComputerMoves(guesses);
  debugger
  const compMove = getComputerTurn();
  // Wrap setTimeout in a promise
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

  for (let i = 0; i < compMove.length; i ++){
    await wait(1000)
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