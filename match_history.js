document.addEventListener('DOMContentLoaded', () => {
    fetch('https://mikocchidesu.pythonanywhere.com/api/results')
        .then(response => response.json())
        .then(data => {
            const matchHistoryContainer = document.getElementById('matchHistoryContainer');

            data.forEach(match => {
                const matchDiv = document.createElement('div');
                matchDiv.className = 'match';
                matchDiv.style.backgroundColor = game_color(match.gold_grade); // Assume game_color now uses gold_grade

                // Add basic match info
                const matchInfo = document.createElement('div');
                matchInfo.textContent = `Match ID: ${match.match_id}, Champion: ${match.champ} vs ${match.laner}, Win: ${match.win}`;
                matchDiv.appendChild(matchInfo);

                // Add stats for each timeframe
                Object.keys(match).forEach(key => {
                    if (key === '10' || key === '15') { // Extendable to other time points
                        const timeFrame = match[key];

                        const timeFrameDiv = document.createElement('div');
                        timeFrameDiv.className = 'time-frame';
                        timeFrameDiv.textContent = `${key} minutes stats:`;

                        // Create divs for each stat in this time frame
                        const statsList = ['gold_difference', 'level_difference', 'cs_diff', 'cspm', 'avg_gold_diff'];
                        statsList.forEach(stat => {
                            const statDiv = document.createElement('div');
                            statDiv.className = 'stat';
                            statDiv.textContent = `${stat.replace('_', ' ')}: ${timeFrame[stat]}`;
                            timeFrameDiv.appendChild(statDiv);
                        });

                        matchDiv.appendChild(timeFrameDiv);
                    }
                });

                // Append the complete match div to the container
                matchHistoryContainer.appendChild(matchDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            matchHistoryContainer.textContent = 'Failed to load data';
        });
});

// Updated game_color function based on gold_grade
function game_color(grade){
    switch(grade) {
        case 0: return '#990000';
        case 1: return '#cc0000';
        case 2: return '#ff0000';
        case 3: return '#ff3333';
        case 4: return '#e6b800';
        case 5: return '#ffcc00';
        case 6: return '#ffd11a';
        case 7: return '#00cc00';
        case 8: return '#00b300';
        case 9: return '#009900';
        case 10: return '#1A6900';
        default: return '#000000'; // default case to handle unexpected grades
    }
}
