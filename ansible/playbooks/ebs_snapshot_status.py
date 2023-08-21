import boto3
from operator import itemgetter

def get_latest_snapshot_info(profile_name):
    session = boto3.Session(profile_name=profile_name)
    ec2 = session.client('ec2')

    reservations = ec2.describe_instances()['Reservations']
    snapshots_info = []

    for reservation in reservations:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            volumes = instance.get('BlockDeviceMappings', [])

            for volume in volumes:
                volume_id = volume['Ebs']['VolumeId']
                snapshots = ec2.describe_snapshots(
                    OwnerIds=['self'],
                    Filters=[
                        {'Name': 'volume-id', 'Values': [volume_id]}
                    ]
                )['Snapshots']

                if snapshots:
                    latest_snapshot = max(snapshots, key=itemgetter('StartTime'))
                    snapshots_info.append({
                        'InstanceID': instance_id,
                        'EBS VolumeID': volume_id,
                        'LatestSnapshot': latest_snapshot,
						'Snapshot State': State,
						'Snapshot ID": snapshot_id
                    })

    return snapshots_info

if __name__ == '__main__':
    aws_profile = sys.argv[1]

    latest_snapshots_info = get_latest_snapshot_info(aws_profile)
    for info in latest_snapshots_info:
        print(info)