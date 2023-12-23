function ajouterCommentaire(idProduit) {
    var commentaire = document.querySelector(`#produit${idProduit} textarea[name="texte_commentaire"]`).value;

    // Vérifier si le champ de commentaire est vide
    if (commentaire.trim() === '') {
        alert('Veuillez saisir un commentaire avant d\'ajouter.');
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
            alert('Commentaire ajouté avec succès');
            // Vider le champ de commentaire
            document.querySelector(`#produit${idProduit} textarea[name="texte_commentaire"]`).value = '';
            // Rafraîchir la page
            location.reload();
        } else {
            alert('Erreur lors de l\'ajout du commentaire');
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
            alert('Erreur lors de la vérification de la recommandation.');
        }
    })
    .catch(error => console.error('Erreur:', error));
}

