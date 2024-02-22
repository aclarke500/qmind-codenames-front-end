import { store } from '@/store'

export function checkWord(wordObject) {
  if (store.teamOneWords.includes(wordObject.word)) {
    return 'correct'
  } else if (store.assassinWord.includes(wordObject.word)) {
    return 'assassin';
  } else return 'wrong'
}

function getNonGuessedWords() {
  const words = [];
  store.wordObjects.forEach(wordObj => {
    if (!(wordObj.wrongGuess || wordObj.correctGuess)) {
      words.push(wordObj.word);
    }
  })
  return words;
}


function checkComputerMoves(computerGuesses) {
  for (let i = 0; i < computerGuesses.length; i++) {
    const guess = computerGuesses[i];
    if (store.teamTwoWords.includes(guess)) continue;
    else if (store.bystanderWords.includes(guess) || store.teamOneWords.includes(guess)) {
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

function getWordObject(wordLiteral){
  for(let i = 0; i < store.wordObjects.length; i++){
    if (store.wordObjects[i].word == wordLiteral) return store.wordObjects[i];
  }
  throw new Error('AHHH')
}


function updateComputerMove(wordObject){
  if (store.teamOneWords.includes(wordObject) || store.bystanderWords.includes(wordObject)){
    wordObject.guessedRight()
  }
  else wordObject.guessedRight();
}

export async function computerMove() {
  const availableWords = getNonGuessedWords();
  const response = await fetch('http://127.0.0.1:5000/guess_words', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ words: availableWords, hint: 'hint' })
  })

  const data = await response.json();
  const guesses = data.guesses;
  const result = checkComputerMoves(guesses);

  for (let i = 0; i < result.numberOfGuesses; i ++){
    const wordObject = getWordObject(guesses[i])
    await setTimeout(()=>updateComputerMove(wordObject), 500);
  }
  console.log(guesses)
  console.log(result)
}