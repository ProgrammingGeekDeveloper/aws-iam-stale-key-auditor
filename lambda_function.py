import boto3
from datetime import datetime, timezone

# Initialize IAM client
iam = boto3.client('iam')

def lambda_handler(event, context):
    """
    Audits all IAM users for Access Keys older than 90 days.
    """
    users = iam.list_users()['Users']
    stale_threshold_days = 90
    found_stale_keys = False
    
    print(f"Starting IAM Audit at {datetime.now(timezone.utc)}")

    for user in users:
        username = user['UserName']
        access_keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        
        for key in access_keys:
            key_id = key['AccessKeyId']
            creation_date = key['CreateDate']
            
            # Calculate key age
            age_delta = datetime.now(timezone.utc) - creation_date
            age_days = age_delta.days
            
            if age_days > stale_threshold_days:
                found_stale_keys = True
                print(f"[ALARM] User: {username} | Key: {key_id} | Age: {age_days} days. Action Required: Rotate Key.")
            else:
                print(f"[OK] User: {username} | Key: {key_id} | Age: {age_days} days.")

    if not found_stale_keys:
        print("Audit complete: No stale keys found.")
        
    return {"status": "Audit Complete"}
