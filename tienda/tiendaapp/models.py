from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#creacion de los modelos de la tienda

#producto
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    existencia = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='images/', null=True)


    def __str__(self):
        return self.nombre

#cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=10)
    limite = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=False)

    def __str__(self):
        return self.nombre
    
#Cuenta credito
class CuentaCredito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=100, decimal_places=2)
    saldo = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)

    def __str__(self):
        return self.cliente.nombre

#venta
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)
    observaciones = models.TextField(null=True)
    pago_contra_entrega = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.cliente.nombre}"
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles" ,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.producto.precio * self.cantidad
        super(DetalleVenta, self).save(*args, **kwargs)

    def __str__(self):
         return f"{self.producto.nombre} - {self.cantidad}"
        
#reserva
class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cliente.nombre
    
#token
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    create_at = models.DateTimeField(auto_now_add=True)
    
