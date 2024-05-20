function toggleEdit(field) {
    document.getElementById(`${field}-display`).classList.toggle('d-none');
    document.getElementById(`${field}-form`).classList.toggle('d-none');
}

function updateProfile(field) {
    const form = document.getElementById(`${field}-form`);
    const formData = new FormData(form);

    fetch('/profile/update/', {
        method: 'POST',
        body: new URLSearchParams(formData), // Ensure data is sent in correct format
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`${field}-display`).innerText = formData.get(field);
            toggleEdit(field);
        } else {
            console.error(data.errors);
            alert('Error updating profile');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating profile');
    });
}