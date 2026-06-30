# Fix: SSL CERTIFICATE_VERIFY_FAILED (Self-Signed Certificate in Chain)

> **Symptom:**  
> `ServiceRequestError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1081)`  
> Common when behind a corporate proxy/firewall that injects its own TLS certificate.

---

## Option A — Quick Fix: `pip-system-certs` (Recommended for Windows)

This package patches Python's `requests`/`urllib3` to use the **Windows certificate store**, which already trusts your corporate CA.

### Step 1 — Create and activate a virtual environment

```powershell
cd C:\Projects\YourProject
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2 — Install `pip-system-certs`

```powershell
pip install pip-system-certs
```

### Step 3 — Install your project dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 — Add an import at the top of your Python script/notebook

```python
# Must be imported BEFORE any Azure SDK or requests usage
import pip_system_certs.wrapt_requests
```

### Step 5 — Restart the Jupyter kernel

In VS Code: **Ctrl+Shift+P** → `Notebook: Restart Kernel`, and ensure the kernel points to `.venv`.

---

## Option B — Manual CA Bundle Merge

Use this when `pip-system-certs` is not available or you need a portable solution (Linux, CI/CD, containers).

### Step 1 — Export the corporate root CA certificate

#### Method 1: PowerShell (automatic)

```powershell
$url = "https://your-target-endpoint.com/"
$request = [System.Net.HttpWebRequest]::Create($url)
$request.GetResponse() | Out-Null
$cert = $request.ServicePoint.Certificate
$chain = New-Object System.Security.Cryptography.X509Certificates.X509Chain
$chain.Build($cert) | Out-Null
$root = $chain.ChainElements[$chain.ChainElements.Count - 1].Certificate
[System.IO.File]::WriteAllBytes("$HOME\enterprise_root_ca.cer", $root.Export("Cert"))
```

#### Method 2: Windows Certificate Manager (manual)

1. Press **Win+R** → type `certmgr.msc` → Enter.
2. Navigate to **Trusted Root Certification Authorities → Certificates**.
3. Find your corporate proxy CA (e.g. "Zscaler", "Palo Alto", company name).
4. Right-click → **All Tasks → Export…**
5. Choose **Base-64 encoded X.509 (.CER)** → save as `enterprise_root_ca.pem`.

### Step 2 — Install `certifi`

```powershell
pip install certifi
```

### Step 3 — Create a combined CA bundle in Python

Add this as the **first code cell** or at the top of your script:

```python
import os
import certifi

ENTERPRISE_CA = r"C:\path\to\enterprise_root_ca.pem"

_combined = os.path.join(os.path.dirname(ENTERPRISE_CA), "combined_ca_bundle.pem")
if not os.path.exists(_combined) or os.path.getmtime(ENTERPRISE_CA) > os.path.getmtime(_combined):
    with open(_combined, "wb") as out:
        with open(certifi.where(), "rb") as f:
            out.write(f.read())
        out.write(b"\n")
        with open(ENTERPRISE_CA, "rb") as f:
            out.write(f.read())

os.environ["REQUESTS_CA_BUNDLE"] = _combined
os.environ["SSL_CERT_FILE"]      = _combined
os.environ["CURL_CA_BUNDLE"]     = _combined
```

### Step 4 — Verify

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
secret = client.get_secret("your-secret-name")
print("Secret retrieved successfully.")
```

---

## Option C — Set Environment Variables Globally (Session/Machine Level)

If you prefer not to modify code, set the env var before launching VS Code or your script.

### PowerShell (current session)

```powershell
$env:REQUESTS_CA_BUNDLE = "C:\path\to\combined_ca_bundle.pem"
$env:SSL_CERT_FILE      = "C:\path\to\combined_ca_bundle.pem"
```

### System-wide (persistent)

```powershell
[System.Environment]::SetEnvironmentVariable("REQUESTS_CA_BUNDLE", "C:\path\to\combined_ca_bundle.pem", "User")
[System.Environment]::SetEnvironmentVariable("SSL_CERT_FILE", "C:\path\to\combined_ca_bundle.pem", "User")
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `pip install` itself fails with SSL error | Run: `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pip-system-certs` |
| Don't know which cert is the proxy CA | Open `https://your-endpoint` in Chrome → padlock → certificate → view chain → export root |
| Still failing after env var set | Restart VS Code / terminal so the new env var is picked up |
| Jupyter kernel ignores env var | Set it **in code** (`os.environ[...]`) before importing Azure SDKs |
| Running in Docker / CI | Mount the combined bundle and set `SSL_CERT_FILE` in the Dockerfile |

---

## Reference

- [certifi documentation](https://pypi.org/project/certifi/)
- [pip-system-certs](https://pypi.org/project/pip-system-certs/)
- [Azure SDK — Custom CA](https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-authenticate)
- [Python ssl module](https://docs.python.org/3/library/ssl.html)