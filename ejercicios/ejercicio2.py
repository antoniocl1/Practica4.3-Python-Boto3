from common import aws_resource_functions as aws

# AMI ID
ami = 'ami-08e637cea2f053dfa'

# Instance type
instance_type = 't2.micro'

# SSH key name
key_name = 'vockey'

# Instance name and security group name
instance_name = 'backend'
sg_name = 'backend-sg'

# Verificar si el grupo de seguridad existe
if aws.security_group_exists(sg_name) == False:
    print('El grupo de seguridad no existe')
    exit()

# Crear la instancia
aws.create_instance(ami, 1, instance_type, key_name, instance_name, sg_name)

# Listar las instancias
aws.list_instances()