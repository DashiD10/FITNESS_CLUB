// Basic JavaScript for the fitness club
console.log('Fitness Club JS loaded');

// Example function
function greetUser() {
    alert('Welcome to our Fitness Club!');
}

// Dynamic loading of services based on trainer selection
function loadServices(trainerId) {
    if (!trainerId) {
        document.getElementById('id_services').innerHTML = '';
        return;
    }

    fetch(`/api/trainer/${trainerId}/services`)
        .then(response => response.json())
        .then(data => {
            const servicesSelect = document.getElementById('id_services');
            servicesSelect.innerHTML = '';
            data.services.forEach(service => {
                const option = document.createElement('option');
                option.value = service.id;
                option.textContent = service.name;
                servicesSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading services:', error);
        });
}

// Add event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');

    // Check if we're on the create order page
    const trainerSelect = document.getElementById('id_trainer');
    if (trainerSelect) {
        trainerSelect.addEventListener('change', function() {
            loadServices(this.value);
        });
    }
});
