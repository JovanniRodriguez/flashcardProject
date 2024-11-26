// flashdeck/js/MyDecks.js

var saveDeckButton = document.getElementById('saveDeckButton');
var cardGrid = document.getElementById('cardGrid');
var card = document.querySelector('.card');
var nameInput = document.getElementById('nameInput');
var descInput = document.getElementById('descInput');


//add deck card when clicking create button
saveDeckButton.addEventListener('click', function(e){
    e.preventDefault();

    var newCardCol = document.createElement('div');
    newCardCol.classList = 'col-md-4 mb-4';


    var newCard = document.createElement('div');
    newCard.classList = 'card mx-4 py-4';
    newCard.setAttribute('data-bs-toggle', 'modal');
    newCard.setAttribute('data-bs-target', '#cardOptionsModal');

    var newCardBody = document.createElement('div');
    newCardBody.classList = 'card-body text-center';
    
    var h5 = document.createElement('h5');
    h5.classList = 'card-title';
    if(nameInput.value == '')
        h5.textContent = 'New Deck';
    else
        h5.textContent = nameInput.value;  //grab from create modal textContent fields

    var p = document.createElement('p');
    p.classList = 'card-text';
    if(descInput.value == '')
        p.textContent = 'No Description';
    else
        p.textContent = descInput.value;   //grab from create modal textContent fields

    newCardBody.appendChild(h5);
    newCardBody.appendChild(p);
    newCard.appendChild(newCardBody);
    newCardCol.appendChild(newCard);
    cardGrid.appendChild(newCardCol);

    nameInput.value = '';
    descInput.value = '';
})



{/* <div class="col-md-4 mb-4">
        <div class="card mx-4 py-4" data-bs-toggle="modal" data-bs-target="#cardOptionsModal">
          <div class="card-body text-center">
            <h5 class="card-title">Example Deck</h5>
            <p class="card-text">description</p>
          </div>
        </div>
      </div> */}