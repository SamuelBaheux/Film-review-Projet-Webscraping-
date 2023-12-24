import os

import streamlit as st

from utils import get_infos_fim, get_link_by_movie_name

image_extensions = ["png", "jpg", "jpeg", "gif"]

comm =     "I watched this with my wife who was ready to turn it off after about ten minutes, but I talked her into watching it - \"It'll get better, honey. They'll be going into the real world, soon.\"Well, it didn't get better, after they went into the real world. I feel like it was a better show in Barbieland where it seemed more realistic.There isn't anything wrong with the acting or production, but the script is weak, particularly when they get to the real world. People just don't act like that. I'm disappointed for the actors, I think they thought it would be a great movie, however it's much more of a letdown.",



def main():
    st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>🍿Film Review 🎬</h1>", unsafe_allow_html=True)
    text = """
# Bienvenue dans Film Review !

Votre application personnelle de notation de film. Pour chaque film, découvrez trois informations clés :
- **Note basée sur les avis d'IMDB**
- **Pourcentage d'avis positifs**
- **Lien vers la bande-annonce**

Vous pourrez également lire le meilleur et le pire commentaire (au sens de notre modèle de sentiment) pour découvrir
l'avis des internautes !
"""


    st.markdown(f"<h6 margin-bottom: 30px;'>{text}</h5>", unsafe_allow_html=True)


    images_folder = 'images'
    images_list = os.listdir("images")

    images_list = [image for image in images_list if any(image.endswith(ext) for ext in image_extensions)]
    images_list.sort()

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
                    note, pcentage = get_infos_fim(images_list[image_index].split('.jpg')[0])
                    lien = get_link_by_movie_name(images_list[image_index].split('.jpg')[0])

                    st.markdown("<h3 style='text-align: center; margin-bottom: 40px;'>"
                                f'🎬 {images_list[image_index].split(".jpg")[0]} 🎬'
                                "</h1>",
                                unsafe_allow_html=True)
                    st.markdown("<h6 >"
                                f"💯 Note globale : {round(note, 2)}/20"
                                "</h1>",
                                unsafe_allow_html=True)
                    st.markdown("<h6 >"
                                f"😎 {round(pcentage)}% des utilisateurs ont aimé ce film\n"
                                "</h1>",
                                unsafe_allow_html=True)
                    st.markdown(f"<h6 style='margin-bottom: 10px'>"
                                f"🔗 <a href='{lien}' target='_blank'>Lien vers la bande d'annonce</a>"
                                "</h6>",
                                unsafe_allow_html=True)

                    st.markdown(f"<h6 style='margin-bottom: 10px'>"
                                f"✅ Meilleur Commentaire : {comm}"
                                "</h6>",
                                unsafe_allow_html=True)

                    st.markdown(f"<h6 style='margin-bottom: 40px'>"
                                f"❌ Pire Commentaire : {comm}"
                                "</h6>",
                                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
