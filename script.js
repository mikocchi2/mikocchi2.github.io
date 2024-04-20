document.addEventListener('DOMContentLoaded', () => {
    // Fetch the match history data from your API
    fetch('https://243c-79-101-36-217.ngrok-free.app/api/games')
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
            matchDiv.style.backgroundColor = match.win ? '#5383e8' : '#ff5555'; // Color code: blue for win, red for loss

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

