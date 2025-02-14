from common.aws_resource_class import AWS

# Creamos el objeto AWS
aws = AWS()

#Variables instancias
instance_name = ["frontend-1", 
                 "frontend-2", 
                 "balanceador", 
                 "backend", 
                 "nfs"]

# Eliminar IPs
def delete_IP(instance_name):
    try:
        instance_id = aws.get_instance_id(instance_name)
        elastic_ip = aws.get_instance_public_ip(instance_id)
        aws.release_elastic_ip(elastic_ip)
    except:
        print("No se ha encontrado una IP para borrar")

for i in range(len(instance_name)):
    delete_IP(instance_name[i])

# Eliminar instancias
def delete_instances(instance_name):
    aws.terminate_instance(instance_name)

for i in range(len(instance_name)):
    delete_instances(instance_name[i])

#Variables grupos de seguridad
sg_name = ["frontend-sg", 
           "backend-sg", 
           "balanceador-sg", 
           "nfs-sg"]

# Eliminar grupos de seguridad
def delete_sg(sg_name):
    aws.delete_security_group(sg_name)

for i in range(len(sg_name)):
    delete_sg(sg_name[i])