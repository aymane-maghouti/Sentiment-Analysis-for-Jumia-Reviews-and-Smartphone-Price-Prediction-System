from flask import Flask, render_template, redirect, request, jsonify
import mysql.connector
from comments_classification import analyze_sentiment
from translate_comment import translate_french_to_english



app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aymane2002",
    database="product_db")


@app.route('/')
def afficher_produits():
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT p.id_product, p.nom, p.description, p.image_url, c.text AS commentaire_text FROM produit p LEFT JOIN commentaire c ON p.id_product = c.id_prod order by p.id_product')
    result = cursor.fetchall()
    produits = {}

    for row in result:
        if row['id_product'] not in produits:
            produits[row['id_product']] = {
                'id': row['id_product'],
                'nom': row['nom'],
                'description': row['description'],
                'image_url': row['image_url'],
                'commentaires': []
            }

        if row['commentaire_text']:
            produits[row['id_product']]['commentaires'].append(row['commentaire_text'])

    cursor.close()
    db.commit()

    return render_template('index.html', produits=list(produits.values()))




@app.route('/ajouter_commentaire', methods=['POST'])
def ajouter_commentaire():
    id_prod = request.form.get('id_prod')
    texte_commentaire = request.form.get('texte_commentaire')

    commentaire = translate_french_to_english(texte_commentaire)
    cursor = db.cursor()

    requete_insertion = "INSERT INTO commentaire (text, id_prod) VALUES (%s, %s)"

    donnees_insertion = (commentaire, id_prod)

    try:
        cursor.execute(requete_insertion, donnees_insertion)
        cursor.close()
        db.commit()
        return jsonify(success=True)
    except Exception as e:
        print(f"Erreur lors de l'ajout du commentaire : {e}")
        cursor.close()
        db.rollback()
        return jsonify(success=False)



@app.route('/verifier_recommandation', methods=['POST'])
def verifier_recommandation():
    id_prod = request.form.get('id_prod')
    result = analyze_sentiment(int(id_prod))
    print(result)
    return jsonify({'Recommandation': result})

if __name__ == '__main__':
    app.run(debug=True)

