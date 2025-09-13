## Local Simulation (No AWS Required)

This project includes a **Moto-based simulation** of AWS SES, SQS, and SNS.  
You can run the entire pipeline locally without creating any AWS resources.

### Steps
```powershell
# Install dependencies
py -m pip install boto3 moto

# Run simulation
cd worker
py simulate_local.py
