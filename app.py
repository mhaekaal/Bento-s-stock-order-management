import os
import streamlit as st
import json
from PIL import Image

# Path ke file products.json dan folder images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Direktori tempat app.py berada
PRODUCTS_JSON_PATH = os.path.join(BASE_DIR, 'products.json')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

@st.cache_data
def load_products():
    if not os.path.exists(PRODUCTS_JSON_PATH):
        st.error(f"File tidak ditemukan: {PRODUCTS_JSON_PATH}")
        return []
    with open(PRODUCTS_JSON_PATH, 'r') as f:
        products = json.load(f)
    return products

def save_products(products):
    with open(PRODUCTS_JSON_PATH, 'w') as f:
        json.dump(products, f, indent=4)

def main():
    st.title("Manajemen Stok dan Pemesanan Barang")

    products = load_products()

    # Sidebar for navigation
    st.sidebar.title("Navigasi")
    menu = st.sidebar.radio("Menu", ["Lihat Stok", "Pesan Barang", "Tambah Produk"])

    if menu == "Lihat Stok":
        st.header("Daftar Stok Barang")
        for product in products:
            st.write(f"**{product['name']}**")
            st.write(f"Harga: Rp {product['price']:,}")
            st.write(f"Stok: {product['stock']}")
            image_path = os.path.join(IMAGES_DIR, os.path.basename(product['image']))
            st.image(image_path, width=150)
            st.write("---")

    elif menu == "Pesan Barang":
        st.header("Pesan Barang")
        selected_products = []
        total_price = 0

        for product in products:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**{product['name']}**")
                st.write(f"Harga: Rp {product['price']:,}")
                st.write(f"Stok: {product['stock']}")
                image_path = os.path.join(IMAGES_DIR, os.path.basename(product['image']))
                st.image(image_path, width=150)
            with col2:
                quantity = st.number_input(f"Jumlah {product['name']}", 0, product['stock'], key=product['id'])
                if quantity > 0:
                    selected_products.append({
                        "id": product['id'],
                        "name": product['name'],
                        "price": product['price'],
                        "quantity": quantity
                    })
                    total_price += product['price'] * quantity

        if selected_products:
            st.write("### Ringkasan Pesanan")
            for item in selected_products:
                st.write(f"{item['name']} x {item['quantity']} = Rp {item['price'] * item['quantity']:,}")
            st.write(f"**Total Pembayaran: Rp {total_price:,}**")

            if st.button("Konfirmasi Pesanan"):
                for item in selected_products:
                    for product in products:
                        if product['id'] == item['id']:
                            product['stock'] -= item['quantity']
                save_products(products)
                st.success("Pesanan berhasil dikonfirmasi!")

    elif menu == "Tambah Produk":
        st.header("Tambah Produk Baru")
        with st.form("tambah_produk_form"):
            name = st.text_input("Nama Produk")
            price = st.number_input("Harga Produk", min_value=0)
            stock = st.number_input("Stok Produk", min_value=0)
            image = st.file_uploader("Gambar Produk", type=["jpg", "jpeg", "png"])
            submitted = st.form_submit_button("Tambah Produk")

            if submitted:
                if image is not None:
                    image_path = os.path.join(IMAGES_DIR, image.name)
                    with open(image_path, "wb") as f:
                        f.write(image.getbuffer())
                    new_product = {
                        "id": len(products) + 1,
                        "name": name,
                        "price": price,
                        "stock": stock,
                        "image": f"images/{image.name}"
                    }
                    products.append(new_product)
                    save_products(products)
                    st.success("Produk berhasil ditambahkan!")
                else:
                    st.error("Harap upload gambar produk.")

if __name__ == "__main__":
    main()
