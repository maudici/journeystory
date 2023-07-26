document.getElementById('story-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the user's input from the form
    var name = document.getElementById('name').value;
    var currentCity = document.getElementById('current-city').value;
    var birthCity = document.getElementById('birth-city').value;
    var fact1 = document.getElementById('fact1').value;
    var fact2 = document.getElementById('fact2').value;
    var fact3 = document.getElementById('fact3').value;

    // Call the backend to generate the story
    generateStory(name, currentCity, birthCity, fact1, fact2, fact3);
});

document.getElementById('demo-button').addEventListener('click', function() {
    // Set the demo values, these facts are not true, so don't even try. 
    var name = "Daniel";
    var currentCity = "Portland, Oregon, United States";
    var birthCity = "Bogota, Colombia";
    var fact1 = "I moved from Colombia to Miami when I was 17";
    var fact2 = "I moved from Miami to Gainesville for College when I was 18";
    var fact3 = "I lived in Gainesville for 5 years, then moved to Portland and I have been there for 5 years.";

    // Call the backend to generate the story
    generateStory(name, currentCity, birthCity, fact1, fact2, fact3);
});

function generateStory(name, currentCity, birthCity, fact1, fact2, fact3) {
    // Show the loading message and spinner
    document.getElementById('loading-message').style.display = 'block';
    document.getElementById('spinner').style.display = 'block';

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            currentCity: currentCity,
            birthCity: birthCity,
            facts: [fact1, fact2, fact3]
        })
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loading message and spinner
        document.getElementById('loading-message').style.display = 'none';
        document.getElementById('spinner').style.display = 'none';

        // Display the story and images on the page
        var storyContainer = document.getElementById('story');
        storyContainer.textContent = '';
        data.story.forEach(function(part, index) {
            var div = document.createElement('div');
            div.className = 'story-part';

            var p = document.createElement('p');
            p.textContent = part;
            div.appendChild(p);
    
            var img = document.createElement('img');
            img.src = data.image[index];
            div.appendChild(img);

            storyContainer.appendChild(div);
        });
    });
}
