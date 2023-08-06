let deck = [
  'card_face1.png', 'card_face1.png', 'card_face1.png', 'card_face1.png', 'card_face1.png',
  'card_face2.png', 'card_face2.png',
  'card_face3.png', 'card_face3.png',
  'card_face4.png', 'card_face4.png',
  'card_face5.png', 'card_face5.png',
  'card_face6.png',
  'card_face7.png',
  'card_face8.png'
];

let northHand = [];
let southHand = [];
let northDiscard = [];
let southDiscard = [];
let removedCards = [];
let currentPlayer = 'north';
let gameStarted = false;

function shuffleDeck() {
  deck.sort(() => Math.random() - 0.5);
}

function drawCard(playerHand) {
  let card = deck.shift();
  playerHand.push(card);
}

function updateHand(playerHand, player) {
  let handElement = document.querySelector(`.${player} .hand`);
  handElement.innerHTML = '';

  for (let card of playerHand) {
    let li = document.createElement('li');
    let img = document.createElement('img');
    img.src = `../images/card/${card}`;
    li.appendChild(img);
    handElement.appendChild(li);
  }

  attachCardListeners(player, playerHand);
}

function updateDiscard(playerDiscard, player) {
  let discardElement = document.querySelector(`.${player} .discard`);
  discardElement.innerHTML = '';

  for (let card of playerDiscard) {
    let li = document.createElement('li');
    let img = document.createElement('img');
    img.src = `../images/card/${card}`;
    li.appendChild(img);
    discardElement.appendChild(li);
  }
}

function removeCards() {
  for (let i = 0; i < 3; i++) {
    let card = deck.shift();
    removedCards.push(card);
  }

  let cardsElement = document.querySelector('.removed .cards');
  cardsElement.innerHTML = '';

  for (let card of removedCards) {
    let li = document.createElement('li');
    let img = document.createElement('img');
    img.src = `../images/card/card_face0.png`;
    li.appendChild(img);
    cardsElement.appendChild(li);
  }
}

function startGame() {
  shuffleDeck();
  removeCards();
  drawCard(northHand);
  drawCard(southHand);
  updateHand(northHand, 'north');
  updateHand(southHand, 'south');
  gameStarted = true;
}

function attachCardListeners(player, playerHand) {
  let handElement = document.querySelector(`.${player} .hand`);
  let cards = handElement.getElementsByTagName('li');

  for (let i = 0; i < cards.length; i++) {
    cards[i].addEventListener('dblclick', function() {
      let card = playerHand[i];
      playerHand.splice(i, 1);
      if (player === 'north') {
        northDiscard.push(card);
        updateDiscard(northDiscard, 'north');
      } else {
        southDiscard.push(card);
        updateDiscard(southDiscard, 'south');
      }
      updateHand(playerHand, player);
    });
  }
}

document.getElementById('drawButton').addEventListener('click', function() {
    document.querySelector('.game_container').classList.remove('hide');
    document.querySelector('.removed').classList.remove('hide');
  if (!gameStarted) {
    startGame();
  } else if (deck.length > 0) {
    if (currentPlayer === 'north' && northHand.length < 2) {
      drawCard(northHand);
      updateHand(northHand, 'north');
      currentPlayer = 'south';
    } else if (currentPlayer === 'south' && southHand.length < 2) {
      drawCard(southHand);
      updateHand(southHand, 'south');
      currentPlayer = 'north';
    } else {
      alert('No more cards can be drawn, hand limit reached! Discard one card!!');
    }
  } else {
    alert('No more cards in the deck!');
  }
});

