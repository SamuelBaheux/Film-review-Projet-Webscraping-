import pandas as pd
import streamlit as st
import os

image_extensions = ["png", "jpg", "jpeg", "gif"]
trailer_links = pd.read_csv("./data/trailer_links.csv")

def get_link_by_movie_name(movie_name):
    row = trailer_links[trailer_links['Title'] == movie_name]
    if not row.empty:
        return row['TrailerLink'].values[0]
    else:
        return "Pas de lien disponible"

def main():

    st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>🍿Film Review 🎬</h1>", unsafe_allow_html=True)

    images_folder = 'images'
    images_list = os.listdir("images")

    images_list = [image for image in images_list if any(image.endswith(ext) for ext in image_extensions)]

    num_images = len(images_list)
    num_images_per_row = 4
    num_rows = (num_images - 1) // num_images_per_row + 1

    for row in range(num_rows):
        cols = st.columns(num_images_per_row)
        for col_index in range(num_images_per_row):
            image_index = row * num_images_per_row + col_index
            if image_index < num_images:
                image_path = os.path.join(images_folder, images_list[image_index])
                cols[col_index].image(image_path, use_column_width=True)
                cols[col_index].markdown(images_list[image_index].split(".jpg")[0])
                button_key = f"button_{image_index}"
                if cols[col_index].button(f"Plus d'informations", key=button_key):
                    st.markdown("<h3 style='text-align: center; margin-bottom: 40px;'>"
                                f'🎬 {images_list[image_index].split(".jpg")[0]} 🎬'
                                "</h1>",
                                unsafe_allow_html=True)
                    st.markdown("<h6 >"
                                f"💯 Note globale : X/20"
                                "</h1>",
                                unsafe_allow_html=True)
                    st.markdown("<h6 >"
                                f"😎 X% des utilisateurs ont aimé ce film\n"
                                "</h1>",
                                unsafe_allow_html=True)

                    lien = get_link_by_movie_name(images_list[image_index].split('.jpg')[0])

                    if lien:
                        st.markdown(
                            f"<h6 style='margin-bottom: 40px'>"
                            f"🔗 <a href='{lien}' target='_blank'>Lien vers la bande d'annonce</a>"
                            "</h6>",
                            unsafe_allow_html=True
                        )


if __name__ == "__main__":
    main()
