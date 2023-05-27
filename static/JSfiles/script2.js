function validate_password() {
 
    var pass = document.getElementById('pass').value;
    var confirm_pass = document.getElementById('confirm_pass').value;
    if (pass != confirm_pass) {
        document.getElementById('wrong_pass_alert').style.color = 'red';
        document.getElementById('wrong_pass_alert').innerHTML= '<h3>Use same password</h3>';
        document.getElementById('create').disabled = true;  // user cannot click on the submit button until password matches
        document.getElementById('create').style.opacity = (0.4);
    } 
    else {
        document.getElementById('wrong_pass_alert').style.color = 'green';
        document.getElementById('wrong_pass_alert').innerHTML ='<h3>password matched</h3>';
        document.getElementById('create').disabled = false; // user can now use the submit button to sign up
        document.getElementById('create').style.opacity = (1);
    }
}
function wrong_pass_alert() {
    if (document.getElementById('pass').value != "" &&
        document.getElementById('confirm_pass').value != "") {
        alert("Your response is submitted");
    } else {
        alert("Please fill all the fields");
    }
}