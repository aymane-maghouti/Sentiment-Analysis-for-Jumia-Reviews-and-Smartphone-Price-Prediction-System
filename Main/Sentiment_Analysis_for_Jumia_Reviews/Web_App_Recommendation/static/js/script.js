function ajouterCommentaire(idProduit) {
    var commentaire = document.querySelector(`#produit${idProduit} textarea[name="texte_commentaire"]`).value;

    // Vérifier si le champ de commentaire est vide
    if (commentaire.trim() === '') {
        alert('Please enter a comment before adding.');
        return;
    }

    // Envoi du commentaire au serveur
    fetch('/ajouter_commentaire', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `id_prod=${idProduit}&texte_commentaire=${commentaire}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Comment added successfully');
            // Vider le champ de commentaire
            document.querySelector(`#produit${idProduit} textarea[name="texte_commentaire"]`).value = '';
            // Rafraîchir la page
            location.reload();
        } else {
            alert('Error adding comment');
        }
    })
    .catch(error => console.error('Erreur:', error));
}


function verifierRecommandation(idProduit) {
    // Envoi de l'ID du produit au serveur pour la vérification de recommandation
    fetch('/verifier_recommandation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `id_prod=${idProduit}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.Recommandation !== undefined) {
            alert(data.Recommandation);  // Display the recommendation message
        } else {
            alert('Error checking recommendation.');
        }
    })
    .catch(error => console.error('Erreur:', error));
}

