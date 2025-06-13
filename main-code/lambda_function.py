import boto3
import pandas as pd
import io
import os

s3 = boto3.client('s3')

def read_file(file_content, file_name):
    if file_name.endswith('.csv'):
        return pd.read_csv(io.StringIO(file_content.decode('utf-8')))
    elif file_name.endswith('.json'):
        return pd.read_json(io.StringIO(file_content.decode('utf-8')))
    elif file_name.endswith('.xlsx'):
        return pd.read_excel(io.BytesIO(file_content))
    else:
        raise ValueError("Unsupported file format")

def clean_df(df, file_type):
    schemas = {
        'orders': ['order_id', 'customer_id', 'product_id', 'quantity', 'order_date'],
        'products': ['product_id', 'product_name', 'category', 'price'],
        'customers': ['customer_id', 'name', 'email', 'city']
    }

    matched_type = next((ft for ft in schemas if ft in file_type), None)
    if not matched_type:
        raise ValueError(f"Unknown file type for cleaning: {file_type}")

    expected_cols = schemas[matched_type]
    df = df[[col for col in expected_cols if col in df.columns]]
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

    if 'order_date' in df.columns:
        try:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce').dt.strftime('%Y-%m-%d')
        except Exception as e:
            raise ValueError(f"Date parsing failed: {e}")

    df.dropna(inplace=True)
    return df, matched_type

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    input_key = event['Records'][0]['s3']['object']['key']
    file_name = os.path.basename(input_key)

    output_bucket = 's3-lens-project'

    try:
        response = s3.get_object(Bucket=bucket_name, Key=input_key)
        file_content = response['Body'].read()

        df = read_file(file_content, file_name)
        df_cleaned, ftype = clean_df(df, file_name.lower())

        csv_buffer = io.StringIO()
        df_cleaned.to_csv(csv_buffer, index=False)

        output_key = f"output/{ftype}/{ftype}_cleaned.csv"
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=csv_buffer.getvalue())

        return {
            "status": "success",
            "message": f"{file_name} cleaned and saved to {output_key}",
            "rows": len(df_cleaned)
        }

    except Exception as e:
        return {
            "status": "error",
            "file": file_name,
            "reason": str(e)
        }

