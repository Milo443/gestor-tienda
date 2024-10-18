from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.forms.models import inlineformset_factory


from django.contrib.auth.decorators import login_required
from .models import Token, Producto , Cliente, CuentaCredito, Venta, DetalleVenta
from .forms import VentaForm, DetalleFormSet


# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            new_token = get_random_string(length=6, allowed_chars='0123456789')
            Token.objects.create(user=user, token=new_token)
            send_mail(
                'Your login token',
                f'Your login token is {new_token}',
                'cakes98otaku@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('verify_token', email=email)
    return render(request, 'login.html')

def verify_token(request, email):
    if request.method == 'POST':
        token = request.POST.get('token')
        user = User.objects.filter(email=email).first()
        if user:
            token_obj = Token.objects.filter(user=user, token=token).first()
            if token_obj:
                token_obj.delete()
                # Log in the user
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dashboard')
    return render(request, 'verify_token.html', {'email': email})

#logout
def logout(request):
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        if email and username:
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_unusable_password()
                user.save()
            token = get_random_string(length=6, allowed_chars='0123456789')
            Token.objects.create(user=user, token=token)
            send_mail(
                'Your login token',
                f'Your login token is {token}',
                'calderon-1@outlook.com',
                [email],
                fail_silently=False,
            )
            print(f"Email sent to {email} with token {token}")  # Mensaje de depuración
            return redirect('login')
        else:
            print("Email or username not provided")  # Mensaje de depuración
    else:
        print("GET request received")  # Mensaje de depuración
    return render(request, 'register.html')



#vistas de la app de tienda

#dashboard
@login_required
def dashboard(request):
    clientes = Cliente.objects.all()
    return render(request, 'app/dashboard.html', {'clientes': clientes})


#gestion de inventario
@login_required
def gestion_inventario(request):
    query = request.GET.get('buscar')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'app/gestion_inventario.html', {'productos': productos})
   

def form_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
    
        if imagen:
            producto = Producto(nombre=nombre, precio=precio, existencia=cantidad, descripcion=descripcion, imagen=imagen)
        else:
            producto = Producto(nombre=nombre, precio=precio, existencia=cantidad, descripcion=descripcion)
        
        producto.save()
        return redirect('gestion_inventario')

    return render(request, 'app/form_producto.html')

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
    
        if imagen:
            producto.nombre = nombre
            producto.precio = precio
            producto.existencia = cantidad
            producto.descripcion = descripcion
            producto.imagen = imagen
        else:
            producto.nombre = nombre
            producto.precio = precio
            producto.existencia = cantidad
            producto.descripcion = descripcion
        
        producto.save()
        return redirect('gestion_inventario')

    return render(request, 'app/form_producto.html', {'producto': producto})    

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('gestion_inventario')

#clientes
def cliente(request):
    clientes = Cliente.objects.all()
    cuentasCredito = CuentaCredito.objects.all()

    return render(request, 'app/cliente.html', {'clientes': clientes, 'cuentasCredito': cuentasCredito})

def form_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellido')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        limite = request.POST.get('limite_credito')
        saldo = request.POST.get('saldo_credito')
        cliente = Cliente(nombre=nombre, apellidos=apellidos, direccion=direccion, email=email, telefono=telefono, limite=limite, saldo=saldo)
        cliente.save()

        return redirect('cliente')
    
    return render(request, 'app/form_cliente.html')

def editar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellido')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        limite = request.POST.get('limite_credito')
        saldo = request.POST.get('saldo_credito')
        cliente.nombre = nombre
        cliente.apellidos = apellidos
        cliente.direccion = direccion
        cliente.email = email
        cliente.telefono = telefono
        cliente.limite = limite
        cliente.saldo = saldo
        cliente.save()

        return redirect('cliente')

    return render(request, 'app/form_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('cliente')



#ventas
def ventas(request):
    ventas = Venta.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'app/ventas.html', {'ventas': ventas, 'clientes': clientes})

def form_venta(request):
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_formset = DetalleFormSet(request.POST, instance=Venta())

        if venta_form.is_valid() and detalle_formset.is_valid():
            venta = venta_form.save()

           

            venta = venta_form.save(commit=False)
            venta.total = 0
            venta.save()

            detalle_formset.instance = venta
            detalle_formset.save()

            total = sum([detalle.subtotal for detalle in venta.detalles.all()])
            venta.total = total
            venta.save()

            return redirect('ventas')
    else:
        venta_form = VentaForm()
        detalle_formset = DetalleFormSet(instance = Venta())
    
    return render(request, 'app/form_venta.html', {'venta_form': venta_form, 'detalle_formset': detalle_formset, 'clientes': clientes})




#reversas
def reservas(request):
    return render(request, 'app/reservas.html')




