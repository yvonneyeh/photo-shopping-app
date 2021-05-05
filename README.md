# Doge Snappe Shoppe

by [Yvonne Yeh](https://yvonneyeh.com)

**Doge Snappe Shoppe** is a full-stack web app that helps doge lovers buy and sell photos of dogs!

![Doge Shoppe](https://raw.githubusercontent.com/yvonneyeh/photo-shopping-app/main/static/img/homepage.png)

### Table of Contents
- [App Overview](#App)
- [About the Developer](#Dev)
- [Technology](#Tech)
- [Data Structure](#Data)
- [Installation Instructions](#Install)
- [Future Features](#Future)

## <a name="App"></a> App Overview
This is a backend-focused project created with the intention of building an image repository. I wanted to implement a shopping feature, which I had never done before. Users buy and sell photos – they can upload images and manage the photo inventory, see photos for sale, and purchase a photo.

## <a name="Dev"></a> About the Developer
Yvonne is a software engineer from the Silicon Valley who has never seen the show. Curiosity, creativity, and a love of learning are at the root of everything Yvonne does. She loves that coding because it is artful – there are infinite ways to code a program! Before she learned how to code, she worked in K-12 education, design, and mental/physical fitness.

## <a name="Features"></a>Features

- Displays a list of all photos in the inventory on the homepage
- Upload photos from your computer with a title, description, and price. 
- Asset are uploaded and stored in Cloudinary, and the public URL saved to the database.
- Modify the inventory
- Add items to the shopping cart
- Process order with credit card verification with the Stripe API

![Checkout with Stripe](https://raw.githubusercontent.com/yvonneyeh/photo-shopping-app/main/static/img/checkout.png)

## <a name="Tech"></a>Tech Stack
- **Frontend**: JavaScript, HTML, CSS, Bootstrap
- **Backend**: Python3, Flask, PostgreSQL, SQLAlchemy, Jinja2, Bash
- **APIs**: Cloudinary, Stripe

## <a name="Data"></a>Data Structure

![Data Model Graphic](https://raw.githubusercontent.com/yvonneyeh/photo-shopping-app/main/static/img/data_model.png)


## <a name="Install"></a>Installation Instructions

### Prerequisites
To run Doge Shoppe, you will need the following API keys: 
- [Cloudinary](https://cloudinary.com/documentation/cloudinary_references)
- [Stripe](https://stripe.com/docs/api)

**Python3** and **PostgreSQL** will also need to be installed on your machine.

### Running Doge Shoppe

1. Clone this repository:
```shell
git clone https://github.com/yvonneyeh/photo-shopping-app.git
```

***Optional***: Create and activate a virtual environment:
```shell
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

2. Install dependencies: 
```shell
pip3 install -r requirements.txt
```

3. Create environmental variables to hold your API keys in a `secrets.sh` file:
```
export DATABASE_URL='{DATABASE_URL}'
export SECRET_KEY='{SECRET_KEY}'
export CLOUD_NAME='{CLOUD_NAME}'
export CLOUD_API_KEY='{CLOUDINARY_API_KEY}'
export CLOUD_API_SECRET='{CLOUDINARY_API_SECRET}'
export ENV_VAR='{cloudinary://...}'
export STRIPE_SECRET_KEY='{STRIPE_SECRET_KEY}'
export STRIPE_PUBLIC_KEY='{STRIPE_PUBLIC_KEY}'
```

4. Create your database & seed sample data:
```shell
createdb photos
python3 seed.py
```

5. Run the app on localhost:
```shell
source secrets.sh
python3 server.py
```

## <a name="Future"></a>Future Features
- View as Admin or Client
