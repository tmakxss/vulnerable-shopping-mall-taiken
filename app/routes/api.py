from flask import Blueprint, request, jsonify
import sqlite3
import subprocess
import os

bp = Blueprint('api', __name__)

@bp.route('/api/products')
def api_products():
    """商品API"""
    conn = sqlite3.connect('database/shop.db')
    cursor = conn.cursor()
    
    category = request.args.get('category', '')
    
    if category:
        # SQLインジェクション脆弱性
        cursor.execute(f"SELECT * FROM products WHERE category = '{category}'")
    else:
        cursor.execute("SELECT * FROM products")
    
    products = cursor.fetchall()
    conn.close()
    
    # 商品データを辞書形式に変換
    product_list = []
    for product in products:
        product_list.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'stock': product[4],
            'category': product[5]
        })
    
    return jsonify(product_list)
