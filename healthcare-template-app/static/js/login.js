document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent default form submission

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    const errorModal = document.getElementById('errorModal');

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            window.location.href = '/profile'; // Redirect on successful login
        } else {
            // Display error message and remaining attempts
            errorModal.textContent = `${result.message}. You have ${result.remaining_attempts} remaining login attempts.`;
            errorModal.classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorModal.textContent = 'An error occurred. Please try again.';
        errorModal.classList.remove('hidden');
    });
});
