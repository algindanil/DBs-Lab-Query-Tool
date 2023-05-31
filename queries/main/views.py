from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import connection
from rest_framework.views import APIView
from django.views.generic import DeleteView, View, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.apps import apps
from .forms import *
from .models import *


def main_view(request):
    return render(request, 'main.html')


def edit_jewelerypiece(request, pk):
    piece = get_object_or_404(JeweleryPiece, piece_id=pk)
    
    if request.method == 'POST':
        form = JeweleryPieceForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = JeweleryPieceForm(instance=piece)
    
    context = {'form': form,
               'form_name': 'Edit JeweleryPiece'}
    return render(request, 'add_item.html', context)


def edit_materal(request, pk):
    piece = get_object_or_404(Material, material_id=pk)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = MaterialForm(instance=piece)
    
    context = {'form': form,
               'form_name': 'Edit Material'}
    return render(request, 'add_item.html', context)


def edit_order(request, pk):
    piece = get_object_or_404(Order, order_id=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = OrderForm(instance=piece)
    
    context = {'form': form,
               'form_name': 'Edit Order'}
    return render(request, 'add_item.html', context)


def edit_orderdetails(request, pk):
    piece = get_object_or_404(OrderDetails, details_id=pk)
    
    if request.method == 'POST':
        form = OrderDetailsForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = OrderDetailsForm(instance=piece)
    
    context = {'form': form,
               'form_name': 'Edit OrderDetails'}
    return render(request, 'add_item.html', context)


def edit_client(request, pk):
    piece = get_object_or_404(Client, client_id=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = ClientForm(instance=piece)
    
    context = {'form': form,
               'form_name': 'Edit Client'}
    return render(request, 'add_item.html', context)


def edit_category(request, pk):
    piece = get_object_or_404(Category, piece_id=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = CategoryForm(instance=piece)
    
    context = {'form': form,
               'form_name': 'Edit Category'}
    return render(request, 'add_item.html', context)


def delete_jewelerypiece(request, pk):
    jp = get_object_or_404(JeweleryPiece, piece_id=pk)
    jp.delete()
    return redirect(reverse('items_list'))


def delete_client(request, pk):
    client = get_object_or_404(Client, client_id=pk)
    client.delete()
    return redirect(reverse('items_list'))


def delete_material(request, pk):
    m = get_object_or_404(Material, material_id=pk)
    m.delete()
    return redirect(reverse('items_list'))


def delete_orderdetails(request, pk):
    od = get_object_or_404(OrderDetails, details_id=pk)
    od.delete()
    return redirect(reverse('items_list'))


def delete_category(request, pk):
    c = get_object_or_404(Category, category_id=pk)
    c.delete()
    return redirect(reverse('items_list'))

def delete_order(request, pk):
    o = get_object_or_404(Order, order_id=pk)
    o.delete()
    return redirect(reverse('items_list'))


class QueryView(APIView):
    
    def get(self, request, *args, **kwargs):
        result =''
        cursor = connection.cursor()
        if request.GET.get('form1'):
            print('form1')
            value = request.GET.get('value')
            cursor.execute(f'''
                SELECT main_jewelerypiece.name
                    FROM main_jewelerypiece, main_categorypiece, main_category
                    WHERE main_jewelerypiece.piece_id = main_categorypiece.piece_id_id
                    AND main_categorypiece.category_id_id = main_category.category_id
                    AND main_category.name = '{value}';
            ''')
            result = cursor.fetchall()
        elif request.GET.get('form2'):
            value = request.GET.get('value')
            cursor.execute(f'''
                SELECT DISTINCT main_order.order_id
                    FROM main_order, main_orderdetails, main_jewelerypiece
                    WHERE main_order.order_id = main_orderdetails.order_id_id
                    AND main_orderdetails.piece_id_id = main_jewelerypiece.piece_id
                    AND main_jewelerypiece.price > {value};
            ''')
            result = cursor.fetchall()
        elif request.GET.get('form3'):
            value = request.GET.get('value')
            cursor.execute(f'''
                SELECT main_jewelerypiece.name
                    FROM main_jewelerypiece, main_orderdetails
                    WHERE main_jewelerypiece.piece_id = main_orderdetails.piece_id_id
                    AND main_orderdetails.quantity > {value};
            ''')
            result = cursor.fetchall()
        elif request.GET.get('form4'):
            value = request.GET.get('value')
            cursor.execute(f'''
                SELECT main_category.name
                FROM main_category
                WHERE main_category.category_id IN (
                    SELECT main_categorypiece.category_id_id
                    FROM main_categorypiece
                    WHERE main_categorypiece.piece_id_id IN (
                        SELECT main_jewelerypiece.piece_id
                        FROM main_jewelerypiece
                        WHERE main_jewelerypiece.piece_id IN (
                            SELECT main_orderdetails.piece_id_id
                            FROM main_orderdetails
                            WHERE main_orderdetails.order_id_id = {value}
                        )
                    )
                );
            ''')
            result = cursor.fetchall()
        elif request.GET.get('form5'):
            value = request.GET.get('value')
            cursor.execute(f'''
                SELECT main_order.order_id
                FROM main_order
                WHERE main_order.order_id IN (
                    SELECT main_orderdetails.order_id_id
                    FROM main_orderdetails
                    WHERE main_orderdetails.piece_id_id IN (
                        SELECT main_jewelerypiece.piece_id
                        FROM main_jewelerypiece
                        WHERE main_jewelerypiece.material_id = (
                            SELECT material_id
                            FROM main_material
                            WHERE name = '{value}'
                        )
                    )
                );
            ''')
            result = cursor.fetchall()
        elif request.GET.get('form6'):
            value = request.GET.get('value')
            cursor.execute(f'''
                SELECT o.order_id
                FROM main_order AS o
                INNER JOIN main_orderdetails AS od ON od.order_id_id = o.order_id
                INNER JOIN main_jewelerypiece AS jp ON jp.piece_id = od.piece_id_id
                INNER JOIN main_categorypiece AS cp ON cp.piece_id_id = jp.piece_id
                INNER JOIN main_category AS c ON c.category_id = cp.category_id_id
                WHERE o.order_id <> {value}
                AND NOT EXISTS (
                    SELECT 1
                    FROM main_categorypiece AS cp2
                    WHERE cp2.piece_id_id = (
                        SELECT od2.piece_id_id
                        FROM main_orderdetails AS od2
                        WHERE od2.order_id_id = {value}
                        LIMIT 1
                    )
                    AND cp2.category_id_id NOT IN (
                        SELECT cp3.category_id_id
                        FROM main_categorypiece AS cp3
                        WHERE cp3.piece_id_id = jp.piece_id
                    )
                )
                GROUP BY o.order_id



            ''')
            result = cursor.fetchall()
        elif request.GET.get('form7'):
            value = request.GET.get('value')
            cursor.execute(f'''
                SELECT c.name
                    FROM main_category AS c
                    INNER JOIN main_categorypiece AS cp ON cp.category_id_id = c.category_id
                    INNER JOIN main_jewelerypiece AS jp ON jp.piece_id = cp.piece_id_id
                    INNER JOIN main_orderdetails AS od ON od.piece_id_id = jp.piece_id
                    INNER JOIN (
                        SELECT o.order_id
                        FROM main_order AS o
                        INNER JOIN main_client AS cl ON cl.client_id = o.client_id_id
                        WHERE cl.name = '{value}'
                    ) AS o_filtered ON o_filtered.order_id = od.order_id_id
                    GROUP BY c.name
                    HAVING COUNT(DISTINCT jp.piece_id) = (
                        SELECT COUNT(DISTINCT jp2.piece_id)
                        FROM main_jewelerypiece AS jp2
                        INNER JOIN main_categorypiece AS cp2 ON cp2.piece_id_id = jp2.piece_id
                        INNER JOIN main_category AS c2 ON c2.category_id = cp2.category_id_id
                        INNER JOIN main_orderdetails AS od2 ON od2.piece_id_id = jp2.piece_id
                        INNER JOIN (
                            SELECT o2.order_id
                            FROM main_order AS o2
                            INNER JOIN main_client AS cl2 ON cl2.client_id = o2.client_id_id
                            WHERE cl2.name = '{value}'
                        ) AS o_filtered2 ON o_filtered2.order_id = od2.order_id_id
                    );

            ''')
            result = cursor.fetchall()
        elif request.GET.get('form8'):
            cursor.execute(f'''
                SELECT main_order.order_id
                    FROM main_order
                    WHERE main_order.order_id IN (
                        SELECT main_orderdetails.order_id_id
                        FROM main_orderdetails
                        WHERE main_orderdetails.piece_id_id IN (
                            SELECT main_categorypiece.piece_id_id
                            FROM main_categorypiece
                            GROUP BY main_categorypiece.piece_id_id
                            HAVING COUNT(DISTINCT main_categorypiece.category_id_id) = (
                                SELECT COUNT(*)
                                FROM main_category
                            )
                        )
                    );
            ''')
            result = cursor.fetchall()
        result = [i[0] for i in result]
        return render(request, 'q1.html', {'results': result})


def fill_db(request):
    # 1) Adding examples of Material
    materials = [
        {'name': 'Gold', 'quantity': 100, 'measurement_unit': 'grams'},
        {'name': 'Silver', 'quantity': 200, 'measurement_unit': 'grams'},
        {'name': 'Diamond', 'quantity': 50, 'measurement_unit': 'carats'},
        {'name': 'Pearl', 'quantity': 150, 'measurement_unit': 'pieces'},
        {'name': 'Platinum', 'quantity': 80, 'measurement_unit': 'grams'},
        {'name': 'Ruby', 'quantity': 30, 'measurement_unit': 'carats'},
        {'name': 'Sapphire', 'quantity': 40, 'measurement_unit': 'carats'},
        {'name': 'Emerald', 'quantity': 25, 'measurement_unit': 'carats'},
        {'name': 'Topaz', 'quantity': 60, 'measurement_unit': 'carats'},
        {'name': 'Amethyst', 'quantity': 70, 'measurement_unit': 'carats'},
    ]

    for material_data in materials:
        Material.objects.create(**material_data)


    # 2) Adding examples of Category
    categories = [
        {'name': 'Necklaces'},
        {'name': 'Earrings'},
        {'name': 'Bracelets'},
        {'name': 'Rings'},
        {'name': 'Pendants'},
        {'name': 'Anklets'},
        {'name': 'Brooches'},
        {'name': 'Cufflinks'},
        {'name': 'Watches'},
        {'name': 'Charms'},
    ]

    for category_data in categories:
        Category.objects.create(**category_data)


    # 3) Adding examples of JeweleryPiece
    jewelry_pieces = [
        {
            'name': 'Gold Necklace',
            'price': 500,
            'maker_country': 'Italy',
            'material': Material.objects.get(name='Gold'),
            'category': 'Necklaces',
        },
        {
            'name': 'Silver Earrings',
            'price': 100,
            'maker_country': 'France',
            'material': Material.objects.get(name='Silver'),
            'category': 'Earrings',

        },
        {
            'name': 'Diamond Bracelet',
            'price': 1000,
            'maker_country': 'USA',
            'material': Material.objects.get(name='Diamond'),
            'category': 'Bracelets',

        },
        {
            'name': 'Pearl Ring',
            'price': 300,
            'maker_country': 'Japan',
            'material': Material.objects.get(name='Pearl'),
            'category': 'Rings',

        },
        {
            'name': 'Platinum Pendant',
            'price': 800,
            'maker_country': 'Germany',
            'material': Material.objects.get(name='Platinum'),
            'category': 'Pendants',

        },
        {
            'name': 'Ruby Anklet',
            'price': 400,
            'maker_country': 'India',
            'material': Material.objects.get(name='Ruby'),
            'category': 'Anklets',

        },
        {
            'name': 'Sapphire Brooch',
            'price': 600,
            'maker_country': 'UK',
            'material': Material.objects.get(name='Sapphire'),
            'category': 'Brooches',

        },
        {
            'name': 'Emerald Cufflinks',
            'price': 700,
            'maker_country': 'Australia',
            'material': Material.objects.get(name='Emerald'),
            'category': 'Cufflinks',

        },
        {
            'name': 'Topaz Watch',
            'price': 900,
            'maker_country': 'Switzerland',
            'material': Material.objects.get(name='Topaz'),
            'category': 'Cufflinks',

        },
        {
            'name': 'Amethyst Charm',
            'price': 200,
            'maker_country': 'Brazil',
            'material': Material.objects.get(name='Amethyst'),
            'category': 'Charms',
        },
    ]

    for jewelry_data in jewelry_pieces:
        new_data = {key: value for key, value in jewelry_data.items() if key != 'category'}
        jewelry_piece = JeweleryPiece.objects.create(**new_data)
        jewelry_piece.categories.set(Category.objects.filter(name=jewelry_data.get('category')))


    # 4) Adding examples of Client
    clients = [
        {
            'name': 'John Doe',
            'address': '123 Main St',
            'email': 'john@example.com',
            'phone_number': '+1234567890',
        },
        {
            'name': 'Jane Smith',
            'address': '456 Elm St',
            'email': 'jane@example.com',
            'phone_number': '+9876543210',
        },
        {
            'name': 'Michael Johnson',
            'address': '789 Oak St',
            'email': 'michael@example.com',
            'phone_number': '+1111111111',
        },
        {
            'name': 'Emily Davis',
            'address': '321 Pine St',
            'email': 'emily@example.com',
            'phone_number': '+2222222222',
        },
        {
            'name': 'William Wilson',
            'address': '654 Birch St',
            'email': 'william@example.com',
            'phone_number': '+3333333333',
        },
        {
            'name': 'Olivia Martin',
            'address': '987 Cedar St',
            'email': 'olivia@example.com',
            'phone_number': '+4444444444',
        },
        {
            'name': 'James Taylor',
            'address': '159 Maple St',
            'email': 'james@example.com',
            'phone_number': '+5555555555',
        },
        {
            'name': 'Sophia Anderson',
            'address': '357 Walnut St',
            'email': 'sophia@example.com',
            'phone_number': '+6666666666',
        },
        {
            'name': 'Benjamin Martinez',
            'address': '753 Sycamore St',
            'email': 'benjamin@example.com',
            'phone_number': '+7777777777',
        },
        {
            'name': 'Ava Hernandez',
            'address': '951 Poplar St',
            'email': 'ava@example.com',
            'phone_number': '+8888888888',
        },
    ]

    for client_data in clients:
        Client.objects.create(**client_data)


    # 5) Adding examples of Order
    orders = [
        {
            'client_id': Client.objects.get(name='John Doe'),
            'date': '2023-05-01',
            'status': 'Pending',
        },
        {
            'client_id': Client.objects.get(name='Jane Smith'),
            'date': '2023-05-02',
            'status': 'Completed',
        },
        {
            'client_id': Client.objects.get(name='Michael Johnson'),
            'date': '2023-05-03',
            'status': 'Pending',
        },
        {
            'client_id': Client.objects.get(name='Emily Davis'),
            'date': '2023-05-04',
            'status': 'Completed',
        },
        {
            'client_id': Client.objects.get(name='William Wilson'),
            'date': '2023-05-05',
            'status': 'Pending',
        },
        {
            'client_id': Client.objects.get(name='Olivia Martin'),
            'date': '2023-05-06',
            'status': 'Completed',
        },
        {
            'client_id': Client.objects.get(name='James Taylor'),
            'date': '2023-05-07',
            'status': 'Pending',
        },
        {
            'client_id': Client.objects.get(name='Sophia Anderson'),
            'date': '2023-05-08',
            'status': 'Completed',
        },
        {
            'client_id': Client.objects.get(name='Benjamin Martinez'),
            'date': '2023-05-09',
            'status': 'Pending',
        },
        {
            'client_id': Client.objects.get(name='Ava Hernandez'),
            'date': '2023-05-10',
            'status': 'Completed',
        },
    ]

    for order_data in orders:
        Order.objects.create(**order_data)


    # 6) Adding examples of OrderDetail
    order_details = [
        {
            'order_id': Order.objects.get(date='2023-05-01'),
            'piece_id': JeweleryPiece.objects.get(name='Gold Necklace'),
            'quantity': 2,
        },
        {
            'order_id': Order.objects.get(date='2023-05-02'),
            'piece_id': JeweleryPiece.objects.get(name='Silver Earrings'),
            'quantity': 1,
        },
        {
            'order_id': Order.objects.get(date='2023-05-03'),
            'piece_id': JeweleryPiece.objects.get(name='Diamond Bracelet'),
            'quantity': 3,
        },
        {
            'order_id': Order.objects.get(date='2023-05-04'),
            'piece_id': JeweleryPiece.objects.get(name='Pearl Ring'),
            'quantity': 2,
        },
        {
            'order_id': Order.objects.get(date='2023-05-05'),
            'piece_id': JeweleryPiece.objects.get(name='Platinum Pendant'),
            'quantity': 1,
        },
        {
            'order_id': Order.objects.get(date='2023-05-06'),
            'piece_id': JeweleryPiece.objects.get(name='Ruby Anklet'),
            'quantity': 4,
        },
        {
            'order_id': Order.objects.get(date='2023-05-07'),
            'piece_id': JeweleryPiece.objects.get(name='Sapphire Brooch'),
            'quantity': 1,
        },
        {
            'order_id': Order.objects.get(date='2023-05-08'),
            'piece_id': JeweleryPiece.objects.get(name='Emerald Cufflinks'),
            'quantity': 2,
        },
        {
            'order_id': Order.objects.get(date='2023-05-09'),
            'piece_id': JeweleryPiece.objects.get(name='Topaz Watch'),
            'quantity': 1,
        },
        {
            'order_id': Order.objects.get(date='2023-05-10'),
            'piece_id': JeweleryPiece.objects.get(name='Amethyst Charm'),
            'quantity': 3,
        },
    ]

    for order_detail_data in order_details:
        OrderDetails.objects.create(**order_detail_data)
    
    return redirect(reverse('main_view'))


class DeleteAllObjectsView(View):

    def get(self, request, *args, **kwargs):
        # Get all the models in your Django app
        app_models = apps.get_models()

        # Iterate over the models and delete all objects
        for model in app_models:
            model.objects.all().delete()

        # Show a success message
        messages.success(request, "All objects have been deleted.")

        # Redirect to the desired URL
        return redirect('main_view')  # Replace 'home' with the desired URL name
    

def add_jewelerypiece(request):
    if request.method == 'POST':
        form = JeweleryPieceForm(request.POST)
        success_url = reverse('main_view')
        if form.is_valid():
            form.save()
            form._save_m2m()
            return redirect(success_url)
        
    else:
        form = JeweleryPieceForm()

    return render(request, 'add_item.html', {'form': form, 'form_name': 'Add JeweleryPiece'})


def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        success_url = reverse('main_view')
        if form.is_valid():
            form.save()
            return redirect(success_url)
        
    else:
        form = MaterialForm()

    return render(request, 'add_item.html', {'form': form, 'form_name': 'Add Material'})


def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        success_url = reverse('main_view')
        if form.is_valid():
            form.save()
            return redirect(success_url)
        
    else:
        form = OrderForm()

    return render(request, 'add_item.html', {'form': form, 'form_name': 'Add Order'})


def add_orderdetails(request):
    if request.method == 'POST':
        form = OrderDetailsForm(request.POST)
        success_url = reverse('main_view')
        if form.is_valid():
            form.save()
            return redirect(success_url)
        
    else:
        form = OrderDetailsForm()

    return render(request, 'add_item.html', {'form': form, 'form_name': 'Add OrderDetails'})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        success_url = reverse('main_view')
        if form.is_valid():
            form.save()
            return redirect(success_url)
        
    else:
        form = ClientForm()

    return render(request, 'add_item.html', {'form': form, 'form_name': 'Add Client'})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        success_url = reverse('main_view')
        if form.is_valid():
            form.save()
            return redirect(success_url)
        
    else:
        form = CategoryForm()

    return render(request, 'add_item.html', {'form': form, 'form_name': 'Add Category'})


def items_list(request):
    jewelery = JeweleryPiece.objects.all()
    materials = Material.objects.all()
    orders = Order.objects.all()
    details = OrderDetails.objects.all()
    clients = Client.objects.all()
    categories = Category.objects.all()
    context = {
        'jl': jewelery,
        'ml': materials,
        'ol': orders,
        'dl': details,
        'cll': clients,
        'cal': categories,
    }
    return render(request, 'items_list.html', context)

def q1(request):
    return render(request, 'q1.html')

"""
Queries:

ПРОСТІ:

1) Повернути всі вироби, що належать до категорії {category}:
SELECT JeweleryPiece.name
FROM JeweleryPiece, CategoryPiece, Category
WHERE JeweleryPiece.piece_id = CategoryPiece.piece_id
  AND CategoryPiece.category_id = Category.category_id
  AND Category.name = '{category}';

2) Повернути замовлення, в яких є вироб, ціна якого перевищує {price}
SELECT DISTINCT Order.name
FROM Order, OrderDetails, JeweleryPiece
WHERE Order.order_id = OrderDetails.order_id
  AND OrderDetails.piece_id = JeweleryPiece.piece_id
  AND JeweleryPiece.price > {price};

3) Повернути вироби, які є в замовленнях у кількості, що перевищує {quantity}
SELECT JeweleryPiece.name
FROM JeweleryPiece, OrderDetails
WHERE JeweleryPiece.piece_id = OrderDetails.piece_id
  AND OrderDetails.quantity > {quantity};

4) Повернути всі категорії, що є в виробу заказа з id {order_id}:
SELECT Category.name
FROM Category
WHERE Category.category_id IN (
    SELECT CategoryPiece.category_id
    FROM CategoryPiece
    WHERE CategoryPiece.piece_id IN (
        SELECT JeweleryPiece.piece_id
        FROM JeweleryPiece
        WHERE JeweleryPiece.piece_id IN (
            SELECT OrderDetails.piece_id
            FROM OrderDetails
            WHERE OrderDetails.order_id = {order_id}
        )
    )
);

5) Повернути замовлення, в яких є вироб з матеріалу {material}
SELECT Order.order_id
FROM Order
WHERE Order.order_id IN (
    SELECT OrderDetails.order_id
    FROM OrderDetails
    WHERE OrderDetails.piece_id IN (
        SELECT JeweleryPiece.piece_id
        FROM JeweleryPiece
        WHERE JeweleryPiece.material_id = (
            SELECT material_id
            FROM Material
            WHERE name = '{material}'
        )
    )
);


МНОЖИННІ:
знайти клієнтів у яких в замовленні такі ж категорії (всі ті і тільки ті) що і клієнт {A}
простий: хоча б одну категорію що і клієнт {A}

*) Знайти всі замовлення, в яких є вироби з такими ж і тільки тими категоріями, що й у виробу з
замовлення з id {order_id}
SELECT o.order_id, o.client_id, o.date, o.status
FROM Order o, OrderDetails od, JeweleryPiece jp, CategoryPiece cp
WHERE o.order_id = od.order_id
  AND od.piece_id = jp.piece_id
  AND jp.piece_id = cp.piece_id
  AND cp.category_id IN (
    SELECT cp2.category_id
    FROM OrderDetails od2, JeweleryPiece jp2, CategoryPiece cp2
    WHERE od2.order_id = {order_id}
      AND od2.piece_id = jp2.piece_id
      AND jp2.piece_id = cp2.piece_id
  )
  AND NOT EXISTS (
    SELECT 1
    FROM OrderDetails od3, JeweleryPiece jp3, CategoryPiece cp3
    WHERE od3.order_id = o.order_id
      AND od3.piece_id = jp3.piece_id
      AND jp3.piece_id = cp3.piece_id
      AND cp3.category_id NOT IN (
        SELECT cp4.category_id
        FROM OrderDetails od4, JeweleryPiece jp4, CategoryPiece cp4
        WHERE od4.order_id = {order_id}
          AND od4.piece_id = jp4.piece_id
          AND jp4.piece_id = cp4.piece_id
      )
  );


6) Повернути id покупців, в яких є вироб з такими ж категоріями, що й вироб {piece}
SELECT Order.order_id
FROM Order
WHERE Order.order_id IN (
    SELECT OrderDetails.order_id
    FROM OrderDetails
    WHERE OrderDetails.piece_id = {piece}
)
AND Order.order_id IN (
    SELECT OrderDetails.order_id
    FROM OrderDetails
    WHERE OrderDetails.piece_id IN (
        SELECT CategoryPiece.piece_id
        FROM CategoryPiece
        WHERE CategoryPiece.category_id IN (
            SELECT CategoryPiece.category_id
            FROM CategoryPiece
            WHERE CategoryPiece.piece_id = {piece}
        )
    )
);


7) "Повернути назви категорій, які повторюються в 
усіх виробах замовлень покупця з id {customer_id}
SELECT Category.name
FROM Category
WHERE NOT EXISTS (
    SELECT *
    FROM JeweleryPiece
    WHERE JeweleryPiece.piece_id IN (
        SELECT OrderDetails.piece_id
        FROM OrderDetails
        WHERE OrderDetails.order_id IN (
            SELECT Order.order_id
            FROM Order
            WHERE Order.client_id = {customer_id}
        )
    )
    AND NOT EXISTS (
        SELECT *
        FROM CategoryPiece
        WHERE CategoryPiece.piece_id = JeweleryPiece.piece_id
        AND CategoryPiece.category_id = Category.category_id
    )
);


8) Знайти замовлення, в якому є вироб, що належить до усіх категорій
SELECT Order.id
FROM Order
WHERE Order.order_id IN (
    SELECT OrderDetails.order_id
    FROM OrderDetails
    WHERE OrderDetails.piece_id IN (
        SELECT CategoryPiece.piece_id
        FROM CategoryPiece
        GROUP BY CategoryPiece.piece_id
        HAVING COUNT(DISTINCT CategoryPiece.category_id) = (
            SELECT COUNT(*)
            FROM Category
        )
    )
);

    

"""