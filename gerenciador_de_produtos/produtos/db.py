from pymongo import MongoClient
from configs import database_products

# Conecta ao MongoDB
client = MongoClient(database_products)
mydb = client.myproducts
mycol = mydb.products  # Corrigido para refletir o nome da coleção

def add_product(product_id, name, price, image):
    existing_product = mycol.find_one({"product_id": product_id})
    
    if existing_product:
        return "Este ID já existe."
    
    products = {
        "product_id": product_id,
        "infos": {
            "name": name,
            "price": price,
            "image": image
        }
    }

    result = mycol.insert_one(products)
    return 'Produto adicionado com sucesso.'

def edit_product(product_id, new_name, new_price, new_image):
    query = {"product_id": product_id}
    
    new_values = {
        "$set": {
            "infos.name": new_name,
            "infos.price": new_price,
            "infos.image": new_image
        }
    }

    result = mycol.update_one(query, new_values)
    
    if result.modified_count > 0:
        return f"Infos do produto: {new_name} atualizado com sucesso!"
    else:
        return f"Nenhum produto encontrado com o ID: {product_id}."

def delete_product(product_id):
    query = {"product_id": product_id}
    
    result = mycol.delete_one(query)
    
    if result.deleted_count > 0:
        return f"Produto do ID: {product_id} removido com sucesso!"
    else:
        return f"Nenhum produto encontrado com o ID: {product_id}."
    
def view_products():
    # Recupera todos os documentos na coleção
    products = mycol.find()
    
    # Verifica se há produtos na coleção (utilizando uma listagem do cursor)
    product_list = list(products)
    
    if not product_list:
        return "Nenhum produto encontrado."
    
    # Formata os resultados
    result = []
    for product in product_list:
        result.append({
            "product_id": product["product_id"],
            "name": product["infos"]["name"],
            "price": product["infos"]["price"],
            "image": product["infos"]["image"]
        })
    
    return result

# Exemplos de uso:
# add_product(ID do produto, 'Nome', Valor, 'URL da imagem')
# edit_product(ID do Produto, 'Nome', Valor, 'URL da imagem')
# delete_product(ID do produto)
# view_products()
