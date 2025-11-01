import asyncio
import aiohttp
import json


async def test_registration():
    """Test the registration endpoint."""
    url = "http://localhost:1337/api/v1/auth/register"

    # Valid registration data
    data = {
        "username": "testuser123",
        "password": "TestPass123"
    }

    print("Testing registration endpoint...")
    print(f"Sending POST request to: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                response_text = await response.text()
                print(f"Status Code: {response.status}")
                print(f"Response: {response_text}")
                return response.status, response_text
        except Exception as e:
            print(f"Error occurred: {e}")
            return None, str(e)


async def test_login():
    """Test the login endpoint."""
    url = "http://localhost:1337/api/v1/auth/login"

    # Valid login data
    data = {
        "username": "testuser123",  # Use the same username as registered
        "password": "TestPass123"
    }

    print("\nTesting login endpoint...")
    print(f"Sending POST request to: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                response_text = await response.text()
                print(f"Status Code: {response.status}")
                print(f"Response: {response_text}")
                return response.status, response_text
        except Exception as e:
            print(f"Error occurred: {e}")
            return None, str(e)


async def test_invalid_registration():
    """Test registration with invalid data to check error handling."""
    url = "http://localhost:1337/api/v1/auth/register"

    # Invalid registration data (password doesn't meet complexity requirements)
    data = {
        "username": "testuser2",
        "password": "123"  # Too short and doesn't meet complexity
    }

    print("\nTesting registration with invalid data...")
    print(f"Sending POST request to: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                response_text = await response.text()
                print(f"Status Code: {response.status}")
                print(f"Response: {response_text}")
                return response.status, response_text
        except Exception as e:
            print(f"Error occurred: {e}")
            return None, str(e)


async def test_invalid_login():
    """Test login with invalid credentials."""
    url = "http://localhost:1337/api/v1/auth/login"

    # Invalid login data
    data = {
        "username": "nonexistentuser",
        "password": "wrongpassword"
    }

    print("\nTesting login with invalid credentials...")
    print(f"Sending POST request to: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                response_text = await response.text()
                print(f"Status Code: {response.status}")
                print(f"Response: {response_text}")
                return response.status, response_text
        except Exception as e:
            print(f"Error occurred: {e}")
            return None, str(e)


async def main():
    print("Starting API tests...\n")

    # Test 1: Valid registration
    reg_status, reg_response = await test_registration()

    # Wait a moment before testing login
    await asyncio.sleep(1)

    # Test 2: Valid login
    login_status, login_response = await test_login()

    # Wait a moment before error tests
    await asyncio.sleep(1)

    # Test 3: Invalid registration
    invalid_reg_status, invalid_reg_response = await test_invalid_registration()

    # Test 4: Invalid login
    invalid_login_status, invalid_login_response = await test_invalid_login()

    print("\nAll tests completed!")


if __name__ == "__main__":
    asyncio.run(main())