import { store } from '@/store';
export default class Word {

  constructor(word, wordType) {
    this.word = word;
    this.wordType = wordType;
    this.flipped = false;
  }
  /**
   * Handles when the card is clicked.
   * If the card is available to check, returns this.
   * Returns false if it has been flipped.
   */
  clicked(){
    this.flipped = true;
  }
}

function shuffle(arr) {
  return arr
    .map(value => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value);
}


// Function to add word objects from a source array to the store.wordObjects array
function addWordObjects(sourceArray, type) {
  const wordObjectsInThisCategory = []
  sourceArray.forEach(word => {
    const wordObj = new Word(word, type);
    store.wordObjects.push(wordObj);
    wordObjectsInThisCategory.push(wordObj)
  });
  return wordObjectsInThisCategory;
}


export function createWordObjects(){
// Initialize the wordObjects array as empty
store.wordObjects = [];
// Add the assassin word object to the wordObjects array
store.wordObjects.push(new Word(store.assassinWord[0], 'assassin'));

// Add bystander, teamOne, and teamTwo word objects
store.bystanderWordObjects = addWordObjects(store.bystanderWords, 'bystander');
store.teamOneWordObjects = addWordObjects(store.teamOneWords, 'teamOne');
store.teamTwoWordObjects = addWordObjects(store.teamTwoWords, 'teamTwo');

  // disabled for debugging
  store.wordObjects = shuffle(store.wordObjects);
}

/**
 * Get the word object given the string literal
 * @param {String} word 
 * @returns word object
 */
export function getWordObject(word){
  for (let i = 0; i < store.wordObjects.length; i++){
    if (store.wordObjects[i].word == word) return store.wordObjects[i]
  }
}