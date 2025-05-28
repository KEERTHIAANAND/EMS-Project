// 🔗 Frontend Integration Example for EMS Backend
// Add this to your React components to integrate with Django backend

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// API Helper Functions
const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token');
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  };
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  });
  
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.error || `HTTP ${response.status}`);
  }
  
  return data;
};

// Authentication Functions
export const authAPI = {
  // Register new user
  register: async (userData) => {
    try {
      const response = await apiCall('/auth/register/', {
        method: 'POST',
        body: JSON.stringify({
          name: userData.name,
          email: userData.email,
          password: userData.password,
          confirm_password: userData.confirmPassword
        })
      });
      
      // Store authentication data
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      localStorage.setItem('isAuthenticated', 'true');
      
      return response;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await apiCall('/auth/login/', {
        method: 'POST',
        body: JSON.stringify(credentials)
      });
      
      // Store authentication data
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      localStorage.setItem('isAuthenticated', 'true');
      
      return response;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  },

  // Logout user
  logout: async () => {
    try {
      await apiCall('/auth/logout/', {
        method: 'POST'
      });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      // Clear local storage regardless
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('isAuthenticated');
    }
  },

  // Get user profile
  getProfile: async () => {
    try {
      return await apiCall('/auth/profile/');
    } catch (error) {
      console.error('Get profile failed:', error);
      throw error;
    }
  }
};

// Updated SignUpPage component
export const UpdatedSignUpPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await authAPI.register(formData);
      navigate('/'); // Redirect to home page
    } catch (error) {
      alert(error.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        type="text"
        placeholder="Full Name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      <input
        name="email"
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      <input
        name="password"
        type="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
        required
      />
      <input
        name="confirmPassword"
        type="password"
        placeholder="Confirm Password"
        value={formData.confirmPassword}
        onChange={handleChange}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Creating Account...' : 'Sign Up'}
      </button>
    </form>
  );
};

// Updated SignInPage component
export const UpdatedSignInPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await authAPI.login(formData);
      navigate('/'); // Redirect to home page
    } catch (error) {
      alert(error.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="email"
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      <input
        name="password"
        type="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Signing In...' : 'Sign In'}
      </button>
    </form>
  );
};

// Updated Navbar with logout
export const UpdatedNavbar = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      navigate('/sign-in');
    } catch (error) {
      console.error('Logout failed:', error);
      // Still redirect even if API call fails
      navigate('/sign-in');
    }
  };

  return (
    <nav>
      {/* Your existing nav items */}
      <button onClick={handleLogout}>
        Logout
      </button>
    </nav>
  );
};

// Health check function
export const checkBackendHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health/`);
    const data = await response.json();
    console.log('Backend health:', data);
    return response.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
};

// Usage in your App.jsx
export const AppWithBackendIntegration = () => {
  const [backendHealthy, setBackendHealthy] = useState(false);

  useEffect(() => {
    // Check backend health on app start
    checkBackendHealth().then(setBackendHealthy);
  }, []);

  if (!backendHealthy) {
    return (
      <div>
        <h1>Connecting to backend...</h1>
        <p>Make sure Django server is running on http://localhost:8000</p>
      </div>
    );
  }

  return (
    // Your existing app structure
    <div>Your app content</div>
  );
};
