import boto3
import botocore

"""
Create a security group
"""
def create_security_group(group_name, description, ingress_permissions):
  ec2 = boto3.resource('ec2')
  try:
    sg = ec2.create_security_group(GroupName=group_name, Description=description)
    for p in ingress_permissions:
      sg.authorize_ingress(CidrIp=p['CidrIp'], IpProtocol=p['IpProtocol'], FromPort=p['FromPort'], ToPort=p['ToPort'])
    print(f"Security group {group_name} created")
  except botocore.exceptions.ClientError as error:
    print(error)

"""
List all security groups
"""
def list_security_groups():
  ec2 = boto3.resource('ec2')
  for sg in ec2.security_groups.all():
    print(f"group_id: {sg.group_id} \t group_name: {sg.group_name} \t description: {sg.description}")
    for rule in sg.ip_permissions:
      print(rule)
    print()

"""
Delete a security group
"""
def delete_security_group(group_name):
  ec2 = boto3.resource('ec2')

  # Get the security group id from name
  group_id = get_security_group_id(group_name)

  # Check if security group exists
  if group_id is None:
    print('The security group does not exist')
    return

  # Delete the security group
  try:
    sg = ec2.SecurityGroup(group_id)
    sg.delete()
    print(f'The security group {group_name} has been deleted')
  except botocore.exceptions.ClientError as error:
    print(error)

"""
Returns security group id
"""
def get_security_group_id(group_name):
  ec2 = boto3.resource('ec2')
  for sg in ec2.security_groups.all():
    if sg.group_name == group_name:
      return sg.group_id

"""
Check if security group exists
"""
def security_group_exists(group_name):
  ec2 = boto3.resource('ec2')
  for sg in ec2.security_groups.all():
    if sg.group_name == group_name:
      return True
  return False

"""
List EC2 instances
"""
def list_instances():
  ec2 = boto3.resource('ec2')
  print("Instance \t\t State \t\t Name \t\t Private IP \t Public IP")
  for i in ec2.instances.all():
    print(f"{i.id} \t {i.state['Name']} \t {i.tags[0]['Value']} \t {i.private_ip_address} \t {i.public_ip_address}")

"""
Start all EC2 instances
"""
def start_instances():
  ec2 = boto3.resource('ec2')
  for i in ec2.instances.all():
    if i.state['Name'] == 'stopped':
      i.start()
      print(f"Starting instance: {i.id} \t Name: {i.tags[0]['Value']}")
  
"""
Stop all EC2 instances
"""
def stop_instances():
  ec2 = boto3.resource('ec2')
  for i in ec2.instances.all():
    if i.state['Name'] == 'running':
      i.stop()
      print(f"Stopping instance: {i.id} \t Name: {i.tags[0]['Value']}")

"""
Terminate all EC2 instances
"""
def terminate_instances():
  ec2 = boto3.resource('ec2')
  for i in ec2.instances.all():
    if i.state['Name'] == 'running':
      i.terminate()
      print(f"Terminating instance: {i.id} \t Name: {i.tags[0]['Value']}")

"""
Start an EC2 instance by id
"""
def start_instance_by_id(instance_id):
  ec2 = boto3.resource('ec2')
  try:
    for i in ec2.instances.all():
      if i.id == instance_id:
        i.start()
        print(f"Starting instance: {i.id} \t Name: {i.tags[0]['Value']}")
  except botocore.exceptions.ClientError as error:
    print(f"ERROR: {error.response['Error']['Code']}. {error.response['Error']['Message']}")
    #raise error

"""
Stop an EC2 instance by id
"""
def stop_instance_by_id(instance_id):
  ec2 = boto3.resource('ec2')
  try:
    for i in ec2.instances.all():
      if i.id == instance_id:
        i.stop()
        print(f"Stopping instance: {i.id} \t Name: {i.tags[0]['Value']}")
  except botocore.exceptions.ClientError as error:
    print(f"ERROR: {error.response['Error']['Code']}. {error.response['Error']['Message']}")
    #raise error

"""
Terminate an EC2 instance by id
"""
def terminate_instance_by_id(instance_id):
  ec2 = boto3.resource('ec2')
  for i in ec2.instances.all():
    if i.id == instance_id:
      i.terminate()
      print(f"Terminating instance: {i.id} \t Name: {i.tags[0]['Value']}")

