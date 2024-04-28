document.addEventListener('DOMContentLoaded', () => {
    // Fetch the match history data from your API
    fetch('https://mikocchidesu.pythonanywhere.com/api/results')
    .then(response => response.json())  // Convert the returned response into JSON
    .then(data => {
        // Handle the data
        console.log(data); // Log the data to the console

        // Get the container where the match history will be appended
        const matchHistoryContainer = document.getElementById('matchHistoryContainer');

        // Iterate over each match in the data object
        Object.keys(data).forEach(key => {
            const match = data[key];
            
            // Create a new div element for this match
            const matchDiv = document.createElement('div');
            matchDiv.className = 'match';
            matchDiv.style.backgroundColor = game_color(match); // Color code: blue for win, red for loss

            // Create a div to display champion vs. champion information
            const myChamp = document.createElement('div');
            myChamp.className = 'match-history-stat'
            myChamp.textContent = `${match.champ} vs ${match.lanerChamp}`;  // Correctly set textContent to myChamp
            matchDiv.appendChild(myChamp); 

            // Create a new div for CS per minute and add it to the match div
            const csPerMinuteDiv = document.createElement('div');
            csPerMinuteDiv.className = 'match-history-stat'
            csPerMinuteDiv.textContent = `CS per minute: ${match.cs_per_minute.toFixed(2)}`;
            matchDiv.appendChild(csPerMinuteDiv);

            // Create a new div for gold difference and add it to the match div
            const goldDiffDiv = document.createElement('div');
            goldDiffDiv.className = 'match-history-stat'
            goldDiffDiv.textContent = `Gold difference: ${match.gold_difference}`;
            matchDiv.appendChild(goldDiffDiv);

            // Create a new div for CS difference and add it to the match div
            const csDiffDiv = document.createElement('div');
            csDiffDiv.className = 'match-history-stat'
            csDiffDiv.textContent = `CS difference: ${match.cs_difference}`;
            matchDiv.appendChild(csDiffDiv);

            const acScoreDiv = document.createElement('div');
            acScoreDiv.className = 'match-history-stat'
            acScoreDiv.textContent = `AC score: ${match.ac_score}`;
            matchDiv.appendChild(acScoreDiv);

            const laneDiffDiv = document.createElement('div');
            laneDiffDiv.className = 'match-history-stat';
            //laneDiffDiv.style.backgroundColor = game_color(match);
            laneDiffDiv.textContent = bad_or_good(match);
            matchDiv.appendChild(laneDiffDiv);

            // Append the complete match div to the container
            matchHistoryContainer.appendChild(matchDiv);
        });
    })
    .catch(error => {
        // Handle any errors that occur during the fetch
        console.error('Error fetching data:', error);
        const matchHistoryContainer = document.getElementById('matchHistoryContainer');
        matchHistoryContainer.textContent = 'Failed to load data'; // Provide error text directly in the container
    });
});

function game_color(match){
    let color = "";
    switch(match.ac_score) {
        case 1:     color ='#FF0000'; break;
        case 2:     color ='#E60A00'; break;
        case 3:     color ='#CC1400'; break;
        case 4:     color ='#B31F00'; break;
        case 5:     color ='#992900'; break;
        case 6:     color ='#803400'; break;
        case 7:     color ='#4D4A00'; break;
        case 8:     color ='#335400'; break;
        case 9:     color ='#1A6900'; break;
        case 10:    color ='#1A6900'; break;
        default:    color ='000000'; break;
    }
    return color
}

function lane_diff_color(match){
    let color = "";
    if (acScore_difference <= 0){
        color = "#e60000"
    }
    else {
        color = "#2D79FF"
    }
}

function bad_or_good(match){
    if (match.ac_score_difference <= 0){
        return "LOSER"
    }
    else if (match.ac_score_difference > 0 && match.ac_score_difference <= 3){
        return "EVEN"
    }
    else if (match.ac_score_difference > 3){
        return "GG"
    }
    else return "BAG"
}

/* chat gpt
 case 1:     color ='#FF0000'; break;
        case 1:     color ='#FF0000'; break;
        case 2:     color ='#E60A00'; break;
        case 3:     color ='#CC1400'; break;
        case 4:     color ='#B31F00'; break;
        case 5:     color ='#992900'; break;
        case 6:     color ='#803400'; break;
        case 7:     color ='#663F00'; break;
        case 8:     color ='#4D4A00'; break;
        case 9:     color ='#335400'; break;
        case 10:    color ='#1A6900'; break;
    }

*/

/* moje
    case 1:     color ='#990000	 '; break;
    case 2:     color ='#cc0000 '; break;
    case 3:     color ='#ff0000 '; break;
    case 4:     color ='#ff3333'; break;
    case 5:     color ='#e6b800 '; break;
    case 6:     color ='#ffcc00 '; break;
    case 7:     color ='#ffd11a'; break;
    case 8:     color ='#00cc00'; break;
    case 9:     color ='#00b300'; break;
    case 10:    color ='#009900'; break;



*/ 
