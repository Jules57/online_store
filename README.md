The project is an online shop where a user can place orders, add products to the cart and manage them, make test 
payments via Stripe, receive invoices and use the website in two languages - English and Spanish. Also, the user 
can apply coupons.

How to run the project:
1. Run server:`python manage.py runserver`
2. Run Celery: `celery -A myshop worker -l info`
3. Run RabbitMQ: `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management-alpine`
4. Run Stripe CLI: `stripe listen --forward-to localhost:8000/payment/webhook/`
5. Run Redis: `docker run -it --rm --name redis -p 6379:6379 redis`
