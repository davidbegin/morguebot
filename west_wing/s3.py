import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('morgue-files-2944dfb')
x = bucket.objects.all().delete()
print(x)
