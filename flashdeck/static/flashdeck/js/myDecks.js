// flashdeck/js/MyDecks.js

var createDeckButton = document.getElementById('createDeckButton');
var cardGroup = document.getElementById('card-group');
var card = document.querySelector('.card');



//add deck card when clicking create button
createDeckButton.addEventListener('click', function(e){
    e.preventDefault()
    var newCard = card.cloneNode(true);
    cardGroup.appendChild(newCard)
    
})




