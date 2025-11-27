# handlers/roblox_api.py
# Roblox API functions

import aiohttp
import re

async def extract_roblox_username(display_name):
    """Extract Roblox username from Discord display name"""
    match = re.search(r'@(\w+)', display_name)
    if match:
        return match.group(1)
    username = re.sub(r'[^\w\s]', '', display_name).strip().split()[0]
    return username if username else None

async def get_roblox_user_by_username(username):
    """Get Roblox user data by username"""
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data'):
                        return data['data'][0]
    except Exception as e:
        print(f"Error getting Roblox user: {e}")
    return None

async def check_group_membership_and_role(user_id, group_id, required_role):
    """Check if user is in Roblox group with required role"""
    url = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for group in data.get('data', []):
                        if group['group']['id'] == group_id:
                            role_name = group['role']['name']
                            if role_name == required_role:
                                return True, role_name
                            else:
                                return False, f"Wrong role: {role_name}"
                    return False, "Not in group"
    except Exception as e:
        print(f"Error checking group: {e}")
    return False, "API Error"
