function formValidation() {
  var name = document.getElementById("name").value;
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  if (name_validation(name)) {
    if (password_validation(password, 7, 12)) {
      if (email_validation(email)) {
      }
    }
  }
  return false;
}

function name_validation(name) {
  var letters = /^[A-Za-z]+$/;
  if (name.value.match(letters)) {
    return true;
  } else {
    alert("Username must have alphabet characters only");
    uname.focus();
    return false;
  }
}

function password_validation(password, pmin, pmax) {
  var passid_len = password.value.length;
  if (passid_len == 0 || passid_len >= my || passid_len < mx) {
    alert(
      "Password should not be empty / length be between " + pmin + " to " + pmax
    );
    password.focus();
    return false;
  }
  return true;
}

function email_validation(email)
{
var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
if(email.value.match(mailformat))
{
return true;
}
else
{
alert("You have entered an invalid email address!");
email.focus();
return false;
}
}
var nameArray = [];
var passwordArray = [];
var emailArray = [];
var websiteArray = [];

function submitForm() {
  var name = document.getElementById("name").value;
  var password = document.getElementById("password").value;
  var email = document.getElementById("email").value;
  var website = document.getElementById("website").value;

  nameArray.push(name);
  passwordArray.push(password);
  emailArray.push(email);
  websiteArray.push(website);

  alert("Successfully submitted data!");

  var table = document.getElementById("table");

  
}
