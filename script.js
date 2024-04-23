
// send Ag to server
function sendData() {
    const userInput = document.getElementById('summoner_entry').value;

    var sumname = [s1, s2] = splitStringByHash(userInput); 

    const url = 'mikocchiDesu.pythonanywhere.com/api/users';
    const params = {
        game_name:  sumname[0],
        tagline: sumname[1]
    };
    
    // Create the URL with query parameters
    const query = new URLSearchParams(params).toString();
    const fullUrl = `${url}?${query}`;
    console.log(fullUrl)
    // Make a GET request with the query parameters
    fetch(fullUrl)
        .then(response => response.text())  // Convert the response to text
        .then(text => {
            console.log(text)
        })    // Log the text to the console
        .catch(error => console.error('Error:', error));
        
}

function splitStringByHash(inputString) {
    // Use the split() method to divide the string at the first occurrence of '#'
    var parts = inputString.split('#', 2); // Limit to 2 parts to ensure only the first '#' is considered

    // Initialize s1 and s2
    var s1 = parts[0];
    var s2 = parts.length > 1 ? parts[1] : ""; // Check if there is a part after '#'
    
    return [s1, s2];  // Return as an array
}

function viewResults() {
    window.location.href = '/matchHistory.html';
}

