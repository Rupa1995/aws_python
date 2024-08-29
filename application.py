import boto3
import botocore
import os,json

session = boto3.Session(region_name='us-east-1')
s3_client = session.client('s3')
cfn_client = session.client('cloudformation')
iam_client = session.client('iam')

template_path = '/workspaces/aws_python/cloudformation_template'
def create_new_bucket(bucket_name):
    try:
        s3_buckets = s3_client.list_buckets()['Buckets']
        bucket_list = [ech['Name'] for ech in s3_buckets]
        print("bucket_list ",bucket_list,len(bucket_list))
        if len(bucket_list) == 0:
            response = s3_client.create_bucket(Bucket=bucket_name)
        elif bucket_name not in bucket_list:
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            print(f"{bucket_name} Bucket already exists in s3")
    
    except botocore.exceptions.ClientError as error:
        raise error

    return bucket_name

def cFn_stack_exists():
    pass

def put_s3_file(bucket_name):
    file_list=[]
    for filename in os.listdir(template_path):
        file_list.append(filename)
        file_path = template_path+'/'+filename
        s3_client.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=filename,
        )
        # print(f"{filename} uploaded to s3 successfully")
    return file_list

def get_s3_file(bucket_name,obj_list):
    cfn_templates = {}
    for ech_file in obj_list:
        cfn={}
        url = f"https://{bucket_name}.s3.amazonaws.com/{ech_file}"
        service_name = ech_file.split('.')[0]
        cfn[service_name] = url
        cfn_templates.update(cfn)
    return cfn_templates

def cfn_execution(template_url_dict):
    print("inside cfn_execution: ",template_url_dict)
    for ech_file,template_url in template_url_dict.items():
        response = cfn_client.create_stack(
            StackName=ech_file,
            TemplateURL=template_url,
            Capabilities=['CAPABILITY_IAM'],
            )
        print(response) 


def handler():
    Bucket = 'cloudformationbucket-rupa'
    response = create_new_bucket(Bucket)
    print(response)
    if response:
        s3_obj_list = put_s3_file(bucket_name=response)
        if len(s3_obj_list)>0:
            obj_url_dict = get_s3_file(bucket_name=response,obj_list=s3_obj_list)
        print(obj_url_dict)
        cfn = cfn_execution(template_url_dict=obj_url_dict)
        

if __name__ == "__main__":
    handler()
