export default class Word {

  constructor(word) {
    this.word = word;
    this.selected = false;
    this.wrongGuess = false;
    this.correctGuess = false;
  }
  guessedWrong(){
    this.selected = false;
    this.wrongGuess = true;
    this.correctGuess = false;
  }
  guessedRight(){
    this.selected = false;
    this.wrongGuess = false;
    this.correctGuess = true;
  }
  /**
   * Handles when the card is clicked.
   * If the card is available to check, returns this.
   * Returns false if it has been flipped.
   */
  clicked(){
    if (this.correctGuess || this.wrongGuess) return false;
    return this;
  }
}