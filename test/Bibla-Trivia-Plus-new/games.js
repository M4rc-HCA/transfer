'use strict';

var ajv = new Ajv(); // Import Ajv.

// Load all cards
var categories = JSON.parse(cardsJSON);
var cardsSchema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [ "name", "title", "deck" ],
        "properties": {
            "name": { "type": "string" },
            "title": { "type": "string" },
            "deck": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {
                            "type": "object",
                            "additionalProperties": false,
                            "required": [ "questionType", "question", "questionTags", "answer", "answerTags", "reference" ],
                            "properties": {
                                "questionType": {
                                    "type": "string",
                                    "enum": [ "tagged", "numeric" ]
                                },
                                "question": { "type": "string" },
                                "questionTags": {
                                    "type": "array",
                                    "items": { "type": "string" },
                                },
                                "answer": { "type": "string" },
                                "answerTags": {
                                    "type": "array",
                                    "items": { "type": "string" }
                                },
                                "reference": { "type": "string" }
                            }
                        },
                        {
                            "type": "object",
                            "additionalProperties": false,
                            "required": [ "questionType", "question", "unitSingular", "answer", "minPlausible", "maxPlausible", "reference" ],
                            "properties": {
                                "questionType": {
                                    "type": "string",
                                    "enum": [ "numeric" ]
                                },
                                "question": { "type": "string" },
                                "answer": { "type": "string" },
                                "minPlausible": { "type": "number" },
                                "maxPlausible": { "type": "number" },
                                "unitSingular": { "type": "string" },
                                "unitPlural": { "type": "string" },
                                /*TODO: "plausibleDistribution" */
                                "reference": { "type": "string" }
                            }
                        },
                        {
                            "type": "object",
                            "additionalProperties": false,
                            "required": [ "questionType", "question", "answer", "listOfAnswers", "reference" ],
                            "properties": {
                                "questionType": {
                                    "type": "string",
                                    "enum": [ "predefined" ]
                                },
                                "question": { "type": "string" },
                                "answer": { "type": "string" },
                                "listOfAnswers": {
                                    "type": "array",
                                    "items": { "type": "string" },
                                },
                                "overload": { "type": "string" },
                                /*TODO: "plausibleDistribution" */
                                "reference": { "type": "string" }
                            }
                        }
                    ]
                }
            }
        }
    }
};
if(!ajv.validate(cardsSchema, categories))
    console.log('Invalid cards JSON: ' + JSON.stringify(ajv.errors));

// Process answer tags
var tagMap = new Map();
{
    let addAnswerToTag = function(tag, answer) {
        let tagSet = tagMap.get(tag);
        if(!tagSet) {
            tagSet = new Set();
            tagMap.set(tag, tagSet);
        }

        tagSet.add(answer);
    };
    for(let catX = 0; catX < categories.length; ++catX) {
        let deck = categories[catX].deck;
        for(let cardX = 0; cardX < deck.length; ++cardX) {
            let card = deck[cardX];
            if(card.questionType === "tagged"){
                for(let qTagX = 0; qTagX < card.questionTags.length; ++qTagX) {
                    addAnswerToTag(card.questionTags[qTagX], card.answer);
                }
                for(let aTagX = 0; aTagX < card.answerTags.length; ++aTagX) {
                    addAnswerToTag(card.answerTags[aTagX], card.answer);
                }
            }
        }
    }
}

// A master container to hold our splicable decks
var fresh = []; // a master list to hold our lists of decks

for(let x=0; x < categories.length; ++x){ // initaites an empty list for every category
    fresh.push([]);
}

// Prep deck of numbers to be spliced from and insert into master container called fresh
function prepDeck(catX){
    fresh[catX] = [];
    let deckLength =  categories[catX].deck.length;
    for(let cardX = 0; cardX < deckLength; ++cardX){
        fresh[catX][cardX] = cardX;
    }
}

