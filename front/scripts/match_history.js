document.addEventListener('DOMContentLoaded', () => {
    fetch('https://mikocchidesu.pythonanywhere.com/api/results')
        .then(response => response.json())
        .then(data => {
            const matchHistoryContainer = document.getElementById('matchHistoryContainer');

            data.forEach(match => {
                const matchDiv = document.createElement('div');
                matchDiv.className = 'match';
                matchDiv.style.backgroundColor = game_color(match.gold_grade);

                const matchHeader = document.createElement('div');
                matchHeader.className = 'match-header';
                matchHeader.textContent = `Match: ${match.match_id} - ${match.champ} vs ${match.laner} - Win: ${match.win ? 'Yes' : 'No'} - Grade: ${match.gold_grade}`;
                matchDiv.appendChild(matchHeader);

                Object.keys(match).forEach(key => {
                    if (key === '10' || key === '15') {
                        const timeFrameDiv = document.createElement('div');
                        timeFrameDiv.className = 'time-frame';
                        timeFrameDiv.textContent = `${key} minutes stats:`;

                        const toggleButton = document.createElement('button');
                        toggleButton.textContent = 'Toggle Stats';
                        toggleButton.onclick = function () {
                            const statsDivs = timeFrameDiv.querySelectorAll('.stat');
                            statsDivs.forEach(div => {
                                div.style.display = div.style.display === 'none' ? 'block' : 'none';
                            });
                            this.textContent = this.textContent.includes('Hide') ? 'Show Stats' : 'Hide Stats';
                        };
                        timeFrameDiv.appendChild(toggleButton);

                        const statsList = ['gold_difference', 'level_difference', 'cs_diff', 'cspm', 'avg_gold_diff'];
                        statsList.forEach(stat => {
                            const statDiv = document.createElement('div');
                            statDiv.className = 'stat';
                            statDiv.textContent = `${stat.replace('_', ' ')}: ${match[key][stat]}`;
                            statDiv.style.display = 'none'; // Start with stats hidden
                            timeFrameDiv.appendChild(statDiv);
                        });

                        matchDiv.appendChild(timeFrameDiv);
                    }
                });

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
