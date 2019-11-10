from pulumi_aws import lambda_

from modules.source_code_hash import get_soure_code_hash


dependency_layer = lambda_.LayerVersion(
    f"lambda-dependencies",
    compatible_runtimes=["python3.6"],
    layer_name="base_dependencies",
    license_info="GPL",
    s3_bucket="morgue-artifacts",
    s3_key="dependencies.zip",
    source_code_hash=get_soure_code_hash(
        "/Users/begin/code/morguebot/build/dependencies.zip"
    ),
)
