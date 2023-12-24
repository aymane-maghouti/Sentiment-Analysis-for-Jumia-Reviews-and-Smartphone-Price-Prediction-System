function predictPrice() {
    // Récupérer les valeurs des champs du formulaire
    var brand = document.getElementById("brand").value;
    var screen_size = parseFloat(document.getElementById("screen_size").value);
    var ram = parseInt(document.getElementById("ram").value);
    var rom = parseInt(document.getElementById("rom").value);
    var sim_type = document.getElementById("sim_type").value;
    var battery = parseInt(document.getElementById("battery").value);

    // Envoyer les données au serveur Flask pour prédiction
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            brand: brand,
            screen_size: screen_size,
            ram: ram,
            rom: rom,
            sim_type: sim_type,
            battery: battery,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Afficher le résultat au client
        document.getElementById("predictedPrice").textContent = 'Price Estimation : ' + data.predicted_price.toFixed(2) + ' DHS';
        document.getElementById("result").style.display = 'block';

        // Réinitialiser les champs du formulaire
        document.getElementById("brand").value = '';
        document.getElementById("screen_size").value = '';
        document.getElementById("ram").value = '';
        document.getElementById("rom").value = '';
        document.getElementById("sim_type").value = '';
        document.getElementById("battery").value = '';
    })
    .catch(error => console.error('Erreur lors de la prédiction :', error));
}
