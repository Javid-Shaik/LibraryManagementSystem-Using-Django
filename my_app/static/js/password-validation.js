// Select the password input field and the form
const passwordInput = document.querySelector('input[name="password"]');
const form = document.querySelector('form');

// Function to validate the password
function validatePassword(password) {
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return passwordPattern.test(password);
}

// Function to handle form submission
function handleSubmit(event) {
  const password = passwordInput.value;

  if (!validatePassword(password)) {
    event.preventDefault(); // Prevent form submission
    alert('Password must be at least 8 characters and include at least one uppercase letter, one lowercase letter, one number, and one special symbol.');
  }
}

// Attach event listener to form submission
form.addEventListener('submit', handleSubmit);
