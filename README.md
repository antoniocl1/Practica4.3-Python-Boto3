# Practica4.3
IAW 2º ASIR
# Ejercicio1
```python
from common import aws_resource_functions as aws

# Hacer las reglas de entrada del grupo de seguridad
ingress_permissions = [
    {'CidrIp': '0.0.0.0/0', 'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22},
    {'CidrIp': '0.0.0.0/0', 'IpProtocol': 'tcp', 'FromPort': 3306, 'ToPort': 3306}
]

# Definir el nombre y la descripción del grupo de seguridad
sg_name = 'backend-sg'
sg_description = 'SG para el backend'

# Crear el grupo de seguridad
aws.create_security_group(sg_name, sg_description, ingress_permissions)

# Listar los grupos de seguridad
aws.list_security_groups()
```
![](capturas/ejercicio1py.png)
# Ejercicio2
![](capturas/ejercicio2py.png)
# Ejercicio3
![](capturas/ejercicio3py.png)
# Ejercicio4
![](capturas/ejercicio4py.png)
