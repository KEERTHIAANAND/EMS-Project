import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '@/components/Layout.jsx';
import HomePage from '@/pages/HomePage.jsx';
import CreateEventPage from '@/pages/CreateEventPage.jsx';
import EditEventPage from '@/pages/EditEventPage.jsx';
import EventDetailsPage from '@/pages/EventDetailsPage.jsx';
import AdminDashboardPage from '@/pages/AdminDashboardPage.jsx';
import NotFoundPage from '@/pages/NotFoundPage.jsx';
import SignInPage from '@/pages/SignInPage.jsx';
import SignUpPage from '@/pages/SignUpPage.jsx';
import { EventProvider } from '@/contexts/EventContext.jsx';

function App() {
  // Enhanced auth check with token validation
  const isAuthenticated = () => {
    const token = localStorage.getItem('token');
    const isAuth = localStorage.getItem('isAuthenticated') === 'true';
    const user = localStorage.getItem('user');

    // Check if all required auth data exists
    if (!token || !isAuth || !user) {
      // Clear any partial auth data
      localStorage.removeItem('token');
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('user');
      return false;
    }

    try {
      // Validate user data
      const userData = JSON.parse(user);
      if (!userData.email || !userData.id) {
        // Invalid user data
        localStorage.removeItem('token');
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('user');
        return false;
      }

      return true;
    } catch (error) {
      // Invalid JSON in user data
      localStorage.removeItem('token');
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('user');
      return false;
    }
  };

  // Protected route component
  const ProtectedRoute = ({ children }) => {
    if (!isAuthenticated()) {
      return <Navigate to="/sign-in" />;
    }
    return children;
  };

  return (
    <EventProvider>
      <Router
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true
        }}
      >
        <Routes>
          <Route path="/sign-in" element={<SignInPage />} />
          <Route path="/sign-up" element={<SignUpPage />} />

          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            <Route index element={<HomePage />} />
            <Route path="create-event" element={<CreateEventPage />} />
            <Route path="events/:eventId" element={<EventDetailsPage />} />
            <Route path="admin" element={<AdminDashboardPage />} />
            <Route path="admin/edit-event/:eventId" element={<EditEventPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </Router>
    </EventProvider>
  );
}

export default App;