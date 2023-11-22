from random import randint, random

from api.router import router
from db.schema import Category, Customer, Product, Review
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import settings
from tortoise import expand_db_url
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config={
        "connections": {
            "default": expand_db_url(str(settings.POSTGRES_URL), "asyncpg")
        },
        "apps": {
            "models": {
                "models": ["db.schema", "aerich.models"],
                "default_connection": "default",
            }
        },
    },
    generate_schemas=True,
    add_exception_handlers=True,
)


app.include_router(router)


@app.on_event("startup")
async def load_categories():
    if not await Customer.all():
        await Customer.create(
            id="6549976b9kh6d04fc75b81e8",
            first_name="string",
            last_name="string",
            email="string",
            created_at="2023-11-05T21:47:21.594Z",
            updated_at="2023-11-05T21:47:21.594Z",
        )

    if not await Category.all():
        categories = [
            {
                "name": "soda",
                "description": "Fizzy and sweet carbonated beverages, available in various flavors.",
            },
            {
                "name": "vitamin water",
                "description": "Nutrient-enhanced water with added vitamins, offering a refreshing and health-conscious option.",
            },
            {
                "name": "energy drinks",
                "description": "Highly caffeinated beverages designed to provide a quick energy boost, often containing additional supplements.",
            },
            {
                "name": "tea",
                "description": "A diverse range of traditional and herbal teas, offering soothing and aromatic experiences.",
            },
            {
                "name": "coffee",
                "description": "Rich and flavorful coffee selections, including various roasts and brew styles.",
            },
            {
                "name": "juice",
                "description": "Freshly squeezed or processed fruit juices, offering natural sweetness and a dose of vitamins.",
            },
            {
                "name": "cold brew",
                "description": "Coffee brewed with cold water, resulting in a smooth and less acidic flavor profile.",
            },
            {
                "name": "iced tea",
                "description": "Chilled tea variations, perfect for a refreshing and cooling drink on warm days.",
            },
            {
                "name": "sparkling water",
                "description": "Carbonated water with a hint of natural flavors, providing a bubbly and calorie-free option.",
            },
        ]
        for category in categories:
            await Category.create(**category)

    if not await Product.all():
        beverages = [
            {
                "name": "Coca-Cola",
                "image": "cola.png",
                "category_id": 1,
                "description": "Indulge in the timeless delight of Classic Cola. This iconic soda offers a perfect blend of effervescence and rich cola flavor, satisfying your taste buds with every sip. Crafted by Coca-Cola, a symbol of refreshment for generations.",
                "brand": "Coca-Cola",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Diet Coke",
                "image": "diet_coke.png",
                "category_id": 1,
                "description": "Crisp, cold and reliable, this is the one and only Diet Coke —your everyday wing (wo)man, your deliciously fizzy go-to companion. This is the kind of sugar-free soda that you want throughout your day. Whether you're looking for a tasty way start to your day or to refresh your afternoon, you'll never be lost with a Diet Coke.Diet Coke always hits the spot. Alongside meals, celebrations or just your friends in your backyard, at any time of day. In fact, it's basically a friend itself. Because it's the best kind of familiar, and something you never have to second guess. You trust it, and it's always there for you whenever you want it.Diet Coke also comes in a caffeine-free option. And if you're looking to excite your taste buds even more, there's a host of different flavors to satisfy. Really, it's the diet cola you know you can turn to, no matter what you're looking for.So when you want a diet soda, think Diet Coke. Because Diet Coke is an original, just like you. Oh yeah, and it's incredibly refreshing. Always.",
                "brand": "Coca-Cola",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Coca-Cola Zero",
                "image": "cola_zero.png",
                "category_id": 1,
                "description": "Soda. Pop. Soft drink. Sparkling beverage.Whatever you call it, nothing compares to the refreshing, crisp taste of Coca-Cola Zero Sugar. Enjoy with friends, on the go or with a meal. Whatever the occasion, wherever you are, Coca-Cola Zero Sugar makes life's special moments a little bit better.The great taste of Coca-Cola has stood the test of time. And Coca-Cola Zero Sugar brings you a Coca-Cola taste with zero sugar. Between the delicious taste and refreshing fizz, it's sure to give you that “ahhh” moment whenever you want it.Coca-Cola is available in many different options, including Coca-Cola Original Taste, Coca-Cola Caffeine Free, and a variety of all-time favorite flavors like Coca-Cola Cherry and Coca-Cola Vanilla. Whatever you're looking for, there's a Coca-Cola to satisfy your taste buds.Every sip, every “ahhh,” every smile—find that feeling with Coca-Cola Zero Sugar. Best enjoyed ice-cold for maximum refreshment. Grab a Coca-Cola Zero Sugar, take a sip and find your “ahhh” moment.Enjoy Coca-Cola Zero Sugar.",
                "brand": "Coca-Cola",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Coke Cherry",
                "image": "coke_cherry.png",
                "category_id": 1,
                "description": "Soda. Pop. Soft drink. Sparkling beverage.Whatever you call it, nothing compares to the refreshing, crisp taste of Coca-Cola Cherry. A little flavor can make a lot of magic happen and Coca-Cola Cherry is here to make your taste buds happy. Enjoy with friends, on the go or with a meal. Whatever the occasion, Coca-Cola Cherry makes life's special moments a little bit better.A delicious combination of flavors, Coca-Cola Cherry blends a familiar taste of Coca-Cola Original Taste with something unexpected, creating more ways for you to enjoy Coca-Cola. Between that perfect taste and refreshing fizz, it's sure to give you that “ahhh” moment whenever you want it.Coca-Cola is available in many different options, including Coca-Cola Original Taste and a variety of all-time favorite flavors like Coca-Cola Vanilla and Coca-Cola Cherry Vanilla. Looking for something with zero sugar or caffeine free? Then look no further than Coca-Cola Zero Sugar and Coca-Cola Caffeine Free. Whatever you're looking for, there's a Coca-Cola to satisfy your taste buds.Every sip, every “ahhh,” every smile—find that feeling with Coca-Cola Cherry. Best enjoyed ice-cold for maximum refreshment. Grab a Coca-Cola Cherry and find your “ahhh” moment.Enjoy Coca-Cola Cherry.",
                "brand": "Coca-Cola",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Coke Vanilla",
                "image": "coke_vanilla.png",
                "category_id": 1,
                "description": "Soda. Pop. Soft drink. Sparkling beverage.Whatever you call it, nothing compares to the refreshing, crisp taste of Coca-Cola Vanilla. A little flavor can make a lot of magic happen and Coca-Cola Vanilla is here to make your taste buds happy. Enjoy with friends, on the go or with a meal. Whatever the occasion, Coca-Cola Vanilla makes life's special moments a little bit better.A delicious combination of flavors, Coca-Cola Vanilla blends a familiar taste of Coca-Cola Original Taste with something unexpected, creating more ways for you to enjoy Coca-Cola. Between that perfect taste and refreshing fizz, it's sure to give you that “ahhh” moment whenever you want it.Coca-Cola is available in many different options, including Coca-Cola Original Taste, including a variety of all-time favorite flavors like Coca-Cola Cherry and Coca-Cola Orange Vanilla.. Looking for something with zero sugar or caffeine free? Then look no further than Coca-Cola Zero Sugar and Coca-Cola Caffeine Free. Whatever you're looking for, there's a Coca-Cola to satisfy your taste buds.Every sip, every “ahhh,” every smile— find that feeling with Coca-Cola Vanilla. Best enjoyed ice-cold for maximum refreshment. Grab a Coca-Cola Vanilla and find your “ahhh” moment.Enjoy Coca-Cola Vanilla.",
                "brand": "Coca-Cola",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Dr Pepper",
                "image": "drpepper.png",
                "category_id": 1,
                "description": "Satisfy your game day craving for flavor with the unique taste of Dr Pepper! It's not your ordinary soda and it's definitely not a cola. It's the sweet treat that fans deserve. So, whether you enjoy the original or any of the varieties like Dr Pepper Cherry, Dr Pepper & Cream Soda or Dr Pepper Zero Sugar, you'll get the satisfying flavor that only Dr Pepper can deliver straight to your taste buds. Established in 1885 in Waco, TX, Dr Pepper is the oldest major soft drink in the United States. It's a refreshing favorite that's always smooth and delicious at dinner, lunch, or breakfast. Although you can enjoy the unique flavor all on its own, you can also pair it with food. Dr Pepper is the perfect companion for every college football occasion, from tailgating to home-gating, and will pair perfectly with burgers, pizza or rotisserie chicken to a quick snack like pastries, chocolates or your favorite candy. You can't go wrong with a Dr Pepper when you want to satisfy your sweet cravings. Give your taste buds something to cheer for with the smooth, satisfying flavor of an ice-cold Dr Pepper, Dr Pepper Cherry or Dr Pepper & Cream Soda and they'll thank you for it every time!",
                "brand": "Dr. Pepper",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Diet Dr Pepper",
                "image": "diet_drpepper.png",
                "category_id": 1,
                "description": "It's the Sweeeeeeeet One! Satisfy your craving for flavor with the authentic taste of Diet Dr Pepper! It's not your ordinary soda and it's definitely not a cola. Made with the original recipe of 23 signature flavors but with zero calories, it's the sweet treat that can't be beat. Established in 1885 in Waco, TX, Dr Pepper is the oldest major soft drink in the United States. It's a refreshing favorite that's always smooth and delicious at dinner, lunch or breakfast (we won't judge you). Although you can enjoy the unique flavor all on its own, you can also pair it with food. Dr Pepper is the perfect companion for everything from a full meal like pizza, burgers or rotisserie chicken to a quick snack like pastries, chocolates or your favorite candy. You can't go wrong with a Diet Dr Pepper when you want to satisfy your sweet cravings. Give your tastebuds something to cheer for with the smooth, satisfying flavor of an ice-cold Dr Pepper and they'll thank you for it every time!",
                "brand": "Dr. Pepper",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Dr Pepper Zero",
                "image": "drpepper_zero.png",
                "category_id": 1,
                "description": "Satisfy your game day craving for flavor with the unique taste of Dr Pepper! It's not your ordinary soda and it's definitely not a cola. It's the sweet treat that fans deserve. So, whether you enjoy the original or any of the varieties like Dr Pepper Cherry, Dr Pepper & Cream Soda or Dr Pepper Zero Sugar, you'll get the satisfying flavor that only Dr Pepper can deliver straight to your taste buds. Established in 1885 in Waco, TX, Dr Pepper is the oldest major soft drink in the United States. It's a refreshing favorite that's always smooth and delicious at dinner, lunch, or breakfast. Although you can enjoy the unique flavor all on its own, you can also pair it with food. Dr Pepper is the perfect companion for every college football occasion, from tailgating to home-gating, and will pair perfectly with burgers, pizza or rotisserie chicken to a quick snack like pastries, chocolates or your favorite candy. You can't go wrong with a Dr Pepper when you want to satisfy your sweet cravings. Give your taste buds something to cheer for with the smooth, satisfying flavor of an ice-cold Dr Pepper, Dr Pepper Cherry or Dr Pepper & Cream Soda and they'll thank you for it every time!",
                "brand": "Dr. Pepper",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Pepsi",
                "image": "pepsi.png",
                "category_id": 1,
                "description": "Enjoy the sweet taste of Pepsi Cola soda. They come in a pack of 24 cans and each contains 12 fl oz. You can share them with others or save them for yourself to drink. Perfect for parties, meals, and anywhere you need to make a big impression. This 12 fl oz Pepsi is free of sugar and fat. It's suitable for sporting events and holidays. You can recycle the cans when they're empty. This Pepsi is formulated to be refreshing and crisp. Enjoy the refreshing cola taste right out of the can, over ice, or with a twist of lemon or lime. For a classic treat, try serving with a scoop of vanilla ice cream!",
                "brand": "Pepsi",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Diet Pepsi",
                "image": "diet_pepsi.png",
                "category_id": 1,
                "description": "Diet Pepsi Cola Soda Pop light, crisp taste, With its light, crisp taste, diet pepsi gives you all the refreshment you need - with zero sugar, zero calories and zero carbs.",
                "brand": "Pepsi",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Pepsi Zero",
                "image": "pepsi_zero.png",
                "category_id": 1,
                "description": "Pepsi Zero Sugar is the only soda with zero calories and maximum Pepsi taste!",
                "brand": "Pepsi",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Pepsi Cherry",
                "image": "pepsi_cherry.png",
                "category_id": 1,
                "description": "Only Wild Cherry Pepsi Cola soda has the thrilling burst of unique cherry flavor and a sweet, crisp taste that gives you more to go wild for.",
                "brand": "Pepsi",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Nitro Pepsi",
                "image": "nitro_pepsi.png",
                "category_id": 1,
                "description": "Introducing Nitro Pepsi™: the first-ever nitrogen-infused cola. It's more than just a cola, it's an experience. The easy texture. The silky foam. The rising cascade. The unapologetically Pepsi® taste. It sparks connection and conversation, straight from the very first sip. With lower carbonation and smaller bubbles, Nitro Pepsi is smooth and easy to drink. To best experience it, chill the can, pour hard, then admire and enjoy.",
                "brand": "Pepsi",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Sprite",
                "image": "sprite.png",
                "category_id": 1,
                "description": "Dive into the bold and adventurous Blue Raspberry Soda. Brought to you by Blue Sky, this soda features the electrifying flavor of blue raspberries, delivering a unique and vibrant taste experience.",
                "brand": "Sprite",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Sprite Zero",
                "image": "sprite_zero.png",
                "category_id": 1,
                "description": "Dive into the bold and adventurous Blue Raspberry Soda. Brought to you by Blue Sky, this soda features the electrifying flavor of blue raspberries, delivering a unique and vibrant taste experience.",
                "brand": "Blue Sky",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Mountain Dew",
                "image": "mountain_dew.png",
                "category_id": 1,
                "description": "Experience all the exhilarating taste of Mountain Dew by cracking open a cold can of Mountain Dew. Refresh your taste buds with chuggable, intense refreshment that delivers the great Dew flavor without the guilt. The ingredients include citric acid, orange juice concentrate, and carbonated water, all contributing to the 100% natural flavors. Enjoy the satisfying, crisp taste of Mountain Dew without compromising on refreshment.",
                "brand": "Blue Sky",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Diet Mountain Dew",
                "image": "diet_mountain_dew.png",
                "category_id": 1,
                "description": "Experience all the exhilarating taste of Mountain Dew with none of the calories by cracking open a cold can of Diet Mountain Dew. Refresh your taste buds with chuggable, intense refreshment that delivers the great Dew flavor without the guilt. The ingredients include citric acid, orange juice concentrate, and carbonated water, all contributing to the 100% natural flavors. Enjoy the satisfying, crisp taste of Diet Mountain Dew without compromising on refreshment.",
                "brand": "Blue Sky",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Mountain Dew Zero",
                "image": "mountain_dew_zero.png",
                "category_id": 1,
                "description": "Mtn Dew exhilarates and quenches with its one of a kind, bold taste. Enjoy its chuggable intense refreshment. Crack open a cold Mtn Dew and refresh your taste buds.",
                "brand": "Blue Sky",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Starry",
                "image": "starry.png",
                "category_id": 1,
                "description": "It's time to refresh yourself - introducing Starry! Starry is a new lemon lime soda bringing you a crisp hit of refreshing lemon-lime flavor with a bite. Starry is here to help give you a lift and brighten things up, because we know things can get crazy out there. It's the brightest lemon lime.",
                "brand": "Starry",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Starry Zero",
                "image": "starry_zero.png",
                "category_id": 1,
                "description": "It's time to refresh yourself - introducing Starry! Starry is a new lemon lime soda bringing you a crisp hit of refreshing lemon-lime flavor with a bite. Starry is here to help give you a lift and brighten things up, because we know things can get crazy out there. It's the brightest lemon lime.",
                "brand": "Starry",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Fanta Strawberry",
                "image": "fanta_strawberry.png",
                "category_id": 1,
                "description": "Choosing the right fruit soda can be a whole thing. But when you've got a delicious bottle of Fanta Strawberry ready to go, the decision is easy. Why?​Because who doesn't want to try the ripeness, the sweetness, the juiciness of plump, red strawberries, all in a caffeine-free soda? It's like finding the most perfect strawberry out of the bunch. And raising it as if it were your own. Drinking Fanta Strawberry soda.Fanta has been making delicious flavors like this for literally, a long time. Not Jurassic long, or like a tortoises' lifespan long, but most likely before you were born long (unless you are a grandparent, in which case rock on gramps!). So anyway, you should trust Fanta when it comes to fruit soda. We have a lot of flavors you should try, and they are all super good.Grab yourself a 12oz 12 pack of Fanta Strawberry soda—come on, the decision is easy.",
                "brand": "Fanta",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Fanta Orange",
                "image": "fanta_orange.png",
                "category_id": 1,
                "description": "Choosing the right fruit soda can be a whole thing. But when you've got a delicious bottle of Fanta Orange ready to go, the decision is easy. Why?​Well, it tastes like it's ripe from the tree. The orangiest of orange you can imagine. Simply iconic citrus-y flavor, like a caffeine-free sunset on the beach, where you're living in the moment, shooting for the stars and discovering new ones while you're at it. It tastes so bright it's in the gifted program. A flavor that's effervescent and luminescent and all the other -escents.Fanta has been making delicious flavors like this for literally a long time. Not Jurassic long, or like a tortoise's lifespan long, but most likely before you were born long (unless you are a grandparent, in which case: rock on gramps!). So anyway, you should trust Fanta when it comes to fruit soda. We have a lot of flavors you should try, and they are all super good.Grab yourself a 12oz 12 pack of Fanta Orange—come on, the decision is easy.",
                "brand": "Fanta",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
            {
                "name": "Canada Dry Ginger Ale",
                "image": "canada_dry.png",
                "category_id": 1,
                "description": "Sip into your comfort zone with the refreshing taste of Canada Dry Ginger Ale. There comes a time when we all need a break from the treadmill of life, and there's only one thing to do during those moments when we need an escape from stresses and obligations... Grab an ice-cold can of Canada Dry Ginger Ale, and sip into your comfort zone. Whether that means you're sitting on your front porch swing, listening to your favorite podcast or just taking a quiet moment for yourself, Canada Dry is the perfect ginger ale to make it even better. And it's caffeine free! Once transported to the comfort zone, you can enjoy refreshing ginger taste made with only high quality ingredients, soothing you with each comforting sip. For over 100 years, Canada Dry has been creating quality carbonated beverages and mixers that can be enjoyed at any time of day. There are so many ways you can enjoy the great taste of Canada Dry Ginger Ale. You can make delicious cocktails like a Moscow Mule in a cold copper cup, or simply sit back and relax with a Canada Dry Ginger Ale over ice all by itself. So grab an ice-cold can of Canada Dry, sink into your favorite chair, and sip into the comfort zone.",
                "brand": "Canada Dry",
                "price": round(random() + 1, 2),
                "quantity": randint(70, 150),
            },
        ]

        for drink in beverages:
            await Product.create(**drink)

    if not await Review.all():
        reviews = [
            {
                "id": 1,
                "product_id": 1,
                "customer_id": "6549976b9kh6d04fc75b81e8",
                "rating": 4,
                "comment": "Great product! I really enjoyed it.",
                "created_at": "2023-10-15 14:30:00",
                "updated_at": "2023-10-15 15:45:00",
            },
            {
                "id": 2,
                "product_id": 1,
                "customer_id": "6549976b9kh6d04fc75b81e8",
                "rating": 5,
                "comment": "This is the best product ever!",
                "created_at": "2023-10-16 09:15:00",
                "updated_at": "2023-10-16 10:30:00",
            },
            {
                "id": 3,
                "product_id": 1,
                "customer_id": "6549976b9kh6d04fc75b81e8",
                "rating": 3,
                "comment": "Not bad, but could be improved.",
                "created_at": "2023-10-17 12:20:00",
                "updated_at": "2023-10-17 13:45:00",
            },
            {
                "id": 4,
                "product_id": 1,
                "customer_id": "6549976b9kh6d04fc75b81e8",
                "rating": 5,
                "comment": "Absolutely fantastic!",
                "created_at": "2023-10-18 16:05:00",
                "updated_at": "2023-10-18 17:20:00",
            },
            {
                "id": 5,
                "product_id": 1,
                "customer_id": "6549976b9kh6d04fc75b81e8",
                "rating": 4,
                "comment": "I would recommend this product.",
                "created_at": "2023-10-19 20:10:00",
                "updated_at": "2023-10-19 21:25:00",
            },
        ]

        for review in reviews:
            await Review.create(**review)