// Draw a card from a specific deck - shuffle if the length of the deck is 0
function draw(catX){
    // if the deck is empty, we prep it and fill it with data
    if (fresh[catX].length == 0) {
        prepDeck(catX);
    }

    // freshX is just a random number that is selected in comparison to the lenth of the deck
    let freshX = Math.floor(Math.random()*fresh[catX].length);
    // cardX is the actual card drawn from the deck, a splice is performed to remove that it from the master list
    let cardX = fresh[catX].splice(freshX, 1)[0];
    return categories[catX].deck[cardX];
}

function drawSeveral(catX, drawCount) {
    let realDraw = draw(catX); // Choose a random question card.
    let shuffledHand = [ realDraw.answer ]; // Include the real answer.
    if(drawCount > 1){

        switch(realDraw.questionType) {
            case 'tagged': {
                if(realDraw.questionTags.length >= 1) {
                    // Get all of the question's tags' answer sets, making note of which is smallest:
                    let smallestSet = tagMap.get(realDraw.questionTags[0]);
                    let largerSets = new Array(realDraw.questionTags.length-1);
                    for(let qTagX = 1; qTagX < realDraw.questionTags.length; ++qTagX) {
                        let tagSet = tagMap.get(realDraw.questionTags[qTagX]);
                        if(!(tagSet.size >= smallestSet.size)) {
                            let swap = smallestSet;
                            smallestSet = tagSet;
                            tagSet = swap;
                        }
                        largerSets[qTagX-1] = tagSet;
                    }

                    // Compute the intersection of the question's tags' answer sets:
                    let plausibleSet = new Set(smallestSet); // Start with a shallow copy, to avoid modifying the original tag set.
                    for(let largeX = 0; largeX < largerSets.length; ++largeX) {
                        let largerSet = largerSets[largeX];
                        for(let answer of plausibleSet) {
                            if(!largerSet.has(answer))
                                plausibleSet.remove(answer);
                        }
                    }

                    // Convert the plausible answer set to an array so that we can get answers by numerical index:
                    let plausible = Array.from(plausibleSet);

                    // Limit the number of answers to a number that can be quickly and reliably retrieved:
                    if(drawCount*3 > plausible.length*2)
                        drawCount = Math.floor(plausible.length*2/3);

                    if(drawCount > 1) {
                        // Fill out the hand with random plausible wrong answers:
                        let hand = new Set(shuffledHand);
                        shuffledHand.length = drawCount;
                        let shuffledX = 1;
                        while(hand.size < drawCount) {
                            // TODO: Fix infinite run-time worst case.
                            let answer = plausible[Math.floor(Math.random()*plausible.length)];
                            if(!hand.has(answer)) {
                                hand.add(answer);
                                shuffledHand[shuffledX] = answer;
                                ++shuffledX;
                            }
                        }

                        // Swap the real answer into a random location in the hand:
                        shuffledX = Math.floor(Math.random()*drawCount);
                        shuffledHand[0] = shuffledHand[shuffledX];
                        shuffledHand[shuffledX] = realDraw.answer;
                    }
                }
                break;
            }
            case 'numeric': {
                // Fill out the hand with random plausible wrong answers:
                let hand = new Set(shuffledHand);
                shuffledHand.length = drawCount;
                let shuffledX = 1;
                while(hand.size < drawCount) {
                    // TODO: Fix infinite run-time worst case.
                    let randomNumber = Math.floor(Math.random() * 
                    (realDraw.maxPlausible - realDraw.minPlausible) + realDraw.minPlausible);
                    let unit = (randomNumber == 1)? realDraw.unitSingular : realDraw.unitPlural;
                    let answer = randomNumber.toString() + " " + unit;

                    if(!hand.has(answer)) {
                        hand.add(answer);
                        shuffledHand[shuffledX] = answer;
                        ++shuffledX;
                    }
                }

                // Swap the real answer into a random location in the hand:
                shuffledX = Math.floor(Math.random()*drawCount);
                shuffledHand[0] = shuffledHand[shuffledX];
                shuffledHand[shuffledX] = realDraw.answer;
                break;
            }
            case 'predefined': {
                let shuffledX = 1;
                let plausible = Array.from(realDraw.listOfAnswers);

                // Override the size of the return hand to include all answers
                if(realDraw.overload === "yes"){
                    drawCount = plausible.length + 1;
                }

                // if there are less answers than drawCount adjust
                if(plausible.length < (drawCount-1)){
                    drawCount = plausible.length + 1;
                }
                shuffledHand.length = drawCount;

                while(shuffledX < drawCount) {
                    let randomNumber = Math.floor(Math.random() * plausible.length);
                    shuffledHand[shuffledX] = plausible.splice(randomNumber,1)[0];
                    ++shuffledX;
                }

                // Swap the real answer into a random location in the hand:
                shuffledX = Math.floor(Math.random()*drawCount);
                shuffledHand[0] = shuffledHand[shuffledX];
                shuffledHand[shuffledX] = realDraw.answer;
                break;
            }
            default: 
                Console.log('Error: Unknown question type.');
        }
    }
    return [ realDraw, shuffledHand ];
}

