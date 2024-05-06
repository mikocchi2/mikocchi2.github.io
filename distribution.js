document.addEventListener("DOMContentLoaded", function() {
    // Replace 'url-to-your-api' with the actual URL of your API
    fetch('https://mikocchidesu.pythonanywhere.com/api/results')
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Network response was not ok.');
      })
      .then(data => processData(data))
      .catch(error => console.error('Fetch error:', error));
  });
  
  function processData(data) {
    const gradeCounts = {};
    data.forEach(item => {
      // Assuming each item in your data has a 'gold_grade' field
      const grade = item.gold_grade;
      gradeCounts[grade] = (gradeCounts[grade] || 0) + 1;
    });
  
    const distributionContainer = document.getElementById('distribution');
    Object.keys(gradeCounts).sort((a, b) => a - b).forEach(grade => {
      const bar = document.createElement('div');
      bar.className = 'bar';
      bar.style.height = `${gradeCounts[grade] * 20}px`; // Adjust height scaling as needed
      distributionContainer.appendChild(bar);
  
      const label = document.createElement('div');
      label.className = 'bar-label';
      label.innerText = `${grade}`;
      bar.appendChild(label);
  
      const countText = document.createElement('div');
      countText.innerText = gradeCounts[grade];
      bar.appendChild(countText);
    });
  }
  