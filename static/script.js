var input = document.getElementById("guess");
var guesses = 0;
var correct = false;
var submissions = [];
console.log("aUHHH")
//populate(submissions)
$('#populator').click();


function actionOnSubmit()
  {
  
  //Get the select select list and store in a variable
  var e = document.getElementById("list_type");
  console.log(e)
  
  //Get the selected value of the select list
  var formaction = e.options[e.selectedIndex].value;
  var name = document.getElementById("username").value;
  //Update the form action
  document.form1.action = formaction + "/" + name;
  console.log(formaction)
  
  }


function populate(allAnime) {
  submissions = allAnime;
  var options = allAnime;
  $.each(allAnime, function(i, p) {
      $('#submission').append($('<option></option>').val(p).html(p));
  });
}

// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    console.log(correct)
    console.log(guesses)
    if (correct==false) {
      console.log("submitting")
      document.getElementById("submit").click();
      console.log("submitting")
    }
    else{
      document.getElementById("modalHeader").innerHTML = "LOADING...";
      console.log("resetting")
      document.getElementById("reset").click();
    }
    document.getElementById('guess').value = ''
  }
});

function postData(data) {
  document.getElementById("modalHeader").innerHTML = "LOADING...";
  console.log("resetting")
  console.log("huh")
  $("html").load("/");
  populate(data)
  console.log("populating")
  document.getElementById("populator").click();
  
  /*let addParagraph = document.createElement("ul");
  document.getElementById("resultLeft").innerHTML = "";
  console.log("uo");
  for (const [key, value] of Object.entries(data)) {
    let li = document.createElement("li");
    li.textContent = key + " - " + value;
    addParagraph.appendChild(li);
    resultLeft.appendChild(addParagraph);
  };*/
}

function guess(names, season, score, popularity, genres, studios, answers) {
  console.log(correct + "HOLY SHIT")
  console.log("bruh")
  console.log(names)
  var guess = document.getElementById("guess").value;
  for(var i = 0;i<names.length;i++){
    if (guess.toLowerCase() == names[i]){
      correct = true;
      console.log("righyoo")
    }
    console.log(guess.toLowerCase())
    console.log(names[i])
  }
  console.log(correct + "DAMN SON")
  if(correct==true){document.getElementById("result").innerHTML = "CORRECT\nGuesses Needed: " + guesses; console.log(correct); console.log("FUCK YOU"); fin(true, answers[0], answers[1])}
  else{guesses+=1; document.getElementById("result").innerHTML = "INCORRECT";}
  switch(guesses) {
  case 0:
    break;
  case 1:
    document.getElementById("season").style.color="blue";
    document.getElementById("season").innerHTML = "Season:\n" + season + "\n\nGuess: " + guess;
    break;
  case 2:
    document.getElementById("score").innerHTML = "Average Score:\n" + score + "\n\nGuess: " + guess;
    break;
  case 3:
    document.getElementById("popularity").innerHTML = "Popularity:\n" + popularity + "\n\nGuess: " + guess;
    break;
  case 4:
    document.getElementById("genres").innerHTML = "Genres:\n" + genres + "\n\nGuess: " + guess;
    break;
  case 5:
    document.getElementById("studios").innerHTML = "Studios:\n" + studios + "\n\nGuess: " + guess;
    break;
  default:
    document.getElementById("result").innerHTML = "YER OUT\n" + answers;
    correct = true;
    fin(false, answers[0], answers[1]);
    // code block
}
  
}

function fin(result, romaji, english){
  if(result){
    document.getElementById("modalHeader").innerHTML = "Correct!"
    changeCSS('green', 'modal-header', 'background-color');
    changeCSS('green', 'modal-footer', 'background-color');
  }
  else{
    document.getElementById("modalHeader").innerHTML = "Failed!"
    changeCSS('red', 'modal-header', 'background-color')
    changeCSS('red', 'modal-footer', 'background-color');
  }
  document.getElementById("answer").innerHTML = "Correct Answer: " + romaji + " - " + english;
  displayModal();
  document.activeElement.blur();
}

function changeCSS(color, element, value){
  var stylesheet = $('link#mainStyle')[0].sheet;
  let elementRules;
  console.log(stylesheet);
  // looping through all its rules and getting your rule
  for(let i = 0; i < stylesheet.cssRules.length; i++) {
    if(stylesheet.cssRules[i].selectorText === '.' + element) {
      elementRules = stylesheet.cssRules[i];
    }
  }
  
  // modifying the rule in the stylesheet
  console.log(elementRules);
  elementRules.style.setProperty(value, color);
  }

var modal = document.getElementById("myModal");

// Get the button that opens the modal
//var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
function displayModal() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}