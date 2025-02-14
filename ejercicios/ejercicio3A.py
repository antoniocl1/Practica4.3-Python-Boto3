from common import aws_resource_functions as aws
import boto3
import time

# AMI ID
ami = 'ami-04b4f1a9cf54c11d0'

# Tipo de instancia
instance_type = 't2.micro'

# Nombre de la clave SSH
key_name = 'vockey'

# Nombres de las instancias y grupos de seguridad
nombres_instancias = ['frontend-1', 'frontend-2', 'backend', 'balanceador', 'nfs']
nombres_sg = ['frontend-sg', 'frontend-sg', 'backend-sg', 'balanceador-sg', 'nfs-sg']

# Reglas de los grupos de seguridad para las instancias..
reglas_sg = {
    'frontend-sg': [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 2049, 'ToPort': 2049, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 3306, 'ToPort': 3306, 'CidrIp': '0.0.0.0/0'}
    ],
    'backend-sg': [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 3306, 'ToPort': 3306, 'CidrIp': '0.0.0.0/0'}
    ],
    'balanceador-sg': [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 3306, 'ToPort': 3306, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 2049, 'ToPort': 2049, 'CidrIp': '0.0.0.0/0'}
    ],
    'nfs-sg': [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 2049, 'ToPort': 2049, 'CidrIp': '0.0.0.0/0'}
    ]
}

# Crear los grupos de seguridad si no existen ya.
for nombre_sg, reglas in reglas_sg.items():
    if not aws.security_group_exists(nombre_sg):
        aws.create_security_group(nombre_sg, f'Reglas para {nombre_sg}', reglas)

# Crear las IPs elásticas.
ips_elasticas = {}
for nombre_instancia in nombres_instancias:
    ip_elastica = aws.allocate_elastic_ip()
    ips_elasticas[nombre_instancia] = ip_elastica

# Crear las instancias y asociar las IPs elásticas a las instancias creadas. 
for nombre_instancia, nombre_sg in zip(nombres_instancias, nombres_sg):
    aws.create_instance(ami, 1, instance_type, key_name, nombre_instancia, nombre_sg)
    id_instancia = aws.get_instance_id(nombre_instancia)
    
    # Esperar hasta que la instancia esté en estado 'running' para asociar la IP elástica.
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(id_instancia)
    instance.wait_until_running()
    
    # Asociar la IP elástica a la instancia.
    aws.associate_elastic_ip(ips_elasticas[nombre_instancia], id_instancia)