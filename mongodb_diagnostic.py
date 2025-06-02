#!/usr/bin/env python3
"""
MongoDB Atlas connection diagnostic script
"""
import socket
import requests
from urllib.parse import urlparse

def check_internet_connectivity():
    """Check basic internet connectivity"""
    print("🌐 Checking internet connectivity...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("✅ Internet connectivity is working")
            return True
        else:
            print("❌ Internet connectivity issue")
            return False
    except Exception as e:
        print(f"❌ Internet connectivity error: {e}")
        return False

def check_mongodb_atlas_connectivity():
    """Check connectivity to MongoDB Atlas"""
    print("🗄️  Checking MongoDB Atlas connectivity...")
    
    # Your MongoDB Atlas connection string
    connection_string = "mongodb+srv://keerthiaanand77:alnH2HG9FPYEiPrp@cluster0.bvndqsy.mongodb.net/ems_database"
    
    # Parse the connection string to get the host
    try:
        # Extract host from connection string
        host = "cluster0.bvndqsy.mongodb.net"
        port = 27017
        
        print(f"Testing connection to {host}:{port}...")
        
        # Test socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ Can connect to MongoDB Atlas host")
            return True
        else:
            print(f"❌ Cannot connect to MongoDB Atlas host (error code: {result})")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB Atlas connectivity error: {e}")
        return False

def check_dns_resolution():
    """Check DNS resolution for MongoDB Atlas"""
    print("🔍 Checking DNS resolution...")
    try:
        host = "cluster0.bvndqsy.mongodb.net"
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolution successful: {host} -> {ip}")
        return True
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
        return False

def get_public_ip():
    """Get public IP address"""
    print("🌍 Getting your public IP address...")
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        if response.status_code == 200:
            ip = response.text.strip()
            print(f"✅ Your public IP: {ip}")
            print(f"📝 Make sure this IP is whitelisted in MongoDB Atlas Network Access")
            return ip
        else:
            print("❌ Could not get public IP")
            return None
    except Exception as e:
        print(f"❌ Error getting public IP: {e}")
        return None

def test_pymongo_connection():
    """Test direct PyMongo connection"""
    print("🐍 Testing direct PyMongo connection...")
    try:
        import pymongo
        
        connection_string = "mongodb+srv://keerthiaanand77:alnH2HG9FPYEiPrp@cluster0.bvndqsy.mongodb.net/ems_database?retryWrites=true&w=majority&appName=Cluster0"
        
        # Create client with short timeout
        client = pymongo.MongoClient(
            connection_string,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ PyMongo connection successful")
        
        # Test database access
        db = client.ems_database
        collections = db.list_collection_names()
        print(f"✅ Database access successful. Collections: {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ PyMongo connection failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔧 MongoDB Atlas Connection Diagnostic")
    print("=" * 50)
    
    # Test 1: Internet connectivity
    if not check_internet_connectivity():
        print("\n❌ Basic internet connectivity is not working. Please check your network connection.")
        return
    
    print()
    
    # Test 2: Get public IP
    public_ip = get_public_ip()
    
    print()
    
    # Test 3: DNS resolution
    if not check_dns_resolution():
        print("\n❌ DNS resolution failed. This could be a network or DNS issue.")
        return
    
    print()
    
    # Test 4: MongoDB Atlas connectivity
    if not check_mongodb_atlas_connectivity():
        print("\n❌ Cannot connect to MongoDB Atlas. Possible issues:")
        print("   1. Your IP address is not whitelisted in MongoDB Atlas Network Access")
        print("   2. Firewall is blocking the connection")
        print("   3. MongoDB Atlas cluster is paused or having issues")
        if public_ip:
            print(f"   4. Make sure IP {public_ip} is added to MongoDB Atlas Network Access")
        return
    
    print()
    
    # Test 5: PyMongo connection
    if not test_pymongo_connection():
        print("\n❌ PyMongo connection failed. This could be:")
        print("   1. Authentication issues (wrong username/password)")
        print("   2. Database permissions")
        print("   3. Network timeout issues")
        return
    
    print()
    print("🎉 All diagnostic tests passed!")
    print("✅ MongoDB Atlas connection should be working")
    print("\n📋 Next steps:")
    print("   1. Restart your Django server")
    print("   2. Try creating events from the frontend")
    print("   3. Check MongoDB Atlas dashboard for data")

if __name__ == "__main__":
    main()
