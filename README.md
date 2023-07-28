The project is an online shop where a user can place orders, add products to the cart and manage them, make test 
payments via Stripe, receive invoices and use the website in two languages - English and Spanish. Also, the user 
can apply coupons.

How to run the project:
1. Get secret keys at: [TBD]
2. Load data: `python manage.py loaddata myshop.json`
3. Migrate: `python manage.py migrate`
4. Run server:`python manage.py runserver`
5. Run Celery: `celery -A myshop worker -l info`
6. Run RabbitMQ: `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management-alpine`
7. Run Stripe CLI: `stripe listen --forward-to localhost:8000/payment/webhook/`
8. Run Redis: `docker run -it --rm --name redis -p 6379:6379 redis`