// Game board
var board = JSON.parse(boardJSON);
var boardSchema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "additionalProperties": false,
    "required": [ "startPath", "startSpot", "paths" ],
    "properties": {
        "startPath": { "type": "string" },
        "startSpot": { "type": "integer" },
        "paths": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": false,
                "required": [ "name", "count", "isCircular", "bidirectional", "bridges", "pins" ],
                "properties": {
                    "name": { "type": "string" },
                    "count": { "type": "integer" },
                    "isCircular": { "type": "boolean" },
                    "bidirectional": { "type": "boolean" },
                    "bridges": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": false,
                            "required": [ "fromSpot", "toPath", "toSpot" ],
                            "properties": {
                                "fromSpot": { "type": "integer" },
                                "toPath": { "type": "string" },
                                "toSpot": { "type": "integer" }
                            }
                        }
                    },
                    "pins": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": false,
                            "required": [ "spot", "x", "y" ],
                            "properties": {
                                "spot": { "type": "integer" },
                                "x": { "type": "number" },
                                "y": { "type": "number" }
                            }
                        }
                    }
                }
            }
        }
    }
};
if(!ajv.validate(boardSchema, board))
    console.log('Invalid board JSON: ' + JSON.stringify(ajv.errors));

class Spot {
    constructor() {
        this.next = null;
        this.back = null;
        this.bridge = null;
    }
}

var startSpot = null;
{
    let mapOfPaths = new Map();

    // create paths and fill with spots
    for(let p = 0; p < board.paths.length; ++p) {
        let currentPath = board.paths[p];
        let pathSpots = new Array(currentPath.count);

        if(pathSpots.length >= 1) {
            for(let s = 0; s < pathSpots.length; ++s)
                pathSpots[s] = new Spot();

            // create intrapath links
            for(let s = 1; s < pathSpots.length; ++s) {
                pathSpots[s - 1].next = pathSpots[s];
                if(currentPath.bidirectional)
                    pathSpots[s].back = pathSpots[s - 1];
            }
            if(currentPath.isCircular) {
                pathSpots[pathSpots.length - 1].next = pathSpots[0];
                if(currentPath.bidirectional)
                    pathSpots[0].back = pathSpots[pathSpots.length - 1];
            }
        }

        mapOfPaths.set(currentPath.name, pathSpots);
    }


    // find bridge data and link paths and bridges
    for(let p = 0; p < board.paths.length; ++p){
        let currentPath = board.paths[p];
        let pathSpots = mapOfPaths.get(currentPath.name);
        for(let b =0; b < currentPath.bridges.length; ++b){
            let currentBridge = currentPath.bridges[b];
            pathSpots[currentBridge.fromSpot].bridge = mapOfPaths.get(currentBridge.toPath)[currentBridge.toSpot];
        }
    }

    startSpot = mapOfPaths.get(board.startPath)[board.startSpot];
}