"""
Start an EC2 instance by name
"""
def start_instance(instance_name):
  # Create a boto3 instance
  ec2 = boto3.resource('ec2')

  # Get the instance using the filter method
  instances = ec2.instances.filter(Filters=[{'Name':'tag:Name', 'Values':[instance_name]}])

  # Store the instances in a list
  instances_list = [i for i in instances]

  if instances_list:
      # Start the instances
      for instance in instances_list:
          instance.start()
          print(f'Instance {instance.id} was started')
  else:
      print(f'The instance {instance_name} does not exist')

"""
Stop an EC2 instance by name
"""
def stop_instance(instance_name):
  # Create a boto3 resource instance
  ec2 = boto3.resource('ec2')

  # Get the instance using the filter method
  instances = ec2.instances.filter(Filters=[{'Name':'tag:Name', 'Values':[instance_name]}])

  # Store the instances in a list
  instances_list = [i for i in instances]

  if instances_list:
      # Stop the instances
      for instance in instances_list:
          instance.stop()
          print(f'Instance {instance.id} was stopped')
  else:
      print(f'The instance {instance_name} does not exist')

"""
Terminate an EC2 instance by name
"""
def terminate_instance(instance_name):
  # Create a boto3 resource instance
  ec2 = boto3.resource('ec2')

  # Get the instance using the filter method
  instances = ec2.instances.filter(Filters=[{'Name':'tag:Name', 'Values':[instance_name]}])

  # Store the instances in a list
  instances_list = [i for i in instances]

  if instances_list:
      # Terminate the instances
      for instance in instances_list:
          instance.terminate()
          print(f'Instance {instance.id} was terminated')
  else:
      print(f'The instance {instance_name} does not exist')

"""
Create a new EC2 instance
"""
def create_instance(image_id, max_count, instance_type, key_name, instance_name, security_group_name):
  # Create a boto3 resource instance
  ec2 = boto3.resource('ec2')

  # Create an EC2 instance
  instance = ec2.create_instances(
    ImageId = image_id,
    MinCount = 1,
    MaxCount = max_count,
    InstanceType = instance_type,
    SecurityGroups = [ security_group_name ],
    KeyName = key_name,
    TagSpecifications=[{
      'ResourceType': 'instance',
      'Tags': [{
        'Key': 'Name',
        'Value': instance_name
      }]
    }])

  #print(instance)
  print(f'The instance {instance[0].id} has been created')

"""
Returns instance id
"""
def get_instance_id(instance_name):
  ec2 = boto3.resource('ec2')
  for i in ec2.instances.all():
    if i.tags[0]['Value'] == instance_name:
      return i.id

"""
Get the public IP of an instance
"""
def get_instance_public_ip(instance_id):
  ec2 = boto3.resource('ec2')
  instance = ec2.Instance(instance_id)
  return instance.public_ip_address

"""
Allocate an elastic IP
"""
def allocate_elastic_ip():
  ec2 = boto3.resource('ec2')
  response = ec2.meta.client.allocate_address()
  print(f"The elastic IP {response['PublicIp']} has been allocated")
  return response['PublicIp']

"""
Disassociate an elastic IP from an instance
"""
def disassociate_elastic_ip(public_ip):
    ec2 = boto3.resource('ec2')
    addresses = ec2.meta.client.describe_addresses(PublicIps=[public_ip])
    if addresses['Addresses']:
        association_id = addresses['Addresses'][0]['AssociationId']
        ec2.meta.client.disassociate_address(AssociationId=association_id)
        print(f"The elastic IP {public_ip} has been disassociated")

"""
Get the allocation id of an elastic IP
"""
def get_allocation_id(public_ip):
  ec2 = boto3.resource('ec2')
  addresses = ec2.meta.client.describe_addresses(PublicIps=[public_ip])
  if addresses['Addresses']:
      return addresses['Addresses'][0]['AllocationId']
  else:
      return None

"""
Associate an elastic IP to an instance
"""
def associate_elastic_ip(public_ip, instance_id):
  ec2 = boto3.resource('ec2')
  
  print('Waiting until the instance is running...')
  ec2.Instance(instance_id).wait_until_running()

  allocation_id = get_allocation_id(public_ip)
  ec2.meta.client.associate_address(AllocationId=allocation_id, InstanceId=instance_id)
  print(f"The elastic IP {public_ip} has been associated to the instance {instance_id}")

"""
Release an elastic IP
"""
def release_elastic_ip(public_ip):
    ec2 = boto3.resource('ec2')
    allocation_id = get_allocation_id(public_ip)
    address = ec2.VpcAddress(allocation_id)
    address.release()
    print(f"The elastic IP {public_ip} has been released")