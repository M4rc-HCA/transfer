'use strict';

// Get the modal
var modal = document.getElementById("myModal");
modal.closeBtn = document.getElementsByClassName("close")[0];

// When the user clicks on the <button> (x), close the modal
modal.closeBtn.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var questionCard;
let decks = document.getElementById('decks');
for(let catX = 0; catX < categories.length; ++catX) {
    let catName = categories[catX].name;

    let catButton = document.createElement('button');
    catButton.id = 'draw-' + catName;
    catButton.innerHTML = 'Draw<br>' + catName;
    catButton.onclick = function() {
        let drawn = drawSeveral(catX, 4);
        questionCard = drawn[0];

        let question = document.getElementById('question');
        question.classList.add('unanswered');
        question.innerHTML = drawn[0].question +
            ' <span class="reference">(' + drawn[0].reference + ')</span>';

        let radios = document.getElementById('radios');
        radios.innerHTML = '';

        for(let drawnX = 0; drawnX < drawn[1].length; ++drawnX) {
            let answerRadio = document.createElement('input');
            answerRadio.type = 'radio';
            answerRadio.setAttribute('name', 'answers');
            answerRadio.setAttribute('class', 'radio');
            answerRadio.id = 'answer' + drawnX;
            answerRadio.value = (drawn[0].answer === drawn[1][drawnX]);
            radios.appendChild(answerRadio);

            let answerLabel = document.createElement('label');
            answerLabel.setAttribute('class', 'radio-label');
            answerLabel.htmlFor = answerRadio.id;
            answerLabel.innerHTML = drawn[1][drawnX];
            radios.appendChild(answerLabel);
        }
    };
    decks.appendChild(catButton);
}

document.getElementById('answers').onsubmit = function(event) {
    let chosen = document.querySelectorAll('input[name=answers]:checked');
    if(chosen.length == 1){
        modal.style.display = "block";
        let modalContent = document.getElementById('modal-content');
        if(chosen[0].value == 'true'){
            modalContent.setAttribute('class', 'modal-content modal-true');
        } else {
            modalContent.setAttribute('class', 'modal-content modal-false');
        }
        let modalText = document.getElementById('modal-text');
        modalText.innerHTML = '<h2 class="capitalize">' + chosen[0].value + '</h2>' +
        '<span class="reference"> Bible reference: ' + questionCard.reference + '</span>';
    }
    
    else if(chosen.length > 1)
        alert('Cheater, cheater, CHEATER! (Probably. Sorry if this is really my fault because it\'s actually a bug.)');
    else {
        modal.style.display = "block";
        let modalContent = document.getElementById('modal-content');
        modalContent.setAttribute('class', 'modal-content');
        let modalText = document.getElementById('modal-text');
        modalText.innerHTML = '<h2>No answer selected.</h2><br>Please choose an answer first.';
    }
    document.getElementById('question').classList.remove('unanswered');
    event.preventDefault();
};
