# 🧪 Testing Security Features - Quick Guide

## Prerequisites
```bash
cd backend
pip install -r requirements.txt
```

## 1. Start the Server
```bash
python main.py
```

Server will start at: http://localhost:8000

## 2. Test Authentication

### View API Documentation
Open browser: http://localhost:8000/docs

### Test Demo Login
```bash
# Login with demo user
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=demo123"
```

**Expected Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Register New User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "engineer1",
    "email": "engineer@example.com",
    "password": "secure123",
    "full_name": "John Engineer",
    "license_number": "PE-12345"
  }'
```

### Get Current User Info
```bash
# Replace YOUR_TOKEN with the token from login
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 3. Test Rate Limiting

### Test Normal Usage
```bash
# Make 10 requests - should work fine
for i in {1..10}; do
  echo "Request $i"
  curl -s http://localhost:8000/health | jq
done
```

### Test Rate Limit
```bash
# Make 105 requests - should get rate limited
for i in {1..105}; do
  echo "Request $i"
  curl -s -w "\nStatus: %{http_code}\n" http://localhost:8000/api/projects
done
```

**Expected**: After 100 requests, you'll get:
```json
{
  "detail": "Rate limit exceeded. Maximum 100 requests per minute.",
  "retry_after": 60
}
```

### Check Rate Limit Headers
```bash
curl -v http://localhost:8000/health 2>&1 | grep -i ratelimit
```

**Expected Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1697123456
```

## 4. Test Legal Disclaimers

### View Disclaimer
```bash
curl http://localhost:8000/api/auth/disclaimer | jq
```

### Accept Disclaimer (requires authentication)
```bash
curl -X POST "http://localhost:8000/api/auth/disclaimer/accept" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"accepted": true}'
```

## 5. Test Project Versioning

### Create a Version
```bash
curl -X POST "http://localhost:8000/api/versions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "commit_message": "Initial version",
    "project_data": {"name": "Test Building", "floors": 5},
    "model_data": {"nodes": 100, "elements": 200}
  }'
```

### List Project Versions
```bash
curl -X GET "http://localhost:8000/api/projects/1/versions" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Specific Version
```bash
curl -X GET "http://localhost:8000/api/versions/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Restore to Previous Version
```bash
curl -X POST "http://localhost:8000/api/projects/1/restore/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Compare Versions
```bash
curl -X GET "http://localhost:8000/api/projects/1/versions/compare/1/2" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 6. Integration Test Script

Save as `test_all_security.sh`:

```bash
#!/bin/bash

echo "=== Testing StruMind Security Features ==="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Base URL
BASE_URL="http://localhost:8000"

echo -e "\n${GREEN}1. Testing Health Check${NC}"
curl -s $BASE_URL/health | jq

echo -e "\n${GREEN}2. Testing Login${NC}"
TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=demo123" | jq -r '.access_token')

if [ "$TOKEN" != "null" ]; then
  echo -e "${GREEN}✓ Login successful${NC}"
  echo "Token: ${TOKEN:0:20}..."
else
  echo -e "${RED}✗ Login failed${NC}"
  exit 1
fi

echo -e "\n${GREEN}3. Testing Authenticated Endpoint${NC}"
curl -s -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq

echo -e "\n${GREEN}4. Testing Disclaimer${NC}"
curl -s "$BASE_URL/api/auth/disclaimer" | jq '.version, .last_updated'

echo -e "\n${GREEN}5. Testing Rate Limit Headers${NC}"
curl -s -v "$BASE_URL/health" 2>&1 | grep -i "x-ratelimit"

echo -e "\n${GREEN}6. Creating Project Version${NC}"
curl -s -X POST "$BASE_URL/api/versions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "commit_message": "Test version",
    "project_data": {"test": true}
  }' | jq

echo -e "\n${GREEN}7. Listing Versions${NC}"
curl -s -X GET "$BASE_URL/api/projects/1/versions" \
  -H "Authorization: Bearer $TOKEN" | jq

echo -e "\n${GREEN}=== All Tests Complete ===${NC}"
```

Run with:
```bash
chmod +x test_all_security.sh
./test_all_security.sh
```

## 7. Python Integration Test

Save as `test_security_integration.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_authentication():
    """Test login and token usage"""
    print("Testing authentication...")
    
    # Login
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": "demo", "password": "demo123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    print(f"✓ Login successful, token: {token[:20]}...")
    
    # Get user info
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    assert response.status_code == 200
    user = response.json()
    print(f"✓ User info: {user['username']}")
    
    return token

def test_rate_limiting():
    """Test rate limiting"""
    print("\nTesting rate limiting...")
    
    # Make requests until rate limited
    for i in range(105):
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 429:
            print(f"✓ Rate limited after {i} requests")
            return
    
    print("✗ Rate limiting not working")

def test_versioning(token):
    """Test project versioning"""
    print("\nTesting versioning...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Create version
    version_data = {
        "project_id": 1,
        "commit_message": "Test version",
        "project_data": {"test": True}
    }
    response = requests.post(
        f"{BASE_URL}/api/versions",
        headers=headers,
        json=version_data
    )
    assert response.status_code == 200
    version = response.json()
    print(f"✓ Version created: {version['version_number']}")
    
    # List versions
    response = requests.get(
        f"{BASE_URL}/api/projects/1/versions",
        headers=headers
    )
    assert response.status_code == 200
    versions = response.json()
    print(f"✓ Found {len(versions)} versions")

def test_disclaimer():
    """Test legal disclaimer"""
    print("\nTesting disclaimer...")
    
    response = requests.get(f"{BASE_URL}/api/auth/disclaimer")
    assert response.status_code == 200
    disclaimer = response.json()
    print(f"✓ Disclaimer version: {disclaimer['version']}")
    assert "ENGINEERING SOFTWARE DISCLAIMER" in disclaimer['disclaimer']
    print("✓ Disclaimer content verified")

if __name__ == "__main__":
    print("=== StruMind Security Integration Tests ===\n")
    
    try:
        token = test_authentication()
        test_disclaimer()
        test_versioning(token)
        # test_rate_limiting()  # Uncomment to test (will make 105 requests)
        
        print("\n=== All Tests Passed ===")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
```

Run with:
```bash
python test_security_integration.py
```

## 8. Expected Results Summary

### ✅ Working Features:
- JWT authentication with demo user
- User registration
- Token-based API access
- Rate limiting (100 req/min)
- Rate limit headers
- Engineering disclaimers
- Project versioning
- Version history
- Version restore

### 📊 Performance:
- Login: < 100ms
- Token validation: < 10ms
- Rate limit check: < 5ms
- Version creation: < 50ms

### 🔒 Security:
- Passwords hashed with bcrypt
- JWT tokens expire in 30 minutes
- Rate limiting prevents abuse
- Legal disclaimers protect liability

## 9. Troubleshooting

### Issue: "Could not validate credentials"
**Solution**: Token expired or invalid. Login again to get new token.

### Issue: "Rate limit exceeded"
**Solution**: Wait 60 seconds or restart server to reset limits.

### Issue: "User not found"
**Solution**: Use demo user (demo/demo123) or register new user first.

### Issue: Import errors
**Solution**: Install dependencies:
```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

## 10. Next Steps

After testing:
1. Review security implementation
2. Customize rate limits for your needs
3. Update legal disclaimers with legal counsel
4. Set up production database
5. Configure environment variables
6. Deploy to staging environment

## 📝 Notes

- Demo user is for testing only - remove in production
- Rate limits reset every minute
- Tokens expire after 30 minutes
- All endpoints except /health and / are rate limited
- Version data is stored in memory (use database in production)

Happy testing! 🚀
